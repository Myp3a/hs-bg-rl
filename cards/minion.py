from __future__ import annotations
from typing import TYPE_CHECKING

from enum import Enum
from models.card import Card

if TYPE_CHECKING:
    from models.army import Army

class MinionClass(Enum):
    Beast = "beast"
    Demon = "demon"
    Dragon = "dragon"
    Elemental = "elemental"
    Mech = "mech"
    Murloc = "murloc"
    Naga = "naga"
    Pirate = "pirate"
    Quilboar = "quilboar"
    Undead = "undead"

class Minion(Card):
    def __init__(self, army: Army) -> None:
        self.army = army
        self.hooks = {
            "on_attack_pre": [],
            "on_attack_post": [],
            "on_defence_pre": [],
            "on_defence_post": [],
            "on_fight_start": [],
            "on_turn_start": [],
            "on_turn_end": [],
            "on_sell": [],
            "battlecry": [],
            "deathrattle": [],
            "rebirth": [],
        }
        self.classes = []
        self.level = 0
        self.base_attack_value = 0
        self.base_health_value = 0
        self.attack_value = self.base_attack_value
        self.health_value = self.base_health_value
        self.is_dead = False
        self.rebirth = False
        self.divine_shield = False
        self.toxic = False
        self.taunt = False
        self.attacked_this_turn = False
        self.triplet = False
        self.immediate_attack = False

    def __str__(self) -> str:
        basename = f"{type(self).__name__}{self.attack_value},{self.health_value}"
        name = basename
        if self.triplet:
            name = f"G{name}G"
        if self.taunt:
            name = f"v{name}v"
        if self.rebirth:
            name = f"R{name}R"
        if self.divine_shield:
            name = f"({name})"
        if self.toxic:
            name = f"!{name}!"
        return name

    def death(self) -> None:
        position = self.army.index(self)
        self.army.remove(self)
        for hook in self.hooks["deathrattle"]:
            hook(position)
        if self.rebirth:
            self.rebirth = False
            self.attack_value = self.base_attack_value
            self.health_value = self.base_health_value
            self.army.add(self, position)
        else:
            self.is_dead = True

    def attack(self, target: Minion | None) -> None:
        if target is None:
            return
        for hook in self.army.hooks["on_attack"]:
            hook(target)
        for hook in self.hooks["on_attack_pre"]:
            hook(target)
        for hook in self.army.hooks["on_defence"]:
            hook(target)
        for hook in self.hooks["on_defence_pre"]:
            hook(target)
        if not self.divine_shield:
            self.health_value -= target.attack_value
            if target.toxic:
                target.toxic = False
                self.death()
        else:
            if target.attack_value > 0:
                self.divine_shield = False
        if not target.divine_shield:
            target.health_value -= self.attack_value
            if self.toxic:
                self.toxic = False
                self.death()
        else:
            if self.attack_value > 0:
                target.divine_shield = False
        for hook in self.hooks["on_attack_post"]:
            hook(target)
        for hook in self.hooks["on_defence_post"]:
            hook(target)
        if self.health_value <= 0:
            self.death()
        if target.health_value <= 0:
            target.death()
