Some example values for $INSTANCE would be:

- up-union-prod-api-instance
- up-union-dev-api-instance
- up-union-dev-worker-instance
- up-union-dev-build-instance
- up-union-<env>-<service>-instance


`../union/infrastructure/tools/ec2_authorize_ingress.sh:`

    CLUSTER=$(aws ec2 describe-instances --filters "Name=tag:Name,Values=$INSTANCE" --region $REGION --profile $PROFILE --output text | grep INSTANCES | awk '{print $13}' | grep -v ebs | tr $'\n' ' ')


`../union/infrastructure/tools/ec2_authorize_ingress.sh:`

    TARGET=$(aws ec2 describe-instances --filters "Name=private-ip-address,Values=$DUTY" --region $REGION --output text)


`../union/infrastructure/tools/ec2_authorize_ingress.sh:`

    IP=$(aws ec2 describe-instances --query "Reservations[*].Instances[*].PublicIpAddress" --filters "Name=private-ip-address,Values=$DUTY" --region $REGION --output text)


`../union/infrastructure/tools/ec2_authorize_ingress.sh:`

    SG=$(aws ec2 describe-instances --query "Reservations[*].Instances[*].SecurityGroups" --filters "Name=private-ip-address,Values=$DUTY" --region $REGION --output text | awk '{print $1}')


`../union/infrastructure/tools/ec2_cluster_ips.sh:`

    CLUSTER=$(aws ec2 describe-instances --query "Reservations[*].Instances[*].PublicIpAddress" --filters "Name=tag:Name,Values=$INSTANCE" --region $REGION --profile $PROFILE --output text)


`../union/infrastructure/tools/ec2_duty_public_ip.sh:`

    CLUSTER=$(aws ec2 describe-instances --query "Reservations[*].Instances[*].PrivateIpAddress" --filters "Name=tag:Name,Values=$INSTANCE" --region $REGION --profile $PROFILE --output text)


`../union/infrastructure/tools/ec2_duty_public_ip.sh:`

    IP=$(aws ec2 describe-instances --query "Reservations[*].Instances[*].PublicIpAddress" --filters "Name=private-ip-address,Values=$DUTY" --region $REGION --output text)


`../union/infrastructure/tools/ec2_report_service.sh:`

    CLUSTER=($(aws ec2 describe-instances --query "Reservations[*].Instances[*].PublicIpAddress" --filters "Name=tag:Name,Values=$INSTANCE" --region $REGION --profile $PROFILE --output text))


`../union/infrastructure/tools/ec2_restart_service.sh:`

    CLUSTER=($(aws ec2 describe-instances --query "Reservations[*].Instances[*].PublicIpAddress" --filters "Name=tag:Name,Values=$INSTANCE" --region $REGION --profile $PROFILE --output text))

----

Response skeleton from describe-instances command

```
$ aws ec2 describe-instances generate-cli-skeleton output

{
    "Reservations": [
        {
            "Groups": [
                {
                    "GroupName": "GroupName", 
                    "GroupId": "GroupId"
                }
            ], 
            "Instances": [
                {
                    "AmiLaunchIndex": 0, 
                    "ImageId": "ImageId", 
                    "InstanceId": "InstanceId", 
                    "InstanceType": "InstanceType", 
                    "KernelId": "KernelId", 
                    "KeyName": "KeyName", 
                    "LaunchTime": "1970-01-01T00:00:00", 
                    "Monitoring": {
                        "State": "State"
                    }, 
                    "Placement": {
                        "AvailabilityZone": "AvailabilityZone", 
                        "Affinity": "Affinity", 
                        "GroupName": "GroupName", 
                        "HostId": "HostId", 
                        "Tenancy": "Tenancy", 
                        "SpreadDomain": "SpreadDomain"
                    }, 
                    "Platform": "Platform", 
                    "PrivateDnsName": "PrivateDnsName", 
                    "PrivateIpAddress": "PrivateIpAddress", 
                    "ProductCodes": [
                        {
                            "ProductCodeId": "ProductCodeId", 
                            "ProductCodeType": "ProductCodeType"
                        }
                    ], 
                    "PublicDnsName": "PublicDnsName", 
                    "PublicIpAddress": "PublicIpAddress", 
                    "RamdiskId": "RamdiskId", 
                    "State": {
                        "Code": 0, 
                        "Name": "Name"
                    }, 
                    "StateTransitionReason": "StateTransitionReason", 
                    "SubnetId": "SubnetId", 
                    "VpcId": "VpcId", 
                    "Architecture": "Architecture", 
                    "BlockDeviceMappings": [
                        {
                            "DeviceName": "DeviceName", 
                            "Ebs": {
                                "AttachTime": "1970-01-01T00:00:00", 
                                "DeleteOnTermination": true, 
                                "Status": "Status", 
                                "VolumeId": "VolumeId"
                            }
                        }
                    ], 
                    "ClientToken": "ClientToken", 
                    "EbsOptimized": true, 
                    "EnaSupport": true, 
                    "Hypervisor": "Hypervisor", 
                    "IamInstanceProfile": {
                        "Arn": "Arn", 
                        "Id": "Id"
                    }, 
                    "InstanceLifecycle": "InstanceLifecycle", 
                    "ElasticGpuAssociations": [
                        {
                            "ElasticGpuId": "ElasticGpuId", 
                            "ElasticGpuAssociationId": "ElasticGpuAssociationId", 
                            "ElasticGpuAssociationState": "ElasticGpuAssociationState", 
                            "ElasticGpuAssociationTime": "ElasticGpuAssociationTime"
                        }
                    ], 
                    "NetworkInterfaces": [
                        {
                            "Association": {
                                "IpOwnerId": "IpOwnerId", 
                                "PublicDnsName": "PublicDnsName", 
                                "PublicIp": "PublicIp"
                            }, 
                            "Attachment": {
                                "AttachTime": "1970-01-01T00:00:00", 
                                "AttachmentId": "AttachmentId", 
                                "DeleteOnTermination": true, 
                                "DeviceIndex": 0, 
                                "Status": "Status"
                            }, 
                            "Description": "Description", 
                            "Groups": [
                                {
                                    "GroupName": "GroupName", 
                                    "GroupId": "GroupId"
                                }
                            ], 
                            "Ipv6Addresses": [
                                {
                                    "Ipv6Address": "Ipv6Address"
                                }
                            ], 
                            "MacAddress": "MacAddress", 
                            "NetworkInterfaceId": "NetworkInterfaceId", 
                            "OwnerId": "OwnerId", 
                            "PrivateDnsName": "PrivateDnsName", 
                            "PrivateIpAddress": "PrivateIpAddress", 
                            "PrivateIpAddresses": [
                                {
                                    "Association": {
                                        "IpOwnerId": "IpOwnerId", 
                                        "PublicDnsName": "PublicDnsName", 
                                        "PublicIp": "PublicIp"
                                    }, 
                                    "Primary": true, 
                                    "PrivateDnsName": "PrivateDnsName", 
                                    "PrivateIpAddress": "PrivateIpAddress"
                                }
                            ], 
                            "SourceDestCheck": true, 
                            "Status": "Status", 
                            "SubnetId": "SubnetId", 
                            "VpcId": "VpcId"
                        }
                    ], 
                    "RootDeviceName": "RootDeviceName", 
                    "RootDeviceType": "RootDeviceType", 
                    "SecurityGroups": [
                        {
                            "GroupName": "GroupName", 
                            "GroupId": "GroupId"
                        }
                    ], 
                    "SourceDestCheck": true, 
                    "SpotInstanceRequestId": "SpotInstanceRequestId", 
                    "SriovNetSupport": "SriovNetSupport", 
                    "StateReason": {
                        "Code": "Code", 
                        "Message": "Message"
                    }, 
                    "Tags": [
                        {
                            "Key": "Key", 
                            "Value": "Value"
                        }
                    ], 
                    "VirtualizationType": "VirtualizationType"
                }
            ], 
            "OwnerId": "OwnerId", 
            "RequesterId": "RequesterId", 
            "ReservationId": "ReservationId"
        }
    ], 
    "NextToken": "NextToken"
}
```
