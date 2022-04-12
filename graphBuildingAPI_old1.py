import networkx as nx
from pyvis.network import Network
net                = Network()
Graph              = nx.DiGraph()
GraphToShow        = nx.DiGraph()
import os
import json
import mysql.connector

file_path                           = os.path.dirname(os.path.realpath(__file__)) + os.path.sep
config_path                         = file_path + 'configProperties.json'

with open(config_path) as application_conf:
    cf                              = json.load(application_conf)

sql_host                            = str(cf["sql.host"])
sql_user                            = str(cf["sql.user"])
sql_password                        = str(cf["sql.password"])
sql_database                        = str(cf["sql.database"])
sql_table                           = str(cf["sql.table"])
graph_storage_path                  = str(cf["graph.folder"])

connection                          = mysql.connector.connect(
                                        host              = sql_host,
                                        user              = sql_user,
                                        password          = sql_password,
                                        database          = sql_database
                                    )
cursor                              = connection.cursor()
def ClearDirectory():
    print("Deleting contents in the graph storage folder")

    for f in os.listdir(graph_storage_path):
        os.remove(os.path.join(graph_storage_path, f))

    print("Deleted contents in the graph storage folder")

def fetchSkillDetailsFromTable():
    sql_select_Query                = "select skill,synonyms,primary_level_skillset,secondary_level_skillset  from "+str(sql_table)+str(";")
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    print("Total number of rows in table: ", cursor.rowcount)
    return records

def buildGraph(records):
    graph_storage_path                  = str(cf["graph.folder"])
    for row in records:
        if(row[0] != ""):
            skill                       = str(row[0])
            if(row[1] != ""):
                synonyms_string         = str(row[1])
            else:
                synonyms_string         = ""
            Graph.add_node(skill, synonyms=synonyms_string)
        else:
            pass
        if(row[2] != ""):
            primary_level_skillset_string    = row[2]
            primary_level_skill_list  = primary_level_skillset_string.split("_")
            for primary_level_skill in primary_level_skill_list:
                Graph.add_edge(skill, primary_level_skill, weight=.75)
        else:
            pass
        if (row[3] != ""):
            secondary_level_skillset_string = row[3]
            secondary_level_skill_list = secondary_level_skillset_string.split("_")
            for secondary_level_skill in secondary_level_skill_list:
                Graph.add_edge(skill, secondary_level_skill, weight=.50)
        else:
            pass

    graph_storage_path                      = graph_storage_path +"/skillGraph.gpickle"
    graphStorageStatus                      =  nx.write_gpickle(Graph,graph_storage_path)
    return graphStorageStatus


def showTheCurrentGraph():
    graph_storage_path                      = str(cf["graph.folder"])
    graph_storage_path                      = graph_storage_path + "/skillGraph.gpickle"
    graph_status                            = os.path.isfile(graph_storage_path)
    if(graph_status):
        Graph                                   = nx.read_gpickle(graph_storage_path)
        nodeList                                = list(Graph.nodes)
        for node in nodeList:
            GraphToShow.add_node(node)
        edgeList                                = list(Graph.edges)
        for edge in edgeList:
            weightDetails                       = Graph.get_edge_data(edge[0], edge[1])
            if ('weight' in weightDetails):
                if(weightDetails['weight']==0.75):
                    GraphToShow.add_edge(edge[0], edge[1], value=20)  # show bold
                else:
                    GraphToShow.add_edge(edge[0], edge[1])
            else:
                pass
        net.from_nx(GraphToShow)
        net.show("graph.html")
        return_code                                 = 200
    else:
        return_code                                 = 400

    return return_code
if __name__ == '__main__':
    ClearDirectory()
    records                      =  fetchSkillDetailsFromTable()
    graphStorageStatus           =  buildGraph(records)
    print(graphStorageStatus)

