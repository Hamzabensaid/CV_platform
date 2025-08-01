def sanitize_cv_data(cv_data: dict) -> dict:
    # Trim spaces in strings
    for key, value in cv_data.items():
        if isinstance(value, str):
            cv_data[key] = value.strip()

    # Clean skills and languages: strip, capitalize, remove duplicates
    if "skills" in cv_data and isinstance(cv_data["skills"], list):
        cv_data["skills"] = list({skill.strip().capitalize() for skill in cv_data["skills"]})

    if "languages" in cv_data and isinstance(cv_data["languages"], list):
        cv_data["languages"] = list({lang.strip().capitalize() for lang in cv_data["languages"]})

    # Clean education and experience entries
    if "education" in cv_data:
        for edu in cv_data["education"]:
            for k, v in edu.items():
                if isinstance(v, str):
                    edu[k] = v.strip()

    if "experience" in cv_data:
        for exp in cv_data["experience"]:
            for k, v in exp.items():
                if isinstance(v, str):
                    exp[k] = v.strip()
            if "technologies" in exp and isinstance(exp["technologies"], list):
                exp["technologies"] = list({tech.strip().capitalize() for tech in exp["technologies"]})

    return cv_data
