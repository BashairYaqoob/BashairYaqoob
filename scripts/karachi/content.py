"""Everything the cards say. Edit copy here, then run `python scripts/render.py`.

Every claim below is taken from the linked repositories; keep it that way.
"""

USERNAME = "BashairYaqoob"
NAME = ("Bashair", "Yaqoob")
LOCALE = "Karachi, Pakistan"

TAGLINE = ("Builds AI that ", "listens, retrieves", " and acts.")

# neofetch-style detail block in the hero
DETAILS = [
    ("Role", "CS undergraduate · FAST NUCES Karachi"),
    ("Focus", "AI/ML engineering · NLP · LLM applications"),
    ("Building", "RAG systems · AI agents · realtime voice"),
    ("Also", "software engineering · full-stack web"),
    ("Stack", "Python · TypeScript · LangGraph · FastAPI"),
    ("Leads", "ACM · GitHub Campus Club · PROCOM"),
    ("Locale", LOCALE),
]

ARSENAL = [
    ("ai/", "LLMs, agents & retrieval",
     ["LangChain", "LangGraph", "RAG", "Chroma", "Groq", "Gemini Realtime", "LiveKit Agents", "Vapi"]),
    ("backend/", "services & data",
     ["Python", "FastAPI", "Pydantic", "Node.js", "SQLite", "Supabase", "pytest"]),
    ("web/", "interfaces",
     ["TypeScript", "React", "Vite", "Tailwind CSS", "TanStack Start", "Vercel"]),
    ("automation/", "browsers & pipelines",
     ["Playwright", "BeautifulSoup", "openpyxl", "Git", "GitHub Actions"]),
    ("foundations/", "coursework in C, C++ & systems",
     ["C", "C++", "Assembly", "Data Structures", "DBMS", "Operating Systems", "Networks"]),
]

PROJECTS = [
    dict(
        slug="ai-video-interviewer", no="01", title="AI Video Interviewer",
        url="https://github.com/BashairYaqoob/AI-Video-Interviewer",
        kind="hackathon · in progress",
        blurb=["Joins a live video call and interviews a candidate with",
               "questions grounded in their resume, the job description",
               "and their actual GitHub code."],
        flow=["JD + resume", "GitHub evidence", "gap analysis", "question plan", "recruiter gate", "live call"],
        stack=["Python", "LangGraph", "LiveKit", "Gemini Realtime", "FastAPI", "SQLite"],
    ),
    dict(
        slug="blindspot-ai", no="02", title="Blindspot AI",
        url="https://github.com/shahirahere5/Blindspot-AI",
        kind="hackathon · team project",
        blurb=["Reviews decision documents through six adversarial",
               "agents and a moderator, tracks blind spots across",
               "revisions and answers grounded follow-up questions."],
        flow=["document", "structured analysis", "6-agent debate", "knowledge graph", "grounded chat"],
        stack=["FastAPI", "Pydantic", "React 19", "TypeScript", "Groq"],
    ),
    dict(
        slug="whatsapp-rag-bot", no="03", title="Bashair AI · WhatsApp",
        url="https://github.com/BashairYaqoob/Whatsapp-Langchain-Bot",
        kind="RAG assistant",
        blurb=["A WhatsApp assistant that answers from a RAG",
               "knowledge base and remembers personal facts",
               "about each person it talks to."],
        flow=["WhatsApp", "Baileys", "Chroma retrieval", "Groq LLM", "per-user memory"],
        stack=["Node.js", "LangChain", "Chroma", "Groq", "Baileys"],
    ),
    dict(
        slug="lead-generation-agent", no="04", title="Lead Generation Agent",
        url="https://github.com/BashairYaqoob/Lead-Generation-Agent",
        kind="browser automation",
        blurb=["Turns “find gyms in Karachi” into a formatted Excel",
               "sheet of leads, scraped from Google Maps with",
               "retrying browser automation and email discovery."],
        flow=["prompt", "query parser", "Google Maps", "scrape + emails", "Excel"],
        stack=["Python", "Playwright", "BeautifulSoup", "openpyxl"],
    ),
]

LINKS = [
    ("linkedin", "LinkedIn", "in/bashair-y", "https://www.linkedin.com/in/bashair-y-a1a274357/"),
    ("portfolio", "Portfolio", "bashairyaqoob.vercel.app", "https://bashairyaqoob.vercel.app"),
    ("email", "Email", "bashairyaqoob@gmail.com", "mailto:bashairyaqoob@gmail.com"),
    ("github", "GitHub", "@BashairYaqoob", "https://github.com/BashairYaqoob"),
]

SECTIONS = {
    "who": ("01", "Who am I", "whoami"),
    "arsenal": ("02", "Technical arsenal", "ls ~/arsenal"),
    "work": ("03", "Selected work", "ls ~/projects"),
    "city": ("04", "A year in lights", "./render-city"),
    "now": ("05", "Currently", "cat ~/now.md"),
    "connect": ("06", "Connect", "ssh bashair@karachi"),
}
