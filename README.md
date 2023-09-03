# LightHouse-GenerativeAI-Application
<br> 

## Lighthouse GenerativeAI Application Workflow

### Introduction

The Lighthouse GenerativeAI Application is a web-based platform designed to provide detailed information about lighthouses. This document explains the workflow of the application, from user input to the presentation of the response.

### Workflow Overview

The Lighthouse GenerativeAI Application employs several components to deliver information to users efficiently. The workflow can be divided into the following steps:

![Workflow_FlowChat](https://i.imgur.com/vR7wwyp.png)


1. **User Interaction**: Users access the application through a web interface. They can input questions or prompts related to lighthouses, seeking information or details.

2. **User Input Processing**: When a user submits a question or prompt, the application begins processing it. This step ensures that the input is clear, relevant, and suitable for further analysis.

3. **Interaction with GPT-3 (Large Language Model - LLM)**: The processed user input is then sent to a powerful language model called GPT-3 (Generative Pre-trained Transformer 3), often referred to as the Large Language Model (LLM). GPT-3 is a sophisticated AI model capable of understanding and generating human-like text.

4. **Data Retrieval from Lighthouse Database**: Simultaneously, a DataFrame Agent comes into play. This agent is responsible for querying a lighthouse database. It retrieves relevant information and facts about lighthouses based on the user's input.

5. **Data Combination**: The DataFrame Agent collects and organizes the data gathered from the lighthouse database. It ensures that the retrieved information is properly structured and ready for presentation.

6. **Information Fusion**: The processed user input from GPT-3 and the organized lighthouse data from the DataFrame Agent are combined to create a comprehensive response. This fusion involves synthesizing the information and generating an accurate answer.

7. **Response Formatting by LLM**: Once the response is generated, it is passed back to GPT-3 (LLM). The LLM is not only skilled at generating text but also at making it look clean and well-formatted.

8. **Displaying the Response**: Finally, the beautifully formatted response is presented on the user's screen. Users can read and explore the detailed information about lighthouses, all within the application's user-friendly interface.

## Conclusion

The Lighthouse GenerativeAI Application leverages the power of AI and data retrieval to provide users with accurate and engaging information about lighthouses. It streamlines the process from user input to response, ensuring that users receive well-structured and informative answers to their questions.

This workflow enables users to have an enjoyable and informative experience while learning about lighthouses through a simple chat interface.

<br>

## Installation and Setup

### Step 1: Clone the Repository

1. Go to the GitHub repository of your project.
2. Click the "Code" button and copy the repository URL.
3. Open a terminal on your computer.

```bash
git clone https://github.com/sureshsgith/LightHouse-GenerativeAI-Application.git
cd LightHouse-GenerativeAI-Application
```

### Step 2: Set up a Virtual Environment

1. In the terminal, navigate to the project directory if you aren't already there.
```bash
cd LightHouse-GenerativeAI-Application
```
2. Create a virtual environment (if you don't have it installed, run pip install virtualenv first).
```bash
python -m venv venv
```
3. Activate the virtual environment.
   #### On Windows:
  ```bash
    .\venv\Scripts\activate
  ```
   #### On macOS and Linux:
  ```bash
    source ./venv/bin/activate
  ```
### Step 3: Install Required Python Modules
1. With the virtual environment active, install the required Python modules using pip by providing the requirements.txt file.
   ```bash
   pip install -r requirements.txt
   ```
2. Set Your OPENAI API Key in chat.py from [OPENAI](https://platform.openai.com/account/api-keys)
## Running the Web App
Now that you've set up the environment, you can run your LightHouse GenerativeAI Application.

### Step 4: Start the App
1. Make sure you are still in the project directory with the virtual environment activated.
2. Run the Chat application by executing the app.py file.
```bash
sudo python3 app.py
```
## Access the Web App

1. Open a web browser.
2. In the browser's address bar, enter the [http://localhost](http://localhost) URL to access your LightHouse GenerativeAI Application.

**That's it! You've successfully installed and run your GenerativeAI app. Enjoy using it** 


