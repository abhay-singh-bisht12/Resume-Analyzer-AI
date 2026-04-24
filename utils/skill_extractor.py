import re

skills_list = [
    "python", "java", "c++", "c#", "javascript", "typescript", "php",
    "html", "css", "bootstrap", "tailwind", "react", "react.js",
    "angular", "vue", "node.js", "express.js", "django", "flask",
    "spring boot", "rest api", "api", "nodejs",
    "sql", "mysql", "postgresql", "mongodb", "oracle", "sqlite",
    "firebase", "redis",
    "machine learning", "deep learning", "artificial intelligence",
    "data analysis", "data science", "nlp", "pandas", "numpy",
    "matplotlib", "seaborn", "scikit-learn", "tensorflow", "keras",
    "pytorch", "power bi", "tableau", "excel",
    "git", "github", "docker", "linux", "aws", "azure", "postman",
    "dsa", "data structures", "algorithms", "oops", "dbms",
    "operating system", "computer networks",
    "communication", "teamwork", "leadership", "problem solving"
]

def clean_text(text):
    text = text.lower()
    text = text.replace("\n", " ")
    text = re.sub(r"[^a-z0-9+#. ]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text

def extract_skills(text):
    found_skills = []
    text = clean_text(text)

    for skill in skills_list:
        pattern = r"\b" + re.escape(skill.lower()) + r"\b"
        if re.search(pattern, text):
            found_skills.append(skill)

    found_skills = sorted(list(set(found_skills)))

    database_tools = ["mysql", "postgresql", "sqlite", "oracle"]
    if any(db in found_skills for db in database_tools):
        if "sql" not in found_skills:
            found_skills.append("sql")

    return sorted(found_skills)