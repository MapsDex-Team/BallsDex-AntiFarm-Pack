import logging
from typing import TYPE_CHECKING

from .cog import AntiFarm

if TYPE_CHECKING:
    from ballsdex.core.bot import BallsDexBot

log = logging.getLogger("ballsdex.packages.antifarm")


async def setup(bot: "BallsDexBot"):
    log.info("Loading AntiFarm package...")
    await bot.add_cog(AntiFarm(bot))
    log.info("AntiFarm package loaded successfully!")
