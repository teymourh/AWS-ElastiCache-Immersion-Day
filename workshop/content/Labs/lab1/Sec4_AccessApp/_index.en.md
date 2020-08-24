+++
title = "Access Application"
weight = 4
+++

We are now ready to explore the performance improvements granted by Redis caching for SQL queries. 

## Browse Application

Using your web browser of choice, past the ECS Cluster Public IP into browser address bar.  Once the app page loads, click on the ‘Query DB’ button to run:

{{% img "BrowserUI.png" "app ui" %}}

The blue bar shows the number of queries that were served from the Redis cache, or cache HITS, and the duration for those queries on the order of 300 micro seconds. The orange bar shows the number of queries that were served from the database directly, or cache MISSES, and the duration for those queries around 1,600 micro seconds.


## Exploring in more detail

At the heart of the application is the following python function which will take a SQL query string, e.g. 

`SELECT customer_id, review_id FROM reviews limit 123`, 

converts that into a unique hash, e.g. 

`7d21fb0d3bf1478d4f22f40a7f9c89d8674c28613ac77d8b4b1a11f4`. 

If an entry for that hash exists in redis it will return that, otherwise it will query the MySQL database, cache the result in redis, and return it:

```python
    def fetch(sql):
        global mysql_time, redis_time, redis_counter, mysql_counter, hits_counter, end_time_value

        # Format the SQL string
        SQLCmd = sql.format(random.randrange(1,75))
        
        # Create unique hash key from query string
        hash = hashlib.sha224(SQLCmd.encode('utf-8')).hexdigest()
        key = key_prefix + hash

        # Gather timing stats while fetching from Redis
        start_timer()
        value = redis_reader_con.get(key)
        redis_counter = redis_counter + 1

        if value is not None:
            # Result was in cache
            redis_time =  redis_time + end_timer()
            ql = query_line(SQLCmd,redis_time,redis_counter,'hit')
            log_data(redis_writer_con, 'DBCACHE',ql)
            hits_counter = hits_counter + 1
            redis_writer_con.set('db_cache_redis_time',redis_time)
            redis_writer_con.incr('db_cache_hit_counter')
            return value
        else:
            # Get data from SQL
            cursor=mySQL_con.cursor()
            cursor.execute(SQLCmd)
            value = cursor.fetchall()[0][0]
            mysql_time = mysql_time + end_timer()
            mysql_counter = mysql_counter + 1
            ql = query_line(SQLCmd,mysql_time,mysql_counter,'miss')
            redis_writer_con.incr('db_cache_miss_counter')
            redis_writer_con.set('db_cache_mysql_time',mysql_time)
            redis_writer_con.psetex(key, TTL, value)
            log_data(redis_writer_con, 'DBCACHE',ql)
            return value    

```

## Connect to Redis

Using the terminal session you opened in the previous session type the following:

```bash
sudo su - ec2-user
```

{{% img "sudo.png" "Redis Endpoint" %}}

Then use the redis command line specifying Redis host & port (default 6379).  Here we use the '$REDIS_MASTER_HOST' environment variable which has been pre-configured for you:

```bash
redis-cli -h $REDIS_MASTER_HOST -p 6379
```

{{% notice info %}}
redis-cli:
The redis-cli command is a Redis client that speaks the Redis protocol and can be launched from the command line on any major operating system. This version was compiled for Linux. To see additional options, type redis-cli --help
{{% /notice %}}


Upon successful connection, you should see something similar to below:
{{% img "SampleCli.png" "CLI" %}}


Now you can check for keys already stored in Redis as a result of clicking the "Query DB" button earlier. To do this, run the KEYS command on the Redis CLI:


```bash
KEYS *
```

{{% notice info %}}
KEYS pattern:
Returns all keys matching a pattern. A wildcard (*) indicates to output all keys in our database. In production the KEYS command should be used with caution because it blocks the Redis server until the command is finished. Retrieving millions of key names may take several seconds to complete and could cause other clients to timeout. The SCAN command produces results that can be iterated over, and should be used in lieu of the KEYS command in production environments.
{{% /notice %}}



As you can see from the output below, the application has created 5 keys that it utilizes:

{{% img "Keys.png" "Keys *" %}}

**ACTION:** In the terminal where the redis-cli is running, type the following command to get the value of key ‘db_cache_redis_time’:

```bash
GET  db_cache_redis_time
```

**ACTION:** Click ‘Query Db’ on the browser and repeat the above command to see the value updated”
{{% img "GetDBCacheTime.png" "Get command" %}}


Following the description of caching above, we would expect to also see hash keys for the cache. The reason you might not see those in the output above is that the keys are set to expire after a few seconds. If you want to assure yourself that things are working as expected call the db update and redis check back-to back from the terminal. To do so, first set the IP address of the ECS cluster:

```bash
exit
export ECS_IP=<IP>
```

where `<IP>` is replaced by the IP address of the ECS cluster you recorded in the previous section. Then run the following commands:

```bash
curl http://${ECS_IP}/start_db_run
echo 'keys ex4:*' | redis-cli -h $REDIS_MASTER_HOST | head -n 10
echo
```
