from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class DeflectOBot(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 64
        self.classes = [MinionClass.Mech]
        self.level = 3
        self.base_attack_value = 3
        self.base_health_value = 2
        self.base_divine_shield = True
        # Probably safe to set to default play/lose, cause no mechs should be summoned outside of fight
        self.hooks["on_play"].append(self.put_hook)
        self.hooks["on_lose"].append(self.remove_hook)

    def put_hook(self) -> None:
        self.log.debug(f"{self} put hook on_minion_summon")
        self.army.hooks["on_minion_summon"].append(self.get_shield)
        
    def remove_hook(self) -> None:
        self.log.debug(f"{self} removed hook on_minion_summon")
        self.army.hooks["on_minion_summon"].remove(self.get_shield)

    def get_shield(self, summoned: Minion) -> None:
        if MinionClass.Mech in summoned.classes:
            self.log.debug(f"{self} found summoned mech, boosting self atk and shield")
            if self.triplet:
                atk_boost = 4
            else:
                atk_boost = 2
            self.feature_overrides["shield"].append({"state": True, "one_turn": True})
            self.attack_temp_boost += atk_boost
