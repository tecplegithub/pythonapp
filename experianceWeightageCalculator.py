import os
import json
file_path                           = os.path.dirname(os.path.realpath(__file__)) + os.path.sep
config_path                         = file_path + 'configProperties.json'

with open(config_path) as application_conf:
    cf                              = json.load(application_conf)

exp_nor_range    				    = cf['exp_normalization_range']
exp_full_weightage					= cf['exp_full_weightage']
	
def calculateExperianceWeightage(min_ex,max_ex,cand_ex):
	if((min_ex<=cand_ex) and (cand_ex<=max_ex)):
		cand_exp_weight 	= exp_full_weightage

	elif(( (min_ex-exp_nor_range)<=cand_ex) and (cand_ex<=(max_ex+exp_nor_range))):
		cand_exp_weight 	= exp_full_weightage - 10

	elif(cand_ex<(min_ex-exp_nor_range)):
		exp_diff   			= (min_ex-exp_nor_range)-cand_ex
		cand_exp_weight 	= (exp_full_weightage -20)/exp_diff

	elif(cand_ex > (max_ex+exp_nor_range)):
		exp_diff   			= cand_ex-(max_ex+exp_nor_range)
		cand_exp_weight 	= (exp_full_weightage-20)/exp_diff
	else:
		cand_exp_weight     = 0

	return cand_exp_weight