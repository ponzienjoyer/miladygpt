# MiladyGPT

A minimalist discord bot built using gpt-3.5-turbo and langchain. 

You'll need to [setup a Discord bot](https://discordpy.readthedocs.io/en/stable/discord.html) and get an API key from [OpenAI](https://platform.openai.com/) to get started. You can put them in a .env file in the root directory of the project for local development/utilization or use environment variables in production.

## Getting Started

### Local

```bash
pip install -r requirements.txt
python bot.py
```

### Docker

```bash
docker build -t miladygpt .
docker run -d miladygpt --env-file .env
```

## Usage

To get a response from the bot, simply mention it in a channel and it will respond with a generated response. There are also some additional commands to let you tweak the bot's behavior at runtime:

- `$show_prompt`: Show the current prefix prompt used by the chatbot
- `$update_prompt <prompt>`: Set the prefix prompt used byt the chatbot
- `$reset_prompt`: Reset the prefix prompt to the default specified in `bot.py`
- `$show_temperature`: Show the current temperature configured for the chatbot
- `$update_temperature <temperature>`: Set the temperature used by the chatbot
- `$reset_temperature`: Reset the temperature to the default specified in `bot.py`

### Limitations

Right now it doesn't seem that the ConversationalBufferMemory features in langchain aren't playing nicely with the way chat completion works in gpt-3.5-turbo. This means the bot currently has no memory; will fix once langchain is updated.