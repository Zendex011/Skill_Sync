export const mockJobs = [
    {
        id: 1,
        title: "Senior Frontend Engineer",
        company: "TechFlow",
        location: "Remote / San Francisco",
        matchScore: 94,
        salary: "$140k - $180k",
        type: "Full-time",
        skills: ["React", "TypeScript", "Framer Motion", "Tailwind CSS"],
        missingSkills: ["Next.js"],
        description: "We are looking for a frontend wizard to join our design systems team..."
    },
    {
        id: 2,
        title: "AI Solutions Architect",
        company: "DataMinds",
        location: "New York, NY",
        matchScore: 82,
        salary: "$160k - $210k",
        type: "Contract",
        skills: ["Python", "PyTorch", "LLMs"],
        missingSkills: ["Kubernetes", "Docker"],
        description: "Join our core AI team to build next-gen RAG applications..."
    },
    {
        id: 3,
        title: "Product Designer",
        company: "Starlight UI",
        location: "Austin, TX",
        matchScore: 65,
        salary: "$120k - $150k",
        type: "Full-time",
        skills: ["Figma", "Design Systems"],
        missingSkills: ["React", "A/B Testing"],
        description: "Design beautiful, functional interfaces for our global user base..."
    }
];

export const mockResumeData = {
    skills: ["React", "JavaScript", "CSS3", "HTML5", "Python", "Git", "Figma"],
    experience: [
        { title: "Junior Web Developer", company: "WebWiz", period: "2021 - Present" },
        { title: "Freelance Designer", company: "Self-employed", period: "2020 - 2021" }
    ],
    education: [
        { degree: "BS in Computer Science", school: "University of Tech", year: "2020" }
    ]
};

export const mockCandidates = [
    {
        id: 1,
        name: "Alex Johnson",
        title: "Full Stack Developer",
        matchScore: 98,
        skills: ["React", "Node.js", "PostgreSQL"],
        experience: "5 years",
        education: "BS in CS"
    },
    {
        id: 2,
        name: "Sarah Chen",
        title: "UI/UX Designer",
        matchScore: 88,
        skills: ["Figma", "Adobe XD", "CSS"],
        experience: "3 years",
        education: "BFA in Design"
    },
    {
        id: 3,
        name: "Michael Smith",
        title: "Backend Engineer",
        matchScore: 72,
        skills: ["Python", "Django", "AWS"],
        experience: "4 years",
        education: "MS in Engineering"
    }
];
