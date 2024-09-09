# Optional Review Project Guidelines

## Project:
Create a Python application that connects to a MySQL database,
loads data into Spark dataframes, and answers some analytical questions listed below. 
Your answers should be generated by transforming your Spark dataframes using
filters and joins. Feel free to use SparkSQL as you see fit. Your output
can either be printed to the terminal, or saved in a file(s).
The application should connect to the "sakila" example database that comes with
your installation of MySQL, and save each table into a dataframe in Spark.

[Installation instructions if you do not have the sakila DB](https://dev.mysql.com/doc/sakila/en/sakila-installation.html)


## Questions to answer:

    1. How many distinct actors last names are there?
    2. Which last names are not repeated?
    3. Which last names appear more than once?
    4. What is that average running time of all the films in the sakila DB?
    5. What is the average running time of films by category?

## Tech Stack:
    - Python 3.12.4
        - mysql-connector-python
        - pandas
        - tqdm
        - pyspark
    - PySpark
    - VS Code
    - MySQL

## Due Date

This optional project will be due by EOD on Friday. Feel free to send me the project (GitHub link)
for me to review and provide feedback. Otherwise, there will be no mandatory evaluation/presentation.

## Stretch Goals

    - Make a CLI to prompt the user for info they might want to see
    - Allow for custom queries using SQL syntax in a CLI
    - Keep logs for your application and store them in a MongoDB

## Issues Encountered and How to Fix:

Originally, it was planned to use pandas.read_sql(sql_query, sql_connection), but it was found to require a bunch of packages that were unfamiliar to me, so 
I decided to stick with the more familiar mysql-connector-python package, and use the pandas.DataFrame class to load in results and set its respective columns using the MySQLCursor class.

Struggled with connecting to MySQL server installed on Windows from WSL2 Ubuntu, and 
ultimately decided that it was a huge waste of time because I kept getting errors. 
First, it was a problem with authenticating user 'root'@'localhost', so I ran the commands on the mysql cli: 
CREATE USER 'root'@'%' IDENTIFIED BY 'password'; 
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%';
FLUSH PRIVILEGES;

It seemed to work, but then encountered another issue: It couldn't connect to 127.0.0.1:3306; 
This one had me, and searched as much as I could until I found out that I can check ports. 
The only ports available to me on WSL2 were 33060 and 33061, so I changed it to use the port 33060. 

I then encountered another error, Server and Client Protocol versions do not match. 
They were both up to date on respective systems, so I gave up here and installed the 
sakila database to the WSL2 server, and moved on. 

I now set the port to 33061, so that it connects to the WSL2 MySQL server instead. If I had the time, 
I would revisit this issue and attempt again using additional resources. 

The next set of issues I faced was getting pandas dataframes to play nice with spark dataframes. 
After searching around for a while, an article was found that detailed the process of using Apache Arrow 
for Python. I installed the required package:

pip install pyspark[sql] 

Then added the following before calling spark.createDataFrame(pandas_dataframe)

spark.conf.set('spark.sql.execution.arrow.enabled', 'true') 

The schema is now inferred properly and no more errors were encountered.

## Design Decisions

I prefer Object Oriented Programming, so I wrote a class that handles Spark specific functionality, a class for retrieving tables from MySQL database, and a class for CLI. Each exception is its own class, and handles logging of database events.

I also prefer using interface classes that provide documentation for each method in a class. Simply hover over the method name and get documentation details, reducing clutter in the implementation file.