"""Week modules package for Web-OOP platform."""

from app.modules.base import WeekModule
from app.modules.registry import WeekRegistry, week_registry

__all__ = ["WeekModule", "WeekRegistry", "week_registry"]
