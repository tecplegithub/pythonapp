import uvicorn
import os
import json
from fastapi import FastAPI,Body
from pydantic import BaseModel
from graphBuildingAPI import ClearDirectory
from graphBuildingAPI import fetchSkillDetailsFromTable
from graphBuildingAPI import buildGraph
from graphBuildingAPI import showTheCurrentGraph

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

if __name__ == '__main__':
	uvicorn.run(app,host=cf['app.host'],port=cf['app.port'])