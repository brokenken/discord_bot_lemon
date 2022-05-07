import discord
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option
from config import settings


class Moderator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
        name='avatar',
        description='shows user avatar',
        options=[
            create_option(
                name="user",
                description="select user",
                required=True,
                option_type=9
            )
        ],
        guild_ids=settings['guild_ids']
    )
    @commands.command()
    async def avatar(self, ctx, user):
        member = await self.bot.fetch_user(int(user))
        embed = discord.Embed(title="Avatar", description='<@{}> avatar'.format(member.id), color=0x752386)
        embed.set_author(name='{}'.format(ctx.author), icon_url=ctx.author.avatar_url)
        embed.set_image(url=member.avatar_url)
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(
        name='clear',
        description='how many messages from the end to delete?',
        options=[
            create_option(
                name="quantity",
                description="type a integer",
                required=True,
                option_type=4
            )
        ],
        guild_ids=settings['guild_ids']
    )
    @commands.command()
    async def clear(self, ctx, quantity: int):
        deleted = await ctx.channel.purge(limit=quantity)
        await ctx.send('Deleted {} messages'.format(len(deleted)))
        await ctx.channel.purge(limit=1)

    @cog_ext.cog_slash(
        name='clearFromUser',
        description='delete all messages from user',
        options=[
            create_option(
                name="user",
                description="select user",
                required=True,
                option_type=9
            )
        ],
        guild_ids=settings['guild_ids']
    )
    @commands.command()
    async def clearFromUser(self, ctx, user):
        def checkUser(message):
            return message.author.id == int(user)
        deleted = await ctx.channel.purge(check=checkUser)
        await ctx.send('Deleted {} messages'.format(len(deleted)))
        await ctx.channel.purge(limit=1)


def setup(bot):
    bot.add_cog(Moderator(bot))
