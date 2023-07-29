const fs = require('fs');
const util = require('util');

// Read the combined.json file
fs.readFile('combined.json', (err, data) => {
	if (err) {
		console.error('Error reading file:', err);
    return;
	}

	// Parse the JSON data
	const jsonData = JSON.parse(data);

	// Generate the seed code block
	const seedCode = generateSeedCode(jsonData.response);

	// Save the seed code to a text file
	fs.writeFile('seed-code.txt', seedCode, err => {
		if (err) {
		  console.error('Error writing file:', err);
		  return;
		}
		console.log('Seed code saved to seed-code.txt');
	});
  
	// Generate the SQL code block
	const sqlCode = generateSqlCode(jsonData.response);

	// Save the SQL code to a text file
	fs.writeFile('insert-airports.sql', sqlCode, err => {
		if (err) {
			console.error('Error writing file:', err);
			return;
		}
		console.log('SQL code saved to insert-airports.sql');
	});
});

// Function to generate the seed code block
function generateSeedCode(response) {
    let seedCode = 'protected void Seed_Airport(ModelBuilder builder)\n{\n';
    seedCode += '    var order = 1;\n';
    seedCode += '    var airports = new[]\n';
    seedCode += '    {\n';
    let names = {};

    for (const airport of response) {
        // skip if name is empty or null
        if(!airport.name) continue;

        let name = escapeQuotes(airport.name);
        // check if name is duplicate
        if(names[name]){
            names[name]++;
            name = name + '_' + names[name];
        } else {
            names[name] = 1;
        }
        
        seedCode += `new { Name = "${name}", ICAO = "${escapeQuotes(airport.icao_code)}" },\n`;
    }

    seedCode += '    };\n\n';
    seedCode += '    foreach (var airport in airports)\n';
    seedCode += '    {\n';
    seedCode += '        builder.Entity<Airport>().HasData(new Airport\n';
    seedCode += '        {\n';
    seedCode += '            Id = order,\n';
    seedCode += '            Name = airport.Name,\n';
    seedCode += '            ICAO = airport.IATA,\n';
    seedCode += '        });\n';
    seedCode += '    }\n';
    seedCode += '}\n';
	
    seedCode += 'public long CountryCodeToId(string countryCode)\n';
    seedCode += '{\n';
    seedCode += '    // Get the country from the Country table using the country code\n';
    seedCode += '    var country = Countries.FirstOrDefault(c => c.Code == countryCode);\n';
    seedCode += '\n';
    seedCode += '    // If a matching country is found, return its ID; otherwise, return a default value\n';
    seedCode += '    return country != null ? country.Id : 0;\n';
    seedCode += '}\n';

    return seedCode;
}

// Function to generate the SQL insert code block
function generateSqlCode(response) {
    const nameCounts = {};
    let sqlCode = '';
    let order = 1;  // Initialize order/Id variable

    for (const airport of response) {
        let name = escapeQuotes(airport.name);

        if (name in nameCounts) {
            nameCounts[name]++;
            name += '_' + nameCounts[name];
        } else {
            nameCounts[name] = 1;
        }

        let icao = airport.icao_code !== undefined ? airport.icao_code : '';  // If ICAO is undefined, use an empty string

        sqlCode += util.format("INSERT INTO dbo.airports (Id, Name, ICAO) " +
            "VALUES(%d, '%s', '%s');\n",
            order, name, icao);  // Use order variable instead of airport.id
        order++;  // Increment order for next iteration
    }

    return sqlCode;
}

// Function to escape single and double quotes in a string for SQL compatibility
function escapeQuotes(str) {
    if (str === undefined || str === null) {
        return '';
    }
    // Escape double quotes
    str = str.replace(/"/g, '\\"');
    // Escape single quotes for SQL (replace single quote with two single quotes)
    str = str.replace(/'/g, "''");
    return str;
}