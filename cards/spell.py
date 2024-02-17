from __future__ import annotations
from typing import TYPE_CHECKING

from models.card import Card

if TYPE_CHECKING:
    from cards.minion import Minion
    from models.player import Player


class Spell(Card):
    def __init__(self, player) -> None:
        self.player: Player = player

    def play(self, target: Minion | None) -> None:
        raise NotImplementedError