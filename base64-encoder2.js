const fs = require('fs');

function encodeImage(filePath) {
  fs.readFile(filePath, (err, data) => {
    if (err) {
      console.error('Error reading file:', err);
      return;
    }

    const base64String = Buffer.from(data).toString('base64');
    console.log(base64String);
    // You can do something with the base64 encoded string here, like sending it to a server
  });
}

// Example usage:
const imagePath = 'path/to/your/image.jpg'; // Change this to the path of your image file
encodeImage(imagePath);
