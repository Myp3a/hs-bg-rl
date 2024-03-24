from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class ZestyShaker(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 94
        self.classes = [MinionClass.Naga]
        self.level = 3
        self.base_attack_value = 3
        self.base_health_value = 4
        self.spell_count = 0
        self.hooks["on_play"].append(self.put_hook)
        self.hooks["on_lose"].append(self.remove_hook)
        self.hooks["on_turn_start"].append(self.reset_spell)
        self.hooks["on_play"].append(self.reset_spell)

    def put_hook(self) -> None:
        self.log.debug(f"{self} put hook on_spell_cast")
        self.army.hooks["on_spell_cast"].append(self.get_new_copy)

    def remove_hook(self) -> None:
        self.log.debug(f"{self} removed hook on_spell_cast")
        self.army.hooks["on_spell_cast"].remove(self.get_new_copy)

    def reset_spell(self):
        if self.triplet:
            self.spell_count = 2
        else:
            self.spell_count = 1

    def get_new_copy(self, casted, target):
        if self.spell_count > 0 and target is self:
            self.log.debug(f"{self} duplicating {casted}")
            self.army.player.hand.add(type(casted)(self.army.player, triplet=casted.triplet), len(self.army.player.hand))
            self.spell_count -= 1
