from random import randint
import discord
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option
from config import settings, gif


class Emotions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
        name='hug',
        description='hug someone',
        options=[
            create_option(name="member", description="user tag or id", option_type=6, required=True)
        ],
        guild_ids=settings['guild_ids']
    )
    @commands.command()
    async def hug(self, ctx, member):
        if member.id == ctx.author.id:
            embed = discord.Embed(title="Huge", description="<@{}> you can't hug yourself".format(ctx.author.id), color=0xea3434)
            embed.set_author(name='{}'.format(ctx.author), icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            return
        x = randint(1, len(gif['hug_gifs'])) - 1
        embed = discord.Embed(title="Huge", description='<@{}> hugged <@{}>'.format(ctx.author.id, member.id), color=0xffae00)
        embed.set_author(name='{}'.format(ctx.author), icon_url=ctx.author.avatar_url)
        embed.set_image(url=gif['hug_gifs'][x])
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(
        name='kiss',
        description='kiss someone',
        options=[
            create_option(name="member", description="user tag or id", option_type=6, required=True)
        ],
        guild_ids=settings['guild_ids']
    )
    @commands.command()
    async def kiss(self, ctx, member):
        if member.id == ctx.author.id:
            embed = discord.Embed(title="Kiss", description="<@{}> you can't kiss yourself".format(ctx.author.id), color=0xea3434)
            embed.set_author(name='{}'.format(ctx.author), icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            return
        x = randint(1, len(gif['kiss_gifs'])) - 1
        embed = discord.Embed(title="Kiss", description='<@{}> kissed <@{}>'.format(ctx.author.id, member.id), color=0xffae00)
        embed.set_author(name='{}'.format(ctx.author), icon_url=ctx.author.avatar_url)
        embed.set_image(url=gif['kiss_gifs'][x])
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(
        name='stroke',
        description='stroke someone',
        options=[
            create_option(name="member", description="user tag or id", option_type=6, required=True)
        ],
        guild_ids=settings['guild_ids']
    )
    @commands.command()
    async def stroke(self, ctx, member):
        if member.id == ctx.author.id:
            embed = discord.Embed(title="Stroke", description="<@{}> you can't stroke yourself".format(ctx.author.id), color=0xea3434)
            embed.set_author(name='{}'.format(ctx.author), icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            return
        x = randint(1, len(gif['stroke_gifs'])) - 1
        embed = discord.Embed(title="Stroke", description='<@{}> stroked <@{}>'.format(ctx.author.id, member.id), color=0xffae00)
        embed.set_author(name='{}'.format(ctx.author), icon_url=ctx.author.avatar_url)
        embed.set_image(url=gif['stroke_gifs'][x])
        await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(Emotions(bot))
