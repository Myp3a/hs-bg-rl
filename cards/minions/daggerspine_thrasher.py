from __future__ import annotations
import random
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class DaggerspineThrasher(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 103
        self.classes = [MinionClass.Naga]
        self.level = 4
        self.base_attack_value = 4
        self.base_health_value = 5
        self.available = []
        self.hooks["on_turn_start"].append(self.remove_features)
        self.hooks["on_play"].append(self.put_hook)
        self.hooks["on_sell"].append(self.remove_hook)
        self.hooks["on_sell"].append(self.remove_features)
        self.remove_features()

    def remove_features(self):
        if self.triplet:
            return
        self.divine_shield = False
        self.windfury = False
        self.toxic = False
        self.available = ["shield", "wind", "toxic"]

    def put_hook(self) -> None:
        self.army.hooks["on_spell_cast"].append(self.boost_values)

    def remove_hook(self) -> None:
        self.army.hooks["on_spell_cast"].remove(self.boost_values)

    def boost_values(self, casted, target):
        if len(self.available) > 0:
            feat = random.choice(self.available)
            self.available.remove(feat)
            match feat:
                case "shield":
                    self.divine_shield = True
                case "wind":
                    self.windfury = True
                case "toxic":
                    self.toxic = True
