+++
title = "Getting Started"
weight = 2
+++
Your lab will be performed on a temporary AWS account with all AWS resources provisioned. These resources and service instances are deployed individually for each lab participant so there is no shared environment. 

At this point you are ready to log into Event Engine and AWS Console:

[https://dashboard.eventengine.run/login](https://dashboard.eventengine.run/login).


Login with the 12-digit hash provided:

{{% img "EELogin.png" "EELogin" %}}

## Log into Event Engine and AWS Console

Once logged into the Event Engine Team Dashboard access AWS Console. 

**ACTION:** On dashboard click on “AWS Console” button to be directed to console login page and login: 

{{% img "TeamDashAWSConsole.png" "TeamDash AWSConsole" %}}

{{% img "AWSConsoleLogin.png" "AWS Console Login" %}}

**ACTION:** Retrieve the Public IP address to be able to access sample application.

1. On the AWS Console navigate to ECS dashboard:
{{% img "AWSmgmtConsoleEcs.png" "AWS Mgmt Ec2 Console" %}}

2. Select the ECS “CacheDemoECSService1” Cluster:
{{% img "AWSmgmtConsoleEcsCluster1.png" "Ec2 Resources" %}}
3. Go to the Tasks tab, and select the running task, to find the IP associated with sample application:
{{% img "AWSmgmtConsoleEcsCluster2.png" "Ec2 Resources" %}}
4. Copy Public IP Address:
{{% img "AWSmgmtConsoleEcsClusterIP.png" "Ec2 Resources" %}}


