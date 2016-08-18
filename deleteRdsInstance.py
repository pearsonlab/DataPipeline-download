import boto3
import time
from datetime import date
import properties

client = boto3.client('rds')

db_id = properties.dbInstanceId

def main():
	# get today's date
	today = date.today()
	today_date = str(today)
	# add today's date to the current db name
	finalId = db_id + '-' + today_date
	print("%s is the new snapshot of current instance." % (finalId))
	print("")
	response = client.delete_db_instance(
		DBInstanceIdentifier=db_id,
		SkipFinalSnapshot=False,
		FinalDBSnapshotIdentifier=finalId
		)

if __name__ == '__main__':
	main()