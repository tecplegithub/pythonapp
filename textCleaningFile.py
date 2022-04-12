def generalPreprocess(skill):
    # for removing both end white spaces
    cleaned_skill           = skill.strip()
    # for removing starting special characters
    for char in cleaned_skill:
        if char.isalnum():
            break
        else:
            cleaned_skill   = cleaned_skill[1:]

    return cleaned_skill
def preProcessSkills(skillList):
    cleanedSkillList                = []
    for skill in skillList:
        skill                       = skill.lower()
        cleaned_skill               = generalPreprocess(skill)
        # for taking skills from key value paried texts
        if ":" in cleaned_skill:
            cleaned_skill           = cleaned_skill.split(":")[1]
            cleaned_skill           = generalPreprocess(cleaned_skill)
        if "=" in cleaned_skill:
            cleaned_skill           = cleaned_skill.split("=")[1]
            cleaned_skill           = generalPreprocess(cleaned_skill)

        cleanedSkillList.append(cleaned_skill)

    return cleanedSkillList
    