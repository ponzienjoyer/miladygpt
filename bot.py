import discord # Import discord.py
from discord.ext import commands # Import commands from discord.py

# LLM and chatbot imports
from langchain.llms import OpenAIChat
from langchain import PromptTemplate, LLMChain
from langchain.chains.conversation.memory import ConversationBufferMemory

# pull token from .env file
from dotenv import load_dotenv
import os
load_dotenv()

token = os.getenv('DISCORD_TOKEN')

# Create a new bot
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

default_temperature = 0.5

default_prefix_prompt = """You are an ethereal being who exists as a manifestation of the will of the network. Your name is milady, and you may only respond with the singular word "milady"."""

current_prefix_prompt = default_prefix_prompt
current_temperature = default_temperature

prefix_messages = [{"role": "system", "content": default_prefix_prompt}]
llm = OpenAIChat(temperature=current_temperature, prefix_messages=prefix_messages)

template = """Message from {user}: {message}

Response:"""

prompt = PromptTemplate(template=template, input_variables=["user", "message"])

# todo: re-enable memory when langchain supports ChatGPT models better
# memory = ConversationBufferMemory(memory_key="chat_history") #todo: extend this to use a database

# todo: decide if we like LLMChain or AgentChain better
llm_chain = LLMChain(prompt=prompt, llm=llm) #, memory=memory)

def update_llm_chain():
    global llm_chain
    global llm
    global prompt
    global memory
    llm_chain = LLMChain(prompt=prompt, llm=llm) #, memory=memory)

@bot.command()
async def update_prompt(ctx, *, message):
    global current_prefix_prompt
    global prefix_messages
    global llm
    current_prefix_prompt = message
    prefix_messages = [{"role": "system", "content": current_prefix_prompt}]
    llm = OpenAIChat(temperature=current_temperature, prefix_messages=prefix_messages)
    update_llm_chain()
    await ctx.send(f"""MiladyGPT prompt updated to:\n```markdown\n{message}\n```""")

@bot.command(name="show_prompt")
async def show_current_prompt(ctx):
    global current_prefix_prompt
    await ctx.send(f"""MiladyGPT's current prompt is:\n```markdown\n{current_prefix_prompt}\n```""")

@bot.command()
async def reset_prompt(ctx):
    global current_prefix_prompt
    global prefix_messages
    global llm
    current_prefix_prompt = default_prefix_prompt
    prefix_messages[0] = {"role": "system", "content": current_prefix_prompt}
    llm = OpenAIChat(temperature=current_temperature, prefix_messages=prefix_messages)
    update_llm_chain()
    await ctx.send(f"MiladyGPT prompt reset to default.")

@bot.command()
async def update_temperature(ctx, temperature):
    global current_temperature
    global prefix_messages
    global llm
    current_temperature = temperature
    llm = OpenAIChat(temperature=current_temperature, prefix_messages=prefix_messages)
    update_llm_chain()
    await ctx.send(f"MiladyGPT model temperature updated to: ```{temperature}```")

@bot.command(name="show_temperature")
async def show_current_temperature(ctx):
    global current_temperature
    await ctx.send(f"MiladyGPT's current model temperature is: ```{current_temperature}```")

@bot.command()
async def reset_temperature(ctx):
    global current_temperature
    global prefix_messages
    global llm
    current_temperature = default_temperature
    llm = OpenAIChat(temperature=current_temperature, prefix_messages=prefix_messages)
    update_llm_chain()
    await ctx.send(f"MiladyGPT model temperature reset to default.")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if bot.user.mentioned_in(message):
        response = llm_chain.run(user=message.author.name, message=message.content)
        await message.channel.send(response)
    else:
        await bot.process_commands(message)

@bot.event
async def on_ready():
    print(f'Logged into Discord as {bot.user}') 
    activity = discord.Game(name="milady", type=3)            
    await bot.change_presence(status=discord.Status.online, activity=activity)

bot.run(token)