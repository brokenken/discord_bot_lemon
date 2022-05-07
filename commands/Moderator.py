import discord
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option
from config import settings
import asyncio


class Moderator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def check_moder(member):
        flag = False
        for role in member.roles:
            for moder_role in settings['moderation_role']:
                if role.id == moder_role:
                    flag = True
                    break
        return flag

    @cog_ext.cog_slash(
        name='avatar',
        description='shows user avatar',
        options=[
            create_option( name="user", description="select user", required=True, option_type=9)
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
            create_option( name="quantity", description="type a integer", required=True, option_type=4)
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
            create_option(name="user", description="select user", required=True, option_type=9)
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

    async def auto_uncmute(self, ctx, member):
        role = discord.utils.get(ctx.guild.roles, id=settings['chat_mute_role_id'])
        await member.remove_roles(role)
        channel = self.bot.get_channel(settings['channel_logs_id'])
        embed = discord.Embed(title="Logs - auto uncmute", color=0x04ff00)
        embed.add_field(name="Chat unmute", value="removed chat mute from <@{}>".format(member.id), inline=False)
        embed.set_thumbnail(url=member.avatar_url)
        await channel.send(embed=embed)

    async def auto_unvmute(self, ctx, member):
        role = discord.utils.get(ctx.guild.roles, id=settings['voice_mute_role_id'])
        await member.remove_roles(role)
        channel = self.bot.get_channel(settings['channel_logs_id'])
        embed = discord.Embed(title="Logs - auto unvmute", color=0x04ff00)
        embed.add_field(name="Voice unmute", value="removed voice mute from <@{}>".format(member.id), inline=False)
        embed.set_thumbnail(url=member.avatar_url)
        await channel.send(embed=embed)

    @cog_ext.cog_slash(
        name='cmute',
        description='give chat mute to user',
        options=[
            create_option(name="member", description="user tag or id", option_type=6, required=True),
            create_option(name="time", description="time for mute", option_type=3, required=True),
            create_option(name="reason", description="reason of mute", option_type=3, required=False)
        ],
        guild_ids=settings['guild_ids']
    )
    @commands.command()
    async def cmute(self, ctx, member, time, reason=None):
        if not self.check_moder(ctx.author):
            return
        a = str()
        b = str()
        if reason is None:
            reason = "No reason"
        for i in time:
            if i == 's' or i == 'm' or i == 'h' or i == 'd':
                b += i
            else:
                a += i
        a = int(a)
        role = discord.utils.get(ctx.guild.roles, id=settings['chat_mute_role_id'])
        await member.add_roles(role)
        await ctx.send('<@{}> was given chat mute'.format(member.id))
        channel = self.bot.get_channel(settings['channel_logs_id'])
        embed = discord.Embed(title="Logs - cmute", description="<@{}> gave chat mute to <@{}>\n for {} {}\n **Reason:** `{}`".format(ctx.author.id, member.id, a, b, reason), color=0xff0000)
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name="Moderator", value="<@{}>".format(ctx.author.id, inline=True))
        embed.add_field(name="Intruder", value="<@{}>".format(member.id, inline=True))
        await channel.send(embed=embed)
        if b == 'm':
            a *= 60
        if b == 'h':
            a *= 60 * 60
        if b == 'd':
            a *= 60 * 60 * 60
        await asyncio.sleep(a)
        await self.auto_uncmute(ctx, member)

    @cog_ext.cog_slash(
        name='uncmute',
        description='remove chat mute from user',
        options=[
            create_option(name="member", description="user tag or id", option_type=6, required=True)
        ],
        guild_ids=settings['guild_ids']
    )
    @commands.command()
    async def uncmute(self, ctx, member):
        if not self.check_moder(ctx.author):
            return
        role = discord.utils.get(ctx.guild.roles, id=settings['chat_mute_role_id'])
        await member.remove_roles(role)
        await ctx.send('<@{}> was removed chat mute'.format(member.id))
        channel = self.bot.get_channel(settings['channel_logs_id'])
        embed = discord.Embed(title="Logs - uncmute", color=0x04ff00)
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name="Chat unmute", value="<@{}> removed chat mute from <@{}>".format(ctx.author.id, member.id), inline=False)
        await channel.send(embed=embed)

    @cog_ext.cog_slash(
        name='vmute',
        description='give voice mute to user',
        options=[
            create_option(name="member", description="user tag or id", option_type=6, required=True),
            create_option(name="time", description="time for mute", option_type=3, required=True),
            create_option(name="reason", description="reason of mute", option_type=3, required=False)
        ],
        guild_ids=settings['guild_ids']
    )
    @commands.command()
    async def vmute(self, ctx, member, time, reason=None):
        if not self.check_moder(ctx.author):
            return
        a = str()
        b = str()
        if reason is None:
            reason = "No reason"
        for i in time:
            if i == 's' or i == 'm' or i == 'h' or i == 'd':
                b += i
            else:
                a += i
        a = int(a)
        role = discord.utils.get(ctx.guild.roles, id=settings['voice_mute_role_id'])
        await member.add_roles(role)
        await ctx.send('<@{}> was given voice mute'.format(member.id))
        channel = self.bot.get_channel(settings['channel_logs_id'])
        embed = discord.Embed(title="Logs - vmute", description="<@{}> gave voice mute to <@{}>\n for {} {}\n **Reason:** `{}`".format(ctx.author.id, member.id, a, b, reason), color=0xff0000)
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name="Moderator", value="<@{}>".format(ctx.author.id, inline=True))
        embed.add_field(name="Intruder", value="<@{}>".format(member.id, inline=True))
        await channel.send(embed=embed)
        if b == 'm':
            a *= 60
        if b == 'h':
            a *= 60 * 60
        if b == 'd':
            a *= 60 * 60 * 60
        await asyncio.sleep(a)
        await self.auto_unvmute(ctx, member)

    @cog_ext.cog_slash(
        name='unvmute',
        description='remove voice mute from user',
        options=[
            create_option(name="member", description="user tag or id", option_type=6, required=True)
        ],
        guild_ids=settings['guild_ids']
    )
    @commands.command()
    async def unvmute(self, ctx, member):
        if not self.check_moder(ctx.author):
            return
        role = discord.utils.get(ctx.guild.roles, id=settings['voice_mute_role_id'])
        await member.remove_roles(role)
        await ctx.send('<@{}> was removed voice mute'.format(member.id))
        channel = self.bot.get_channel(settings['channel_logs_id'])
        embed = discord.Embed(title="Logs - unvmute", color=0x04ff00)
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name="Voice unmute", value="<@{}> removed voice mute from <@{}>".format(ctx.author.id, member.id), inline=False)
        await channel.send(embed=embed)

    @cog_ext.cog_slash(
        name='ban',
        description='ban user',
        options=[
            create_option(name="member", description="user tag or id", option_type=6, required=True),
            create_option(name="reason", description="reason of ban", option_type=3, required=False)
        ],
        guild_ids=settings['guild_ids']
    )
    @commands.command()
    async def ban(self, ctx, member, reason=None):
        if not self.check_moder(ctx.author):
            return
        if reason is None:
            reason = "No reason"

        await member.ban(reason=reason)
        await ctx.send('<@{}> banned'.format(member.id))
        channel = self.bot.get_channel(settings['channel_logs_id'])
        embed = discord.Embed(title="Logs - ban", description="<@{}> gave ban to <@{}>\n  **Reason:** `{}`".format(ctx.author.id, member.id, reason), color=0x000000)
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name="Moderator", value="<@{}>".format(ctx.author.id, inline=True))
        embed.add_field(name="Intruder", value="<@{}>".format(member.id, inline=True))
        await channel.send(embed=embed)

    @cog_ext.cog_slash(
        name='unban',
        description='unban user',
        options=[
            create_option(name="member", description="user tag or id", option_type=6, required=True)
        ],
        guild_ids=settings['guild_ids']
    )
    @commands.command()
    async def unban(self, ctx, member):
        if not self.check_moder(ctx.author):
            return
        banned_users = await ctx.guild.bans()
        for banned in banned_users:
            if banned.user.id == member:
                await ctx.guild.unban(banned.user)
                break
        await ctx.send('<@{}> unbanned'.format(member))
        channel = self.bot.get_channel(settings['channel_logs_id'])
        embed = discord.Embed(title="Logs - unban", color=0x04ff00)
        embed.add_field(name="Unban", value="<@{}> removed ban from <@{}>".format(ctx.author.id, member), inline=False)
        await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Moderator(bot))
