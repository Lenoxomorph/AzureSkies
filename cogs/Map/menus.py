import pickle

import discord


def open_maps(interaction):
    with open(f'./db/maps/map_{interaction.message.id}.pckl', 'rb') as f:
        return pickle.load(f)


async def update_map(interaction: discord.Interaction, maps=None):
    if maps is None:
        maps = open_maps(interaction)
    await interaction.response.edit_message(attachments=maps.render_files())


class MainMenu(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Reload", style=discord.ButtonStyle.grey)
    async def reload_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await update_map(interaction)

    @discord.ui.button(label="Test", style=discord.ButtonStyle.grey)
    async def test_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        maps = open_maps(interaction)
        print(maps.canvases[0].get_aircraft_coords)
        await update_map(interaction, maps)
