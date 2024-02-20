from __future__ import annotations
from typing import TYPE_CHECKING

import random

if TYPE_CHECKING:
    from .player import Player


class Field:
    def __init__(self, first: Player, second: Player) -> None:
        self.first = first
        self.second = second
        self.first_snapshot = None
        self.second_snapshot = None
        self.turn_flag = random.randint(0, 1)

    def __str__(self) -> str:
        first_army = str(self.first.army)
        second_army = str(self.second.army)
        field_width = max(len(first_army), len(second_army))
        return f"""+-{'-'*field_width}-+
| {second_army:^{field_width}} |
+-{'-'*field_width}-+
| {first_army:^{field_width}} |
+-{'-'*field_width}-+
"""
    
    def snapshot(self) -> None:
        self.first_snapshot = list(self.first.army.cards)
        self.second_snapshot = list(self.second.army.cards)

    def restore(self) -> None:
        self.first.army.cards = self.first_snapshot
        self.second.army.cards = self.second_snapshot

    def check_battle_end(self) -> bool:
        if len(self.first.army) == 0:
            self.first.health -= self.second.army.power + self.second.level
            return True
        if len(self.second.army) == 0:
            self.second.health -= self.first.army.power + self.first.level
            return True
        if len(self.first.army) == 0 and len(self.second.army) == 0 or self.first.army.attack_power == 0 and self.second.army.attack_power == 0:
            return True
        return False

    def fight(self) -> None:
        self.snapshot()
        while len(self.first.army) > 0 and len(self.second.army) > 0:
            self.turn_flag = (self.turn_flag + 1) % 2
            match self.turn_flag:
                case 0:
                    self.first.army.attack(self.second.army)
                case 1:
                    self.second.army.attack(self.first.army)
            immediate_attacks = True
            while immediate_attacks:
                if self.check_battle_end():
                    self.restore()
                    return
                immediate_attacks = False
                for card in self.first.army.cards:
                    if card.immediate_attack:
                        immediate_attacks = True
                        card.attack(self.second.army.get_target())
                for card in self.second.army.cards:
                    if card.immediate_attack:
                        immediate_attacks = True
                        card.attack(self.first.army.get_target())
            if self.check_battle_end():
                self.restore()
                return
