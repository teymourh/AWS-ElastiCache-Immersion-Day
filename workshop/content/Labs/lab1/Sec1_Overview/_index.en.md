+++
title = "Lab Overview"
weight = 1
+++

{{% img "Lab1.png" "Lab Architecture" %}}

The lab showcases the performance improvements that can be achieved when using Amazon ElastiCache for Redis to accelerate relational (RDS MySQL) database queries.

The lab incorporates  a single page web application [SPA](https://en.wikipedia.org/wiki/Single-page_application) that performs semi-random queries on a MySQL RDS database and caches results in  ElastiCache for Redis. The application then collects stats on performance of cache vs. the database queries. 

The application queries the database a 1000 times; each query will use a random number of records to fetch back. Query results will be returned from ElastiCache if in cache [hit] or returned from the DB if not [miss].  ElastiCache is deployed in Multi-AZ mode with a single Master and read-0nly Replica.  The application leverages the Primary Endpoint (on the Master node) to write to the cache, and the Reader Endpoint (on the Replica node) to read the statistics for query performance. 
The application is implemented in [Python Flask](https://www.fullstackpython.com/flask.html) (backend) and Javascript on a client HTML page. It runs in a Docker container to make dependencies easier to manage.


