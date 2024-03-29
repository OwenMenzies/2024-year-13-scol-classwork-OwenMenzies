import fs from 'fs';
import path from 'path';
import readline from 'readline';

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

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
    // Display the list of images
    console.log('Available images:');
    imageFiles.forEach((file, index) => {
      console.log(`${index + 1}. ${file}`);
    });
    // Prompt user to select an image
    rl.question('Enter the number of the image you want to encode (Enter "0" to exit): ', async userInput => {
      const selectedIndex = parseInt(userInput);
      if (selectedIndex === 0) {
        rl.close(); // Exit if the user inputs '0'
        return;
      }
      if (selectedIndex >= 1 && selectedIndex <= imageFiles.length) {
        const selectedImage = imageFiles[selectedIndex - 1];
        const imagePath = path.join(imagesFolder, selectedImage);
        try {
          const base64String = await convertImageToBase64(imagePath);
          console.log(`${selectedImage}: ${base64String}`);
        } catch (error) {
          console.error(`Error converting ${selectedImage} to base64:`, error);
        }
      } else {
        console.log('Invalid input. Please enter a number between 0 and', imageFiles.length);
      }
      rl.close();
    });
  })
  .catch(error => {
    console.error('Error reading images folder:', error);
  });
