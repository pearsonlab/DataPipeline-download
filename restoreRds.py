import boto3
import time
import properties
import modify

client = boto3.client('rds')

db_id = properties.dbInstanceId
vpc_id = properties.vpcSecurityGroupId
iamRoleName = properties.domainIAMRoleName
instanceClass = properties.dbInstanceClass
dbEngine = properties.dbEngine
optionGroup = properties.optionGroup
dbPort = properties.dbPort
licenseModel = properties.licenseModel
dbSubnetGroup = properties.dbSubnetGroup
storageType = properties.storageType
publiclyAccessible = properties.publiclyAccessible
multiAZ = properties.multiAZ
minorVersionUpgrade = properties.minorVersionUpgrade
tagsToSnapshot = properties.tagsToSnapshot

def main():
    user_input = input("Enter the date of the snapshot you want to restore (YYYY-MM-DD): ")
    snapshot_name = db_id + user_input
    print("You are restoring %s DB snapshot." % (snapshot_name))
    print("***************************************************")
    restore(user_input)

def restore(date):
    snapshot_id = db_id+'-'+date
    response = client.restore_db_instance_from_db_snapshot(
       DBInstanceIdentifier=db_id,
       DBSnapshotIdentifier=snapshot_id,
       DBInstanceClass=instanceClass,
       Port=dbPort,
       DBSubnetGroupName=dbSubnetGroup,
       MultiAZ=multiAZ,
       PubliclyAccessible=publiclyAccessible,
       AutoMinorVersionUpgrade=minorVersionUpgrade,
       LicenseModel=licenseModel,
       Engine=dbEngine,
       OptionGroupName=optionGroup,
       StorageType=storageType,
       CopyTagsToSnapshot=tagsToSnapshot,
    )

    # continue here
    print("It may take around 8-10 minutes to restore the DB snapshot. Check below for the status")
    print("...")
    while checkStatus() != "available":
        time.sleep(75)
        checkStatus()
    else:
        print("")
        print("The snapshot is completely restored. Now, trying to modify it for easy access.")
        modify.main()

def checkStatus():
    response = client.describe_db_instances(
        DBInstanceIdentifier=db_id,
    )

    currentStatus = ""

    for responses in response["DBInstances"]:
        currentStatus = responses["DBInstanceStatus"]

    print("Instance is ", currentStatus)
    return currentStatus

if __name__ == '__main__':
    main()
