import boto3
import properties

client = boto3.client('ec2')

instance_id = properties.ec2InstanceId

def main():
	response = client.describe_instances(
    	InstanceIds=[
        	instance_id,
    	],
	)
	status = ""
	
	for responses in response["Reservations"]:
		for instances in responses["Instances"]:
			status = instances["State"]["Name"]

	print("The instance is currently: ",status)
	return status

if __name__ == '__main__':
	main()