import discord, os, logging
from discord.ext import commands

print("> Beginning bot setup")

dirpath = os.path.dirname(os.path.realpath(__file__))
os.chdir(dirpath)

print(f"> Changed working directory to {os.getcwd()}")

from self_secrets import SECRETS

print("> Imported custom modules")

class HomunculusBot(commands.Bot):
	
	async def setup_hook(self):
		
		for file in os.listdir("cogs"):
			if file.endswith(".py") and not file.startswith("_"):
				await self.load_extension(f"cogs.{file[:-3]}")
	
	async def on_ready(self):
		print(f"> Bot started as {self.user}")

bot = HomunculusBot(command_prefix="/", intents=discord.Intents.all())

# !!! #
@bot.tree.command(name="sync")
async def sync(interaction: discord.Interaction):
	
	#synced = await bot.tree.sync()
	
	bot.tree.copy_global_to(guild=discord.Object(id="435549645574504450"))
	synced = await bot.tree.sync(guild=discord.Object(id="435549645574504450"))
	
	await interaction.response.send_message(f"Synced {len(synced)} commands!", ephemeral=True)
# !!! #

print("> Setup finished, calling client run")
bot.run(SECRETS['token'], log_level=logging.WARN)
