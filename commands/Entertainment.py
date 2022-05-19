import discord
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option
from config import settings
from discord.ext import tasks
import json


class Entertainment(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_users.start()

    @cog_ext.cog_slash(
        name='avatar',
        description='shows user avatar',
        options=[
            create_option(name="member", description="select user", required=True, option_type=6)
        ],
        guild_ids=settings['guild_ids']
    )
    @commands.command()
    async def avatar(self, ctx, member):
        embed = discord.Embed(title="Аватар", description='Аватар пользователя <@{}>'.format(member.id), color=0x752386)
        embed.set_author(name='{}'.format(ctx.author), icon_url=ctx.author.avatar_url)
        embed.set_image(url=member.avatar_url)
        await ctx.send(embed=embed)

    @tasks.loop(seconds=5)
    async def check_users(self):
        for guild in self.bot.guilds:
            for member in guild.members:
                with open('.\\databases\\user_data.json', 'r') as file:
                    user_data = json.load(file)
                    new_user = str(member.id)
                if new_user not in user_data:
                    user_data[new_user] = 0
                    with open('.\\databases\\user_data.json', 'w') as new_user_data:
                        json.dump(user_data, new_user_data, indent=4)
                if member.voice is not None:
                    user_data[new_user] += 5
                    with open('.\\databases\\user_data.json', 'w') as update_user_data:
                        json.dump(user_data, update_user_data, indent=4)

    @check_users.before_loop
    async def before_my_task(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(Entertainment(bot))
