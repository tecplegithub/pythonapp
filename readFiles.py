import json
import os
file_path                           = os.path.dirname(os.path.realpath(__file__)) + os.path.sep
skill_corpus_path                   = file_path + 'skillCorpus.json'

def readSkillCorpus():
    with open(skill_corpus_path) as skilCorpusFile:
        skillCorpusDict             = json.load(skilCorpusFile)

    return skillCorpusDict
