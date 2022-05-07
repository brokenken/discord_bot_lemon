import json
import discord
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option
from config import settings


class VoiceTracker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        with open('.\\databases\\voice_cnt.json', 'r') as file:
            voice_data = json.load(file)
            new_user = str(member.id)

        if new_user in voice_data:
            voice_data[new_user] += 1
            with open('.\\databases\\voice_cnt.json', 'w') as update_user_data:
                json.dump(voice_data, update_user_data, indent=4)
        else:
            voice_data[new_user] = 1
            with open('.\\databases\\voice_cnt.json', 'w') as new_user_data:
                json.dump(voice_data, new_user_data, indent=4)




def setup(bot):
    bot.add_cog(VoiceTracker(bot))
