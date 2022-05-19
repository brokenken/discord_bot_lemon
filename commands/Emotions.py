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
            embed = discord.Embed(title="Объятие", description="<@{}> вы не можете обнять сами себ".format(ctx.author.id), color=0xea3434)
            embed.set_author(name='{}'.format(ctx.author), icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            return
        x = randint(1, len(gif['hug_gifs'])) - 1
        embed = discord.Embed(title="Объятие", description='<@{}> обнял <@{}>'.format(ctx.author.id, member.id), color=0xffae00)
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
            embed = discord.Embed(title="Поцелуй", description="<@{}> вы не можете поцеловать сами себя".format(ctx.author.id), color=0xea3434)
            embed.set_author(name='{}'.format(ctx.author), icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            return
        x = randint(1, len(gif['kiss_gifs'])) - 1
        embed = discord.Embed(title="Поцелуй", description='<@{}> поцеловал <@{}>'.format(ctx.author.id, member.id), color=0xffae00)
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
            embed = discord.Embed(title="Гладить", description="<@{}> вы не можете погладить сами себя".format(ctx.author.id), color=0xea3434)
            embed.set_author(name='{}'.format(ctx.author), icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            return
        x = randint(1, len(gif['stroke_gifs'])) - 1
        embed = discord.Embed(title="Гладить", description='<@{}> погладил <@{}>'.format(ctx.author.id, member.id), color=0xffae00)
        embed.set_author(name='{}'.format(ctx.author), icon_url=ctx.author.avatar_url)
        embed.set_image(url=gif['stroke_gifs'][x])
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(
        name='cry',
        description='cry because of someone',
        options=[
            create_option(name="member", description="user tag or id", option_type=6, required=True)
        ],
        guild_ids=settings['guild_ids']
    )
    @commands.command()
    async def cry(self, ctx, member):
        x = randint(1, len(gif['crying_gifs'])) - 1
        embed = discord.Embed(title="Плач", description='<@{}> заплакал из-за <@{}>'.format(ctx.author.id, member.id), color=0xffae00)
        embed.set_author(name='{}'.format(ctx.author), icon_url=ctx.author.avatar_url)
        embed.set_image(url=gif['crying_gifs'][x])
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(
        name='punch',
        description='punch someone',
        options=[
            create_option(name="member", description="user tag or id", option_type=6, required=True)
        ],
        guild_ids=settings['guild_ids']
    )
    @commands.command()
    async def punch(self, ctx, member):
        x = randint(1, len(gif['punch_gifs'])) - 1
        embed = discord.Embed(title="Удар", description='<@{}> ударил <@{}>'.format(ctx.author.id, member.id), color=0xffae00)
        embed.set_author(name='{}'.format(ctx.author), icon_url=ctx.author.avatar_url)
        embed.set_image(url=gif['punch_gifs'][x])
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(
        name='angry',
        description='being angry',
        options=[
            create_option(name="member", description="user tag or id", option_type=6, required=True)
        ],
        guild_ids=settings['guild_ids']
    )
    @commands.command()
    async def angry(self, ctx, member):
        x = randint(1, len(gif['punch_gifs'])) - 1
        embed = discord.Embed(title="Злость", description='<@{}> злится на <@{}>'.format(ctx.author.id, member.id), color=0xffae00)
        embed.set_author(name='{}'.format(ctx.author), icon_url=ctx.author.avatar_url)
        embed.set_image(url=gif['angry_gifs'][x])
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Emotions(bot))
