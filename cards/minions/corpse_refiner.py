from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class CorpseRefiner(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 31
        self.classes = [MinionClass.Undead, MinionClass.Pirate]
        self.level = 2
        self.base_attack_value = 2
        self.base_health_value = 3
        self.avenge_cntr = 4
        self.additional_gold = 0
        self.hooks["on_sell"].append(self.give_add_gold)
        self.hooks["on_lose"].append(self.remove_hook)
        self.hooks["on_turn_start"].append(self.reset_avenge)
        self.hooks["on_play"].append(self.put_hook)

    def put_hook(self) -> None:
        self.log.debug(f"{self} put hook on_minion_death")
        self.army.hooks["on_minion_death"].append(self.on_another_death)

    def remove_hook(self) -> None:
        self.log.debug(f"{self} removed hook on_minion_death")
        self.army.hooks["on_minion_death"].remove(self.on_another_death)

    def on_another_death(self, died, position) -> None:
        if self.health_value > 0 and self in self.army.cards:
            if not died is self:
                self.avenge_cntr -= 1
            self.log.debug(f"{self} decreased avenge, new cntr {self.avenge_cntr}")
            if self.avenge_cntr == 0:
                self.additional_gold += 1
                self.reset_avenge()

    def reset_avenge(self) -> None:
        self.avenge_cntr = 4

    def give_add_gold(self) -> None:
        gold = self.additional_gold
        if self.triplet:
            gold *= 2
        self.log.debug(f"{self} giving {self.army.player} {gold} gold")
        self.army.player.gold += gold