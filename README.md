# Natural Language SQL Query Generator using text-davinci-003. It seems to be a useful tool for generating SQL statements from natural language queries.

## Just to clarify, this script uses the OpenAI text-davinci-003 API to generate SQL SELECT statements from natural language queries, and then executes these statements on a MySQL database using the mysql-connector-python package.

## Users will need to create a creds.txt file containing the credentials for their MySQL database, an api.key file containing their OpenAI API key, and a tables.txt file containing a list of the table names that they want to use for generating queries.

## Once the setup is complete, users can run the script and enter a natural language query. The script will use the OpenAI API to generate a SQL SELECT statement based on the tables specified in tables.txt and execute it on the *MySQL database* specified in *creds.txt*. The results will be printed to the console.(For this particula beta.)

## However, it is important to note that the generated SQL statement may not always be correct, so it is essential to review it carefully before executing it on your database.

## Finally, it is great to know that this script is licensed under the *MIT License*, which means that users can use, modify, and distribute the code freely.

## Original boilerplate READ.ME

*This is a Python code that uses OpenAI's GPT-3 model to generate SQL queries from natural language prompts.* The code connects to a MySQL database, extracts the schema and sample data of specified tables, and prompts the user to enter the desired information to retrieve. Using the provided schema and sample data, the code generates a SQL select statement using GPT-3 and executes it on the database.

### Requirements
  Python 3.6 or higher
  MySQL Connector/Python
  OpenAI API key
### Usage
  Clone the repository and navigate to the project directory.
  Install the required packages using the following command:
  pip install -r requirements.txt

* Create a creds.txt file containing the following information:
``<MySQL server host>
<MySQL database name>
<MySQL username>
<MySQL password>``

### Create an OpenAI API key and save it in a file named api.key.
*Create a file named tables.txt containing the names of the tables from which to generate schema and sample data, one table name per line.
Run the program using the following command:*
`python sql_query_generator.py`

### Follow the on-screen prompts to enter the desired information to retrieve.
#### Code Overview
  MySQLConnection class: Connects to a MySQL database and executes SQL queries.
  MySQLDatabase class: Generates schema and sample data from specified tables in a MySQL database.
  Codegen class: Generates SQL select statements from natural language prompts using GPT-3.
  main function: Orchestrates the generation of SQL queries from natural language prompts using the MySQLDatabase, Codegen, and MySQLConnection classes.
  Disclaimer
  This code is for demonstration purposes only and should not be used in production environments without appropriate modifications and security measures.

##### Shoutout to https://github.com/SkipTabor for the idea for the main mechanism (Feed in the schema and then ask questions).
