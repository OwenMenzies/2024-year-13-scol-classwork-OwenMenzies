import fs from 'fs';
import path from 'path';
import OpenAI from "openai";
import readline from 'readline';

// Set up global variables 
const openai = new OpenAI();
var i = 0;
var runQuantity = 0;
const history = new Array();
// set up the prompt to chatgpt  
var messTextBase = "\u001b[34mHello Chatgpt, please respond with 2-3 sentence responses. You have been asked 'what is this image? ";
var messText = "";
var img = "";
const responses = new Array();
// Set up the connection to the terminal
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});
async function callgpt(question) {
  // send and wait for a response from chatgpt
  const completion = await openai.chat.completions.create({
    messages: [{ role: "system", content: "Greetings" }, { role: "user", content: question }],
    model: "gpt-4",
  });
  // recieve the answer from chatgpt and return it 
  const answer = completion.choices[0].message.content;
  return answer;
  
}
async function Base64Image() {
  const convertImageToBase64 = async (imagePath) => {
    try {
      // Read the image file
      const data = await fs.promises.readFile(imagePath);
      // Encode the image data to base64
      return Buffer.from(data).toString('base64');
    } catch (error) {
      throw error;
    }
  };

  // Get the directory name using import.meta.url
  const __dirname = path.dirname(new URL(import.meta.url).pathname);
  // Path to the images folder
  const imagesFolder = path.join(__dirname.replace(/^\/([a-z]):/i, '$1:'), 'images');

  try {
    const files = await fs.promises.readdir(imagesFolder);
    // Filter out non-image files
    const imageFiles = files.filter(file => /\.(jpg|jpeg|png|gif)$/i.test(file));
    // Display the list of images
    console.log('Available images:');
    imageFiles.forEach((file, index) => {
      console.log(`${index + 1}. ${file}`);
    });

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
          global.img = base64String;
          
          return base64String
        } catch (error) {
          console.error(`Error converting ${selectedImage} to base64:`, error);
        }
      } else {
        console.log('Invalid input. Please enter a number between 0 and', imageFiles.length);
      }
    });
  } catch (error) {
    console.error('Error reading images folder:', error);
  }
}

// Call Base64Image and initiate the process
img = await Base64Image();
console.log(img)
askQuestion(img); // Call askQuestion with base64 string
// Create the API function 
async function callgpt(question) {
  try {
    // Send and wait for a response from ChatGPT
    console.log("sent")
    console.log(question)
    const completion = await openai.chat.completions.create({
      messages: [{ role: "system", content: "Greetings" }, { role: "user", content: question }],
      model: "gpt-4-vision-preview",
    });
    // Receive the answer from ChatGPT and return it 
    console.log("received")

    console.log(completion.choices[0].message);
   // console.log(completion.choices[0].message.content);
    return completion.choices[0].message.content;
  } catch (error) {
    console.error('Error in callgpt:', error);
    throw error;
  }
} 


// Confirm that the program is running and explain its purpose
console.log('Hello, this is a program that connects the user to ChatGPT through an API');

// Create the question - answer loop
async function askQuestion(img) {
  const userInput = await new Promise(resolve => {
    rl.question('What would you like to ask the almighty? (Enter "0" to exit): ', resolve);
  });

  if (userInput !== '0') {
    console.log(`You asked: ${userInput}\nNow await your response from the divine`);
    history.push(userInput);
    messText = messTextBase;    

    if (history.length !== 0) {
      for (let j = 0; j < history.length - 1; j++) {
        messText = messText + history[j] + "', ";
      }
    }

    if (responses.length !== 0) {
      messText = messText + "and have answered to each question the answer of '";
      for (let k = 0; k < responses.length; k++) {
        console.log(responses);
        messText = "'" + messText + responses[k];
        if (k + 1 === responses.length) {
          messText = messText + "'";
        } else {
          messText = messText + ", '";
        }
      }
      messText = messText + `. Please answer the current question of ${history[history.length - 1]}`;
      console.log(messText);
    }

    if (runQuantity === 0) {
      messText = userInput;
    }

    try {
      const answer = await callgpt(img);
      responses.push(answer);
      console.log(responses);
      console.log(answer);
      runQuantity++;
      askQuestion(img);
    } catch (error) {
      console.error('Error in askQuestion:', error);
      rl.close();
    }
  } else {
    rl.close();
  }
}
