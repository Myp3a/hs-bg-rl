from __future__ import annotations
import random
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass
from .rusted_reggie import RustedReggie
from .magtheridon_prime import MagtheridonPrime
from .baltharak import Baltharak

if TYPE_CHECKING:
    from models.army import Army


class AugmentedLaborer(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 138
        self.classes = [MinionClass.Mech, MinionClass.Demon]
        self.level = 5
        self.base_attack_value = 1
        self.base_health_value = 6
        self.avenge_cntr = 4
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
                self.give_mech_demon()
                self.reset_avenge()

    def reset_avenge(self) -> None:
        self.avenge_cntr = 4

    def choose_and_give_mech_demon(self):
        demons = [RustedReggie, MagtheridonPrime, Baltharak]
        demon = random.choice(demons)
        new_demon = demon(self.army)
        self.log.debug(f"{self} giving mechdemon {new_demon}")
        self.army.player.hand.add(new_demon, len(self.army.player.hand))

    def give_mech_demon(self):
        if self.triplet:
            self.choose_and_give_mech_demon()
        self.choose_and_give_mech_demon()
