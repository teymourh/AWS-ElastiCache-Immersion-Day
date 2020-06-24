+++
title = "Run Application"
weight = 4
+++

We are now ready to run the lab application and introspect ElastiCache Redis directly.

## Initialize and Run App


ACTION: Change directory to ‘/home/ec2-user/ElcDbCacheLab/Code/dbcache’ and execute ‘init_service.sh’ as follows:

```bash
./init_service.sh
```
This will deploy and run the application on docker:

{{% img "initSvc.png" "init Service" %}}

ACTION: From the EC2 instances listing, select the instance and copy the Public DNS (IPv4) or IPv4 Public IP:

{{% img "EC2dns.png" "EC2 DNS" %}}


Using your browser of choice, past the IP or Public DNS.  Once the app page loads, click on the ‘Query DB’ button to run:

{{% img "BrowserUI.png" "app ui" %}}

## Connect to Redis

We will now connect to your Redis cluster. We will accomplish this by using the terminal session you have open. Keep in mind that the terminal is a Unix terminal running on the EC2 instance.  We will need the redis-cli command line tool installed.  In addition, the EC2 instance needs to have network access to your ElastiCache cluster, this has already been configured via Security Groups in the lab environment.

ACTION: Change directory to ‘/home/ec2-user/ElcDbCacheLab/Code’ and execute ‘redisCliSetup.sh’ as follows:

{{% img "rCliSetup.png" "cli Setup" %}}

ACTION: Use the redis-cli tool you just installed to connect to the Primary Endpoint    of the ElastiCache for Redis Cluster:

{{% img "rPrimaryEpoint.png" "Redis Endpoint" %}}

```bash
redis-cli -h [cluster endpoint] -p 6379
```
{{% notice info %}}
redis-cli:
The redis-cli command is a Redis client that speaks the Redis protocol and can be launched from the command line on any major operating system. This version was compiled for Linux. To see additional options, type redis-cli --help
{{% /notice %}}


Upon successful connection, you should see something similar to below:
{{% img "SampleCli.png" "CLI" %}}


ACTION: Run the KEYS command on the Redis CLI:


```bash
KEYS *
```
{{% notice info %}}
KEYS pattern:
Returns all keys matching a pattern. A wildcard (*) indicates to output all keys in our database. In production the KEYS command should be used with caution because it blocks the Redis server until the command is finished. Retrieving millions of key names may take several seconds to complete and could cause other clients to timeout. The SCAN command produces results that can be iterated over, and should be used in lieu of the KEYS command in production environments.
{{% /notice %}}



As you can see from the output below, the application has created 5 keys that it utilizes:

{{% img "Keys.png" "Keys *" %}}

ACTION: In the terminal where the redis-cli is running, type the following command to get the value of key ‘db_cahce_redis_time’:

```bash
GET  db_cahce_redis_time
```

ACTION: Click ‘Query Db’ on the bowser and repeat the above command to see the value updated”
{{% img "Get.png" "Get command" %}}
