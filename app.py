import uvicorn
import os
import json
from fastapi import FastAPI,Body,Query
from pydantic import BaseModel
from graphBuildingAPI import ClearDirectory
from graphBuildingAPI import fetchSkillDetailsFromTable
from graphBuildingAPI import buildGraph
from graphBuildingAPI import showTheCurrentGraph
from resumeScrapFile  import resumeParser
from resumeScoreEngineFile import resumeScoreEngine
from typing import Optional
from typing import List
import traceback

file_path                           = os.path.dirname(os.path.realpath(__file__)) + os.path.sep
config_path                         = file_path + 'configProperties.json'

with open(config_path) as application_conf:
    cf                              = json.load(application_conf)

app                                 = FastAPI()

# Routes
@app.post("/v1/buildSkillGraph/")
async def buildSkillGraphFromTable():
    ClearDirectory()
    tableRecords                    = fetchSkillDetailsFromTable()
    graphStorageStatus              = buildGraph(tableRecords)
    if(graphStorageStatus==None):
        graph_storage_status        = {
                                        "status_text" : "Graph Created Successfully",
                                        "status_code" : 200
                                        }
    else:
        graph_storage_status        = {
                                        "status_text" : "Graph Creation Failed",
                                        "status_code" : 400
                                        }

    return graph_storage_status

@app.post("/v1/showGraph/")
async def showCurrentGraph():
    graphDisplayStatus              = showTheCurrentGraph()
    if(graphDisplayStatus==200):
        graph_display_status        = {
                                        "status_text": "Current Graph Displayed",
                                        "status_code": 200
                                      }
    else:
        graph_display_status        = {
                                        "status_text": "No Graph Found",
                                        "status_code": 400
                                      }
    return graph_display_status

class jdDetails(BaseModel):
    min_req_exp: int
    max_req_exp: int
    req_skills :List[str]= Query(None)
    cand_exp: int
    resume_path: str = Body(...)
    cand_skills: Optional[List[str]] = Query(None)


@app.post("/v1/checkCandidateRelevancy/")
async def resumeMatchingMethod(jdDetails: jdDetails):
    try:
        if (jdDetails.min_req_exp==None or jdDetails.max_req_exp==None):
            resume_match_status = {
                "status_text": "No experience specified",
                "status_code": 400
            }
            return resume_match_status
        else:
            pass
        if (jdDetails.req_skills==None):
            resume_match_status = {
                "status_text": "No required skill set specified",
                "status_code": 400
            }
            return resume_match_status
        else:
            pass
        if (jdDetails.cand_exp==None):
            resume_match_status = {
                "status_text": "No candidate experience specified",
                "status_code": 400
            }
            return resume_match_status
        else:
            pass
        if (jdDetails.cand_skills==None):
            if (jdDetails.resume_path==None):
                resume_match_status     =   {
                                                "status_text": "No Resume path specified",
                                                "status_code": 400
                                             }
                return resume_match_status
            else:
                print("Sending resume for parsing..")
                resumeData                    = resumeParser(str(jdDetails.resume_path))
                if(resumeData["status"]==200):
                    print("Resume parsed successfully")
                    skillList                 = resumeData['skills']
                else:
                    print("Resume parsing failed")
                    resume_match_status         = {
                                                    "status_text": "Resume parsing and skill extraction failed",
                                                    "status_code": 400
                                                  }
                    return resume_match_status
        else:
            skillList                           =   jdDetails.cand_skills

        resume_match_status                 = resumeScoreEngine(int(jdDetails.min_req_exp),int(jdDetails.max_req_exp),list(jdDetails.req_skills),int(jdDetails.cand_exp),list(skillList))

        return resume_match_status
    except:
        print(traceback.print_exc())
        resume_match_status                 = {
                                                    "status_text": "Internal server error",
                                                    "status_code": 400
                                                 }
        return resume_match_status

if __name__ == '__main__':
    if((not(cf['exp_full_weightage']+cf['skill_full_weightage']==100))or(cf['exp_full_weightage']<20)or(cf['skill_full_weightage']<20)):
        print("Experience weightage and skill weightage should be grater than 20 and sum of experiance weightage and skill weightage should be 100")
    else:
        uvicorn.run(app, host=cf['app.host'], port=cf['app.port'])
