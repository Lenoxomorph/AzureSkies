import pickle

import discord


def open_maps(message_id):
    with open(f'./db/maps/map_{message_id}.pckl', 'rb') as f:
        return pickle.load(f)


class MainMenu(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Reload", style=discord.ButtonStyle.grey)
    async def reload_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(attachments=[*open_maps(interaction.message.id)])


