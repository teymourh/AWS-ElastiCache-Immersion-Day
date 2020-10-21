+++
title = "Getting Connected to Redis"
date = 2020-08-17T13:41:53-06:00
weight = 1
chapter = false
+++

Let's get connected to Amazon ElastiCache for Redis to learn some commands. 

## EC2 bastion host

To allow you exploring in your AWS account we have set up an EC2 instance that you can conenct to via SSH. Or via AWS Systems Manager Session Manager. We recommend using Session Manager for this lab exercise.


### Session Manager 

To connect via AWS Systems Manager Session Manager, browse to the [AWS Systems Manager console](https://console.aws.amazon.com/systems-manager/session-manager/start-session), select the desired host, `ElastiCache Lab Bastion Host`, and click "Start session". If you have trouble accessing this location, ensure you are disconnected from a client VPN on your computer.

{{% img "SsmStartSession.png" "Connect via SSM" %}}

### Using the console

Set up the proper login credentials before proceding with your session.

```bash
sudo su - ec2-user
```

You should now be logged-in on the bastion host via a unix shell. You can validate all is well by running these commands


## Elasticache Redis cluster

You account should contain an Elasticache Redis cluster named `elclabcluster`. Navigate to the [AWS ElastiCache console](https://console.aws.amazon.com/elasticache/home?#redis:), select Redis, and expand the entry for `elclabcluster` to find the "Primary Endpoint"

{{% img "ElasticacheConsole.png" "Find Redis connection string" %}}

You can compare this endpoint information with that pre-populated in the bastion host by running this command:

```bash
env | grep REDIS
```

## Getting Started

Then use the Redis Command Line interface specifying Redis host & port (default 6379). Here we use the ‘$REDIS_MASTER_HOST’ environment variable which has been pre-configured for you:

```bash
redis-cli -h $REDIS_MASTER_HOST -p 6379
```

Verify connectivity by running the PING command:

```bash
PING
```
Expected Result: PONG


## Data Structures

Redis is a key-value store. The “values“ represent one of 10 built-in data structures. Before we get to the data structures themselves, lets spend a few moments discussing keys and common practices.

### Keys

Redis keys are binary safe strings. Any data that can be represented as a binary sequence can be a key. While the maximum allowed key size is 512MB, in practice short key names are preferable for both memory usage and performance reasons. For example in the previous lab we were using Redis to cache SQL queries. Rather than use the entire SQL query as the key, we ran the query through a hashing algorithm which then became our key. 

For human readable keys, it is a common practice to provide some separation with a colon character, such as object:id. For example, if we were maintaining a session store with Redis and wanted to access the cart of a user with id 123, this could be represented as cart:123. Further, if we were leveraging Redis for multiple applications, it may make sense to include further information in the key such as app1:cart:123. As a user of Redis it is up to you to strike a balance between short key names and relevant information. 

Next we’ll dive into our first data sructure, the `STRING`.
