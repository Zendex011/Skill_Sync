# resume_parser.py
import os
import sys
import hashlib
import json
import re

# Add parent directory and self directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from models import Resume
from skill_ontology import SkillOntology
from utils.parsing_cache import ParserCache
from dotenv import load_dotenv
import json
import re

load_dotenv()

class ResumeParser:
    """Parse resumes from PDF/DOCX and extract structured data"""
    
    def __init__(self, normalize_skills=True):
        self.normalize_skills = normalize_skills
        
        # Initialize LLM
        endpoint = HuggingFaceEndpoint(
            repo_id="mistralai/Mistral-7B-Instruct-v0.2",
            task="conversational",  # ✅ must be conversational
            temperature=0.1,
            max_new_tokens=2048,  # Increased to allow complete JSON output
            huggingfacehub_api_token=os.getenv("HF_TOKEN")
        )

        self.llm = ChatHuggingFace(
            llm=endpoint,  # ✅ wraps the conversational endpoint
            temperature=0.1
        )
        
        # Initialize Pydantic parser
        self.parser = PydanticOutputParser(pydantic_object=Resume)
        self.cache = ParserCache()
        
        # Create prompt
        self.prompt = PromptTemplate(
            input_variables=["resume_text"],
            template="""You are an expert resume parser. Extract ALL information from this resume and return it in valid JSON format.

Resume Text:
{resume_text}

CRITICAL INSTRUCTIONS - READ CAREFULLY:

1. CONTACT INFORMATION:
   - Extract: name, email, phone, LinkedIn URL, GitHub URL

2. TECHNICAL SKILLS:
   - Extract ALL programming languages, frameworks, tools, databases
   - Look in: Skills section, Technical Skills, Technologies, etc.

3. WORK EXPERIENCE (MANDATORY):
   - Look for sections: "EXPERIENCE", "WORK EXPERIENCE", "PROFESSIONAL EXPERIENCE", "EMPLOYMENT"
   - For EACH job, extract: company, role, duration, description, technologies
   - If you find ANY work experience, include it in "experience" array
   - If truly no work experience exists, return empty array []

4. EDUCATION (MANDATORY):
   - Look for sections: "EDUCATION", "ACADEMIC BACKGROUND", "QUALIFICATIONS"
   - For EACH degree, extract: degree, institution, duration, GPA (as number)
   - If you find ANY education, include it in "education" array
   - Most resumes have education - look carefully!

5. PROJECTS (MANDATORY):
   - Look for: "PROJECTS", "Personal Projects", "Academic Projects", "Key Projects"
   - Projects may be under experience or education sections too
   - For EACH project: title, description, technologies (array), link
   - If you find ANY projects, include them in "projects" array
   - If no projects found, return empty array []

IMPORTANT RULES:
- Return ONLY valid JSON matching the schema
- Do NOT skip sections - extract everything you find
- Arrays should contain ALL items found, not just the first one
- GPA must be a number (e.g., 7.5 not "7.5")
- If a section is missing, use empty array [], do NOT omit the field

{format_instructions}

JSON Output:"""
        )
    
    def load_resume(self, file_path: str) -> str:
        """
        Load resume from PDF or DOCX file
        
        Args:
            file_path: Path to resume file
            
        Returns:
            Resume text content
        """
        print(f"📄 Loading resume: {file_path}")
        
        # Determine file type
        file_ext = os.path.splitext(file_path)[1].lower()
        
        try:
            if file_ext == '.pdf':
                loader = PyPDFLoader(file_path)
                pages = loader.load()
                text = "\n".join([page.page_content for page in pages])
            
            elif file_ext in ['.docx', '.doc']:
                loader = Docx2txtLoader(file_path)
                docs = loader.load()
                text = "\n".join([doc.page_content for doc in docs])
            
            else:
                raise ValueError(f"Unsupported file type: {file_ext}")
            
            print(f"✅ Loaded {len(text)} characters")
            return text
            
        except Exception as e:
            print(f"❌ Error loading file: {e}")
            raise
    
    def parse(self, resume_text: str) -> Resume:
        """
        Parse resume text and return structured data
        """
        try:
            format_instructions = self.parser.get_format_instructions()
            # Create a simple version string or hash of the prompt/instructions
            # This ensures that if we change instructions, the cache invalidates automatically.
            prompt_context = hashlib.md5(f"{self.prompt.template}:{format_instructions}".encode()).hexdigest()
            
            # Format prompt
            formatted_prompt = self.prompt.format(
                resume_text=resume_text,
                format_instructions=format_instructions
            )
            
            # Check cache first with prompt context
            cached_response = self.cache.get(resume_text, category="resume_data", context=prompt_context)
            
            if cached_response:
                print("✨ Found resume data in cache! Skipping LLM call.")
                response = cached_response
            else:
                print("🔄 Parsing resume with LLM...")
                response = self.llm.invoke(formatted_prompt).content
                # Store in cache with context
                self.cache.set(resume_text, category="resume_data", result=response, context=prompt_context)
            
            print("\n📄 Raw LLM Response:")
            print(response[:1500] + "..." if len(response) > 1500 else response)
            print(f"\n📊 Response length: {len(response)} characters")
            print("\n" + "="*60 + "\n")
            
            # Extract JSON from response
            json_str = None
            
            # 1. Try markdown code blocks first
            code_block_match = re.search(r'```json\s*(.*?)\s*```', response, re.DOTALL)
            if code_block_match:
                json_str = code_block_match.group(1)
            
            # 2. Fallback: Find the outermost braces
            if not json_str:
                # Look for the LAST JSON object which usually contains the data (not schema)
                all_json_objects = re.findall(r'\{.*\}', response, re.DOTALL)
                if all_json_objects:
                    # Filter out schema-only objects
                    for obj in reversed(all_json_objects):
                        if "technical_skills" in obj and "$defs" not in obj[:200]:
                            json_str = obj
                            break
                    if not json_str:
                        json_str = all_json_objects[-1]
            
            if json_str:
                json_str = json_str.replace('\n', ' ').strip()
                
                # Parse with Pydantic
                try:
                    # Clean up common issues
                    json_str = json_str.replace('\\_', '_')
                    parsed_data = self.parser.parse(json_str)
                except Exception as parse_err:
                    print(f"⚠️ Pydantic parse failed: {parse_err}. Trying manual fixes.")
                    # Try to remove everything before the first { and after the last }
                    start = json_str.find('{')
                    end = json_str.rfind('}')
                    if start != -1 and end != -1:
                        json_str = json_str[start:end+1]
                    
                    try:
                        pure_json = json.loads(json_str)
                        # Remove $defs if present in the data by mistake
                        if "$defs" in pure_json: del pure_json["$defs"]
                        parsed_data = Resume(**pure_json)
                    except:
                        # Final resort: return empty resume
                        print("🚨 Failed to extract data.")
                        return Resume(summary="", technical_skills=[])
                
                # Normalize skills
                if self.normalize_skills:
                    parsed_data.technical_skills = SkillOntology.normalize_skills(
                        parsed_data.technical_skills
                    )
                    
                    for exp in parsed_data.experience:
                        exp.technologies = SkillOntology.normalize_skills(exp.technologies)
                    
                    for proj in parsed_data.projects:
                        proj.technologies = SkillOntology.normalize_skills(proj.technologies)
                    
                    print("✅ Skills normalized")
                    print(f"📊 Parsed: {len(parsed_data.experience)} experiences, {len(parsed_data.education)} education, {len(parsed_data.projects)} projects")
                    print(f"📊 Parsed: {len(parsed_data.experience)} experiences, {len(parsed_data.education)} education, {len(parsed_data.projects)} projects")
                
                return parsed_data
            else:
                raise ValueError("No JSON found in LLM response")
                
        except Exception as e:
            print(f"❌ Error parsing resume: {e}")
            raise
    
    def parse_file(self, file_path: str) -> Resume:
        """
        Load and parse resume from file
        
        Args:
            file_path: Path to resume file (PDF/DOCX)
            
        Returns:
            Resume: Parsed resume object
        """
        # Load file
        text = self.load_resume(file_path)
        
        # Parse content
        return self.parse(text)

    def parse_upload(self, content: bytes, filename: str) -> Resume:
        """
        Parse resume from uploaded bytes
        
        Args:
            content: File content in bytes
            filename: Original filename (to determine extension)
            
        Returns:
            Resume: Parsed resume object
        """
        import tempfile
        import os
        
        suffix = os.path.splitext(filename)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            temp_file.write(content)
            temp_path = temp_file.name
            
        try:
            return self.parse_file(temp_path)
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    def parse_and_display(self, file_path: str):
        """Parse resume and display results"""
        try:
            result = self.parse_file(file_path)
            return self.display_resume(result)
        except Exception as e:
            print(f"❌ Failed to parse resume: {e}")
            return None
    
    def display_resume(self, result: Resume):
        """Display parsed resume in readable format"""
        if not result:
            print("❌ No data to display")
            return None

        print("✅ PARSED RESUME")
        print("=" * 60)

        if result.summary:
            print(f"\n📝 Summary: {result.summary[:200]}...")



        # Technical Skills
        print(f"\n🔧 Technical Skills ({len(result.technical_skills)}):")
        for skill in result.technical_skills:
            print(f"   • {skill}")

        # Experience
        if result.experience:
            print(f"\n💼 Work Experience ({len(result.experience)}):")
            for i, exp in enumerate(result.experience, 1):
                print(f"\n   {i}. {exp.role} at {exp.company}")
                print(f"      Duration: {exp.duration}")
                if exp.technologies:
                    print(f"      Tech: {', '.join(exp.technologies)}")

        # Education
        if result.education:
            print(f"\n🎓 Education ({len(result.education)}):")
            for edu in result.education:
                print(f"   • {edu.degree} - {edu.institution}")
                print(f"     {edu.duration}")

        # Projects
        if result.projects:
            print(f"\n🚀 Projects ({len(result.projects)}):")
            for i, proj in enumerate(result.projects, 1):
                print(f"\n   {i}. {proj.title}")
                print(f"      {proj.description[:100]}...")
                if proj.technologies:
                    print(f"      Tech: {', '.join(proj.technologies)}")

        print("\n" + "=" * 60)
        return result
    
    def to_json(self, parsed_data: Resume) -> str:
        """Convert to JSON"""
        return parsed_data.model_dump_json(indent=2)
    
    def to_dict(self, parsed_data: Resume) -> dict:
        """Convert to dictionary"""
        return parsed_data.model_dump()