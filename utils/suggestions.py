def get_suggestions(missing_skills):
    roadmap = {
        "react": "Learn React components, props, state and hooks. Build a Todo App.",
        "sql": "Learn SELECT, WHERE, JOIN, GROUP BY and practice database queries.",
        "javascript": "Practice DOM, events, functions and small projects.",
        "python": "Practice Python basics and build automation projects.",
        "git": "Learn clone, add, commit, push, pull and branch.",
        "github": "Upload projects on GitHub with proper README.",
        "css": "Learn Flexbox, Grid and responsive design.",
        "html": "Practice forms, tables and semantic tags.",
        "mongodb": "Learn CRUD operations in MongoDB.",
        "node.js": "Build a simple backend API using Node.js.",
        "power bi": "Learn dashboard creation and data visualization."
    }

    suggestions = []

    for skill in missing_skills:
        suggestions.append(
            roadmap.get(skill, f"Learn {skill} basics and add a small project using {skill}.")
        )

    return suggestions