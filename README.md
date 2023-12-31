# Combine JSON

This Node.js script combines multiple JSON files from a specified directory into a single JSON file. The script is specifically designed to extract the "response" part from each JSON file and then combine them into one.

## How to Use

1. Clone this repository or download the script.

2. Ensure that Node.js is installed on your machine.

3. Put the JSON files you want to combine in the 'data' directory.

4. Run the script using the command `node combine-json.js`.

The output file named 'combined.json' will be created in the root directory.

## Script Explanation

The script uses Node.js built-in 'fs' module to read and write files. It first reads all the files in the given directory. Then for each file that ends with '.json', it reads the file, parses the JSON data, extracts the "response" part, and adds it to an array. Once all the JSON files have been processed, it saves the combined response to a new JSON file named 'combined.json'.

# Generate Seed

This is a Node.js script that reads a JSON file containing airport data and generates a C# Seed method and SQL insert commands. The seed method and SQL commands are saved as text files. This script is useful for creating database seed data and SQL commands based on a JSON data source.

## How to Use

1. Clone this repository or download the script.

2. Ensure that Node.js is installed on your machine.

3. Run the script using the command `node generate-seed.py`.

The output files 'seed-code.txt' and 'insert-airports.sql' will be created.

## Script Explanation

The script first reads the 'combined.json' file and parses the JSON data. 

It then generates the seed method by iterating over the response data. For each airport, it checks if the name is not empty and if it is not a duplicate. It then adds a new line to the seed method code with the airport's name and ICAO code. 

Next, it generates the SQL commands by iterating over the response data again. For each airport, it escapes any single or double quotes in the name and ICAO code, and then adds a new line to the SQL commands with an INSERT INTO statement. 

Both the seed method and SQL commands are saved as text files. The script also includes a function to escape single and double quotes in a string for SQL compatibility.
