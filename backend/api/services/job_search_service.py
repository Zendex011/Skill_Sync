import urllib.parse
from typing import List, Dict, Any

class JobSearchService:
    """
    Generates intelligent job search links for various platforms based on resume data.
    """
    
    PLATFORMS = {
        'linkedin': {
            'name': 'LinkedIn',
            'base_url': 'https://www.linkedin.com/jobs/search/',
            'params': {'keywords': '{query}', 'location': '{location}'}
        },
        'naukri': {
            'name': 'Naukri',
            'base_url': 'https://www.naukri.com/{query}-jobs-in-{location}',
            'params': {}  # Naukri uses path-based params mostly
        },
        'indeed': {
            'name': 'Indeed',
            'base_url': 'https://www.indeed.com/jobs',
            'params': {'q': '{query}', 'l': '{location}'}
        },
        'instahyre': {
            'name': 'Instahyre',
            'base_url': 'https://www.instahyre.com/search-jobs/',
            'params': {'q': '{query}', 'location': '{location}'} # Instahyre acts differently, but generic search works
        }, 
        'google_jobs': {
            'name': 'Google Jobs',
            'base_url': 'https://www.google.com/search',
            'params': {'q': '{query} jobs in {location}', 'ibp': 'htl;jobs'}
        },
         'wellfound': {
            'name': 'Wellfound',
            'base_url': 'https://wellfound.com/jobs',
            'params': {'q': '{query}', 'l': '{location}'} 
        }
    }

    def generate_links(self, resume_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate a list of job search objects.
        
        link_object = {
            "platform": "LinkedIn",
            "query": "Python Developer",
            "location": "Bangalore",
            "url": "https://...",
            "priority": "High" | "Medium"
        }
        """
        links = []
        
        # 1. Extract context
        skills = resume_data.get('technical_skills', [])
        # Prefer "role" from latest experience, else infer from skills
        current_role = self._extract_current_role(resume_data)
        location = "India" # Default, could extract from resume specific city
        
        top_skills = skills[:3] if skills else ['Software Engineer']
        
        # 2. Generate Queries
        queries = []
        
        # Query A: Role based (High Priority)
        if current_role:
            queries.append({
                'text': current_role,
                'priority': 'High',
                'desc': f"{current_role} roles"
            })
            
        # Query B: Top Skill + Role (High Priority)
        if top_skills:
            main_skill = top_skills[0]
            role_suffix = "Developer" if "Developer" not in current_role else ""
            q_text = f"{main_skill} {role_suffix}".strip()
            queries.append({
                'text': q_text,
                'priority': 'High',
                'desc': f"{main_skill} opportunities"
            })
            
        # Query C: Skill Combos (Medium Priority)
        if len(top_skills) >= 2:
            combo = f"{top_skills[0]} {top_skills[1]}"
            queries.append({
                'text': combo,
                'priority': 'Medium',
                'desc': f"{combo} stack jobs"
            })

        # 3. Build Links for each platform
        for q in queries:
            for platform_key, config in self.PLATFORMS.items():
                
                # Specialized logic for Naukri path construction
                if platform_key == 'naukri':
                    # sanitize for url path
                    q_slug = q['text'].lower().replace(' ', '-')
                    loc_slug = location.lower().replace(' ', '-')
                    url = config['base_url'].format(query=q_slug, location=loc_slug)
                else:
                    # Standard query param construction
                    params = {}
                    for k, v in config['params'].items():
                        params[k] = v.format(query=q['text'], location=location)
                    
                    query_string = urllib.parse.urlencode(params)
                    url = f"{config['base_url']}?{query_string}"
                
                links.append({
                    'platform': config['name'],
                    'platform_key': platform_key,
                    'query': q['desc'],
                    'url': url,
                    'priority': q['priority'],
                    'location': location
                })
                
        # Limit total suggestions to avoid overwhelm (e.g., top 8)
        return links[:12]

    def _extract_current_role(self, resume_data: Dict) -> str:
        """Helper to find the most recent role"""
        experience = resume_data.get('experience', [])
        if experience:
            # Assuming first in list is most recent
            return experience[0].get('role', 'Software Engineer')
        return 'Software Engineer'
