import fs from 'fs';
import path from 'path';
import OpenAI from "openai";
import readline from 'readline';
// set up global variables 
const openai = new OpenAI();
var i = 0;
var runQuantity = 0;
const history = new Array();
// set up the prompt to chatgpt  
var messTextBase = "\u001b[34mHello Chatgpt, please respond with 2-3 sentence responses. You have been asked 'what is this image? ";
var messText = "";
var img = "";
var j = 0;
var k = 0;
const responses = new Array();
// set up the connection to the terminal
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});
console.log("8")
async function  Base64Image() {
  console.log("7")
  async function convertImageToBase64(imagePath) {
    console.log("6")
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
  console.log("5")
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
      console.log("4")
      // Prompt user to select an image
      rl.question('Enter the number of the image you want to encode (Enter "0" to exit): ', async userInput => {
        const selectedIndex = parseInt(userInput);
        console.log("3")
        if (selectedIndex === 0) {
          rl.close(); // Exit if the user inputs '0'
          return;
        }
        console.log("2")
        if (selectedIndex >= 1 && selectedIndex <= imageFiles.length) {
          const selectedImage = imageFiles[selectedIndex - 1];
          const imagePath = path.join(imagesFolder, selectedImage);
          try {
            console.log("1")
            const base64String = await convertImageToBase64(imagePath);
            console.log(`${selectedImage}: ${base64String}`);
            return string(base64String);
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

}
(async () => {
  img = await Base64Image();
  console.log(img);
  // Start the question loop
  askQuestion();
})();

console.log(img);
// create the api function 
async function callgpt(question) {
  // send and wait for a response from chatgpt
  const completion = await openai.chat.completions.create({
    
    messages: [{ role: "system", content: "Greetings" }, { role: "user", content: question }],
    model: "gpt-4-vision-preview",
  });
  // recieve the answer from chatgpt and return it 
  const answer = completion.choices[0].message.content;
  return answer;  
} 

// confirm that the program is running and explain its purpose
console.log('Hello, this is a program that connects the user to chatgpt through an api');
// create the question - answer loo[]
async function askQuestion() {
  // receive the quesiton from the user
  console.log("promise!")
  const userInput = await new Promise(resolve => {
    rl.question('What would you like to ask the almighty? (Enter "0" to exit): ', resolve);
   
  });
  // if the answer is not 0 (0 will end the code)
  if (userInput !== '0') {
    // print to the user what quesiton the asked
    console.log(`You asked: ${userInput}\nNow await your response from the divine`);
    // add the question to the history array for later reference 
    history[i] = userInput;
    i = i+1;
    // reset the prompt to the original state
    messText = messTextBase;    
    // if there have been questions asked by the user, messText will need to be updated with prevous questions
    if (history.length!=0){
      // for every previous quesiton, append it to messText for ChatGPT's reference, except the current question
      for (j=0; j < history.length-1; j++){
        messText = messText+history[j] + "', "
     
      }
    }
    // if ChatGPT has answer any prevois questions, add them to the prompt
    if (responses.length!= 0) {
    messText = messText + "and have answered to each question the the answer of '"
    // add each response 
    for (k=0; k < (responses.length); k++){
      console.log(responses)
      messText ="'"+ messText+responses[k] 
      // logic for proper syntax 
      if (k+1==responses.length){
        
        messText = messText+ "'"
      }
      else{
        messText = messText + ", '"
      }
    }
      // add the current question to the prompt
      messText = messText + ". Please anwser the current question of " + history[history.length-1]
      console.log(messText)
    }
    // if this is the first question chatgpt as asked, make the prompt the the user input
    if( runQuantity == 0) {
      messText = userInput


    }
    // Call the OpenAI API after creating the prompt 
    const answer = await callgpt(img);
    // add the responce to the answer 
    responses[i-1] = answer
    //display chatgpt's answer to the user's question
    console.log(responses)
    console.log(answer);
    runQuantity ++
    // Ask the next question
    askQuestion();
  } else {
    // Close the readline interface when the user enters '0'
    rl.close();
  }
}

// Start the question loop
askQuestion();
