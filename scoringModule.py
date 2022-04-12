import operator
from filtering import expWeightageCalculator
import os
import json

file_path                                   = os.path.dirname(os.path.realpath(__file__)) + os.path.sep
config_path                                 = file_path + 'configProperties.json'

with open(config_path) as application_conf:
    cf                                      = json.load(application_conf)

skill_weightage                             = cf['skill_weightage']

punc                                        = '''!()-[]{};:'"\, <>/?@$%^&*_~'''

def cleanSkill(skill):
    skill                                   = skill.lower()
    for ele in skill:
        if ele in punc:
            skill                           = skill.replace(ele, "")

    cleanedskill                            = skill.strip()

    return cleanedskill

def scoringResume(req_exp,domainDetailsDict,filteredContentDict):
    resumeScoreDict                         = {}
    resume_score                            = 0
    keys_count                              = len(list(domainDetailsDict.keys()))
    each_skill_weightage                    = skill_weightage/keys_count
    for resume_name,resumeObject in filteredContentDict.items():
        cand_exp                            = resumeObject["total_exp"]
        dynamic_exp_weightage               = expWeightageCalculator(req_exp,cand_exp)
        exp_score                           = dynamic_exp_weightage
        skill_set_score                     = 0
        candSkillList                       = resumeObject['skills']
        for each_skill in candSkillList:
            each_skill                      = cleanSkill(each_skill)
            for domainskill,domainskillList in domainDetailsDict.items():
                if each_skill in domainskillList:
                    skill_set_score         = skill_set_score + each_skill_weightage
                else:
                    pass

        resume_score                        = exp_score + skill_set_score

        resumeScoreDict[resume_name]        = resume_score



    return resumeScoreDict

def scoringEvaluation(resumeScoreDict):
    scoreEvaluationResults = dict(sorted(resumeScoreDict.items(), key=operator.itemgetter(1), reverse=True))
    return scoreEvaluationResults