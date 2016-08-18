import boto3
import time
import deleteRdsInstance
import properties
import checkStatus

client = boto3.client('ec2')

instance_id = properties.ec2InstanceId

def main():
	if(checkStatus.main() != "stopped"):
		print("Stopping the instance ... ")
		client.stop_instances(InstanceIds=[instance_id,],)
		time.sleep(30)
		print("Instance stopped")
		print("Connecting RDS instance...")
		print("Deleting current RDS instance and creating a new snapshot...")
		deleteRdsInstance.main()

if __name__ == '__main__':
	main()