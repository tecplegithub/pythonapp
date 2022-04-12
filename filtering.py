import os
import json

file_path                               = os.path.dirname(os.path.realpath(__file__)) + os.path.sep
config_path                             = file_path + 'configProperties.json'

with open(config_path) as application_conf:
    cf                                  = json.load(application_conf)

exp_normalize_range                     = cf['exp_normalization_range']
exp_weightage                           = cf['exp_weightage']

def filterContents(resumeContentDict):
    filteredContentDict                 = {}
    for key,object in resumeContentDict.items():
        objectDict                      = {}
        objectDict["total_exp"]         = object["total_exp"]
        objectDict["skills"]            = object["skills"]
        filteredContentDict[key]        = objectDict

    return filteredContentDict


def createDomainDetailsDict(reqSkillList,skillDetailsCorpus):
    domainDetailsDict                   = {}
    for skill in reqSkillList:
        skill                           = skill.lower()
        if skill in skillDetailsCorpus:
            domainDetailsDict[skill]    = skillDetailsCorpus[skill]
        else:
            pass
    return domainDetailsDict

def expWeightageCalculator(req_exp,cand_exp):
    dynamic_exp_weightage               = 0
    if(req_exp>=0 and cand_exp>=0):
        if (cand_exp<=(req_exp+exp_normalize_range) and cand_exp>=(req_exp-exp_normalize_range)):
            dynamic_exp_weightage       =   exp_weightage
        else:
            if(cand_exp>(req_exp+exp_normalize_range)):
                dynamic_exp_weightage   = exp_weightage/cand_exp
            elif(cand_exp<(req_exp-exp_normalize_range)):
                difference              = req_exp - cand_exp
                divide_factor           = req_exp + difference
                dynamic_exp_weightage   = exp_weightage/divide_factor
            else:
                pass
    else:
        pass

    return dynamic_exp_weightage