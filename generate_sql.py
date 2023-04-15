# Natural Language SQL Query Generator using GPT-3
# Scott David Keefe Sr.
# 2023-04-09

import ast
import mysql.connector
import random
import re

import ast
import mysql.connector

class MySQLConnection:
	def __init__(self, creds_file='creds.txt'):
		with open(creds_file, 'r') as f:
			creds = ast.literal_eval(f.read().strip())
		
		self.host = creds[0]
		self.database = creds[1]
		self.username = creds[2]
		self.password = creds[3]

		self.connect()

	def connect(self):
		self.conn = mysql.connector.connect(
			host=self.host,
			database=self.database,
			user=self.username,
			password=self.password
		)
		self.cursor = self.conn.cursor()

	def execute_query(self, query):
		self.cursor.execute(query)
		result = self.cursor.fetchall()
		return [list(row) for row in result]

	def close(self):
		self.cursor.close()
		self.conn.close()


class MySQLDatabase:
	def __init__(self, creds_file, tables_constrain):
		with open(creds_file, 'r') as f:
			creds = ast.literal_eval(f.read().strip())
			self.servername, self.database, self.uid, self.pwd = creds
			self.tables_constrain = tables_constrain

		self.connection = self.connect()

	def connect(self):
		connection = mysql.connector.connect(
			host=self.servername,
			database=self.database,
			user=self.uid,
			password=self.pwd
		)
		return connection

	def get_random_rows(self, table_name, num_rows=1):
		cursor = self.connection.cursor()
		cursor.execute(f"SELECT SQL_NO_CACHE * FROM {table_name} ORDER BY RAND() LIMIT {num_rows}")
		random_rows = cursor.fetchall()
		cursor.close()
		return random_rows

	def get_create_table_statement(self, table_name):
		cursor = self.connection.cursor()
		cursor.execute(f"SHOW CREATE TABLE {table_name}")
		create_table_statement = cursor.fetchone()[1]
		cursor.close()
		return create_table_statement
	
	def extract_columns(self, create_table_statement):
		columns = re.findall(r"`([^`]+)`\s+([^,\n\s]+)(?:[^,]*,|[^,]*$)", create_table_statement)
		result = ",\n".join([f"`{col}` {data_type}" for col, data_type in columns])
		result = re.sub(r"^.*\bforeign\b.*$", "", result, flags=re.MULTILINE | re.IGNORECASE)
		return result

	def generate_data(self):
		cursor = self.connection.cursor()
		cursor.execute("SHOW TABLES")
		tables = cursor.fetchall()
		print("All tables in this database", (table for table in tables))

		result = []

		for table in tables:
			if table[0] not in self.tables_constrain:
				continue
			table_name = table[0]
			create_table_statement = self.get_create_table_statement(table_name)
			create_table_statement = self.extract_columns(create_table_statement)
			print(create_table_statement)

			selected_rows = self.get_random_rows(table_name)

			header_query = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = '{self.database}' AND TABLE_NAME = '{table_name}'"
			cursor.execute(header_query)
			headers = cursor.fetchall()
			header_string = ", ".join([header[0] for header in headers])

			data_rows = [header_string] + [", ".join([str(element) for element in row]) for row in selected_rows]
			combined_data = "\n".join(data_rows)
			#print(combined_data)

			result.append([create_table_statement, combined_data])

		cursor.close()
		return result


# Codegen class
import openai

class Codegen:
	def __init__(self, api_key):
		self.api_key = api_key
		openai.api_key = self.api_key
		self.model = "text-davinci-003"

	def generate_code(self, prompt, max_tokens=500, n=1):
		response = openai.Completion.create(
			engine=self.model,
			prompt=prompt,
			max_tokens=max_tokens,
			n=n,
			stop=None,
			temperature=0.7,
		)

		return response.choices[0].text.strip()

	def generate_code_from_user_prompt(self, prompt):
		code = self.generate_code(prompt)
		return code

# Constrain queries to these tables
with open('tables.txt', 'r') as f:
	tables_constrain = [line.strip() for line in f]

# Get credentials from creds.txt
db = MySQLDatabase("creds.txt", tables_constrain)
data = db.generate_data()

# Get schema data and generate prompt
schema_data = ""
for item in data:		
	#print(item[0])  # CREATE TABLE statement
	#print(item[1])  # Data rows
	### Enable second half of this line to include a random sample row from your database. !This could expose your data.!
	schema_data += "Table schema: " + item[0] + "\n" ## <Safed> ## + "Sample select * from <table>: " + item[1] + "\n"	

if __name__ == "__main__":
	api_key = open("api.key", 'r').readline()  # Replace with your actual API key
	codegen = Codegen(api_key)

	prompt = "Using these tables that I am including the schema and example data from, write a MySQL SQL statement that will "  # Replace with your desired prompt
	user_input = input("Please enter the desired information to retrieve: ")
	prompt = prompt + user_input
	prompt = prompt + "Here is the schema and sample data: "  # Replace with your desired prompt
	prompt = prompt + '`' + schema_data + '`'
	#print ("Full prompt: " + schema_data)
	select_statement = codegen.generate_code_from_user_prompt(prompt)
	print("Generated select_statement:")
	print(select_statement)
	db = MySQLConnection('creds.txt')
	result = db.execute_query(select_statement)
	print("\n\n ----- Result:")
	print(result)
