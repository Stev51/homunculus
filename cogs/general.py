import discord, enum
from discord.ext import commands
from discord import app_commands

class ModuleName(str, enum.Enum):
	General = "general"
	Temp = "temporary placeholder"

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
				["ping", "Test bot latency."],
				["cringe", "Sends the cringe copypasta (w/ optional user tag)."],
				["feedback", "Meant for worldbuilding servers. The bot sends a message with a reaction, letting anyone react to let you know they saw your post."],
				["diceavg", "Calculates the average value of dice rolls. Input as \"NdN+NdN+...\" ex. \"1d10+2d8\" \"8d6\" etc. Can separate multiple calculations with a space."]
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
	
	@app_commands.command(name="cringe", description="Sends the cringe copypasta (w/ optional user tag).")
	@app_commands.describe(user="User to ping.")
	async def cringe(self, interaction: discord.Interaction, user: discord.User|None):
		
		text = "You contribute nothing to this server, your humor is obnoxious and a waste of my time, and your superiority complex is obnoxious at best and insulting at best. You are cringe. Goodbye."
		
		if user != None:
			text = f"{user.mention} " + text
		
		await interaction.response.send_message(text)
	
	@app_commands.command(name="feedback", description="The bot sends a message with a reaction, letting anyone react to let you know they saw your post.")
	@app_commands.describe(emoji="The emoji which the bot adds as a reaction to its message. Defaults to 👋")
	async def feedback(self, interaction: discord.Interaction, emoji: str|None):
		
		fallback_emoji = "👋"
		
		if emoji == None:
			emoji = fallback_emoji
		
		embed = discord.Embed(color=discord.Color.gold(), description="React to this message if you don't wish to give feedback but want to let this person know you've read their post! ^^^")
		await interaction.response.send_message(embed=embed)
		
		selfmsg = await interaction.original_response()
		
		try:
			await selfmsg.add_reaction(emoji)
		except:
			await selfmsg.add_reaction(fallback_emoji)
	
	@app_commands.command(name="diceavg", description="Calculates the average value of dice rolls.")
	@app_commands.describe(text="Input as \"NdN+NdN+...\" ex. \"1d10+2d8\" \"8d6\" etc. Can separate multiple calculations with a space.")
	async def cringe(self, interaction: discord.Interaction, text: str):
		
		title = ""
		buf = ""
		embed = discord.Embed(color=discord.Color.gold())
		arr0 = text.strip().split(" ")
		
		if len(arr0) <= 0:
			
			embed.title = "No valid dice values found in input"
			embed.color = discord.Color.brand_red()
			
		else:
			
			for x in range(len(arr0)):
				
				title = f"Average #{str(x+1)}"
				buf = f"Input: {arr0[x]}\n"
			
				arr1 = arr0[x].split("+")
				if len(arr1) <= 0:
					
					buf += "No valid dice values found in input\n"
					embed.color = discord.Color.brand_red()
					
				else:
					
					arr2 = []
					for i in arr1:
						
						if i.isdigit():
							
							arr2.append([-1, int(i)])
						
						else:
						
							temp = i.split("d")
							
							if len(temp) == 2:
								
								if temp[0].isdigit() and temp[1].isdigit():
									
									arr2.append(temp)
								
								else:
									
									buf += f"Invalid input \"{i}\" ignored\n"
									embed.color = discord.Color.brand_red()
								
							else:
								
								buf += f"Invalid input \"{i}\" ignored\n"
								embed.color = discord.Color.brand_red()
					
					if len(arr2) <= 0:
						
						buf += "No valid dice values found in input\n"
						embed.color = discord.Color.brand_red()
						
					else:
						
						total = 0
						
						for i in arr2:
							
							count = int(i[0])
							value = int(i[1])
							
							if count >= 0:
							
								avg = (value + 1) / 2
								total += avg * count
							
							else:
								
								total += float(value)
							
						buf += f"Average: **{str(total)}**"
				
				embed.add_field(name=title, value=buf, inline=False)
		
		await interaction.response.send_message(embed=embed)
