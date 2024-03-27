import fetch from 'node-fetch';
import fs from 'fs/promises';

// Function to encode the image
async function encodeImage(imagePath) {
    const imageBuffer = await fs.readFile(imagePath);
    return imageBuffer.toString('base64');
}

// Path to your image
const imagePath = "images/burj.jpg";

// OpenAI API Key
const apiKey = "YOUR_OPENAI_API_KEY";

async function main() {
    try {
        // Getting the base64 string
        const base64Image = await encodeImage(imagePath);

        const headers = {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${apiKey}`
        };

        const payload = {
            "model": "gpt-4-vision-preview",
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

        const response = await fetch("https://api.openai.com/v1/chat/completions", {
            method: 'POST',
            headers: headers,
            body: JSON.stringify(payload)
        });

        const responseData = await response.json();
        console.log(responseData);
    } catch (error) {
        console.error("Error:", error);
    }
}

// Call the main function
main();
