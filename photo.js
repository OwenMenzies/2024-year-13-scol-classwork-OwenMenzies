import fs from 'fs';
import path from 'path';
import readline from 'readline';
// Function to convert image file to base64
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});
const userInput = await new Promise(resolve => {
  rl.question('What would you like to ask the almighty? (Enter "0" to exit): ', resolve);
 
});
console.log(userInput);
async function convertImageToBase64(imagePath) {
  try {
    // Read the image file
    const data = await fs.promises.readFile(imagePath);
    // Encode the image data to base64
    return Buffer.from(data).toString('base64');
  } catch (error) {
    throw error;
  }
}

// Get the directory name using import.meta.url
const __dirname = path.dirname(new URL(import.meta.url).pathname);

// Path to the images folder
const imagesFolder = path.join(__dirname.replace(/^\/([a-z]):/i, '$1:'), 'images');

// Read all files in the images folder
fs.promises.readdir(imagesFolder)
  .then(files => {
    // Filter out non-image files
    const imageFiles = files.filter(file => /\.(jpg|jpeg|png|gif)$/i.test(file));
    // Convert each image file to base64
    imageFiles.forEach(async file => {
      const imagePath = path.join(imagesFolder, file);
      try {
        const base64String = await convertImageToBase64(imagePath);
        console.log(`${file}: ${base64String}`);
      } catch (error) {
        console.error(`Error converting ${file} to base64:`, error);
      }
    });
  })
  .catch(error => {
    console.error('Error reading images folder:', error);
  });
