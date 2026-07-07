import discord, enum
from discord.ext import commands
from discord import app_commands

class ModuleName(str, enum.Enum):
	General = "general"
	Temp = "temporary_placeholder"

async def setup(bot):
	await bot.add_cog(General(bot))

class General(commands.Cog):
	
	def __init__(self, bot):
		self.bot = bot
	
	async def cog_load(self):
		print("> Module loaded: General")
	
	@app_commands.command(name="help", description="Get a list of commands in a specific module.")
	@app_commands.describe(module="The module to list commands for.")
	async def help(self, interaction: discord.Interaction, module: ModuleName):
		
		module = module.strip().lower()
		embed = discord.Embed()
		
		module_texts = {
			"general": [
				["help", "Get a list of commands in a specific module."],
				["ping", "Test bot latency."]
			]
		}
		
		if module in module_texts:
			
			embed.color = discord.Color.gold()
			embed.title = module.title()
			
			for command in module_texts[module]:
				embed.add_field(name=command[0], value=command[1], inline=False)
			
		else:
			
			embed.color = discord.Color.brand_red()
			embed.title = f"Module name \"{module.title()}\" not found."
			
			desc_text = "**List of valid modules:**"
			
			for module_name in module_texts:
				desc_text += f"\n- {module_name.title()}"
			
			embed.description = desc_text
		
		await interaction.response.send_message(embed=embed, ephemeral=True)
	
	@app_commands.command(name="ping", description="Test bot latency.")
	async def ping(self, interaction: discord.Interaction):
		await interaction.response.send_message(f"Pong! {round(self.bot.latency * 1000)}ms", ephemeral=True)
