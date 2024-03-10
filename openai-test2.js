import OpenAI from "openai";
import readline from 'readline';

const openai = new OpenAI();

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

async function callgpt(question) {
  console.log('point 2');
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
    rl.question('What would you like to ask the all mighty? (Enter "0" to exit): ', resolve);
  });

  if (userInput !== '0') {
    console.log(`You asked: ${userInput}\nNow await your response from the divine`);

    // Call the OpenAI API after getting user input
    const answer = await callgpt(userInput);
    console.log('point 1');
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
