from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class ChampionOfThePrimus(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 146
        self.classes = [MinionClass.Undead]
        self.level = 5
        self.base_attack_value = 2
        self.base_health_value = 9
        self.avenge_cntr = 3
        self.hooks["on_lose"].append(self.remove_hook)
        self.hooks["on_turn_start"].append(self.reset_avenge)
        self.hooks["on_play"].append(self.put_hook)

    def put_hook(self) -> None:
        self.log.debug(f"{self} put hook on_minion_death")
        self.army.hooks["on_minion_death"].append(self.on_another_death)

    def remove_hook(self) -> None:
        self.log.debug(f"{self} removed hook on_minion_death")
        self.army.hooks["on_minion_death"].remove(self.on_another_death)

    def on_another_death(self, died: Minion, position: int) -> None:
        if self.health_value > 0 and self in self.army.cards:
            if not died is self:
                self.avenge_cntr -= 1
            self.log.debug(f"{self} decreased avenge, new cntr {self.avenge_cntr}")
            if self.avenge_cntr == 0:
                self.boost_undead()
                self.reset_avenge()

    def reset_avenge(self) -> None:
        self.avenge_cntr = 3

    def boost_undead(self):
        if self.triplet:
            atk_boost = 2
        else:
            atk_boost = 1
        self.log.debug(f"{self} boosting {self.army.player} undead by {atk_boost} atk")
        self.army.player.undead_attack_boost += atk_boost
