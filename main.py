import datetime
import json
import os

import discord
from discord import app_commands, Interaction, TextStyle
from discord.ext import tasks
from discord.ui import Modal, TextInput
from discord.utils import get

import db.constants as constants
import views as views
from functions import command_functions


class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.all())
        self.synced = False

    async def setup_hook(self) -> None:
        self.add_view(views.SotwPingView())

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync(guild=discord.Object(constants.guild))
            await tree.sync(guild=None)
            self.synced = True
        print(f"We have logged in as {self.user}.")
        if not check_time.is_running():
            await check_time.start()


class NewSotwModal(Modal):
    sotwname = TextInput(
        label="Enter the name for the Seed of the Week",
        style=TextStyle.short,
    )

    sotwdesc = TextInput(
        label="Enter a description for the seed",
        style=TextStyle.paragraph,
    )

    sotwsubmitter = TextInput(
        label="Who submitted this one?",
        style=TextStyle.short,
    )

    sotwflags = TextInput(
        label="Enter the flags",
        style=TextStyle.paragraph,
    )

    def __init__(self, title: str) -> None:
        super().__init__(title=title, timeout=None)

    async def on_submit(self, interaction: Interaction, /) -> None:
        await interaction.response.defer()


client = aclient()
tree = app_commands.CommandTree(client)

sotw_group = app_commands.Group(name="sotw", description="Seed of the Week Commands")


@client.event
async def on_message(message):
    try:
        sotw_channel = get(message.guild.channels, name="seed-of-the-week")
        if message.channel == sotw_channel:
            await message.author.send(
                f"The #{sotw_channel} channel only accepts the slash commands `/sotw done` or "
                f"`/sotw forfeit`."
            )
            await message.delete()
    except AttributeError:
        pass

    if message.content.startswith("!test"):
        if message.author.id == 197757429948219392:
            await command_functions.auto_create_new_sotw(client)
        else:
            await message.channel.send(
                "Sorry, only Jones can use the `!test` command. GET REKT DIRTBAG!"
            )


@sotw_group.command(name="done", description="Enter your time for the Seed of the Week")
@app_commands.describe(time="Enter your time in 01:23:45 format")
async def sotw_done_command(interaction: Interaction, time: str):
    await command_functions.enter_time(interaction, time)


@sotw_group.command(name="forfeit", description="Be careful, you can't take it back!")
async def sotw_ff_command(interaction: Interaction):
    await command_functions.enter_time(interaction, "Forfeit")


@sotw_group.command(
    name="submit", description="Get creative and submit your idea for SotW!"
)
async def sotw_new_submission(interaction: Interaction):
    await command_functions.new_submission(interaction)


@sotw_group.command(name="reserve", description="Add a new reserve flagset")
async def sotw_new_reserve(interaction: Interaction):
    await command_functions.new_reserve_choice(interaction)


@sotw_group.command(name="force", description="Force the bot to roll a new SotW")
async def sotw_force_new(interaction: Interaction):
    if "Racebot Admin" in str(interaction.user.roles):
        await interaction.response.send_message("Forcing a new SotW - stand by...", ephemeral=True)
        await command_functions.auto_create_new_sotw(client)
    else:
        await interaction.response.send_message(
            "Only Racebot Admins can use this command.", ephemeral=True
        )


@sotw_group.command(name="review", description="See a list of all submitted SotW ideas")
async def sotw_review(interaction: Interaction):
    await interaction.response.send_message(
        "<http://seedbot.net/sotw-submissions>", ephemeral=True
    )


@sotw_group.command(name="new", description="Create a new Seed of the Week")
async def sotw_new_command(interaction: Interaction):
    if not os.path.exists("settings.json"):
        with open("settings.json", "w") as newfile:
            newfile.write(json.dumps({}))
    with open("settings.json") as x:
        settings = json.load(x)
    if settings["auto-mode"] == "True":
        await interaction.response.send_message(
            "I am set to auto-roll right now. Please use the `/sotw auto` command to change that if you need to.",
            ephemeral=True,
        )
    else:
        role = get(interaction.guild.roles, name="SotW Ping")
        channel = get(interaction.guild.channels, name="seed-of-the-week")
        general_channel = get(interaction.guild.channels, name="ff6wc-general-chat")
        if "Racebot Admin" in str(interaction.user.roles):
            modal = NewSotwModal("Create a new Seed of the Week")
            await interaction.response.send_modal(modal)
            await modal.wait()
            await command_functions.create_new_sotw(
                interaction,
                str(modal.sotwname),
                str(modal.sotwsubmitter),
                str(modal.sotwflags),
                str(modal.sotwdesc),
            )
            try:
                sotwview = views.SotwPingView()
                await general_channel.send(
                    f"<@&{role.id}>: A new SotW is live! **{str(modal.sotwname)}**, crafted by **{str(modal.sotwsubmitter)}**!\n```{str(modal.sotwdesc)}```Check it out @ <#{channel.id}>! And don't "
                    f"forget to submit your own ideas for the Seed of the Week!",
                    view=sotwview,
                )
            except AttributeError:
                await interaction.followup.send(
                    f"<@&{role.id}>: New SotW is live, courtesy of **{str(modal.sotwsubmitter)}**! Check it out @ <#{channel.id}>! And don't "
                    f"forget to submit your own ideas for SotW here: "
                    f"<https://forms.gle/99rEUH7MMaifdhkH6>"
                )
            except TypeError:
                return await interaction.channel.send("wut")
        else:
            await interaction.response.send_message(
                "Only Racebot Admins can use this command.", ephemeral=True
            )


@sotw_group.command(name="refresh", description="Refresh the current SotW data")
async def refresh_sotw(interaction: Interaction):
    if "Racebot Admin" in str(interaction.user.roles):
        await interaction.response.defer()
        await command_functions.refresh(interaction)
        await interaction.followup.send("Data has been refreshed!")
    else:
        await interaction.response.send_message(
            "Only Racebot Admins can use this command.", ephemeral=True
        )


@sotw_group.command(name="auto", description="Set the Auto Mode")
@app_commands.choices(
    choice=[
        app_commands.Choice(name="True", value="True"),
        app_commands.Choice(name="False", value="False"),
    ]
)
async def sotw_auto_command(interaction: Interaction, choice: app_commands.Choice[str]):
    if "Racebot Admin" in str(interaction.user.roles):
        await interaction.response.defer()
        await command_functions.auto_mode(interaction, str(choice.value))
        await interaction.followup.send(f"Auto-Mode set to `{choice.value}`!")
    else:
        await interaction.response.send_message(
            "Only Racebot Admins can use this command.", ephemeral=True
        )


tree.add_command(sotw_group, guild=discord.Object(constants.guild))
tree.clear_commands(guild=None)


@tasks.loop(hours=1)
async def check_time():
    current_time = datetime.datetime.now().strftime("%A, %H")

    if current_time == "Sunday, 00":
        await command_functions.auto_create_new_sotw(client)
        # data = await command_functions.auto_create_new_sotw(client)
        # sotwview = views.SotwPingView()
        # general_channel = data[0]
        # name = data[1]
        # submitter = data[2]
        # description = data[3]
        # sotw_channel = data[4]
        # role = data[5]
        # await general_channel.send(
        #     f"<@&{role.id}>: A new SotW is live! **{name}**, crafted by **{submitter}**!\n```{description}```"
        #     f"Check it out @ <#{sotw_channel.id}>! And don't "
        #     f"forget to submit your own ideas for the Seed of the Week!",
        #     view=sotwview,
        # )
    else:
        pass


client.run(constants.discord_token)
