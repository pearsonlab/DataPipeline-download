import boto3
import time
import restoreRds
import properties
import checkStatus

client = boto3.client('ec2')

instance_id = properties.ec2InstanceId

def main():
	if(checkStatus.main() == "stopped"):
		print("Starting the instance... ")
		client.start_instances(InstanceIds=[instance_id,],)
		print("Instance started")
		print("Connecting to RDS...")
		time.sleep(60)
		print("Restoring RDS DB snapshot...")
		restoreRds.main()
	else:
		print("Stopping the instance ... ")
		client.stop_instances(InstanceIds=[instance_id,],)
		print("Instance stopped")

if __name__ == '__main__':
	main()