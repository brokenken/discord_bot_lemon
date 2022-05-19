import discord
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option
from config import settings
import json
from random import randint


class Entertainment(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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

    @cog_ext.cog_slash(
        name='profile',
        description='shows user profile',
        options=[
            create_option(name="member", description="select user", required=False, option_type=6)
        ],
        guild_ids=settings['guild_ids']
    )
    @commands.command()
    async def avatar(self, ctx, member=None):
        if member is None:
            member = ctx.author
        with open('.\\databases\\user_data.json', 'r') as file:
            user_data = json.load(file)
            new_user = str(member.id)
        cnt = 0
        for user in user_data:
            if user == new_user:
                cnt = user_data[new_user][0]
        embed = discord.Embed(tittle='Профиль', description='Профиль <@{}>'.format(member.id), color=0xec186d)
        h = (cnt // 60) // 60
        m = cnt // 60
        s = cnt - (h * 60 * 60 + m * 60)
        if h == 0:
            if m == 0:
                embed.add_field(name='Время в войсе', value='`{} секунд`'.format(s), inline=False)
            else:
                embed.add_field(name='Время в войсе', value='`{} минут {} секунд`'.format(m, s), inline=False)
        else:
            embed.add_field(name='Время в войсе', value='`{} часов {} минут {} секунд'.format(h, m, s), inline=False)
        embed.add_field(name='Количество сообщений', value='`{} сообщений`'.format(user_data[new_user][1]), inline=False)
        embed.add_field(name='Баланс', value='`{}` :coin:'.format(user_data[new_user][2]), inline=False)
        embed.set_thumbnail(url=member.avatar_url)
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(
        name='slot',
        description='casino',
        options=[
            create_option(name="count", description="pot", required=True, option_type=4)
        ],
        guild_ids=settings['guild_ids']
    )
    @commands.command()
    async def slot(self, ctx, count):
        member = ctx.author
        with open('.\\databases\\user_data.json', 'r') as file:
            user_data = json.load(file)
            new_user = str(member.id)
        if count > user_data[new_user][2]:
            await ctx.send("Мало на счёте")
        else:
            user_data[new_user][2] -= count
            x = randint(1, 100)
            if x >= 90:
                user_data[new_user][2] += count * 2
                await ctx.send("Победа!")
            else:
                await ctx.send("Казино....")
            with open('.\\databases\\user_data.json', 'w') as update_user_data:
                json.dump(user_data, update_user_data, indent=4)





def setup(bot):
    bot.add_cog(Entertainment(bot))
