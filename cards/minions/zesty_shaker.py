from __future__ import annotations
import random
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
        self.first_spell = True
        self.hooks["on_play"].append(self.put_hook)
        self.hooks["on_sell"].append(self.remove_hook)
        self.hooks["on_turn_start"].append(self.reset_spell)

    def put_hook(self) -> None:
        self.army.hooks["on_spell_cast"].append(self.get_new_copy)

    def remove_hook(self) -> None:
        self.army.hooks["on_spell_cast"].remove(self.get_new_copy)

    def reset_spell(self):
        self.first_spell = True

    def get_new_copy(self, casted, target):
        if self.first_spell and target is self:
            self.army.player.hand.add(type(casted)(self.army.player), len(self.army.player.hand))
            self.first_spell = False
