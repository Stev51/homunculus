import discord, enum
from discord.ext import commands
from discord import app_commands

REACTORS = {
	408065042433703936: "<:tea_pog:779007351181017109>",			# tea1w4 - tea pog
	183945859057057792: "<:youjustgotamglid:702957492262404146>"	# Missalot - amgli
}

async def setup(bot):
	await bot.add_cog(AutoReact(bot))

class AutoReact(commands.Cog):
	
	def __init__(self, bot):
		self.bot = bot
	
	async def cog_load(self):
		print("> Module loaded: AutoReact")
	
	@commands.Cog.listener()
	async def on_message(self, message: discord.Message):
		
		if message.author.id in REACTORS:
			await message.add_reaction(REACTORS[message.author.id])
		
		if message.content.strip().lower().startswith("dab me up"):
			await message.add_reaction("<:dab1:946946889226526761>")
			await message.add_reaction("<:dab2:946946913364754432>")
