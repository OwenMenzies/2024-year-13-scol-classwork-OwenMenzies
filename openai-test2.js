import OpenAI from "openai";
import readline from 'readline';
// set up global variables 
const openai = new OpenAI();
var i = 0;
var runQuantity = 0;
const history = new Array();
// set up the prompt to chatgpt  
const messTextBase = `\u001b[34mHello Chatgpt, please respond with 2-3 sentence responses. You have been asked '`;
var messText = "";
var j = 0;
var k = 0;
const responses = new Array();
// set up the connection to the terminal
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});
// create the api function 
// ANSI escape codes for text color
const red = '\u001b[31m';
const green = '\u001b[32m';
const reset = '\u001b[0m';

// Use the escape codes to change font color
console.log(red + 'This text is red.' + reset);
console.log(green + 'This text is green.' + reset);

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
// confirm that the program is running and explain its purpose
console.log('Hello, this is a program that connects the user to chatgpt through an api');

// create the question to ask to ChatGPT
async function askQuestion() {
  // receive the quesiton from the user
  const userInput = await new Promise(resolve => {
    rl.question('What would you like to ask the almighty? (Enter "0" to exit): ', resolve);
   
  });
  // if the answer is not 0 (0 will end the code)
  if (userInput !== '0') {
    // print to the user what quesiton the asked
    console.log(`You asked:`+green+ ` ${userInput}`);
   
    // add the question to the history array for later reference 
    history[i] = userInput;
    i = i+1;
    // reset the prompt to the original state
    messText = messTextBase;    
    // if there have been questions asked by the user, messText will need to be updated with prevous questions
    // for every previous quesiton, append it to messText for ChatGPT's reference, except the current question
    for (j=0; j < history.length-1; j++){
      messText = messText+history[j] + "', "
     
    }
    // console.log(messText)

    // if ChatGPT has answered any previous questions, add them to the prompt
    if (responses.length!= 0) {
      messText = messText + "and have answered to each question the the answer of '"
      // add each response 
      for (k=0; k < (responses.length); k++){
        // console.log(responses)
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
    }
    // if this is the first question chatgpt as asked, make the prompt the the user input
    if( runQuantity == 0) {
      messText = userInput


    }
    // Call the OpenAI API after creating the prompt 
    messText = userInput
    console.log(messText)
    const answer = await callgpt(messText);
    // add the responce to the answer 
    responses[i-1] = answer
    //display chatgpt's answer to the user's question
    // console.log(responses)
    console.log("\u001b[34m",answer,reset);
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
