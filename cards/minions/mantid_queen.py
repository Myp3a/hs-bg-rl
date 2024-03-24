from __future__ import annotations
import random
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class MantidQueen(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 196
        self.classes = []
        self.level = 6
        self.base_attack_value = 5
        self.base_health_value = 5
        self.base_toxic = True
        self.hooks["on_fight_start"].append(self.get_features)
        
    def get_features(self):
        if self.triplet:
            self.choose_and_get_features()
        self.choose_and_get_features()

    def choose_and_get_features(self) -> None:
        available = []
        if not self.windfury:
            available.append("wind")
        if not self.rebirth:
            available.append("rebirth")
        if not self.taunt:
            available.append("taunt")
        available.append("boost")
        diff_classes = set()
        for card in self.army.cards:
            diff_classes |= set(card.classes)
        self.log.debug(f"{self} found {len(diff_classes)} diff classes")
        for boost in random.sample(list(available), k=min(len(diff_classes), len(available))):
            self.log.debug(f"{self} getting {boost}")
            match boost:
                case "wind":
                    self.feature_overrides["windfury"].append({"state": True, "one_turn": True})
                case "rebirth":
                    self.feature_overrides["rebirth"].append({"state": True, "one_turn": True})
                case "taunt":
                    self.feature_overrides["taunt"].append({"state": True, "one_turn": True})
                case "boost":
                    self.attack_temp_boost += 5
                    self.health_temp_boost += 5
