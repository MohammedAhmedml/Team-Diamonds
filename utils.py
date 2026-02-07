def analyze_skills(user_skills, required_skills):
    gaps = {}
    strengths = {}

    for skill, req_level in required_skills.items():
        user_level = user_skills.get(skill, 0)

        if user_level >= req_level:
            strengths[skill] = user_level
        else:
            gaps[skill] = req_level - user_level

    return strengths, gaps
