const fs = require('fs');

// Directory where the JSON files are located
const directory = '\data';

// Array to hold all the response objects
const combinedResponse = [];

// Read each JSON file and extract the "response" part
fs.readdir(directory, (err, files) => {
  if (err) {
    console.error('Error reading directory:', err);
    return;
  }

  files.forEach(file => {
    if (file.endsWith('.json')) {
      const filePath = `${directory}/${file}`;
      const data = fs.readFileSync(filePath);
      const jsonData = JSON.parse(data);
      const response = jsonData.response;
      combinedResponse.push(...response);
    }
  });

  // Create an object to hold the combined response
  const combinedData = { response: combinedResponse };

  // Save the combined data to a new JSON file
  const outputFilePath = 'combined.json';
  fs.writeFileSync(outputFilePath, JSON.stringify(combinedData, null, 2));
  console.log('Combined JSON file created successfully!');
});
