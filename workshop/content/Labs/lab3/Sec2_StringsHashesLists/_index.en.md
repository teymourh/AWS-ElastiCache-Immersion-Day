+++
title = "Strings, Hashes, Lists, and Sets"
date = 2020-08-17T13:41:53-06:00
weight = 2
chapter = false
+++

### Strings

The string type is the primitive data type that powers most other data structures within Redis. Since keys are themselves strings, in a sense we are representing one string with another.  Like keys, a STRING can have a maximum value of 512 MB but generally smaller values are recommended. The basic commands to operate against strings are SET and GET. Try setting a string with the key “foo” to the value “bar”

```bash
SET foo bar
```

Expected Result: OK


Notice the OK reply from the server. In future examples we’ll see how the system responds to different commands but for now the OK means that the system has accepted our command, and the data is now stored in Redis. So now that we’ve SET our key, lets retrieve it.

```bash
GET foo
```
Expected Result: "bar"


In this case our previously stored string is returned. The SET command has some interesting options we can use to do more than simply storing a string. These options are passed after the value. The CLI will give you some helpful hints as to how to properly format the command. Try typing just SET and noticing what the CLI gives you:


Example: SET key value [EX seconds|PX milliseconds|KEEPTTL] [NX|XX]


Let’s try setting a new key, but this time with a 60 second expiry:

```bash
SET will-expire "this key will expire in 60 seconds" EX 60 
```
Expected Result: OK

Before it expires, let’s use the TTL command to see how much time our key has left:

```bash
TTL will-expire
```
Expected Result: (integer) 39  - varies

After expiry: 

```bash
GET will-expire
```
Expected Result: (nil)

The final options for the `SET` command are `NX|XX`, which tell the server to only allow the `SET` command to process if the key doesn’t or does exist, respectively. 

Besides setting TTLs, there are commands to remove keys from the server. There are two options, `DEL` and `UNLINK`. For our example today either will work but it is important to understand the difference. DEL is a blocking operation but `UNLINK` tells the server to allow do the garbage collection in a separate thread. When we are operating against small strings this is not necessarily a big difference, but later on when we see some potentially larger data structures the DEL operation can block the server for some time. In general, `UNLINK` is the recommended approach for deleting data. 

```bash
UNLINK foo
```
Expected Result: (integer) 1

Notice that this time we are returned an integer - in this case the number of unlinked items. Now let’s try operating against more than one string at a time with `MSET` and `MGET`:

```bash
MSET a 1 b 2 c 3
```
Expected Result: OK


```bash
MGET a b c 
1) "1"
2) "2"
3) "3"
```
Expected Result: 
1) "1"
2) "2"
3) "3"


```bash
UNLINK a b c 
```
Expected Result: (integer) 3


Notice the pattern of key, value per MSET, the array that gets returned with MGET, and when we UNLINK more than one key the system responds with the number of keys. Next, let’s look at operating against numeric strings with INCR, DECR, and INCRBY

```bash
SET counter 1
```
Expected Result:

```bash
INCR counter 
```
Expected Result:


Notice that the system responds back with the incremented value. In fact, atomic counters is a very popular use case for Redis The opposite approach is possible with DECR, and you can also increment by specified values with INCRBY:

```bash
INCRBY counter 42
```
Expected Result:

### Hashes

 A Redis hash can be thought of as an array of strings. Unlike the SET/GET commands from strings, the commands to operate against hashes all start with H. Let’s look at an example of setting a simple hash with only one element:

```bash
 HSET employee:1 name "jeff bezos"
```
Expected Result: OK


A nice thing about hashes is that you can dynamically add fields to the hash after it has been created. Let’s change our employee:1 key to add a title:

```bash
HSET employee:1 title CEO
```
Expected Result: (integer) 1

You can also specify multiple fields at once with HMSET

```bash
HMSET employee:1 id 1 email jeff@amazon.com start-year 1994
```
Expected Result: OK


Now that we have data stored in a hash, lets first get a single element from the hash, and then get the entirety of the hash. 
```bash
HGET employee:1 email
```
Expected Result: "jeff@amazon.com"


```bash
HGETALL employee:1
```

Expected Result: 
 1) "name"
 2) "jeff bezos"
 3) "title"
 4) "CEO"
 5) "id"
 6) "1"
 7) "email"
 8) "jeff@amazon.com"
 9) "start-year"
10) "1994"


A word of caution, a hash can store up to 2^32-1 elements (over 4 billion), so a command like HGETALL could potentially cause a long term blocking operation. You can see the size of the hash with the HLEN command. 


```bash
HLEN employee:1
```
Expected Result: (integer) 5

Ref: https://redis.io/commands#hash


#### Bonus Questions: 
How would you implement a hit counter for a session store?

Say you did have a large hash with many fields, how could you optimize reading from it?


### Lists

Lists in Redis are implemented as linked lists. Practically speaking this means that the data structure is optimized to perform operations against the head/tail of the list, and less so for accessing elements inside the list. Adding or removing elements from the head or tail of the list is done in constant time, and accessing the Nth element of the list takes longer depending on the size of the list.

In Redis we think of lists as having a Left and Right, and have operations to add and remove elements from either side. An example use case for a list is a job queue, so we’ll work through adding elements to a master queue, and then move elements to individual worker queues. The “left” is considered the head and “right” the tail. 

First, lets add some jobs to our list:

```bash
RPUSH job-list send-email process-logs walk-dog
```

Expected Result: (integer) 3

Next we can see long our list is as well as the contents with LLEN and LRANGE respectively:

```bash
LLEN job-list
```

Expected Result: (integer) 3

```bash
LRANGE job-list 0 -1
```

Expected Result:
1) "send-email"
2) "process-logs"
3) "walk-dog"

Notice for `LRANGE` we can specify a start and stop index location. The value of -1 means return the entire list. Next, lets move some of these jobs to individual worker queues. 

```bash
RPOPLPUSH job-list worker1
```
Expected Result: "walk-dog"

Ref: https://redis.io/commands#list

#### Bonus Questions: 
How can we remove multiple entries in a list?

Can you insert an element to the middle of a list?

How could a connected client establish a blocking connection to wait for new jobs?


### Sets

Redis sets are collections of unique strings that do not have any ordering in place. Sets are very useful to determining membership, counting elements, comparing two (or more) sets against one another, creating new sets based on those comparisons, etc. Let’s take a look at creating some sets that contain information about some fictitious customers, and uncover some marketing opportunities.

First, create a set of customers with their unique IDs with `SADD`:

```bash
SADD customers 1 2 3 4 5
```

Expected Result: (integer) 5

Next, lets imagine we have a premium membership tier for our customers called “Prime” and a few of our customers have signed up for it: 

```bash 
SADD prime-customers 1 3 5
```
Expected Result: (integer) 3

Our marketing team has asked us for the following information: how many Prime customers do we have and who are the customers that are not Prime members. The first can be answered with `SCARD` (short of set-cardinality) and the second can be uncovered with the SDIFF command. 

```bash 
SADD prime-customers 1 3 5
```
Expected Result: (integer) 3

```bash 
SCARD prime-customers
```
Expected Result: (integer) 3

```bash 
SDIFF customers prime-customers
```
Expected Result: 
1) "2"
2) "4"

We can also store the results with `SDIFFSTORE`:

```bash 
SDIFFSTORE marketing-opportunity customers prime-customers
```

Expected Result: (integer) 2

View the members in the set using `SMEMBERS`:
```bash 
SMEMBERS marketing-opportunity
```
Expected Result: 
1) "2"
2) "4"

Ref: https://redis.io/commands#set

#### Bonus Questions:
One of our customers has upgraded to Prime, can you move them to the correct list? 

We want to randomly surprise one of our customers with a free gift - can you choose one at random?

