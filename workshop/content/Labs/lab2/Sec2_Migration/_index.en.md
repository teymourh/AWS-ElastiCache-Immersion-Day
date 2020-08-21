---
title: "Migration"
date: 2020-08-19T08:02:37-06:00
weight: 3
---

In this section we will cover the migration from a standalone Redis server to an AWS ElastiCache Redis with cluster mode disabled.

## Migration to ElastiCache

### Setting up Redis on EC2

Follow the instructions from [Lab1](/labs/lab1/sec3_setupandvalidation.html) to connect to the EC2 bastion host instance. This instance has redis code installed but not running so we will use that to start a standalone server. Using the terminal session run the following command:

```bash
sudo su - ec2-user
/usr/local/src/redis-5.0.6/src/redis-server --daemonize yes
```

Now let's check if redis is running on the local host:

```bash
redis-cli -h localhost
```

Now that you are logged into redis, verify that there are no keys pre-loaded. The `keys *` query should return emtpy:

```redis
keys *
```

Let's exit redis so we can load some data into it:

```redis
exit
```


### Loading data into EC2 redis

We will download this 2000 key dataset [data.txt](sec1_migration/data.txt) and insert it into our standalong Redis server. 

```
wget https://raw.githubusercontent.com/rudpot/AWS-ElastiCache-Immersion-Day/master/workshop/content/Labs/lab2/Sec1_Migration/data.txt
cat ~/data.txt | redis-cli -h localhost --pipe
```

Now let's log back into Redis to check data was inserted successfully:

```bash
redis-cli -h localhost
```

```redis
keys *
dbsize
```

### Connecting to Elasticache

As discussed in [Lab1](/labs/lab1/sec3_setupandvalidation.html) we already started an ElastiCache instance. However, we need to enable external access to the redis cluster we just started. For this we need to enable security group access from ElastiCache and change the [protected mode](https://redis.io/topics/security) setting to allow external access. To unset protected mode connect to redis via the CLI:

```bash
redis-cli -h localhost
```

```redis
config set protected-mode no
exit
```

To enable security group access let's first copy the security group ID associated with the ElastiCache instance. Now navigate to the [ElastiCache console](https://console.aws.amazon.com/elasticache/home?#redis:) and select "Redis". Then select the checkbox besides `elclabcluster`. Then copy the security group ID:

{{% img "ElastiCacheSgSelect.png" "Select ElastiCache security group" %}}

Next navigate to the [EC2 Console](https://console.aws.amazon.com/ec2/v2/home?#Instances:sort=instanceId), select the bastion host instance, then select the security group containing `WebServerSecurityGroup`:

{{% img "BastionSecurityGroup.png" "Bastion security group" %}}

Select the security group based on the filter ID an, select the "Inbound rules" tab, and click "Edit inbound rules":

{{% img "BastionChangeSg.png" "Change bastion security group" %}}

On the next page select "Add Rule", for the "Port range" enter the redis port, `6379`, for "Source" past the security group ID off the ElastiCache cluster. Finally click "Save rules":

{{% img "BastionSecurityGroupAdd.png" "Add bastion security group" %}}


With all the access enabled we will now use the migration functionality of ElastiCache to sync data from the Redis on our EC2 instance. To connect redis on our bastion host to ElastiCache we require the private IP address of the bastion host instance. To find this navigate to the [EC2 console](https://console.aws.amazon.com/ec2/v2/home?#Instances) and find the instance named `ElastiCache Lab Bastion Host` and copy the private IP address:

{{% img "BastionPrivateIp.png" "Bastion private IP" %}}

Now navigate to the [ElastiCache console](https://console.aws.amazon.com/elasticache/home?#redis:) and select "Redis". Then select the checkbox besides `elclabcluster`.

{{% img "ElastiCacheSelect.png" "Select Elasticache" %}}

From the "Actions" dropdown select "Migrate Data From Endpoint"

{{% img "ElastiCacheMigration.png" "Select migration options" %}}

On the dialog box enter the private IP you recorded earlier and select "Start Migration"

{{% img "MigrationEnterIp.png" "Enter VM private IP" %}}

The ElastiCache instance will now show a "modifying" state. Wait a few minutes until this changes to "migrating". You many need to hit refresh to see the state change. :



### Validating replication

At this point our Redis instance is continuously replicating to ElastiCache. First let's verify that the initial replication succeeded. We already have the connection information for the ElastiCache instance configured on the bastion host from Lab1 so we can now directly connect:

```bash
redis-cli -h $REDIS_MASTER_HOST
```

Once connected to redis we should now see the same information as on the local redis: 2000 keys

```redis
keys *
dbsize
```

We can review the replication configuration on either redis using the command:

```redis
info replication
```

Finally we can verify continuous replication by inserting data into the source cluster and reading it back from ElastiCache:

```bash
echo set a 123 | redis-cli -h localhost
echo get a     | redis-cli -h $REDIS_MASTER_HOST
echo set a 321 | redis-cli -h localhost
echo get a     | redis-cli -h $REDIS_MASTER_HOST
```

We can also verify that ElastiCache is currently a read replica and will throw an error if we try to modify it

```bash
echo set a 123 | redis-cli -h $REDIS_MASTER_HOST
```

### Breaking replication

Finally once data is synced we can break the replication by navigating to the [ElastiCache console](https://console.aws.amazon.com/elasticache/home?#redis:) and select "Redis". Then select the checkbox besides `elclabcluster`.

{{% img "ElastiCacheSelect.png" "Select Elasticache" %}}

From the "Actions" dropdown select "Migrate Data From Endpoint"

{{% img "ElastiCacheMigrationDisable.png" "Disable migration options" %}}

Note that it takes a substantial amount of time for this to take effect.




<!-- ### Cluster mode enabled version

Use RDB backup file

```
redis-cli
CONFIG SET dbfilename redis_demo_backup.rdb
bgsave
exit

aws s3 cp ~/redis_demo_backup.rdb s3://MYBUCKET/backups/redis_demo_backup.rdb
```

* enable Elasticache access to S3
  * something public docs canaonical ID TBD pate under "add account" in S3 _file_ permissions. Alternatively do this via bucket policy in "non-standard" regions
* create cluster on console with cluster mode enabled
  * pick small node t2/t3.micro
  * 2 shards / 2 replicas
  * multi-az
  * elasticache subnet
  * s3 back location
 -->
