import OpenAI from "openai";
import readline from 'readline';

const openai = new OpenAI();
var i = 0;
const history = new Array();
var messTextBase = "\u001b[34mHello Chatgpt, please respond with 2-3 sentence responses. You have been asked '";
var messText = "";
var j = 0;
const responses = new Array();
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

async function callgpt(question) {
  
  const completion = await openai.chat.completions.create({
    messages: [{ role: "system", content: "Greetings" }, { role: "user", content: question }],
    model: "gpt-3.5-turbo",
  });

  const answer = completion.choices[0].message.content;
  return answer;
  
} 

console.log('Hello, this is my module!');

async function askQuestion() {
  const userInput = await new Promise(resolve => {
    rl.question('What would you like to ask the almighty? (Enter "0" to exit): ', resolve);
   
  });

  if (userInput !== '0') {
    console.log(`You asked: ${userInput}\nNow await your response from the divine`);
    history[i] = userInput;
    i = i+1;
    
    messText = messTextBase;
    if (history.length!=0){
    for (j=0; j < history.length; j++){
      messText = messText+history[j] + ", "
     
      }
    }
    if (responses.length!= 0) {
    messText = messText + "and have answered to each question the the answer of '"
    
    for (j=0; j < (responses.length-1); j++){
      messText = messText+responses[j] + "', '"
     
      }
      messText = messText + "'"
      console.log(messText)
    }
    // Call the OpenAI API after getting user input
    const answer = await callgpt(userInput);
    // return
    responses[i-1] = answer
    console.log(responses)
    console.log(answer);
    
    // Ask the next question
    askQuestion();
  } else {
    // Close the readline interface when the user enters '0'
    rl.close();
  }
}

// Start the question loop
askQuestion();
