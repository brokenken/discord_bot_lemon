import discord
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option
from config import settings
import json
from random import randint
import asyncio


class Entertainment(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def conv_sm(self, n):
        es = ['а', 'ы', '']
        n = n % 100
        if n >= 11 and n <= 19:
            s = es[2]
        else:
            i = n % 10
            if i == 1:
                s = es[0]
            elif i in [2, 3, 4]:
                s = es[1]
            else:
                s = es[2]
        return s

    def conv_h(self, n):
        es = ['', 'а', 'ов']
        n = n % 100
        if n >= 11 and n <= 19:
            s = es[2]
        else:
            i = n % 10
            if i == 1:
                s = es[0]
            elif i in [2, 3, 4]:
                s = es[1]
            else:
                s = es[2]
        return s

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
        embed = discord.Embed(title="Аватар", description='Аватар пользователя <@{}>'.format(member.id), color=0x7af0d9)
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
    async def profile(self, ctx, member=None):
        if member is None:
            member = ctx.author
        with open('.\\databases\\user_data.json', 'r') as file:
            user_data = json.load(file)
            new_user = str(member.id)
        cnt = 0
        for user in user_data:
            if user == new_user:
                cnt = user_data[new_user][0]
        embed = discord.Embed(tittle='Профиль', description='Профиль <@{}>'.format(member.id), color=0x7af0d9)
        h = (cnt // 60) // 60
        m = cnt // 60
        s = cnt - (h * 60 * 60 + m * 60)
        if h == 0:
            if m == 0:
                embed.add_field(name='Время в войсе', value='`{} секунд{}`'.format(s, self.conv_sm(s)), inline=False)
            else:
                embed.add_field(name='Время в войсе', value='`{} минут{} {} секунд{}`'.format(m, self.conv_sm(m), s, self.conv_sm(s)), inline=False)
        else:
            embed.add_field(name='Время в войсе', value='`{} час{} {} минут{} {} секунд{}'.format(h, self.conv_h(h), m, self.conv_sm(m), s, self.conv_sm(s)), inline=False)
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
            embed = discord.Embed(title="```Недостаточно средств```", color=0xd71414)
            embed.set_thumbnail(url='https://media.giphy.com/media/ZGH8VtTZMmnwzsYYMf/giphy.gif')
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="```Казино```", color=0x7af0d9)
            embed.set_image(url='https://media.giphy.com/media/26uf2YTgF5upXUTm0/giphy.gif')
            msg = await ctx.send(embed=embed)
            user_data[new_user][2] -= count
            with open('.\\databases\\user_data.json', 'w') as update_user_data:
                json.dump(user_data, update_user_data, indent=4)
            await asyncio.sleep(2)

            def checkmsg(message):
                return message.id == msg.id

            await ctx.channel.purge(check=checkmsg)
            x = randint(1, 100)
            if x == 100:
                user_data[new_user][2] += count * 10
                embed = discord.Embed(title="WINNER WINNER CHIKEN DINNER!!!", color=0x06cb13)
                embed.set_thumbnail(url='https://media.giphy.com/media/PhdC5X5qr6mzK/giphy.gif')
                embed.description = "Выпало {}, <@{}> получает {} :coin:, поздравим!!!".format(x, ctx.author.id, count * 10)
                await ctx.send(embed=embed)
            else:
                if x >= 95:
                    user_data[new_user][2] += count * 5
                    embed = discord.Embed(title="Win x5", color=0xe4e70d)
                    embed.set_thumbnail(url='https://media.giphy.com/media/Yl9bVWbTSOR1947QEn/giphy.gif')
                    embed.description = "Выпало {}, <@{}> получает {} :coin:, поздравим!!!".format(x, ctx.author.id, count * 5)
                    await ctx.send(embed=embed)
                else:
                    if x > 80:
                        user_data[new_user][2] += count * 2
                        embed = discord.Embed(title="Win x2", color=0x294fc2)
                        embed.set_thumbnail(url='https://media.giphy.com/media/1DEJwfwdknKZq/giphy.gif')
                        embed.description = "Выпало {}, <@{}> получает {} :coin:, поздравим!!!".format(x, ctx.author.id,  count * 2)
                        await ctx.send(embed=embed)
                    else:
                        embed = discord.Embed(title="Казино...", color=0xd81818)
                        embed.set_thumbnail(url='https://media.giphy.com/media/26uf9REqpyY10QBd6/giphy.gif')
                        embed.description = "Выпало {}, <@{}> проиграл {} :coin:, жаль..".format(x, ctx.author.id,  count)
                        await ctx.send(embed=embed)
            with open('.\\databases\\user_data.json', 'w') as update_user_data:
                json.dump(user_data, update_user_data, indent=4)

    @cog_ext.cog_slash(
        name='transfer',
        description='give money to someone',
        options=[
            create_option(name="user", description="who?", required=True, option_type=6),
            create_option(name="count", description="how many?", required=True, option_type=4)
        ],
        guild_ids=settings['guild_ids']
    )
    @commands.command()
    async def transfer(self, ctx, user, count):
        member = ctx.author
        with open('.\\databases\\user_data.json', 'r') as file:
            user_data = json.load(file)
            new_user = str(member.id)
        if count > user_data[new_user][2]:
            embed = discord.Embed(title="```Недостаточно средств```", color=0xd71414)
            embed.set_thumbnail(url='https://media.giphy.com/media/ZGH8VtTZMmnwzsYYMf/giphy.gif')
            await ctx.send(embed=embed)
            return
        user_data[new_user][2] -= count
        user_data[str(user.id)][2] += count
        with open('.\\databases\\user_data.json', 'w') as update_user_data:
            json.dump(user_data, update_user_data, indent=4)
        embed = discord.Embed(title="```Передача денег```", color=0x7af0d9)
        embed.description = "<@{}> передал <@{}> {} :coin:".format(member.id, user.id, count)
        embed.set_image(url='https://media.giphy.com/media/dZdadd8KqjgsJGjMVp/giphy.gif')
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Entertainment(bot))
