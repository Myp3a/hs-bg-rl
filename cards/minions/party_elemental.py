from __future__ import annotations
import random
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class PartyElemental(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 82
        self.classes = [MinionClass.Elemental]
        self.level = 3
        self.base_attack_value = 2
        self.base_health_value = 5
        self.hooks["on_play"].append(self.put_hook)
        self.hooks["on_lose"].append(self.remove_hook)

    def put_hook(self) -> None:
        self.army.hooks["on_minion_play"].append(self.boost_elemental)

    def remove_hook(self) -> None:
        self.army.hooks["on_minion_play"].remove(self.boost_elemental)

    def boost_elemental(self, played):
        # TODO: check if can buff itself
        if MinionClass.Elemental in played.classes:
            targets = [t for t in self.army.cards if MinionClass.Elemental in t.classes and not t is played]
            if len(targets) == 0:
                return
            if self.triplet:
                atk_boost = 2
                hlt_boost = 4
            else:
                atk_boost = 1
                hlt_boost = 2
            target = random.choice(targets)
            target.attack_perm_boost += atk_boost
            target.health_perm_boost += hlt_boost
            for hook in self.army.hooks["on_values_change_perm"]:
                hook(target, atk_boost, hlt_boost)
