import fs from 'fs';
import path from 'path';
import readline from 'readline';
import OpenAI from "openai";

const openai = new OpenAI();
const questions = new Array();
const responses = new Array();
var frame = 0;
var messTextBase = "Hello Chatgpt, please respond with 2-3 sentence responses. You have been asked '";
var messText = ""


const speechFile = path.resolve("./speech.mp3");

async function audio(text) {
  
  const mp3 = await openai.audio.speech.create({
    model: "tts-1",
    voice: "alloy",
    input: `${text}`,
  });

  console.log(speechFile);
  const buffer = Buffer.from(await mp3.arrayBuffer());
  await fs.promises.writeFile(speechFile, buffer);
}




async function callgpt(question,base64Image) {
  // send and wait for a response from chatgpt
//   console.log(question)
  const completion = await openai.chat.completions.create({
    "model": "gpt-4-turbo",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": `${question}`,
          },
          {
            "type": "image_url",
            "image_url": {
              "url": `data:image/jpeg;base64,${base64Image}`
            }
          }
        ]
      }
    ],
    "max_tokens": 300

  });
  
  
  // recieve the answer from chatgpt and return it 
  const answer = completion.choices[0].message.content;
  console.log("\x1b[36m%s\x1b[0m",answer)
  responses.push(answer)
  audio(answer)
  return answer;
}

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
        // console.log(`${selectedImage}: ${base64String}`);
        askQuestion(base64String)
      } catch (error) {
        console.error(`Error converting ${selectedImage} to base64:`, error);
      }
    } else {
      console.log('Invalid input. Please enter a number between 0 and', imageFiles.length);
    }
    
  });
})
.catch(error => {
  console.error('Error reading images folder:', error);
});

async function genQuesiton(){
    frame += 1;
    const userQuesiton = await new Promise(resolve => {
        rl.question('What would you like to ask the almighty? (Enter "0" to exit): ', resolve);
        
    });
    questions.push(userQuesiton)
    if (userQuesiton == "0") {
      rl.close();


    }
    if (frame != 1){
      messText = messTextBase;
      for (var i=0; i < questions.length-1; i++){
        messText = messText+questions[i] + ","
      }
      messText = messText + "' and have answered each with "
      for (var j=0; j < responses.length; j++){
        messText = messText+responses[j] 
      }
      messText = messText + " Please answer the current question of " +userQuesiton

    }
    else {
      messText = userQuesiton;

    }
    // console.log("\u001b[34m"+messText)
    return messText;

}


async function askQuestion(base64String) {  
    const quesiton = await genQuesiton()

    
    await callgpt(quesiton,base64String);
    askQuestion(base64String)
    
}
