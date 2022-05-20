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
        name='clear',
        description='how many messages from the end to delete?',
        options=[
            create_option( name="quantity", description="type a integer", required=True, option_type=4)
        ],
        guild_ids=settings['guild_ids']
    )
    @commands.command()
    async def clear(self, ctx, quantity: int):
        if not self.check_moder(ctx.author):
            embed = discord.Embed(title="Для этой команды вам нужна одна из этих ролей:")
            embed.description = ""
            for role in settings['moderation_role']:
                embed.description += " <@&{}> ".format(int(role))
            await ctx.send(embed=embed)
            return
        deleted = await ctx.channel.purge(limit=quantity)
        await ctx.send('Удалено {} сообщений'.format(len(deleted)))
        await ctx.channel.purge(limit=1)

    @cog_ext.cog_slash(
        name='clearfromuser',
        description='delete all messages from user',
        options=[
            create_option(name="user", description="select user", required=True, option_type=6)
        ],
        guild_ids=settings['guild_ids']
    )
    @commands.command()
    async def clearfromuser(self, ctx, user):
        if not self.check_moder(ctx.author):
            embed = discord.Embed(title="Для этой команды вам нужна одна из этих ролей:")
            embed.description = ""
            for role in settings['moderation_role']:
                embed.description += " <@&{}> ".format(int(role))
            await ctx.send(embed=embed)
            return

        def checkUser(message):
            return message.author.id == int(user)

        deleted = await ctx.channel.purge(check=checkUser)
        await ctx.send('Удалено {} сообщений от <@{}>'.format(len(deleted), user.id))
        await ctx.channel.purge(limit=1)

    async def auto_uncmute(self, ctx, member):
        role = discord.utils.get(ctx.guild.roles, id=settings['chat_mute_role_id'])
        await member.remove_roles(role)
        channel = self.bot.get_channel(settings['channel_logs_id'])
        embed = discord.Embed(title="Logs - auto uncmute", color=0x04ff00)
        embed.add_field(name="Снятие чат мута", value="Чат мут снят с пользователя <@{}>".format(member.id), inline=False)
        embed.set_thumbnail(url=member.avatar_url)
        await channel.send(embed=embed)

    async def auto_unvmute(self, ctx, member):
        role = discord.utils.get(ctx.guild.roles, id=settings['voice_mute_role_id'])
        await member.remove_roles(role)
        channel = self.bot.get_channel(settings['channel_logs_id'])
        embed = discord.Embed(title="Logs - auto unvmute", color=0x04ff00)
        embed.add_field(name="Снятие войс мута", value="Войс мут снят с пользователя <@{}>".format(member.id), inline=False)
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
            embed = discord.Embed(title="Для этой команды вам нужна одна из этих ролей:")
            embed.description = ""
            for role in settings['moderation_role']:
                embed.description += " <@&{}> ".format(int(role))
            await ctx.send(embed=embed)
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
        await ctx.send('<@{}> получил чат мут'.format(member.id))
        channel = self.bot.get_channel(settings['channel_logs_id'])
        embed = discord.Embed(title="Logs - cmute", description="<@{}> выдал чат мут пользователю <@{}>\n for {} {}\n **Причина:** `{}`".format(ctx.author.id, member.id, a, b, reason), color=0xff0000)
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name="Модератор", value="<@{}>".format(ctx.author.id, inline=True))
        embed.add_field(name="Нарушитель", value="<@{}>".format(member.id, inline=True))
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
            embed = discord.Embed(title="Для этой команды вам нужна одна из этих ролей:")
            embed.description = ""
            for role in settings['moderation_role']:
                embed.description += " <@&{}> ".format(int(role))
            await ctx.send(embed=embed)
            return
        role = discord.utils.get(ctx.guild.roles, id=settings['chat_mute_role_id'])
        await member.remove_roles(role)
        await ctx.send('<@{}> был снят чат мут'.format(member.id))
        channel = self.bot.get_channel(settings['channel_logs_id'])
        embed = discord.Embed(title="Logs - uncmute", color=0x04ff00)
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name="Снятие чат мута", value="<@{}> снял чат мут с <@{}>".format(ctx.author.id, member.id), inline=False)
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
            embed = discord.Embed(title="Для этой команды вам нужна одна из этих ролей:")
            embed.description = ""
            for role in settings['moderation_role']:
                embed.description += " <@&{}> ".format(int(role))
            await ctx.send(embed=embed)
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
        await ctx.send('<@{}> получил войс мут'.format(member.id))
        channel = self.bot.get_channel(settings['channel_logs_id'])
        embed = discord.Embed(title="Logs - vmute", description="<@{}> выдал чат мут пользователю <@{}>\n for {} {}\n **Причина:** `{}`".format(ctx.author.id, member.id, a, b, reason), color=0xff0000)
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name="Модератор", value="<@{}>".format(ctx.author.id, inline=True))
        embed.add_field(name="Нарушитель", value="<@{}>".format(member.id, inline=True))
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
            embed = discord.Embed(title="Для этой команды вам нужна одна из этих ролей:")
            embed.description = ""
            for role in settings['moderation_role']:
                embed.description += " <@&{}> ".format(int(role))
            await ctx.send(embed=embed)
            return
        role = discord.utils.get(ctx.guild.roles, id=settings['voice_mute_role_id'])
        await member.remove_roles(role)
        await ctx.send('с пользователя <@{}> был снят войс мут'.format(member.id))
        channel = self.bot.get_channel(settings['channel_logs_id'])
        embed = discord.Embed(title="Logs - unvmute", color=0x04ff00)
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name="Снятие войс мута", value="<@{}> снял войс мут с пользователя <@{}>".format(ctx.author.id, member.id), inline=False)
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
            embed = discord.Embed(title="Для этой команды вам нужна одна из этих ролей:")
            embed.description = ""
            for role in settings['moderation_role']:
                embed.description += " <@&{}> ".format(int(role))
            await ctx.send(embed=embed)
            return
        if reason is None:
            reason = "No reason"
        await member.ban(reason=reason)
        await ctx.send('<@{}> забанен'.format(member.id))
        channel = self.bot.get_channel(settings['channel_logs_id'])
        embed = discord.Embed(title="Logs - ban", description="<@{}> выдал бан пользователю <@{}>\n  **Причина:** `{}`".format(ctx.author.id, member.id, reason), color=0x000000)
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name="Модератор", value="<@{}>".format(ctx.author.id, inline=True))
        embed.add_field(name="Нарушитель", value="<@{}>".format(member.id, inline=True))
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
            embed = discord.Embed(title="Для этой команды вам нужна одна из этих ролей:")
            embed.description = ""
            for role in settings['moderation_role']:
                embed.description += " <@&{}> ".format(int(role))
            await ctx.send(embed=embed)
            return
        banned_users = await ctx.guild.bans()
        for banned in banned_users:
            if banned.user.id == member:
                await ctx.guild.unban(banned.user)
                break
        await ctx.send('<@{}> разбанен'.format(member))
        channel = self.bot.get_channel(settings['channel_logs_id'])
        embed = discord.Embed(title="Logs - unban", color=0x04ff00)
        embed.add_field(name="Unban", value="<@{}> снял бан с <@{}>".format(ctx.author.id, member), inline=False)
        await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Moderator(bot))
