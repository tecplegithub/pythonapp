from experianceWeightageCalculator import calculateExperianceWeightage
from skillWeightageCalculator import calculateSkillWeightage
from textCleaningFile       import preProcessSkills
def resumeScoreEngine(min_req_exp,max_req_exp,req_skills,cand_exp,skillList):
    cand_exp_weight             = calculateExperianceWeightage(min_req_exp,max_req_exp,cand_exp)
    print("cand_exp_weight")
    print(cand_exp_weight)
    skillList                   = preProcessSkills(skillList)
    print("Candidate skill List")
    print(skillList)
    reqSkills                   = preProcessSkills(req_skills)
    candSkillWeightObject       = calculateSkillWeightage(reqSkills, skillList)
    if(candSkillWeightObject["status_code"]==200):
        cand_skill_weight       = candSkillWeightObject["cand_skill_weightage"]
        print("cand_skill_weight")
        print(cand_skill_weight)
        total_wight             = cand_exp_weight + cand_skill_weight
        candWeightObject        = {
                                        "status_code": 200,
                                        "cand_score": total_wight
                                  }
    else:
        candWeightObject        = {
                                        "status_code": 400,
                                        "status_message": "Graph not found"
                                  }

    return candWeightObject


