import OpenAI from "openai";
import fs from "fs";
import readline from 'readline';

const openai = new OpenAI();
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

// Function to encode the image
function encodeImage(imagePath) {
  const imageBuffer = fs.readFileSync(imagePath);
  return Buffer.from(imageBuffer).toString('base64');
}

// Function to get base64 string from image
function getBase64Image(imagePath) {
  return encodeImage(imagePath);
}

// Path to your image
const imagePath = "images/caveman.jpg";

// Getting the base64 string from file
const base64Image = getBase64Image(imagePath);
console.log(base64Image)
const payload = {
  "model": "gpt-4-turbo",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "What’s in this image?"
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
};

(async () => {
  try {
    const response = await openai.chat.completions.create(payload);
    console.log(response.choices[0]);
  } catch (error) {
    console.error("Error:", error);
  }
})();
