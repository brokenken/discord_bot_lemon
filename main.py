import logging
import os
import discord
from discord.ext import commands
from discord_slash import SlashCommand
from dotenv import load_dotenv
from config import settings


class MainBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Logged in as {self.bot.user} ({self.bot.user.id})')

    @commands.Cog.listener()
    async def on_resumed(self):
        print('Bot has reconnected!')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send('Invalid Command!')
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send('Bot Permission Missing!')


intents = discord.Intents.default()
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix=commands.when_mentioned_or(settings['prefix']),
                   description='Some useless bot.', intents=intents)
slash = SlashCommand(bot, sync_commands=True)

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

if __name__ == '__main__':
    for filename in os.listdir('./commands'):
        if filename.endswith('.py'):
            bot.load_extension(f'commands.{filename[: -3]}')

    bot.add_cog(MainBot(bot))
    load_dotenv()
    bot.run(os.getenv('TOKEN'), reconnect=True)
