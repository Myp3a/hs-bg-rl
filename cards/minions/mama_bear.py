from __future__ import annotations
from typing import TYPE_CHECKING
import sys
from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class MamaBear(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 115
        self.classes = [MinionClass.Beast]
        self.level = 4
        self.base_attack_value = 3
        self.base_health_value = 3
        self.hooks["on_play"].append(self.put_hook)
        self.hooks["on_lose"].append(self.remove_hook)

    def put_hook(self) -> None:
        self.army.hooks["on_minion_play"].append(self.boost_beast)
        self.army.hooks["on_minion_summon"].append(self.boost_beast)

    def remove_hook(self) -> None:
        self.army.hooks["on_minion_play"].remove(self.boost_beast)
        self.army.hooks["on_minion_summon"].remove(self.boost_beast)

    def boost_beast(self, played: Minion):
        if MinionClass.Beast in played.classes and not played is self and self.health_value > 0:
            if self.triplet:
                atk_boost = 6
                hlt_boost = 6
            else:
                atk_boost = 3
                hlt_boost = 3
            if self.in_fight:
                played.attack_temp_boost += atk_boost
                played.health_temp_boost += hlt_boost
            else:
                played.attack_perm_boost += atk_boost
                played.health_perm_boost += hlt_boost
                for hook in self.army.hooks["on_values_change_perm"]:
                    hook(played, atk_boost, hlt_boost)
