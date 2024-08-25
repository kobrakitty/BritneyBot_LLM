# 💃BritneyBot: Pop Star Statistician - Project Components🎤📊

<br>This project was a challenging experiment for me to learn how to build and deploy my first open source LLM API solution. From the user perspective, it's a simple chatbot (built on the personality of Britney Spears, of course) with the purpose of analyzing a simple data set, provided by the Lonely Octopus Program. In future iterations, I would like to use more complex data sets, provide the option to download the chat with BritneyBot, and maybe even generate a fun AI image based on the question as a token of participation for the user.</br>

1. **Python**: The primary programming language used for this project. Python is used for both the backend (FastAPI) and frontend (Streamlit) development.

2. **FastAPI**: A modern, fast (high-performance) web framework for building APIs with Python. In this project, FastAPI is used to create the backend server that handles requests from the Streamlit frontend and communicates with the Hugging Face Inference Endpoint.

3. **Hugging Face Inference Endpoint**: A cloud-hosted API service that runs open source machine learning models. In this project, I am using a dedicated HF Inference Endpoint via NVidia L4 ad the Meta llama3:18b Instruct HLR model, which hosts the language model that powers BritneyBot's responses. The FastAPI backend sends prompts to this endpoint and receives generated text responses. Next time, I would choose to use the Serverless Endpoint, which is FREE and winds-down with inactivity. I only used a dedicated endpoint for this initial project because I was new to the HF platform and still learning my way around the options. Oops (I Did it Again).

4. **Docker**: A platform used to develop, ship, and run applications inside containers. In this project, Docker is used to containerize the FastAPI application, ensuring consistent deployment across different environments.

5. **Render**: A cloud platform used to deploy and host web services. In this project, Render is used to deploy and host the Docker container running the FastAPI backend.

6. **Streamlit**: An open-source Python library used to create web applications for machine learning and data science projects. In this project, Streamlit is used to create the frontend user interface where users can interact with BritneyBot.

7. **pandas**: A Python library used for data manipulation and analysis. In this project, pandas is used to load and process the student grades data.

8. **requests**: A Python library used for making HTTP requests. Used in both the FastAPI backend (to communicate with the Hugging Face Inference Endpoint) and the Streamlit frontend (to communicate with the FastAPI backend).

## Workflow:

1. The user interacts with the Streamlit frontend, entering questions about the student grades data.
2. The Streamlit app sends these questions to the FastAPI backend hosted on Render.
3. The FastAPI backend processes the request, formats the prompt, and sends it to the Hugging Face Inference Endpoint.
4. The Hugging Face Inference Endpoint generates a response using the hosted language model.
5. The FastAPI backend receives the response, processes it to ensure it's in Britney's style, and sends it back to the Streamlit frontend.
6. The Streamlit frontend displays the response to the user.

This setup allows for a scalable, cloud-based application that leverages modern web technologies and machine learning capabilities to create an engaging user experience. 

Special thanks to the 🐙Lonely Octopus Program🐙, teachers, mentors, and Discord community for all of your support! Learn more about their AI and data science program here: www.lonelyoctopus.com</br>