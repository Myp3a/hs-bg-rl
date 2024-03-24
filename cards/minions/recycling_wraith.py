from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class RecyclingWraith(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 86
        self.classes = [MinionClass.Elemental]
        self.level = 3
        self.base_attack_value = 4
        self.base_health_value = 2
        self.hooks["on_play"].append(self.put_hook)
        self.hooks["on_sell"].append(self.remove_hook)

    def put_hook(self) -> None:
        self.log.debug(f"{self} put hook on_minion_play")
        self.army.hooks["on_minion_play"].append(self.free_roll)

    def remove_hook(self) -> None:
        self.log.debug(f"{self} removed hook on_minion_play")
        self.army.hooks["on_minion_play"].remove(self.free_roll)

    def free_roll(self, played):
        if MinionClass.Elemental in played.classes:
            self.log.debug(f"{self} making next roll free")
            self.army.player.free_rolls = 1
