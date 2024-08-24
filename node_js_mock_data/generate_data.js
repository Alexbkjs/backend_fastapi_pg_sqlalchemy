/*This Node.js script is generating a mock data string that includes a hash used for verifying the integrity of the data. 
It mimics part of a process related to secure data transmission. */

// node generate_data.js

// There is a difference of how nodejs encodes data and how it performed in other languages like Python, so pay attetion to which format of 
// data is used to make a hash from it

const crypto = require('crypto');

// Replace with your fake bot token
const fakeBotToken = "test_bot_token";

// Create mock data
const initDataRaw = new URLSearchParams([
    ['user', encodeURIComponent(JSON.stringify({
        id: 99281932,
        first_name: 'Andrew',
        last_name: 'Rogue',
        username: 'rogue',
        language_code: 'en',
        is_premium: true,
        allows_write_to_pm: true,
    }))],
    ['auth_date', '1716922846'],
    ['start_param', 'debug'],
    ['chat_type', 'sender'],
    ['chat_instance', '8428209589180549439'],
]);

// Generate data_check_string
const dataCheckString = Array.from(initDataRaw.entries())
    .map(([key, value]) => `${key}=${value}`)
    .sort()
    .join('\n');

// Log data check string and secret key
// console.log("Data Check String:", dataCheckString);
// console.log("Secret Key:", fakeBotToken + 'WebAppData');


// Generate hash using fake bot token
const hash = crypto.createHmac('sha256', fakeBotToken + 'WebAppData')
    .update(dataCheckString)
    .digest('hex');

// Add the generated hash to initDataRaw
initDataRaw.append('hash', hash);

// console.log("Generated Hash:", hash);

// Output the generated data
console.log('Generated initDataRaw string for POST request to your backend with "Content-Type: application/json" header and JSON body in format {"initDataRaw": "user=%257B%2522id%2522%...}:');
console.log(initDataRaw.toString());
