+++
title = "Setup & Configuration"
weight = 3
+++
In the following steps we will connect to EC2 instance and go through setup and configuration of the environment such that the application can be run.

## Connect via SSH into EC2 instance

ACTION: From the Instances page of the AWS Console EC2 Dashboard select the running EC2 instance and click the “Connect” button.

{{% img "EC2Dash.png" "EC2 Dash" %}}

Take appropriate steps to connect via SSH Client.  Details on connecting via Putty are available here [Connect Using Putty](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/putty.html?icmpid=docs_ec2_console).  For Linux/OSX based environments permissions on SHH key must be adjusted to allow for SSH to work from Terminal.

{{% img "SSHClientCx.png" "SSH Client Cx" %}}

## Setup EC2 Instance

Once connected to EC2 instance via SSH:


ACTION: In user home directory change access privileges for application data in ‘ElcDbCacheLab’:

```bash
sudo chmod -R 777 ElcDbCacheLab/
```
{{% img "Chmod.png" "chmod" %}}

ACTION: Change directory to ‘/home/ec2-user/ElcDbCacheLab/Code’ and execute the ‘dockerSetup.sh’ bash script:

{{% img "dockerSetupSh.png" "docker setup" %}}

The script will reboot the instance and therefore you will be disconnected.  Please re-connect via SSH:

{{% img "SSHreCon.png" "SSH Re-Connect" %}}

## Create and populated RDS MySQL table

We will now connect to the RDS MySQL database and create ‘reviews’ table.  This is the table that is queried by the lab application and for which data is cached. 


ACTION: From the AWS Console navigate to the RDS dashboard.

{{% img "RDSmgmtConsole.png" "RDS Console" %}}

From the Databases listing select the ‘demodb’ instance and copy the Endpoint string.

{{% img "demoDBdash.png" "DemoDB" %}}

ACTION: Change directory to ‘/home/ec2-user/ElcDbCacheLab/Code/dbcache’ and execute ‘reviews.sql’ as follows:

```bash
mysql -u demoUser -pdemoPassword -h '[Database Endpoint]' < reviews.sql
```

The script will take a few minutes to complete as data is loaded into the ‘reviews’ table, continue to the next section as this proceeds:

{{% img "reviewsTable.png" "create reviews table " %}}

## Configure Application environment 

The lab application, which runs in docker, utilizes host environment variables to establish configurations to run.  As such the following variables must be set prior to running the application:

```bash
export REDIS_MASTER_HOST={redis_master_node_endpoint}
export REDIS_READER_HOST={redis_replica_node_endpoint}     
export REDIS_MASTER_PORT=6379
export REDIS_READER_PORT=6379      
export HOST={mysql_endpoint}
export PASS=demoPassword
export USER=demoUser
export DB=DemoDB
export SQL_QUERY_TEXT='SELECT customer_id, review_id FROM reviews limit {}'
export FLASK_ENV=development
export PYTHONPATH=/code
```
ACTION: Retrieve DB endpoint details form ‘demodb’ instance details, as you did above in section 3.3.

{{% img "DemoDbEndP.png" "Db Endpoint" %}}

Replace {mysql_endpoint} in the information bubble above with DB endpoint.
ACTION:  On AWS Console navigate to ElastiCache Dashboard.

{{% img "ELCmgmtConsole.png" "ELC Console" %}}

On the Redis Cluster listing select the ‘elclabcluster’ and copy Primary Endpoint and
Reader Endpoint (note: you do not need to port information).

{{% img "ELClabclusterdash.png" "ELC Cluster dash" %}}

Replace {redis_master_node_endpoint} in the information bubble above with 
 Primary Endpoint details copied.

Replace {redis_replica_node_endpoint} in the information bubble above with 
Reader Endpoint details copied.

ACTION:  Export the environment variables from the SSH Session command line bash prompt:

```bash
export REDIS_MASTER_HOST= {copied redis_master_node_endpoint}
export REDIS_READER_HOST={copied redis_replica_node_endpoint}     
export REDIS_MASTER_PORT=6379
export REDIS_READER_PORT=6379      
export HOST={copied mysql_endpoint}
export PASS=demoPassword
export USER=demoUser
export DB=DemoDB
export SQL_QUERY_TEXT='SELECT customer_id, review_id FROM reviews limit {}'
export FLASK_ENV=development
export PYTHONPATH=/code
```

Copy the updated the environment variables from the info bubble above and paste into bash prompt to execute:

{{% img "EnvExport.png" "Export Environment" %}}





