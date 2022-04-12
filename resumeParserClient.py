import os
#os.environ['TIKA_SERVER_JAR'] = 'https://repo1.maven.org/maven2/org/apache/tika/tika-server/1.19/tika-server-1.19.jar'

import tika
from tika import parser

from resume_parser import resumeparse

def resumeParser(resume_path):
    resumeContentDict                       = dict()
    data                                    = resumeparse.read_file(resume_path)
    resumeContentDict["score"]              = data
    return resumeContentDict