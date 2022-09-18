import os

import discord
from discord.utils import get
from discord import app_commands, Interaction, TextStyle
from discord.ui import Modal, TextInput
from dotenv import load_dotenv

import constants.discord_ids as ids
from functions import command_functions

load_dotenv()


class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.all())
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
            self.synced = True
        print(f"We have logged in as {self.user}.")


class NewSotwModal(Modal):
    sotwname = TextInput(
        label="Enter the name for the Seed of the Week",
        style=TextStyle.short,
    )

    sotwsubmitter = TextInput(
        label="Who submitted this one?",
        style=TextStyle.short,
    )

    sotwseed = TextInput(
        label="What's the seed link?",
        style=TextStyle.short,
    )

    def __init__(self, title: str) -> None:
        super().__init__(title=title, timeout=None)

    async def on_submit(self, interaction: Interaction, /) -> None:
        await interaction.response.defer()


client = aclient()
tree = app_commands.CommandTree(client)

sotw_group = app_commands.Group(name='sotw', description="Seed of the Week Commands")


@client.event
async def on_message(message):
    try:
        sotw_channel = get(message.guild.channels, name='seed-of-the-week')
        if message.channel == sotw_channel:
            await message.author.send(f"The #{sotw_channel} channel only accepts the slash commands `/sotw done` or "
                                      f"`/sotw forfeit`.")
            await message.delete()
    except AttributeError:
        pass


@sotw_group.command(name="done", description="Enter your time for the Seed of the Week")
@app_commands.describe(time='Enter your time in 01:23:45 format')
async def sotw_done_command(interaction: Interaction, time: str):
    await command_functions.enter_time(interaction, time)


@sotw_group.command(name="forfeit", description="Be careful, you can't take it back!")
async def sotw_ff_command(interaction: Interaction):
    await command_functions.enter_time(interaction, "Forfeit")


@sotw_group.command(name="new", description="Create a new Seed of the Week")
async def sotw_new_command(interaction: Interaction):
    if "Racebot Admin" in str(interaction.user.roles):
        modal = NewSotwModal("Create a new Seed of the Week")
        await interaction.response.send_modal(modal)
        await modal.wait()
        await command_functions.create_new_sotw(interaction, str(modal.sotwname), str(modal.sotwsubmitter),
                                                str(modal.sotwseed))
        await interaction.followup.send(f"New SotW is live! Check it out @ #seed-of-the-week!")
    else:
        await interaction.response.send_message(f"Only Racebot Admins can use this command.", ephemeral=True)


@sotw_group.command(name="refresh", description="Refresh the current SotW data")
async def refresh_sotw(interaction: Interaction):
    if "Racebot Admin" in str(interaction.user.roles):
        await interaction.response.defer()
        await command_functions.refresh(interaction)
        await interaction.followup.send("Data has been refreshed!")
    else:
        await interaction.response.send_message(f"Only Racebot Admins can use this command.", ephemeral=True)


tree.add_command(sotw_group)

client.run(os.getenv('discord_token'))
