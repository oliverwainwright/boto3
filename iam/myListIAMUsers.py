#!/usr/bin/python3

import boto3, time, sys
from datetime import date

#def lambda_handler(event, context):
# Create IAM client
client = boto3.client('iam')
resource = boto3.resource('iam')

current_date = date.today()

for user in client.list_users()['Users']:
	if "PasswordLastUsed" in user:
		pwd_last_used = user['PasswordLastUsed'].date()
		days_since_pwd_used = current_date - pwd_last_used
		
		print("User: {0}\nUserID: {1}\nARN: {2}\nCreatedOn: {3}\nDays Since Password Used: {4}\n".format(			
			user['UserName'],
			user['UserId'],
			user['Arn'],
			user['CreateDate'].date(),
			days_since_pwd_used
			)
		)
	else:
		user_name = user['UserName']
		id = user['UserId']
		arn = user['Arn']
		result_list_keys = client.list_access_keys(UserName=user_name)
		access_key = (result_list_keys['AccessKeyMetadata'][0]['AccessKeyId'])
		create_date = (result_list_keys['AccessKeyMetadata'][0]['CreateDate']).date()
		LastUsed = client.get_access_key_last_used(AccessKeyId=access_key)

		if 'LastUsedDate' in LastUsed['AccessKeyLastUsed']:
			key_last_used = LastUsed['AccessKeyLastUsed']['LastUsedDate'].date()
			days_since_key_used = current_date - key_last_used

			print("User: {0}\nUserID: {1}\nARN: {2}\nCreated On: {3}\nDays Since Key Used: {4}\n".format(
				user_name,
				id,
#				access_key,
				arn,
				create_date,
				days_since_key_used
				)
			)		
