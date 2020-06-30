+++
title = "Access Application"
weight = 4
+++

We are now ready to access the application and introspect ElastiCache Redis directly.

## Browse Application

Using your web browser of choice, past the ECS Cluster Public IP into browser address bar.  Once the app page loads, click on the ‘Query DB’ button to run:

{{% img "BrowserUI.png" "app ui" %}}

## Connect to Redis

We will now connect to your Redis cluster. We will accomplish this by using the terminal in Systems Manager – Session Manager. Keep in mind that the terminal is a Unix terminal running on the EC2 instance.  We will use the redis-cli command line tool, which has been pre-installed.  In addition, the EC2 instance needs to have network access to your ElastiCache cluster, this has already been configured via Security Groups in the lab environment.


**ACTION:** Connect to EC2 instance (Bastion Host) via Unix terminal:

1. On the AWS Console navigate to Systems Manager dashboard.


{{% img "SysManDash.png" "sys man" %}}

2. Select Session Manager from the left navigation pane, and then “Start Session”:


{{% img "SessionMan.png" "session man" %}}

{{% img "StartSession.png" "start session" %}}

3. Select the existing Session for your “ElastiCache Lab Bastion Host”, and then “Start Session”.


{{% img "BastionStartSession.png" "cli Setup" %}}

4. In the Session Manager, enter the following command:

```bash
sudo su - ec2-user
```

{{% img "sudo.png" "Redis Endpoint" %}}

**ACTION:** Connect to ElastiCache for Redis Cluster via redis-cli tool:

1.

```bash
redis-cli -h $REDIS_MASTER_HOST -p 6379
```

{{% notice info %}}
redis-cli:
The redis-cli command is a Redis client that speaks the Redis protocol and can be launched from the command line on any major operating system. This version was compiled for Linux. To see additional options, type redis-cli --help
{{% /notice %}}


Upon successful connection, you should see something similar to below:
{{% img "SampleCli.png" "CLI" %}}


**ACTION:** Run the KEYS command on the Redis CLI:


```bash
KEYS *
```
{{% notice info %}}
KEYS pattern:
Returns all keys matching a pattern. A wildcard (*) indicates to output all keys in our database. In production the KEYS command should be used with caution because it blocks the Redis server until the command is finished. Retrieving millions of key names may take several seconds to complete and could cause other clients to timeout. The SCAN command produces results that can be iterated over, and should be used in lieu of the KEYS command in production environments.
{{% /notice %}}



As you can see from the output below, the application has created 5 keys that it utilizes:

{{% img "Keys.png" "Keys *" %}}

**ACTION:** In the terminal where the redis-cli is running, type the following command to get the value of key ‘db_cahce_redis_time’:

```bash
GET  db_cahce_redis_time
```

**ACTION:** Click ‘Query Db’ on the browser and repeat the above command to see the value updated”
{{% img "GetDBCacheTime.png" "Get command" %}}
