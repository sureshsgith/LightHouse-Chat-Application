# Import necessary modules and classes from langchain library
# and other Python standard libraries
from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent, AgentOutputParser
from langchain.prompts import BaseChatPromptTemplate
from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from typing import List, Union
from langchain.schema import AgentAction, AgentFinish, HumanMessage
import re
import os 
from langchain.agents import create_pandas_dataframe_agent,Tool
from langchain.llms import OpenAI
import pandas as pd
import os 
import json

# Attempt to load chat history from a JSON file, or create an empty list if it doesn't exist
with open("./static/chat_history.json", 'a') as f:
    try:
        chat_history = json.loads(f.readlines())
    except:
        chat_history = []
        
# Set the OpenAI API key
os.environ["OPENAI_API_KEY"]="YOUR_OPENAI_API_KEY_HERE"

# Initialize the OpenAI language model (GPT-3)
llm=OpenAI(model="text-davinci-003",temperature=0.7)

# Load data from an Excel file into a Pandas DataFrame  
df=pd.read_excel("./static/lighthouse_data.xlsx")

# Create a Pandas DataFrame agent for interacting with the DataFrame
df_agent=create_pandas_dataframe_agent(llm,df,verbose=True)
# Define a list of tools available for the agent to use
tools=[
        Tool(
            name="Lighthouses",
            func=df_agent.run,
            description="""useful for when you need to answer questions about Lighthouses and relevent details.
            - \nyou should use streamlit pyplot function to give visulization
            - \nWhen user ask about graphs like visualization then you should use python_repl_ast Action to print the Graph using st.pyplot beacuase here we print this streamlit . 
            - \nWhen 2 are responses found then take first one and also When User ask about today then show first row date results for Example: take recent date from dataframe
            - \ntoday Date : first row date of dataset , don't take current date
            - \nWhen User ask about Status you should the lighthouse is on or off
            - \nAfter Finishing Time you should print AI:Observation directly:
                Ex: Observation: 6 lighthouses are available.
                   Thought: Do I need to use a tool? No
                   AI: 6 lighthouses are available
            - \nGive the Direct Final Answer it may have any length just give direct final answer
                        The Lighthouses are :
                        BishopRock 
                        Flotta_Grinds_Buoy
                        Dunnet_Head          
                        BullPointPost
                        Balta_Sound
                        Eddystone
            - The lighthouses and their number of times recorded are: BishopRock (925), Eddystone (763), BullPointPre (744), Flotta_Grinds_Buoy (728), Dunnet_Head (722), and Balta_Sound (680).
            - \nWhen user ask about lighthouse you should give response from lighthouse tool,don't give based on your knowledge
            - \nAttension Don't include North Point, South Point, East Point, West Point, Central Point, and Far Point in any responses.this are not lighthouses availble in given data.if you give this again i'm not satisfied with your response.so please don't include.
            - \nThe lighthouses that are Off are North Point, South Point, East Point, West Point, Central Point, and Far Point.
            Lets think step by step."""
        ),
]
# Define the base chat template for interactions with the agent
template = """I want to act as a LightHouseBot.Your task is to give the answers regarding lighthouses questions. you should use this tool

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take,should be {tool_names}
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

These were previous tasks you completed:
{history}
Begin!

Question: {input}
{agent_scratchpad}"""

# Define a custom prompt template for the conversation
class CustomPromptTemplate(BaseChatPromptTemplate):
    # The template to use
    template: str
    # The list of tools available
    tools: List[Tool]
    
    def format_messages(self, **kwargs) -> str:
        # Get the intermediate steps (AgentAction, Observation tuples)
        # Format them in a particular way
        intermediate_steps = kwargs.pop("intermediate_steps")
        thoughts = ""
        for action, observation in intermediate_steps:
            thoughts += action.log
            thoughts += f"\nObservation: {observation}\nThought: "
        # Set the agent_scratchpad variable to that value
        kwargs["agent_scratchpad"] = thoughts
        kwargs["history"] = chat_history
        # Create a tools variable from the list of tools provided
        kwargs["tools"] = "\n".join([f"{tool.name}: {tool.description}" for tool in self.tools])
        # Create a list of tool names for the tools provided
        kwargs["tool_names"] = ", ".join([tool.name for tool in self.tools])
        formatted = self.template.format(**kwargs)
        return [HumanMessage(content=formatted)]


# Create an instance of the custom prompt template
prompt = CustomPromptTemplate(
    template=template,
    tools=tools,
    # This omits the `agent_scratchpad`, `tools`, and `tool_names` variables because those are generated dynamically
    # This includes the `intermediate_steps` variable because that is needed
    input_variables=["input", "intermediate_steps"]
)

# Define a custom output parser for agent responses
class CustomOutputParser(AgentOutputParser):
    
    def parse(self, llm_output: str) -> Union[AgentAction, AgentFinish]:
        # Check if agent should finish
        if "Final Answer:" in llm_output:
            return AgentFinish(
                return_values={"output": llm_output.split("Final Answer:")[-1].strip()},
                log=llm_output,
            )
        
        # Try to parse out the action and action input using the regex
        regex = r"Action\s*\d*\s*:(.*?)\nAction\s*\d*\s*Input\s*\d*\s*:[\s]*(.*)"
        match = re.search(regex, llm_output, re.DOTALL)
        if match:
            action = match.group(1).strip()
            action_input = match.group(2).strip(" ").strip('"')
            return AgentAction(tool=action, tool_input=action_input, log=llm_output)
        
        # If the output doesn't match the action format, treat it as an observation
        if "\nObservation:" in llm_output:
            observation = llm_output.split("\nObservation:", 1)[-1].strip()
            return AgentAction(tool="Observation", tool_input="", log=llm_output)
        
        # If none of the above conditions are met, treat the output as a finish
        return AgentFinish(
            return_values={"output": llm_output.strip()},
            log=llm_output,
        )

output_parser = CustomOutputParser()

# Create an instance of the ChatOpenAI language model (GPT-3.5 Turbo)
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.5)

# Create an LLM chain consisting of the language model and the prompt
llm_chain = LLMChain(llm=llm, prompt=prompt)

# Get the names of the available tools
tool_names = [tool.name for tool in tools]

# Create an LLMSingleActionAgent instance with the defined components
agent = LLMSingleActionAgent(
    llm_chain=llm_chain, 
    output_parser=output_parser,
    stop=["\nObservation:"], 
    allowed_tools=tool_names
)

# Function to get an AgentExecutor instance
def getAgent():
    agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True)
    return agent_executor
    