from __future__ import annotations
from typing import TYPE_CHECKING

import random

from cards.minion import Minion

from .cardset import CardSet
if TYPE_CHECKING:
    from .card import Card

class Army(CardSet):
    def __init__(self, player) -> None:
        super().__init__(player)
        self.hooks = {
            "on_attack": [],
            "on_defence": [],
            "on_minion_play": [],
            "on_divine_shield_lost": [],
        }
        self.max_len = 7
        self.cards: list[Minion] = []

    @property
    def power(self) -> int:
        return sum([c.level for c in self.cards])
    
    @property
    def attack_power(self) -> int:
        return sum([c.attack_value for c in self.cards])
    
    def attack(self, other: Army) -> None:
        available_attackers = [c for c in self.cards if c.attack_value > 0]
        if len(available_attackers) == 0:
            return
        if len(other.cards) == 0:
            return
        for attacker in available_attackers:
            if not attacker.attacked_this_turn:
                break
        if attacker.attacked_this_turn:
            for attacker in available_attackers:
                attacker.attacked_this_turn = False
            attacker = available_attackers[0]
        
        target = other.get_target()

        attacker.attack(target)
    
    def get_target(self) -> Card | None:
        if len(self) == 0:
            return None
        targets = [t for t in self.cards if t.taunt]
        if len(targets) == 0:
            targets = [t for t in self.cards]
        target = random.choice(targets)
        return target