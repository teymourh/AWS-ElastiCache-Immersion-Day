+++
title = "Setup  and validation"
date = 2020-08-17T13:41:53-06:00
weight = 3
chapter = false
+++

Let's explore the resources created in the "Getting Started" section of this workshop:

## EC2 bastion host

To allow you exploring in your AWS account we have set up an EC2 instance that you can conenct to via SSH. Or via AWS Systems Manager Session Manager. 

### Option 1: SSH

To connect via SSH, browse to the [EC2 console](https://console.aws.amazon.com/ec2/v2/home?#Instances) and find an instance named `ElastiCache Lab Bastion Host`. Select the instance and find the public IP. 

{{% img "Ec2PublicIp.png" "Find EC2 public IP" %}}

Then using an ssh client, e.g. putty, connect to the instance IP with user name `ec2-user` and the public key that you created in the getting started secion.

### Option 2: Session Manager - Preferred

To connect via AWS Systems Manager Session Manager, browse to the [AWS Systems Manager console](https://console.aws.amazon.com/systems-manager/session-manager/start-session), select the desired host, `ElastiCache Lab Bastion Host`, and click "Start session". If you have trouble accessing this location, ensure you are disconnected from a client VPN on your computer.

{{% img "SsmStartSession.png" "Connect via SSM" %}}

### Using the console

Set up the proper login credentials before proceding with your session.

```bash
sudo su - ec2-user
source /etc/profile
export PATH=$PATH:/usr/local/src/redis-5.0.6/src/:/usr/local/bin/
```

You should now be logged-in on the bastion host via a unix shell. You can validate all is well by running these commands

```bash
env | grep REDIS
env | grep MYSQL
```

## RDS MySQL

Navigate to the [RDS console](https://console.aws.amazon.com/rds/home?#databases:) and selet "Databases". You should see a database called `elaticachemysql`:

{{% img "RdsConsoleOverview.png" "Find RDS in console" %}}

Click on the database to get more details. In particular you may  be interested in the database connection string or endpoint:

{{% img "RdsConsoleEndpoint.png" "Find RDS MySQL endpoint" %}}

To validate that your bastion host is configured correctly, switch to the terminal session you opened in the previous section and verify that the output from this command matches the endpoint from the console:

```bash
echo $MYSQL_HOST
```

To verify that you can connect to the MySQL database type the following into the terminal. When asked for a password enter the password you used in the GettingStarted phase, by default `DatabasePassword`:

```
mysql -u DatabaseUser -p  reviews <<EOT
show columns from reviews;
EOT
```

## Elasticache Redis cluster

You account should contain an Elasticache Redis cluster named `elclabcluster`. Navigate to the [AWS ElastiCache console](https://console.aws.amazon.com/elasticache/home?#redis:), select Redis, and expand the entry for `elclabcluster` to find the "Primary Endpoint"

{{% img "ElasticacheConsole.png" "Find Redis connection string" %}}

You can compare this endpoint information with that pre-populated in the bastion host by running this command:

```bash
env | grep REDIS
```

## ECS cluster for web application

The core of the lab is a docker container running in ECS. This container serves a web page that shows the performance of database lookups. To locate the URL for the web interface to access the sample application,  navigate to the [AWS Elastic Container Service console](https://console.aws.amazon.com/ecs/home?#/clusters), select the ECS “CacheDemoECSService1” Cluster:

{{% img "AWSmgmtConsoleEcsCluster1.png" "Ec2 Resources" %}}

go to the Tasks tab, and select the running task, to find the IP associated with sample application:

{{% img "AWSmgmtConsoleEcsCluster2.png" "Ec2 Resources" %}}

and copy Public IP Address:

{{% img "AWSmgmtConsoleEcsClusterIP.png" "Ec2 Resources" %}}

Finally type `http://<IP>` into a new browser tab to access the application where `<IP>` is replaced by the IP address you just copied.

