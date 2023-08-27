import os
import discord
from discord.ext import commands

token = os.getenv('DISCORD_BOT_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=".", intents=intents)
# prefix can't be '/' which is default

@bot.command()
@commands.has_permissions(administrator=True)
async def synccommands(ctx):
    # At most 200 times per day
    await bot.tree.sync()
    await ctx.send("Sync finished")

@bot.hybrid_command()
async def ping(ctx):
    '''Test YingBot is online or not'''
    await ctx.send("pong")


@bot.hybrid_command()
async def add(ctx, a: int, b: int):
    '''Add two numbers'''
    await ctx.send(a+b)

@bot.hybrid_command()
async def play(ctx):
    '''Rock-Paper-Scissors game'''
    await ctx.send("Choose: ", view=PlayView())

class PlayView(discord.ui.View):
    def get_content(self, label):
        counter = {
            "Scissors": "Rock",
            "Rock": "Paper",
            "Paper": "Scissors"
        }
        return f"You: {label}, bot: {counter[label]}, you lose!"
    
    @discord.ui.button(label="Scissors", style=discord.ButtonStyle.green, emoji="✌")
    async def scissors(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content=self.get_content(button.label))

    @discord.ui.button(label="Rock", style=discord.ButtonStyle.green, emoji="✊")
    async def rock(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content=self.get_content(button.label))

    @discord.ui.button(label="Paper", style=discord.ButtonStyle.green, emoji="✋")
    async def paper(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content=self.get_content(button.label))

    @discord.ui.button(label="Quit", style=discord.ButtonStyle.red)
    async def stop(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content="Why you quit :(", view=None)

bot.run(token)
