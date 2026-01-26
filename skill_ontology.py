# skill_ontology.py (enhanced version) 
#FUTURE UPDATE: CAN APPLY PREFIX TREE TO THIS TO IMPROVE EFFICIENCY IN TERMS OF TIME COMPLEXITY
import re
from typing import List, Set

class SkillOntology:
    """Enhanced with regex-based skill extraction"""
    
    # All known skills (expanded from before)
    KNOWN_SKILLS = {
    # Programming languages
    "python", "java", "javascript", "typescript", "c++", "c#", "go", "rust", "ruby",
    "scala", "kotlin", "swift", "objective-c", "php", "perl", "haskell", "dart",
    "r", "matlab", "bash", "shell", "powershell",

    # Databases & query languages
    "sql", "mysql", "postgresql", "mongodb", "redis", "cassandra", "oracle", "sqlite",
    "dynamodb", "elasticsearch", "firebase", "mariaDB", "neo4j",

    # Web frameworks & libraries
    "django", "flask", "fastapi", "spring", "spring boot", "express", "node.js",
    "react", "angular", "vue", "svelte", "ember.js", "backbone.js", "next.js",
    "nuxt.js", "gatsby",

    # Machine learning / AI / Data Science
    "machine learning", "ml", "deep learning", "nlp", "computer vision", "reinforcement learning",
    "supervised learning", "unsupervised learning", "tensorflow", "pytorch", "keras",
    "scikit-learn", "pandas", "numpy", "matplotlib", "seaborn", "plotly", "opencv",
    "xgboost", "lightgbm", "catboost", "huggingface", "transformers", "llms", "chatgpt",
    "stable diffusion", "diffusers", "fastai", "spaCy", "nltk", "gensim", "pytorch lightning",
    "mlflow", "wandb", "optuna",

    # Cloud platforms & DevOps tools
    "aws", "azure", "gcp", "docker", "kubernetes", "jenkins", "circleci", "travisci",
    "terraform", "ansible", "chef", "puppet", "helm", "cloudformation", "airflow",
    "mlops", "ci/cd", "gitlab ci", "github actions", "prometheus", "grafana",

    # Version control & collaboration
    "git", "github", "gitlab", "bitbucket", "jira", "confluence", "trello",
    "agile", "scrum", "kanban", "jira agile", "notion", "microsoft teams", "slack",

    # Frontend & UI technologies
    "html", "css", "sass", "less", "bootstrap", "tailwind", "material-ui", "chakra-ui",
    "jquery", "d3.js", "three.js",

    # Backend & API technologies
    "rest api", "graphql", "grpc", "soap", "microservices", "api design", "oauth2", "jwt",

    # Other tech skills / tools
    "linux", "unix", "windows server", "networking", "security", "encryption",
    "tensorflow serving", "docker-compose", "pandas profiling", "data visualization",
    "etl", "spark", "hadoop", "hive", "pig", "kafka", "rabbitmq", "celery",
    "pytest", "unittest", "mock", "selenium", "cypress", "jupyter", "notebooks",
    "power bi", "tableau", "qlikview", "excel", "vba", "matplotlib", "seaborn",
    "data analysis", "data mining", "big data", "statistics", "probability",
    "reinforcement learning", "genetic algorithms", "optimization", "linear algebra",
    "calculus", "algorithm design", "data structures",

    # Misc / general skills
    "teamwork", "communication", "leadership", "problem solving", "critical thinking",
    "time management", "project management", "presentation skills", "adaptability",
}

    
    # Skill patterns (regex)
    SKILL_PATTERNS = {
        r'\bpython\s*\d*\b': 'Python',
        r'\bjs\b|\bjavascript\b': 'JavaScript',
        r'\bml\b|\bmachine\s*learning\b': 'Machine Learning',
        r'\bdl\b|\bdeep\s*learning\b': 'Deep Learning',
        r'\bnlp\b': 'Natural Language Processing',
        r'\bcv\b|\bcomputer\s*vision\b': 'Computer Vision',
        r'\bk8s\b|\bkubernetes\b': 'Kubernetes',
        r'\bpostgres\b|\bpostgresql\b': 'PostgreSQL',
        r'\bmysql\b': 'MySQL',
        r'\bmongo\b|\bmongodb\b': 'MongoDB',
        r'\baws\b|\bamazon\s*web\s*services\b': 'AWS',
        r'\bgcp\b|\bgoogle\s*cloud\b': 'Google Cloud Platform',
        r'\bazure\b': 'Microsoft Azure',
        r'\bdocker\b': 'Docker',
        r'\bpytorch\b': 'PyTorch',
        r'\btensorflow\b|\btf\b': 'TensorFlow',
        r'\bsklearn\b|\bscikit[-\s]learn\b': 'scikit-learn',
        r'\bpandas\b': 'Pandas',
        r'\bnumpy\b': 'NumPy',
        r'\bdjango\b': 'Django',
        r'\bflask\b': 'Flask',
        r'\breact\b|\breactjs\b': 'React',
        r'\bangular\b': 'Angular',
        r'\bvue\b|\bvuejs\b': 'Vue.js',
        r'\bgit\b': 'Git',
        r'\bjenkins\b': 'Jenkins',
        r'\bairflow\b': 'Apache Airflow',
    }
    
    SKILL_MAPPING = {
        # Python variations
        "python": "Python",
        "python3": "Python",
        "python 3": "Python",
        "py": "Python",
        "python2": "Python 2",
        "python 2": "Python 2",
        
        # Machine Learning
        "machine learning": "Machine Learning",
        "ml": "Machine Learning",
        "machinelearning": "Machine Learning",
        "machine-learning": "Machine Learning",
        
        # Data Science
        "data science": "Data Science",
        "ds": "Data Science",
        "datascience": "Data Science",
        
        # Deep Learning
        "deep learning": "Deep Learning",
        "dl": "Deep Learning",
        "deeplearning": "Deep Learning",
        
        # Natural Language Processing
        "natural language processing": "Natural Language Processing",
        "nlp": "Natural Language Processing",
        "nlu": "Natural Language Understanding",
        
        # Computer Vision
        "computer vision": "Computer Vision",
        "cv": "Computer Vision",
        
        # SQL variations
        "sql": "SQL",
        "mysql": "MySQL",
        "postgresql": "PostgreSQL",
        "postgres": "PostgreSQL",
        "mssql": "Microsoft SQL Server",
        "sql server": "Microsoft SQL Server",
        "oracle": "Oracle SQL",
        "sqlite": "SQLite",
        
        # Cloud platforms
        "aws": "AWS",
        "amazon web services": "AWS",
        "azure": "Microsoft Azure",
        "microsoft azure": "Microsoft Azure",
        "gcp": "Google Cloud Platform",
        "google cloud": "Google Cloud Platform",
        "google cloud platform": "Google Cloud Platform",
        
        # JavaScript
        "javascript": "JavaScript",
        "js": "JavaScript",
        "java script": "JavaScript",
        "node": "Node.js",
        "nodejs": "Node.js",
        "node.js": "Node.js",
        
        # Frameworks - Python
        "django": "Django",
        "flask": "Flask",
        "fastapi": "FastAPI",
        "fast api": "FastAPI",
        "pytorch": "PyTorch",
        "tensorflow": "TensorFlow",
        "keras": "Keras",
        "scikit-learn": "scikit-learn",
        "sklearn": "scikit-learn",
        "pandas": "Pandas",
        "numpy": "NumPy",
        
        # Frameworks - JS
        "react": "React",
        "reactjs": "React",
        "react.js": "React",
        "angular": "Angular",
        "angularjs": "Angular",
        "vue": "Vue.js",
        "vuejs": "Vue.js",
        "vue.js": "Vue.js",
        
        # DevOps
        "docker": "Docker",
        "kubernetes": "Kubernetes",
        "k8s": "Kubernetes",
        "jenkins": "Jenkins",
        "gitlab": "GitLab",
        "github": "GitHub",
        "git": "Git",
        
        # Databases
        "mongodb": "MongoDB",
        "mongo": "MongoDB",
        "redis": "Redis",
        "cassandra": "Cassandra",
        "elasticsearch": "Elasticsearch",
        "elastic search": "Elasticsearch",
        
        # Big Data
        "hadoop": "Hadoop",
        "spark": "Apache Spark",
        "apache spark": "Apache Spark",
        "pyspark": "PySpark",
        "kafka": "Apache Kafka",
        "apache kafka": "Apache Kafka",
        
        # Languages
        "java": "Java",
        "c++": "C++",
        "cpp": "C++",
        "c#": "C#",
        "csharp": "C#",
        "c sharp": "C#",
        "r": "R",
        "r programming": "R",
        "golang": "Go",
        "go": "Go",
        "rust": "Rust",
        "scala": "Scala",
        
        # Other tools
        "tableau": "Tableau",
        "power bi": "Power BI",
        "powerbi": "Power BI",
        "excel": "Microsoft Excel",
        "ms excel": "Microsoft Excel",
        "jupyter": "Jupyter",
        "jupyter notebook": "Jupyter",
        "airflow": "Apache Airflow",
        "apache airflow": "Apache Airflow",
        "pydantic": "Pydantic",
    }
    
    # NEW: Skill Hierarchy (Parent Skill -> List of Child/Equivalent Skills)
    SKILL_HIERARCHY = {
        "Machine Learning": [
            "Deep Learning", "Natural Language Processing", "Computer Vision",
            "Reinforcement Learning", "Supervised Learning", "Unsupervised Learning",
            "TensorFlow", "PyTorch", "scikit-learn", "Keras", "XGBoost", "LightGBM", 
            "CatBoost", "MLflow", "HuggingFace", "Transformers"
        ],
        "Deep Learning": ["TensorFlow", "PyTorch", "Keras", "Neural Networks"],
        "Data Science": [
            "Machine Learning", "Data Analysis", "Statistics", "Probability", 
            "Data Mining", "Pandas", "NumPy", "Matplotlib", "Seaborn"
        ],
        "Frontend Development": [
            "JavaScript", "TypeScript", "HTML", "CSS", "React", "Angular", 
            "Vue.js", "Next.js", "SASS", "Tailwind"
        ],
        "Backend Development": [
            "Python", "Java", "Node.js", "Go", "Rust", "Ruby", "Django", "Flask", 
            "FastAPI", "Spring Boot", "Express", "REST API", "GraphQL", "Microservices"
        ],
        "Cloud Computing": ["AWS", "Microsoft Azure", "Google Cloud Platform", "Cloud Architecture"],
        "AWS": ["S3", "EC2", "Lambda", "DynamoDB", "CloudFormation", "SageMaker"],
        "DevOps": [
            "Docker", "Kubernetes", "Jenkins", "Terraform", "Ansible", "CI/CD", 
            "GitLab CI", "GitHub Actions", "Helm"
        ],
        "Big Data": ["Hadoop", "Apache Spark", "Apache Kafka", "ETL", "PySpark"],
        "SQL": ["PostgreSQL", "MySQL", "Microsoft SQL Server", "Oracle SQL", "SQLite"],
        "NoSQL": ["MongoDB", "Redis", "Cassandra", "DynamoDB", "Elasticsearch"],
        "Python": ["Django", "Flask", "FastAPI", "Pandas", "NumPy", "scikit-learn", "PyTorch", "TensorFlow"],
        "JavaScript": ["React", "Angular", "Vue.js", "Node.js", "Next.js", "Express", "TypeScript"]
    }
    
    @classmethod
    def extract_skills_from_text(cls, text: str) -> List[str]:
        """
        Extract skills from text using regex patterns (FAST)
        
        Args:
            text: Job description or resume text
            
        Returns:
            List of normalized skill names
        """
        text_lower = text.lower()
        found_skills = set()
        
        # Method 1: Regex pattern matching
        for pattern, canonical_skill in cls.SKILL_PATTERNS.items():
            if re.search(pattern, text_lower, re.IGNORECASE):
                found_skills.add(canonical_skill)
        
        # Method 2: Word-by-word matching
        words = re.findall(r'\b\w+\b', text_lower)
        bigrams = [f"{words[i]} {words[i+1]}" for i in range(len(words)-1)]
        
        # Check individual words
        for word in words:
            if word in cls.SKILL_MAPPING:
                found_skills.add(cls.SKILL_MAPPING[word])
        
        # Check bigrams (two-word skills like "machine learning")
        for bigram in bigrams:
            if bigram in cls.SKILL_MAPPING:
                found_skills.add(cls.SKILL_MAPPING[bigram])
        
        return sorted(list(found_skills))
    
    @classmethod
    def normalize_skill(cls, skill: str) -> str:
        """Normalize a skill name handling case variations"""
        if not skill:
            return ""
            
        # 1. Normalize to lowercase for lookup
        normalized_key = skill.lower().strip()
        normalized_key = " ".join(normalized_key.split())
        
        # 2. Check mapping first
        if normalized_key in cls.SKILL_MAPPING:
            return cls.SKILL_MAPPING[normalized_key]
            
        # 3. Fallback: Title Case (e.g. "machine learning -> Machine Learning")
        # Ensure we don't return all lowercase unless intended
        return skill.strip().title()
    
    @classmethod
    def normalize_skills(cls, skills: List[str]) -> List[str]:
        """Normalize a list of skills with strict deduplication"""
        if not skills:
            return []
            
        normalized_list = []
        for skill in skills:
            if not skill or not isinstance(skill, str):
                continue
            
            norm = cls.normalize_skill(skill)
            normalized_list.append(norm)
            
        # Deduplicate while preserving case-insensitivity consistency
        seen_lower = set()
        result = []
        
        for skill in normalized_list:
            # Check lowercase version to catch "Docker" vs "docker" duplicates
            if skill.lower() not in seen_lower:
                seen_lower.add(skill.lower())
                result.append(skill)
        
        return sorted(result)

    @classmethod
    def get_equivalent_skills(cls, skill: str) -> Set[str]:
        """
        Get all skills that are considered equivalent or children of this skill.
        
        Args:
            skill: Standardized skill name
            
        Returns:
            Set containing the input skill and all its hierarchy children
        """
        related = {skill}
        if skill in cls.SKILL_HIERARCHY:
            related.update(cls.SKILL_HIERARCHY[skill])
        return related