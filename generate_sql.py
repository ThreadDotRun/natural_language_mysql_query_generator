# Natural Language SQL Query Generator using GPT-3
# Scott David Keefe Sr.
# 2023-04-09

import ast
import mysql.connector
import random
import re
import openai


class MySQLConnection:
	def __init__(self, creds_file='creds.txt'):
		with open(creds_file, 'r') as f:
			creds = ast.literal_eval(f.read().strip())

		self.host, self.database, self.username, self.password = creds
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
		self.tables_constrain = tables_constrain
		with open(creds_file, 'r') as f:
			creds = ast.literal_eval(f.read().strip())

		self.servername, self.database, self.uid, self.pwd = creds
		self.connection = self.connect()

	def connect(self):
		return mysql.connector.connect(
			host=self.servername,
			database=self.database,
			user=self.uid,
			password=self.pwd
		)

	def get_random_rows(self, table_name, num_rows=1):
		with self.connection.cursor() as cursor:
			cursor.execute(f"SELECT SQL_NO_CACHE * FROM {table_name} ORDER BY RAND() LIMIT {num_rows}")
			return cursor.fetchall()

	def get_create_table_statement(self, table_name):
		with self.connection.cursor() as cursor:
			cursor.execute(f"SHOW CREATE TABLE {table_name}")
			return cursor.fetchone()[1]

	@staticmethod
	def extract_columns(create_table_statement):
		columns = re.findall(r"`([^`]+)`\s+([^,\n\s]+)(?:[^,]*,|[^,]*$)", create_table_statement)
		result = ",\n".join([f"`{col}` {data_type}" for col, data_type in columns])
		return re.sub(r"^.*\bforeign\b.*$", "", result, flags=re.MULTILINE | re.IGNORECASE)

	def generate_data(self):
		with self.connection.cursor() as cursor:
			cursor.execute("SHOW TABLES")
			tables = cursor.fetchall()

		result = []

		for table in tables:
			if table[0] not in self.tables_constrain:
				continue
			table_name = table[0]
			create_table_statement = self.get_create_table_statement(table_name)
			create_table_statement = self.extract_columns(create_table_statement)

			selected_rows = self.get_random_rows(table_name)

			with self.connection.cursor() as cursor:
				header_query = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = '{self.database}' AND TABLE_NAME = '{table_name}'"
				cursor.execute(header_query)
				headers = cursor.fetchall()

			header_string = ", ".join([header[0] for header in headers])

			data_rows = [header_string] + [", ".join([str(element) for element in row]) for row in selected_rows]
			combined_data = "\n".join(data_rows)

			result.append([create_table_statement, combined_data])

		return result


import openai

# -!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!
# This is the response max length!!!
# -!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!
G_max_tokens = 500

class Codegen:
	def __init__(self, api_key):
		self.api_key = api_key
		openai.api_key = self.api_key
		self.model = "gpt-3.5-turbo"

	def generate_code(self, prompt, max_tokens=G_max_tokens, n=1):
		prompt = f"You are a helpful assistant that translates natural language to MySQL SQL code. {prompt}"
		response = openai.Completion.create(
			engine=self.model,
			prompt=prompt,
			max_tokens=max_tokens,
			n=n,
			stop=None,
			temperature=0.7,
		)

		return response.choices[0].text.strip()

if __name__ == "__main__":
	api_key = "your_api_key_here"  # Replace with your actual API key
	codegen = Codegen(api_key)

	prompt = "Write a Python function to reverse a string"  # Replace with your desired prompt
	generated_code = codegen.generate_code(prompt)
	print("Generated code:")
	print(generated_code)

import time

def write_result_to_file(result):
	# Get the first four words of the result string
	first_four_words = " ".join(result.split()[:4])

	# Generate a timestamp
	timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")

	# Create a filename based on the first four words and the timestamp
	filename = f"{first_four_words}_{timestamp}.txt"

	# Write the result to the file
	with open(filename, "w") as f:
		f.write(result)

# Example usage:

def main():
	with open('tables.txt', 'r') as f:
		tables_constrain = [line.strip() for line in f]

	db = MySQLDatabase("creds.txt", tables_constrain)
	data = db.generate_data()

	schema_data = ""
	for item in data:
		schema_data += "Table schema: " + item[0] + "\n" + "Sample select * from <table>: " + item[1] + "\n"

	api_key = open("api.key", 'r').readline()
	codegen = Codegen(api_key)

	user_input = input("Please enter the desired information to retrieve: ")
	prompt = f"Using these tables that I am including the schema and example data from, write a SQL statement that will {user_input}Here is the schema and sample data: `{schema_data}`"

	select_statement = codegen.generate_code_from_user_prompt(prompt)
	print("Generated select_statement:")
	print(select_statement)

	db_conn = MySQLConnection('creds.txt')
	result = db_conn.execute_query(select_statement)
	print("Result:")
	print(result)


if __name__ == "__main__":
	main()

