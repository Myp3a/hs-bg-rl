from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class RockRock(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 202
        self.classes = [MinionClass.Elemental]
        self.level = 6
        self.base_attack_value = 5
        self.base_health_value = 5
        self.flag_attack = True
        self.hooks["on_turn_start"].append(self.flip_flag)
        self.hooks["on_lose"].append(self.remove_hook)
        self.hooks["on_play"].append(self.put_hook)

    def put_hook(self) -> None:
        self.log.debug(f"{self} put hook on_minion_play")
        self.army.hooks["on_minion_play"].append(self.on_play)

    def remove_hook(self) -> None:
        self.log.debug(f"{self} put hook on_minion_play")
        self.army.hooks["on_minion_play"].remove(self.on_play)

    def flip_flag(self):
        self.flag_attack = not self.flag_attack

    def on_play(self, played: Minion):
        if MinionClass.Elemental in played.classes:
            self.log.debug(f"{self} boosting {played}")
            if self.triplet:
                boost = 4
            else:
                boost = 2
            for t in self.army.cards:
                if self.flag_attack:
                    t.attack_perm_boost += boost
                    for hook in self.army.hooks["on_values_change_perm"]:
                        hook(t, boost, 0)
                else:
                    t.health_perm_boost += boost
                    for hook in self.army.hooks["on_values_change_perm"]:
                        hook(t, 0, boost)
