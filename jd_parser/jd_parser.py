# jd_parser_hybrid.py
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List, Optional
from dotenv import load_dotenv
import os
import json
import re
import sys
import hashlib

# Add parent directory and self directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from skill_ontology import SkillOntology
from utils.parsing_cache import ParserCache
import time

load_dotenv()

# Simplified model for LLM (no skills)
class JobMetadata(BaseModel):
    """Metadata that requires LLM understanding"""
    job_title: str = Field(description="Job title")
    company: Optional[str] = Field(default=None, description="Company name")
    location: Optional[str] = Field(default=None, description="Location")
    experience_required: str = Field(description="Years of experience")
    job_type: Optional[str] = Field(default=None, description="Job type")
    salary_range: Optional[str] = Field(default=None, description="Salary range")

class JobDescription(BaseModel):
    """Complete job description"""
    job_title: str
    company: Optional[str] = None
    location: Optional[str] = None
    experience_required: str
    technical_skills: List[str] = []
    soft_skills: List[str] = []
    job_type: Optional[str] = None
    salary_range: Optional[str] = None

class HybridJDParser:
    """
    Hybrid parser: Regex for skills + LLM for metadata
    Faster and cheaper than pure LLM approach
    """
    
    def __init__(self):
        endpoint = HuggingFaceEndpoint(
            repo_id="mistralai/Mistral-7B-Instruct-v0.2",
            task="conversational",  # ✅ must be conversational
            temperature=0.1,
            huggingfacehub_api_token=os.getenv("HF_TOKEN") or os.getenv("HUGGINGFACEHUB_API_TOKEN")
        )

        llm = ChatHuggingFace(
            llm=endpoint,  # ✅ wraps the conversational endpoint
            temperature=0.1
        )
        self.llm = llm
        self.parser = PydanticOutputParser(pydantic_object=JobMetadata)
        self.cache = ParserCache()
        
        # Simpler prompt (no skill extraction)
        self.prompt = PromptTemplate(
            input_variables=["job_description"],
            template="""Extract metadata from this job description. DO NOT extract skills.

Job Description:
{job_description}

Extract ONLY:
- Job title
- Company name
- Location
- Experience required
- Job type
- Salary range

Return ONLY valid JSON. Do not escape underscores:
{format_instructions}

JSON:"""
        )
    
    def parse(self, job_text: str) -> JobDescription:
        """Parse using hybrid approach"""
        
        print("="*60)
        print("🚀 HYBRID PARSING")
        print("="*60)
        
        # STEP 1: Fast skill extraction (regex)
        print("\n⚡ Step 1: Extracting skills (regex)...")
        start_time = time.time()
        
        technical_skills = SkillOntology.extract_skills_from_text(job_text)
        
        skills_time = time.time() - start_time
        print(f"✅ Found {len(technical_skills)} skills in {skills_time:.3f}s")
        print(f"   Skills: {', '.join(technical_skills[:5])}{'...' if len(technical_skills) > 5 else ''}")
        
        # STEP 2: LLM for complex metadata
        print("\n🤖 Step 2: Extracting metadata (LLM)...")
        start_time = time.time()
        try:
            format_instructions = self.parser.get_format_instructions()
            # Create a hash of the prompt and format instructions for cache context
            prompt_context = hashlib.md5(f"{self.prompt.template}:{format_instructions}".encode()).hexdigest()

            # 1. Check cache first
            cached_response = self.cache.get(job_text, category="jd_data", context=prompt_context)
            if cached_response:
                print("✨ Found job data in cache!")
                response = cached_response
            else:
                # 2. Call LLM
                formatted_prompt = self.prompt.format(
                    job_description=job_text, # Changed from jd_text to job_description to match prompt template
                    format_instructions=format_instructions
                )
                print("🤖 Calling LLM for metadata...") # Adjusted print message
                response = self.llm.invoke(formatted_prompt).content
                # Store in cache with context
                self.cache.set(job_text, category="jd_data", result=response, context=prompt_context)
        except Exception as e:
            print(f"❌ Error during LLM metadata extraction: {e}")
            response = "{}" # Provide a default empty JSON or handle as needed
        
        llm_time = time.time() - start_time
        print(f"✅ LLM completed in {llm_time:.3f}s")
        
        # Parse LLM response
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            json_str = json_match.group(0).replace('\n', ' ').strip()
            # Fix escaped underscores
            json_str = json_str.replace("\\_", "_")
            metadata = self.parser.parse(json_str)
        else:
            raise ValueError("Failed to extract metadata from LLM response")
        
        # STEP 3: Combine results
        print("\n🔗 Step 3: Combining results...")
        
        result = JobDescription(
            job_title=metadata.job_title,
            company=metadata.company,
            location=metadata.location,
            experience_required=metadata.experience_required,
            technical_skills=technical_skills,  # From regex!
            soft_skills=[],  # Could also extract with regex if needed
            job_type=metadata.job_type,
            salary_range=metadata.salary_range
        )
        
        total_time = skills_time + llm_time
        print(f"\n⏱️  Total time: {total_time:.3f}s")
        if total_time > 0:
            print(f"   Regex: {skills_time:.3f}s ({skills_time/total_time*100:.1f}%)")
            print(f"   LLM: {llm_time:.3f}s ({llm_time/total_time*100:.1f}%)")
        else:
            print("   (Parsing completed instantly via cache)")
        print("="*60)
        
        return result
    
    def parse_and_display(self, job_text: str):
        """Parse and display results"""
        result = self.parse(job_text)
        
        print("\n✅ PARSED JOB DESCRIPTION")
        print("="*60)
        print(f"📌 Job Title: {result.job_title}")
        print(f"⏳ Experience: {result.experience_required}")
        
        print(f"\n🔧 Technical Skills ({len(result.technical_skills)}) [REGEX EXTRACTED]:")
        for skill in result.technical_skills:
            print(f"   • {skill}")
        
        print("="*60)
        return result

    def to_json(self, parsed_data: JobDescription) -> str:
        """Convert parsed data to JSON string"""
        return parsed_data.model_dump_json(indent=2)
    
    def to_dict(self, parsed_data: JobDescription) -> dict:
        """Convert parsed data to dictionary"""
        return parsed_data.model_dump()