import discord
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option
from config import settings
from discord.ext import tasks
import json


class Background_tasks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_users.start()

    @tasks.loop(seconds=settings['time'])
    async def check_users(self):
        for guild in self.bot.guilds:
            for member in guild.members:
                with open('.\\databases\\user_data.json', 'r') as file:
                    user_data = json.load(file)
                    new_user = str(member.id)
                if new_user not in user_data:
                    user_data[new_user] = [0, 0, 0]
                    with open('.\\databases\\user_data.json', 'w') as new_user_data:
                        json.dump(user_data, new_user_data, indent=4)
                if member.voice is not None:
                    user_data[new_user][0] += settings['time']
                    user_data[new_user][2] += settings['money']
                    with open('.\\databases\\user_data.json', 'w') as update_user_data:
                        json.dump(user_data, update_user_data, indent=4)

    @check_users.before_loop
    async def before_my_task(self):
        await self.bot.wait_until_ready()

    @commands.Cog.listener()
    async def on_message(self, message):
        member = message.author
        with open('.\\databases\\user_data.json', 'r') as file:
            user_data = json.load(file)
            new_user = str(member.id)
        if new_user not in user_data:
            user_data[new_user] = [0, 0, 0]
            with open('.\\databases\\user_data.json', 'w') as new_user_data:
                json.dump(user_data, new_user_data, indent=4)
        user_data[new_user][1] += 1
        with open('.\\databases\\user_data.json', 'w') as update_user_data:
            json.dump(user_data, update_user_data, indent=4)


def setup(bot):
    bot.add_cog(Background_tasks(bot))
