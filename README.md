Natural Language MySQL Query Generator
This Python script allows users to query a MySQL database using natural language. The script connects to a MySQL database, retrieves schema and sample data from specified tables, and uses OpenAI's GPT-powered Codegen class to generate SQL code based on user input provided in natural language.

Prerequisites
To run this script, you need to have the following Python libraries installed:

mysql-connector-python
openai
You can install these libraries using pip:

Copy code
pip install mysql-connector-python openai
Configuration
Create a file named creds.txt in the same directory as the script, and add your MySQL credentials in the following format:

php
Copy code
[<your_host>, <your_database>, <your_username>, <your_password>]
Replace <your_host>, <your_database>, <your_username>, and <your_password> with your actual MySQL credentials.

Usage
In the script, define the tables you want to query by modifying the tables_constrain list:
python
Copy code
tables_constrain = ['table1', 'table2']
Replace 'table1' and 'table2' with the names of the tables you want to query.

Replace the placeholder API key with your actual OpenAI API key:
python
Copy code
api_key = "your_openai_api_key"
Run the script:
Copy code
python script_name.py
Follow the on-screen prompt to enter the desired information to retrieve from the specified tables using natural language (e.g., "Get the average price of all products").

The script will generate a SQL SELECT statement based on your input and the schema and sample data of the specified tables. The generated SQL code will be displayed on the screen.

Code Structure
The script consists of the following classes:

MySQLConnection: A class that handles connections to a MySQL database.
MySQLDatabase: A class that retrieves schema and sample data from specified tables in the connected MySQL database.
Codegen: A class that uses OpenAI's GPT-powered Codegen API to generate SQL code based on user input provided in natural language and the retrieved schema and sample data.
License
This project is licensed under the MIT License.
