---
title: "Migration"
date: 2020-08-19T08:02:37-06:00
weight: 1
---

### Cluster mode disabled

In this section we will cover the migration from EC2 Redis cluster to cluster mode disabled Elasticache Redis cluster. 

* Log into console and find EC2 instancess named "Redis on EC2"
* locate and note private IP
* locate and note public IP
* verify security group for access?!? Probably better to use SSM?

* connect to EC2 redis
  * ssh? redis-cli?

```
keys *
exit
```

* insert data [data.txt](sec1_migration/data.txt) where is that data file? What 2000 lines does it contain?
```
cat ~/data.txt | redis-cli --pipe
```

* check data
```
redis-cli
keys *
dbsize
```

* connect to elasticache redis
  * ssh? redis-cli?

```
keys *
dbsize
```

* remove protected mode on EC2 redis
```
config set protected-mode no
```

* connect to elasticache dashboard
* find cluster named `online-migration-cluster`
* actions migrate data from endpoint - NOTE: destructive
* copy paste private EC2 IP
* check modifying state on elasticache; refresh: then migrating
* validate on both sides with CLI `dbsize` - should now see same data

```
dbsize
keys *
get Key:184
```

* note: replication tools is _live_ so we can delete a key in source and it will delete the key in destination

```
del Key:184
```

```
get Key:184
```

* update with another 2000 data points [changelog.txt](sec1_migration/changelog.txt)

```
cat changelog.txt | redis-cli --pipe
redis-cli
dbsize
```

* review cloudwatch on master node of Elasticache

* stop migration - console - stop migration

* check repliction?!? THis is weird. Ah this is because the modifying state change takes time. A LOT OF TIME!

```
info replication
```

* verify cluster state after breaking

```
set a
get a
```

* "zero downtime"?!? How is the client migrated?


### Cluster mode enabled version

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

