# MealBot
A serverless dining concierge chatbot implemented with AWS Lex, Lambda, API Gateway, Cognito, S3 and Yelp API.

## INTRODUCTION:
##### Log In
You can sign up on our site or log in via third-party account like Google.

##### How To Use

1. First, user can use ‘hello’ or some other greeting sentences to invoke the chat bot and bot will use hello response set in AutoHelloMesage intent to guide user how to get suggestions.

2. Then user input the cuisine he want. The lex can save this parameter as ‘FoodType’ . There should be a food type validation function to verify the format of the input. 
In this case, we use a simple list which save the food types in test using. ( But the yelp searching method can return the result even in a strange input, so we disabled this function.)

3. Next, the bot will ask user to input the location and amount of people who will attend.

4. After defining restaurant style informations, the bot will ask user to input the time message. The date can in different format like ‘Today’, ‘3-11’, ‘March 13’ etc. The time  should in ‘7PM’ format. The message which in other format will get False return value in intent validation functions and output the guide message.

5. After getting suggestions, user can input goodbye sentences ‘thanks’ to end the conversation.

