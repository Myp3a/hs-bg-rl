from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class BananaSlamma(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 142
        self.classes = [MinionClass.Beast]
        self.level = 5
        self.base_attack_value = 3
        self.base_health_value = 6
        self.hooks["on_play"].append(self.put_hook)
        self.hooks["on_lose"].append(self.remove_hook)

    def put_hook(self) -> None:
        self.log.debug(f"{self} put hook on_minion_summon")
        self.army.hooks["on_minion_summon"].append(self.boost_beast)

    def remove_hook(self) -> None:
        self.log.debug(f"{self} removed hook on_minion_summon")
        self.army.hooks["on_minion_summon"].remove(self.boost_beast)

    def boost_beast(self, played: Minion):
        if self.in_fight and MinionClass.Beast in played.classes and not played is self and self.health_value > 0:
            self.log.debug(f"{self} boosting {played}")
            if self.triplet:
                atk_boost = played.attack_value * 3 - played.base_attack_value
                hlt_boost = played.health_value * 3 - played.base_health_value
            else:
                atk_boost = played.attack_value * 2 - played.base_attack_value
                hlt_boost = played.health_value * 2 - played.base_health_value
            played.attack_temp_boost += atk_boost
            played.health_temp_boost += hlt_boost
