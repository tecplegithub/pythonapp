from resumeParserClient import resumeParser
from filtering import filterContents,createDomainDetailsDict
from readFiles import readSkillCorpus
from scoringModule import scoringResume
from dataGenerator import responseGenerator

import traceback
""" import spacy
import en_core_web_sm """
import uvicorn
import os
import json
from fastapi import FastAPI,Body
from pydantic import BaseModel

file_path                           = os.path.dirname(os.path.realpath(__file__)) + os.path.sep
config_path                         = file_path + 'configProperties.json'

with open(config_path) as application_conf:
    cf                              = json.load(application_conf)


app                                 = FastAPI()

class jdDetails(BaseModel):
    req_exp: int
    req_skills: list


skillDetailsCorpus                  = readSkillCorpus()

def resumeScoring(resume_path,jdDetails):

    resumeContentDict               = resumeParser(resume_path)

    filteredContentDict             = filterContents(resumeContentDict)

    domainDetailsDict               = createDomainDetailsDict(jdDetails.req_skills, skillDetailsCorpus)

    resumeScoreDict                 = scoringResume(jdDetails.req_exp, domainDetailsDict, filteredContentDict)

    response                        = responseGenerator(resumeScoreDict)

    return response

# Routes
@app.post("/v1/resumeScoring/")
async def resumeScoringMethod(jdDetails: jdDetails, resume_path: str = Body(...)):

    try:
        if(resume_path.strip()==""):
            response                    = {
                                                "status_code": 400,
                                                "status_text": "Resume path cannot be NULL"
                                           }
        elif(jdDetails.req_exp<0):
            response                    =  {
                                                "status_code": 400,
                                                "status_text": "Required experience cannot be negative"
                                            }
        elif(len(jdDetails.req_skills)==0):
            response                    =   {
                                                "status_code": 400,
                                                "status_text": "Required skill list cannot be empty"
                                            }
        else:
            response 	                    = resumeScoring(resume_path,jdDetails)


        return response
    except:
        print("Traceback occurred "+ str(traceback.print_exc()))

        response                        = {
                                             "status_code":400,
                                             "status_text": "Failed to score resume"
                                          }
        return response

if __name__ == '__main__':
	uvicorn.run(app,host=cf['app.host'],port=cf['app.port'])



