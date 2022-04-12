import os
#os.environ['TIKA_SERVER_JAR'] = 'https://repo1.maven.org/maven2/org/apache/tika/tika-server/1.19/tika-server-1.19.jar'

import tika
from tika import parser
#current working version resumeparser 8.0
from resume_parser import resumeparse

def resumeParser(resume_path):
    resumeData                              = {}
    resumeParserObject                      = resumeparse.read_file(resume_path)
    if "skills" in resumeParserObject:
        if (len(resumeParserObject['skills'])>0):
            resumeData['status']                = 200
            resumeData['skills']                = resumeParserObject['skills']
        else:
            resumeData['status']                = 400
    else:
        resumeData['status']                = 400

    return resumeData

if __name__ == '__main__':
    resumeParserObject                      = resumeParser("resume_remya.pdf")
    print(resumeParserObject)