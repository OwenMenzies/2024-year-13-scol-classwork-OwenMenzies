// main.js
import readline from 'readline';

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

console.log('Hello, this is my module!');

// Use the readline interface to prompt for user input
rl.question('Please enter something: ', (answer) => {
  console.log(`You entered: ${answer}`);
  rl.close();
});
