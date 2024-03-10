import OpenAI from "openai";
import { userInfo } from "os";
import readline from 'readline';
var userInput = "1";
const openai = new OpenAI();

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

async function callgpt(question) {
  console.log('point 2')
  const completion = await openai.chat.completions.create({
    messages: [{ role: "system", content: "Greetings" }, { role: "user", content: question }],
    model: "gpt-3.5-turbo",
  });

  const answer = completion.choices[0].message.content;
  return answer;
} 

console.log('Hello, this is my module!');

// Use the readline interface to prompt for user input
// rl.question('What would you like to ask the all mighty?: ', async (userInput) => {
//   console.log(`You asked: ${userInput} \nNow await your response from the divine`);

//   // Call the OpenAI API after getting user input
//   const answer = await callgpt(userInput);
//   console.log('point 1');
//   console.log(answer);

//   rl.close();
// });

while (userInput != '0'){

  rl.question('What would you like to ask the all mighty?: ', async (userInput) => {
    console.log(`You asked: ${userInput} \nNow await your response from the divine`);
  
    // Call the OpenAI API after getting user input
    const answer = await callgpt(userInput);
    console.log('point 1');
    console.log(answer);
  
    rl.close();
  });
}