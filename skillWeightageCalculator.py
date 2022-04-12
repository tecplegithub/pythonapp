import networkx as nx
import os
import json
file_path                                   = os.path.dirname(os.path.realpath(__file__)) + os.path.sep
config_path                                 = file_path + 'configProperties.json'

with open(config_path) as application_conf:
    cf                                      = json.load(application_conf)

graph_storage_path                          = str(cf["graph.folder"])
onlyfiles                                   = [f for f in os.listdir(graph_storage_path) if os.path.isfile(os.path.join(graph_storage_path, f))]
current_graph_name                          = ""
for file in onlyfiles:
    if file.endswith(".gpickle"):
        current_graph_name                  = file
    else:
        pass
graph_storage_path                          = graph_storage_path + "/"+current_graph_name
skill_full_weightage					    = cf['skill_full_weightage']

def getSynonymMatchingScore(Graph,each_req_skill, candskillList,each_skill_full_weightage):
    if(Graph.has_node(each_req_skill)):
        if('synonyms' in Graph.nodes[each_req_skill]):
            synonym_string                     = Graph.nodes[each_req_skill]['synonyms']
            synonymList                        = synonym_string.split(",")
            if(len(list(set(synonymList) & set(candskillList)))>0):
                synonym_skill_weightage     =each_skill_full_weightage
            else:
                synonym_skill_weightage     =0
        else:
            synonym_skill_weightage         = 0
    else:
        synonym_skill_weightage             = 0

    return synonym_skill_weightage

def get75PercentMatchingScore(Graph, each_req_skill, candskillList,each_skill_full_weightage):
    list75PercetMatchingSkills              = []
    if (Graph.has_node(each_req_skill)):
        skillPairList                       =   Graph.edges(each_req_skill)
        if(len(skillPairList)>0):
            for skillPair in skillPairList:
                if(Graph[skillPair[0]][skillPair[1]]["weight"]==.75):
                    list75PercetMatchingSkills.append(skillPair[0])
                    if (Graph.has_node(skillPair[0])):
                        if ('synonyms' in Graph.nodes[skillPair[0]]):
                            synonym_string              = Graph.nodes[skillPair[0]]['synonyms']
                            synonymList                 = synonym_string.split(",")
                            list75PercetMatchingSkills  = list75PercetMatchingSkills+synonymList
                        else:
                            pass
                    else:
                        pass
                    list75PercetMatchingSkills.append(skillPair[1])
                    if (Graph.has_node(skillPair[1])):
                        if ('synonyms' in Graph.nodes[skillPair[1]]):
                            synonym_string              = Graph.nodes[skillPair[1]]['synonyms']
                            synonymList                 = synonym_string.split(",")
                            list75PercetMatchingSkills  = list75PercetMatchingSkills+synonymList
                        else:
                            pass
                    else:
                        pass
                else:
                    pass
        else:
            pass
    else:
        pass

    if (len(list(set(list75PercetMatchingSkills) & set(candskillList))) > 0):
        reasonable_skill_weightage          = (each_skill_full_weightage*0.75)
    else:
        reasonable_skill_weightage          = 0

    return reasonable_skill_weightage


def get50PercentMatchingScore(Graph, each_req_skill, candskillList,each_skill_full_weightage):
    list50PercetMatchingSkills              = []
    if (Graph.has_node(each_req_skill)):
        skillPairList                       = Graph.edges(each_req_skill)
        if (len(skillPairList) > 0):
            for skillPair in skillPairList:
                if (Graph[skillPair[0]][skillPair[1]]["weight"] == 0.50):
                    list50PercetMatchingSkills.append(skillPair[0])
                    if (Graph.has_node(skillPair[0])):
                        if ('synonyms' in Graph.nodes[skillPair[0]]):
                            synonym_string              = Graph.nodes[skillPair[0]]['synonyms']
                            synonymList                 = synonym_string.split(",")
                            list50PercetMatchingSkills  = list50PercetMatchingSkills+synonymList
                        else:
                            pass
                    else:
                        pass
                    list50PercetMatchingSkills.append(skillPair[1])
                    if (Graph.has_node(skillPair[1])):
                        if ('synonyms' in Graph.nodes[skillPair[1]]):
                            synonym_string              = Graph.nodes[skillPair[1]]['synonyms']
                            synonymList                 = synonym_string.split(",")
                            list50PercetMatchingSkills  = list50PercetMatchingSkills+synonymList
                        else:
                            pass
                    else:
                        pass
                else:
                    pass
        else:
            pass
    else:
        pass

    if (len(list(set(list50PercetMatchingSkills) & set(candskillList))) > 0):
        partial_skill_weightage = (each_skill_full_weightage * 0.50)
    else:
        partial_skill_weightage = 0

    return partial_skill_weightage


def calculateSkillWeightage(req_skills, candskillList):
    graph_status                            = os.path.isfile(graph_storage_path)
    print(graph_status)
    print(graph_storage_path)
    if (graph_status):
        Graph                               = nx.read_gpickle(graph_storage_path)
        each_skill_full_weightage           = skill_full_weightage/len(req_skills)
        print("each_skill_full_weightage")
        print(each_skill_full_weightage)
        cand_skill_weightage                = 0
        for each_req_skill in req_skills:
            exactMatch                      = False
            synonymMatch                    = False
            reasonableMatch                 = False
            partialMatch                    = False
            #check for exact match
            if each_req_skill in candskillList:
                print("exact matched " + str(each_req_skill))
                cand_skill_weightage        = cand_skill_weightage+each_skill_full_weightage
                exactMatch                  = True
            # check for synonyms match
            if (not(exactMatch)):
                synonym_skill_weightage     = getSynonymMatchingScore(Graph,each_req_skill, candskillList,each_skill_full_weightage)
                if (synonym_skill_weightage>0):
                    print("synonym matched "+str(each_req_skill))
                    cand_skill_weightage    = cand_skill_weightage + synonym_skill_weightage
                    synonymMatch            = True
                else:
                    pass

            #Check for 75% match
            if(not(exactMatch)  and not(synonymMatch)):
                reasonable_skill_weightage  = get75PercentMatchingScore(Graph, each_req_skill, candskillList,each_skill_full_weightage)
                if (reasonable_skill_weightage>0):
                    print("75% matched " + str(each_req_skill))
                    cand_skill_weightage    = cand_skill_weightage + reasonable_skill_weightage
                    reasonableMatch         = True
                else:
                    pass
            #Check for 50% match
            if (not(exactMatch) and not(synonymMatch) and not(reasonableMatch)):
                partial_skill_weightage     = get50PercentMatchingScore(Graph, each_req_skill, candskillList,each_skill_full_weightage)
                if (partial_skill_weightage > 0):
                    print("50% matched " + str(each_req_skill))
                    cand_skill_weightage    = cand_skill_weightage + partial_skill_weightage
                    partialMatch = True
                else:
                    pass
            if (not(exactMatch) and not(synonymMatch) and not(reasonableMatch) and not(partialMatch)):
                pass

        skillWeightageStatus                =   {
                                                "status_code": 200,
                                                "cand_skill_weightage": cand_skill_weightage
                                                }

    else:
        skillWeightageStatus                =   {
                                                "status_code":400,
                                                "status_text":"No graph found in the folder"
                                                }
    return skillWeightageStatus


