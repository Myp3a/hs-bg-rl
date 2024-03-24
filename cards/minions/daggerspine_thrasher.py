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
        self.hooks["on_turn_start"].append(self.reset_features)
        self.hooks["on_play"].append(self.put_hook)
        self.hooks["on_lose"].append(self.remove_hook)
        self.hooks["on_lose"].append(self.reset_features)
        self.reset_features()

    def reset_features(self):
        self.available = []
        if not self.divine_shield:
            self.available.append("shield")
        if not self.windfury:
            self.available.append("wind")
        if not self.toxic:
            self.available.append("toxic")

    def put_hook(self) -> None:
        self.log.debug(f"{self} put hook on_spell_cast")
        self.army.hooks["on_spell_cast"].append(self.boost_values)

    def remove_hook(self) -> None:
        self.log.debug(f"{self} removed hook on_spell_cast")
        self.army.hooks["on_spell_cast"].remove(self.boost_values)

    def boost_values(self, casted, target):
        if len(self.available) > 0:
            feat = random.choice(self.available)
            self.log.debug(f"{self} getting {feat}")
            self.available.remove(feat)
            match feat:
                case "shield":
                    if self.triplet:
                        self.feature_overrides["shield"].append({"state": True, "one_turn": False})
                    else:
                        self.feature_overrides["shield"].append({"state": True, "one_turn": True})
                case "wind":
                    if self.triplet:
                        self.feature_overrides["windfury"].append({"state": True, "one_turn": False})
                    else:
                        self.feature_overrides["windfury"].append({"state": True, "one_turn": True})
                case "toxic":
                    if self.triplet:
                        self.feature_overrides["toxic"].append({"state": True, "one_turn": False})
                    else:
                        self.feature_overrides["toxic"].append({"state": True, "one_turn": True})
