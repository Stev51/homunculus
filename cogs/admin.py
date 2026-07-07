import discord, enum
from discord.ext import commands
from discord import app_commands

admin_ids = [318403136589004800]
async def is_not_admin(interaction: discord.Interaction) -> bool:
	output = not interaction.user.id in admin_ids
	if output:
		await interaction.response.send_message("You're not allowed to use that command!", ephemeral=True)
	return output

async def setup(bot):
	await bot.add_cog(Admin(bot))

class Admin(commands.GroupCog, name="admin", description="Bot owner-only functions."):
	
	_sync = app_commands.Group(name="sync", description="Sync commands.")
	
	def __init__(self, bot):
		self.bot = bot
	
	async def cog_load(self):
		print("> Module loaded: Admin")
	
	@app_commands.command(name="check", description="Bot owner-only function.")
	async def admin_check(self, interaction: discord.Interaction):
		
		check = await is_not_admin(interaction)
		if check:
			return
		
		await interaction.response.send_message("Yes, you are an admin!", ephemeral=True)
	
	@_sync.command(name="private", description="Bot owner-only function.")
	async def admin_sync_private(self, interaction: discord.Interaction):
		
		check = await is_not_admin(interaction)
		if check:
			return
		
		private_guild = discord.Object(self.bot.Secrets["private_guild_id"])
		
		self.bot.tree.copy_global_to(guild=private_guild)
		synced = await self.bot.tree.sync(guild=private_guild)
		
		await interaction.response.send_message(f"Synced {len(synced)} commands!", ephemeral=True)
	
	@_sync.command(name="global", description="Bot owner-only function.")
	async def admin_sync_global(self, interaction: discord.Interaction):
		
		check = await is_not_admin(interaction)
		if check:
			return
		
		synced = await self.bot.tree.sync()
		
		await interaction.response.send_message(f"Synced {len(synced)} commands!", ephemeral=True)
