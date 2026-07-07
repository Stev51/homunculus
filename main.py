import discord, os, logging
from discord.ext import commands

print("> Beginning bot setup")

dirpath = os.path.dirname(os.path.realpath(__file__))
os.chdir(dirpath)

print(f"> Changed working directory to {os.getcwd()}")

from self_secrets import SECRETS

class HomunculusBot(commands.Bot):
	
	async def setup_hook(self):
		
		self.Secrets = SECRETS
		
		for file in os.listdir("cogs"):
			if file.endswith(".py") and not file.startswith("_"):
				await self.load_extension(f"cogs.{file[:-3]}")
	
	async def on_ready(self):
		print(f"> Bot started as {self.user}")

bot = HomunculusBot(
	command_prefix = "/",
	intents = discord.Intents.all(),
	activity = discord.Game(name="Version 2.0"),
	status = discord.Status.do_not_disturb
)

print("> Setup finished, calling client run")
bot.run(SECRETS["token"], log_level=logging.WARN)
