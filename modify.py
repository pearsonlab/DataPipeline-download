import boto3
import properties

client = boto3.client('rds')

db_id = properties.dbInstanceId
allocatedStorage = properties.allocatedStorage
instanceClass = properties.dbInstanceClass
vpc_id = properties.vpcSecurityGroupId
iamRoleName = properties.domainIAMRoleName
dbParameterGroup = properties.dbParameterGroup
optionGroup = properties.optionGroup
dbPort = properties.dbPort
backupRetention = properties.backupRetention
publiclyAccessible = properties.publiclyAccessible
storageType = properties.storageType
multiAZ = properties.multiAZ
applyImmediately = properties.applyImmediately
minorVersionUpgrade = properties.minorVersionUpgrade

def main():
    response_modify = client.modify_db_instance(
        DBInstanceIdentifier=db_id,
        AllocatedStorage=allocatedStorage,
        DBInstanceClass=instanceClass,
        VpcSecurityGroupIds=[
            vpc_id
        ],
        ApplyImmediately=applyImmediately,
        DBParameterGroupName=dbParameterGroup,
        BackupRetentionPeriod=backupRetention,
        MultiAZ=multiAZ,
        AutoMinorVersionUpgrade=minorVersionUpgrade,
        OptionGroupName=optionGroup,
        StorageType=storageType,
        DBPortNumber=dbPort,
        PubliclyAccessible=publiclyAccessible,
        DomainIAMRoleName=iamRoleName,
    )

if __name__ == '__main__':
    main()