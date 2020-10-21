+++
title = "Advanced Commands: Sorted Sets, Geospatial, HyperLogLog, and Streams"
date = 2020-08-17T13:41:53-06:00
weight = 3
chapter = false
+++

Let's explore the resources created in the "Getting Started" section of this workshop:
### Sorted Sets

Sorted sets in Redis expand upon the idea of Sets, being that individual elements must be unique - however each element is also associated a floating point score. The scoring mechanism allows for a set to be taken in order. While elements of the sorted set must be unique, their scores can be identical. In that case, the string that is lexicographically greater becomes higher on the list.

Sorted sets unlock a number of interesting use cases. We’ll examine two powerful options, leaderboards and secondary indexes. Leaderboards are very common in gaming companies, as well as real-time bid management systems. Lets take a look at a simple gaming leaderboard, we’ll start by initializing the sorted set with blank scores with `ZADD` and checking with `ZRANGE`: 


```bash
ZADD scores 0 player1 0 player2 0 player3
```
Expected Result: (integer) 3

```bash
ZRANGE scores 0 -1 WITHSCORES
```
Expected Result: 
1) "player1"
2) "0"
3) "player2"
4) "0"
5) "player3"
6) "0"

Notice that while the players all have the same score, the arranged in lexicographical order. Lets add some points to our players scores with ZINCRBY, and then output a final leaderboard for our game:

```bash 
ZINCRBY scores 10 player2
```
Expected Result: "10"
```bash 
ZINCRBY scores 15 player3
```
Expected Result: "15"

```bash 
ZINCRBY scores 5 player1
```
Expected Result: "5"

```bash 
ZREVRANGE scores 0 -1
```
Expected Result: 
1) "player3"
2) "player2"
3) "player1"

Note the ZREVRANGE command, ZRANGE returns the scores from lowest to highest. Since we are interested in the players listed with the highest score first, we can use the ZREVRANGE command.

Secondary indexing allows us add and retrieve items within a specified range. Imagine we had a dataset about our customers that looked like:


```bash 
HMSET customer:1 id 1 name jim email jim@test.com state TX age 37
HMSET customer:2 id 2 name alice email alice@test.com state WA age 65
HMSET customer:3 id 3 name jeff email jeff@test.com state CA age 22
HMSET customer:4 id 4 name mary email mary@test.com state MA age 44
```

And so on. Now lets imagine we wanted a way to sort our customers by age. They are currently indexed by their ID number, so the question becomes how? We can use a sorted set where the elements are our names from above, and the scores (which must be numeric) will be the ages. 


```bash 
ZADD secondary-index 37 jim 65 alice 22 jeff 44 mary
```
Expected Result: (integer) 4

Next, say we want to see an order of our users by youngest to oldest, or oldest to youngest, or perhaps between the age of 20 to 40 and also return the ages. Sorted sets can handle all of these with `ZRANGE`, `ZREVRANGE`, and `ZRANGEBYSCORE`.

```bash 
ZRANGE secondary-index 0 -1
```
Expected Result:
1) "jeff"
2) "jim"
3) "mary"
4) "alice"


```bash 
ZREVRANGE secondary-index 0 -1
```
Expected Result:
1) "alice"
2) "mary"
3) "jim"
4) "jeff"

```bash 
ZRANGEBYSCORE secondary-index 20 40 WITHSCORES
```
Expected Result:
1) "jeff"
2) "22"
3) "jim"
4) "37"

### Geospatial

Redis extends the Sorted Set datatype to encode and represent geographical information. This is handy for building location based lookups within your app. For example a ride sharing app might show you the approximate location of nearby drivers, or a dating app may show only show you members with a certain radius. Let’s add a few example entries and perform some queries. We’ll start by adding some locations in New York City to our nyc geohash with `GEOADD`.

```bash 
GEOADD nyc 40.7648057 -73.9733487 "central park n/q/r" 40.7362513 -73.9903085 "union square" 40.7126674 -74.0131604 "wtc one" 40.6428986 -73.7858139 "jfk" 40.7498929 -73.9375699 "q4" 40.7480973 -73.9564142 4545
```

Since the geospatial datatype is technically also a sorted set, we can use ZRANGE to query the structure. 

```bash 
ZRANGE nyc 0 -1
```
Expected Result:
1) "wtc one"
2) "union square"
3) "central park n/q/r"
4) "4545"
5) "q4"
6) "jfk"

Let’s examine some location abilities with `GEORADIUS`:

```bash 
GEORADIUS nyc 40.7598464 -73.9798091 3 km
```
Expected Result: 
1) "union square"
2) "central park n/q/r"
3) "4545"

Neat! Say we wanted to include the distance in the response, but this time in miles: 

```bash 
GEORADIUS nyc 40.7598464 -73.9798091 3 mi WITHDIST
```

Expected Result: 
"union square"
"0.8538"
"central park n/q/r"
"0.4564"
"4545"
"1.6323"
"q4"
"2.9255"
"wtc one"
"2.4740"

Ref: https://redis.io/commands#geo

#### Bonus Questions:
How can we return the results in a descending manner? 

Can you find a way to return the distance between two members of the set? 


### HyperLogLog

HyperLogLog is a probabilistic data structure used to estimate the cardinality of a large set of objects with a 0.81% standard error rate with low, fixed memory usage. This is very useful for counting large numbers of objects where precision is not needed (e.g. “likes”, number of comments, etc).

HyperLogLog is very easy to use with two commands, `PFADD` and `PFCOUNT`:

```bash 
PFADD hll-example a b c d e f g
```
Expected Result: (integer) 1


```bash 
PFCOUNT hll-example
```

Expected Result: (integer) 7

Note: since we are well below the standard error percentage we don’t expect any discrepancy between the counts. 


### HyperLogLog

Streams are the newest data structure to Redis, and can conceptually be thought of as a combination of Lists and Hashes, written to in an append-only fashion. Each entry in a stream is composed of field/value pairs, and identified with a unique integer, usually a UNIX timestamp. A common use for Streams is for a distributed log file, or high volume messaging bus with scale out capabilities on both producers and consumers. We’ll show a simple example of adding and reading entries from a list, but highly encourage further reference. 

Suppose you had an application that periodically published events about user activity to a stream called app-log:

```bash 
XADD app-log * user jim browser chrome event "/checkout"
```

Expected Result: "1602876446387-0"

XADD is the command to add entries to the Stream, app-log is the name of the Stream, the * tells Redis to automatically generate an ID based on the timestamp, followed by field value pairs. Let’s add another entry: 

```bash 
XADD app-log * user teymour browser safari event "/home"
```

Expected Result: "1602876642116-0"

Next, we’ll read from the list with XRANGE: 

```bash 
XRANGE app-log - +
```

The - and + characters are special to Streams, which indicate the beginning and end of the Stream. You could also specify individual timestamps to narrow the results. As mentioned, Streams are very powerful and we encourage further research into their full capabilities: https://redis.io/topics/streams-intro

