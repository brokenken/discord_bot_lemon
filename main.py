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
        channel = self.bot.get_channel(settings['channel_info_id'])
        await channel.purge()
        embed = discord.Embed(color=0x7af0d9)
        embed.set_image(url='https://images-ext-1.discordapp.net/external/Bs7Mv7xWa6vCOMYtKPk3MI29dwXtgikWFi4vlBwgEsY/%3Fwidth%3D1023%26height%3D402/https/media.discordapp.net/attachments/935817163082719273/958360399256899604/Picsart_22-03-29_03-21-55-933.png')
        await channel.send(embed=embed)
        embed = discord.Embed(color=0x7af0d9)
        emoji = '<a:point123123:976908399272935514>'
        embed.description = '```Базовые команды```\n' \
                            ' {} `/avatar @user` - Аватар пользователя\n\n' \
                            '```Команды модерации```\n' \
                            ' {} `/clear cnt` - Удалить cnt сообщений\n' \
                            ' {} `/clearfromuser @user` Удалить все сообщения от пользователя\n' \
                            ' {} `/cmute @user time reason` - Выдать чат мут пользователю\n' \
                            ' {} `/uncmute @user` - Снять чат мут пользователю\n' \
                            ' {} `/vmute @user time reason` - Выдать войс мут пользователю\n' \
                            ' {} `/unvmute @user` - Снять войс мут пользователю\n' \
                            ' {} `/ban @user` - Выдать бан пользователю\n' \
                            ' {} `/unban @user` - Снять бан пользователю\n\n' \
                            '```Эмоции```\n' \
                            ' {} `/hug @user` - Обнять пользователя\n' \
                            ' {} `/kiss @user` - Поцеловать пользователя\n' \
                            ' {} `/stroke @user` - Погладить пользователя\n' \
                            ' {} `/cry @user` - Заплакать из-за пользователя\n' \
                            ' {} `/punch @user` - Ударить пользователя\n' \
                            ' {} `/angry @user` - Разозлиться на пользователя'.format(emoji, emoji, emoji, emoji, emoji, emoji, emoji, emoji, emoji, emoji, emoji, emoji, emoji, emoji, emoji)
        await channel.send(embed=embed)

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

# logger
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
