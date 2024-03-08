from __future__ import annotations
import random
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class SprightlyScarab(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 90
        self.classes = [MinionClass.Beast]
        self.level = 3
        self.base_attack_value = 2
        self.base_health_value = 1
        self.hooks["on_play"].append(self.boost_beast)
        
    def boost_beast(self) -> None:
        targets = [t for t in self.army.cards if MinionClass.Beast in t.classes and not t is self]
        if len(targets) == 0:
            return
        target = random.choice(targets)
        # TODO: effect selection mechanic
        action = random.randint(0,1)
        match action:
            case 0:
                if self.triplet:
                    atk_boost = 2
                    hlt_boost = 2
                else:
                    atk_boost = 1
                    hlt_boost = 1
                target.attack_perm_boost += atk_boost
                target.health_perm_boost += hlt_boost
                target.feature_overrides["rebirth"].append({"state": True, "one_turn": False})
                for hook in self.army.hooks["on_values_change_perm"]:
                    hook(target, atk_boost, hlt_boost)
            case 1:
                if self.triplet:
                    atk_boost = 6
                    hlt_boost = 6
                else:
                    atk_boost = 2
                    hlt_boost = 2
                target.attack_perm_boost += atk_boost
                target.health_perm_boost += hlt_boost
                target.feature_overrides["taunt"].append({"state": True, "one_turn": False})
                for hook in self.army.hooks["on_values_change_perm"]:
                    hook(target, atk_boost, hlt_boost)
