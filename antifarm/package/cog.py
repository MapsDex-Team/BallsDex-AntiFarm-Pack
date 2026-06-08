import logging
from types import MethodType
from typing import TYPE_CHECKING

import discord
from discord.ext import commands

if TYPE_CHECKING:
    from ballsdex.core.bot import BallsDexBot

log = logging.getLogger("ballsdex.packages.antifarm")

# Configuration constants
MIN_MEMBERS = 15 # Treated as human members when the members intent is enabled.

async def count_members(bot: "BallsDexBot", guild: discord.Guild) -> int:
    if not bot.intents.members:
        return guild.member_count or 0

    total = 0
    async for member in guild.fetch_members(limit=None):
        if not member.bot:
            total += 1
    return total


class AntiFarm(commands.Cog):
    def __init__(self, bot: "BallsDexBot"):
        self.bot = bot
        self.manager = None
        self.config_channel = None

    async def cog_load(self):
        self.patch_config_channel()
        self.patch_spawn_manager()

    def patch_config_channel(self):
        config = self.bot.get_cog("Config")
        if config is None:
            log.warning("Config cog was not found; could not antifarm patch /config channel.")
            return

        self.config_channel = config.channel
        original_callback = getattr(self.config_channel, "_antifarm_original_callback", self.config_channel.callback)
        self.config_channel._antifarm_original_callback = original_callback

        async def channel(config_self, interaction: discord.Interaction["BallsDexBot"], channel=None):
            guild = interaction.guild
            if guild and await count_members(self.bot, guild) < MIN_MEMBERS:
                member_label = "human members" if self.bot.intents.members else "members"
                await interaction.response.send_message(
                    f"This server needs at least {MIN_MEMBERS} {member_label} before spawning can be configured.",
                    ephemeral=True,
                )
                return

            return await original_callback(config_self, interaction, channel)

        self.config_channel._callback = channel

    def patch_spawn_manager(self):
        spawner = self.bot.get_cog("CountryBallsSpawner")
        if spawner is None:
            log.warning("CountryBallsSpawner cog was not found; could not antifarm patch spawning.")
            return

        manager = spawner.spawn_manager
        self.manager = manager
        original_handle_message = getattr(manager, "_antifarm_original_handle_message", manager.handle_message)
        manager._antifarm_original_handle_message = original_handle_message

        async def handle_message(manager_self, message: discord.Message):
            guild = message.guild
            if guild and await count_members(self.bot, guild) < MIN_MEMBERS:
                return False

            return await original_handle_message(message)

        manager.handle_message = MethodType(handle_message, manager)

    async def cog_unload(self):
        if self.manager and hasattr(self.manager, "_antifarm_original_handle_message"):
            self.manager.handle_message = self.manager._antifarm_original_handle_message
            del self.manager._antifarm_original_handle_message

        if self.config_channel and hasattr(self.config_channel, "_antifarm_original_callback"):
            self.config_channel._callback = self.config_channel._antifarm_original_callback
            del self.config_channel._antifarm_original_callback
