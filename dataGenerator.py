

def responseGenerator(resumeScoreDict):
    finalResponse                   = dict()
    finalResponse['status_code']    = 200

    if(resumeScoreDict['score']>1):
        score                       = 1
    else:
        score                       = resumeScoreDict['score']

    score_in_percent                = score*100

    finalResponse['resume_score_in_percentage']   = score_in_percent
    return finalResponse
