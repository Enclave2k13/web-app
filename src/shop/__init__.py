"""Магазин — веб-приложение для продажи товаров."""

__version__ = "0.1.0"
__author__ = "Nikita"

from .server import MyServer, run_server

__all__ = ['MyServer', 'run_server']