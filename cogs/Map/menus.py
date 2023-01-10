import pickle
from typing import Any, ClassVar

import discord

from cogs.Map.maps import Maps
from utils.errors import on_error, PermissionsError


def open_maps(interaction) -> Maps:
    with open(f'./db/maps/map_{interaction.message.id}.pckl', 'rb') as f:
        return pickle.load(f)


async def update_map(interaction: discord.Interaction, maps=None):
    await interaction.response.defer(thinking=False)
    if maps is None:
        maps = open_maps(interaction)
    await interaction.followup.edit_message(interaction.message.id, attachments=maps.render_files())


class Menu(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    async def on_error(self, interaction: discord.Interaction, error: Exception, item: discord.ui.Item[Any], /) -> None:
        if isinstance(error, PermissionsError):
            await interaction.message.edit(view=MainMenu())
            await interaction.response.send_message(content=str(error), ephemeral=True, delete_after=5)
        else:
            await on_error(interaction.response.send_message, error)


class MainMenu(Menu):
    @discord.ui.button(label="Ship List", style=discord.ButtonStyle.blurple, custom_id='ships')
    async def ships_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        ships_menu = ShipsMenu()
        ships_menu.add_item(discord.ui.Button(label="test"))
        await interaction.response.edit_message(view=ships_menu)

    @discord.ui.button(label="Admin Control", style=discord.ButtonStyle.grey, custom_id='admin')
    async def admin_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(view=AdminMenu())

    @discord.ui.button(label="Canvas Control", style=discord.ButtonStyle.grey, custom_id='canvas')
    async def canvas_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(view=CanvasMenu())


class ChildMenu(Menu):
    def __init__(self, parent_menu: ClassVar):
        super().__init__()
        self.parent_menu = parent_menu

    @discord.ui.button(label="Back", style=discord.ButtonStyle.red, custom_id='back')
    async def back_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(view=self.parent_menu())


class ShipsMenu(ChildMenu):
    def __init__(self):
        super().__init__(MainMenu)


class CanvasMenu(ChildMenu):
    def __init__(self):
        super().__init__(MainMenu)

    @discord.ui.button(label="Reload", style=discord.ButtonStyle.grey, custom_id='reload')
    async def reload_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await update_map(interaction)

    @discord.ui.button(label="Zoom", style=discord.ButtonStyle.grey, custom_id='zoom')
    async def zoom_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(view=ZoomMenu())

    @discord.ui.button(label="Pan", style=discord.ButtonStyle.grey, custom_id='pan')
    async def pan_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(view=PanMenu())


class ZoomMenu(ChildMenu):
    def __init__(self):
        super().__init__(CanvasMenu)

    @discord.ui.button(label="Zoom In", style=discord.ButtonStyle.grey, custom_id='zoom_in', emoji="🔎")
    async def zoom_in_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.zoom(interaction, True)

    @discord.ui.button(label="Zoom Out", style=discord.ButtonStyle.grey, custom_id='zoom_out', emoji="🔍")
    async def zoom_out_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.zoom(interaction, False)

    @staticmethod
    async def zoom(interaction: discord.Interaction, is_zoom_in: bool):
        maps = open_maps(interaction)
        maps.pxl_per_ft *= 1.25 if is_zoom_in else 0.8
        maps.save()
        await update_map(interaction, maps)


class PanMenu(ChildMenu):
    def __init__(self):
        super().__init__(CanvasMenu)

    @discord.ui.button(label="Pan Forward  ", style=discord.ButtonStyle.grey, custom_id='pan_forward', emoji="⬆", row=1)
    async def pan_forward_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.pan(interaction, 2, True)

    @discord.ui.button(label="Pan Backward", style=discord.ButtonStyle.grey, custom_id='pan_backward', emoji="⬇", row=2)
    async def pan_backward_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.pan(interaction, 2, False)

    @discord.ui.button(label="Pan Right", style=discord.ButtonStyle.grey, custom_id='pan_right', emoji="➡", row=1)
    async def pan_right_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.pan(interaction, 0, True)

    @discord.ui.button(label="Pan Left ", style=discord.ButtonStyle.grey, custom_id='pan_left', emoji="⬅", row=2)
    async def pan_left_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.pan(interaction, 0, False)

    @discord.ui.button(label="Pan Up   ", style=discord.ButtonStyle.grey, custom_id='pan_up', emoji="🔼", row=1)
    async def pan_up_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.pan(interaction, 1, True)

    @discord.ui.button(label="Pan Down", style=discord.ButtonStyle.grey, custom_id='pan_down', emoji="🔽", row=2)
    async def pan_down_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.pan(interaction, 1, False)

    @staticmethod
    async def pan(interaction: discord.Interaction, axis_num: int, positive_negative: bool):
        maps = open_maps(interaction)

        temp_coords = list(maps.camera_coords.comps)
        temp_coords[axis_num] += (positive_negative * 2 - 1) * (180 / maps.pxl_per_ft)

        maps.camera_coords.comps = temp_coords
        maps.save()
        await update_map(interaction, maps)


class LockedMenu(ChildMenu):
    async def interaction_check(self, interaction: discord.Interaction, /) -> bool:
        if interaction.user.guild_permissions.administrator:
            return True
        raise PermissionsError("Permissions Error: Not an Admin")


class AdminMenu(LockedMenu):
    def __init__(self):
        super().__init__(MainMenu)

    @discord.ui.button(label="Update", style=discord.ButtonStyle.grey, custom_id='update')
    async def update_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        maps = open_maps(interaction)

        maps.update()
        maps.save()

        await update_map(interaction)
