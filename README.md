# 💃BritneyBot: Pop Star Statistician

This project challenged me to build and deploy my first open source LLM API solution. It's a simple data analysis chatbot built on the personality of Britney Spears, which analyzes a small data set of student grades in math and physics. The data set was provided by the Lonely Octopus Program and inspiration for the challenge came from Ibraheem Ansari, after he taught a super helpful training on open source LLMs. Thank you to him and the entire LO team for your support!

#### <i>Okay, Britney Babes, let's get started!💃</i>

## Project Components🎤

1. 🐍**Python**: The primary programming language used for this project. Python is used for both the backend (FastAPI) and frontend (Streamlit) development.

2. ⚡**FastAPI**: A modern, fast (high-performance) web framework for building APIs with Python. In this project, FastAPI is used to create the backend server that handles requests from the Streamlit frontend and communicates with the Hugging Face Inference Endpoint.

3. 🤗**Hugging Face Inference Endpoint**: A cloud-hosted API service that runs open-source machine learning models. For this project, I'm using a dedicated HF Inference Endpoint with an NVidia L4 and the Meta llama3:18b Instruct HLR model, which powers BritneyBot's responses. The FastAPI backend sends prompts to this endpoint and receives the generated text responses. <b>Note:</b> In the future, I'd opt for the Serverless Endpoint, which is free and automatically scales down during inactivity. I chose the dedicated endpoint for this initial project while I was getting familiar with the HF platform and its options. I spent about about $25 on testing, so I guess for this mistake I just have to say...<i>oh, baby, baby, how was I supposed to know...?🎵</i></br>

5. 🐳**Docker**: A platform used to develop, ship, and run applications inside containers. In this project, Docker is used to containerize the FastAPI application, ensuring consistent deployment across different environments.

6. ☁️**Render**: A cloud platform used to deploy and host web services. In this project, Render is used to deploy and host the Docker container running the FastAPI backend.

7.  🪄**Streamlit**: An open-source Python library used to create web applications for machine learning and data science projects. In this project, Streamlit is used to create the frontend user interface where users can interact with BritneyBot.

8. 🐼**pandas**: A Python library used for data manipulation and analysis. In this project, pandas is used to load and process the student grades data.

9. 📫**requests**: A Python library used for making HTTP requests. Used in both the FastAPI backend (to communicate with the Hugging Face Inference Endpoint) and the Streamlit frontend (to communicate with the FastAPI backend).

## Project Workflow💖:

1. The user interacts with the Streamlit frontend, entering questions about the student grades data.
2. The Streamlit app sends these questions to the FastAPI backend hosted on Render.
3. The FastAPI backend processes the request, formats the prompt, and sends it to the Hugging Face Inference Endpoint.
4. The Hugging Face Inference Endpoint generates a response using the hosted language model.
5. The FastAPI backend receives the response, processes it to ensure it's in Britney's style, and sends it back to the Streamlit frontend.
6. The Streamlit frontend displays the response to the user.

This setup allows for a scalable, cloud-based application that leverages modern web technologies and machine learning capabilities to create an engaging user experience. 

## Prompt Parameters🎨Helpful Tips:
You can adjust various elements to fine-tune the personality of BritneyBot!
Overview:
- For more creative, varied responses: Increase temperature and top_p.
- For more focused, consistent responses: Decrease temperature and top_p.
- For longer or shorter responses: Adjust max_new_tokens.

## Prompt Parameters🌡️Adjustment Instructions: 
Adjust the main.py parameters as desired. See current settings and guide:
1. 🌡️ "max_new_tokens": 200
- This attempts to limit the response to about 5-7 sentences, ensuring brevity. Increase this if you want longer responses, or decrease for shorter ones. Adjusting this affects the response length and potentially the API call cost.
2. 🌡️ "temperature": 0.6
- This attempts to balance creativity with accuracy. This should still allow for Britney's "voice" and emojis while maintaining mathematical correctness. This controls the randomness of the output. Higher values (e.g., 1.0) make output more random, lower values (e.g., 0.2) make it more focused and deterministic. Adjust this based on how creative or precise you want the responses to be.
3. 🌡️"top_p": 0.90
- This focuses the output a bit more, but still allowing for creative elements. This is for nucleus sampling. It controls the cumulative probability of token selection. Lower values (e.g., 0.5) make the output more focused, higher values (e.g., 0.95) allow for more diversity.You can adjust this in conjunction with temperature to fine-tune the output style.
4. 🌡️ "do_sample": True 
- This allows for some randomness in the responses. This enables sampling (as opposed to always choosing the most likely next token). You might set this to False if you want more deterministic outputs.

## 💌Thank You & Contact Info
#### <i>Thank you for visiting BritneyBot!</i>
- Questions? Email glitterpileshop@gmail.com or contact me here at https://github.com/kobrakitty
- Curious? Follow my AI learning journey and www.glitterpile.blog.
<br>🥰xo Kobra Kitty</br>
