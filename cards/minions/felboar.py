from __future__ import annotations
import random
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class Felboar(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 188
        self.classes = [MinionClass.Demon, MinionClass.Quilboar]
        self.level = 6
        self.base_attack_value = 3
        self.base_health_value = 8
        self.spell_cntr = 2
        self.hooks["on_lose"].append(self.remove_hook)
        self.hooks["on_play"].append(self.put_hook)

    def put_hook(self) -> None:
        self.army.hooks["on_spell_cast"].append(self.on_spell_cast)

    def remove_hook(self) -> None:
        self.spell_cntr = 2
        self.army.hooks["on_spell_cast"].remove(self.on_spell_cast)

    def on_spell_cast(self, casted, target) -> None:
        self.spell_cntr -= 1
        if self.spell_cntr == 0:
            self.spell_cntr = 2
            self.eat_minion()

    def eat_minion(self) -> None:
        if self.in_fight:
            return
        available_targets = self.army.player.view
        if len(available_targets) == 0:
            return
        target = random.choice(available_targets)
        card = self.army.player.tavern.buy(target)
        self.army.player.view.remove(card)
        self.contains.append(card)
        if self.triplet:
            atk_boost = card.attack_value * 2
            hlt_boost = card.health_value * 2
        else:
            atk_boost = card.attack_value
            hlt_boost = card.health_value
        self.attack_perm_boost += atk_boost
        self.health_perm_boost += hlt_boost
        for hook in self.army.hooks["on_values_change_perm"]:
            hook(self, atk_boost, hlt_boost)
