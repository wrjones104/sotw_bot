import json

import discord
from discord.ui import View

import functions.command_functions
from functions.command_functions import generate_seed, get_flags, new_submission


class SotwPingView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @discord.ui.button(label="Practice", style=discord.ButtonStyle.green, emoji="🎲",
                       custom_id="practice_button")
    async def practice(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(f'One moment please...', ephemeral=True)
        try:
            with open("sotw_db.json") as x:
                sotw_db = json.load(x)
                flags = await get_flags(sotw_db[str(len(sotw_db))]['seed_id'])
            seedlink = await generate_seed(flags, False)
            await interaction.followup.send(f'Here\'s your practice seed - good luck!\n{seedlink["url"]}',
                                            ephemeral=True)
        except (discord.errors.HTTPException, discord.errors.NotFound):
            await interaction.response.defer()
            await interaction.followup.send(f"I'm a little overloaded - give me a sec and try again",
                                            ephemeral=True)

    @discord.ui.button(label="Submit Idea", style=discord.ButtonStyle.green, emoji="💡",
                       custom_id="idea_button")
    async def submit_idea(self, interaction: discord.Interaction, button: discord.ui.Button):
        await functions.command_functions.new_submission(interaction)
