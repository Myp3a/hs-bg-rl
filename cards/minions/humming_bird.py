from __future__ import annotations
from functools import partial
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class HummingBird(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 37
        self.classes = [MinionClass.Beast]
        self.level = 2
        self.base_attack_value = 2
        self.base_health_value = 4
        self.hooks["on_play"].append(self.put_hook_existing)
        self.hooks["on_lose"].append(self.remove_hook)
        self.hooks["on_death"].append(self.decrease_boost)
        self.hooks["on_turn_start"].append(self.reset_boost)
        
    def count_hummingbirds(self, target, beast) -> None:
        boost = 0
        for c in beast.army.cards:
            if isinstance(c, HummingBird) and not c is self:
                boost += 2
                if c.triplet:
                    boost += 2
        if MinionClass.Beast in beast.classes:
            beast.humming_bird_boost = boost
                
    def put_hook_existing(self) -> None:
        self.army.hooks["on_minion_play"].append(self.put_hook_new)
        for m in self.army.cards:
            if MinionClass.Beast in m.classes:
                m.hooks["on_attack_pre"].append(partial(self.count_hummingbirds, beast=m))
                m.hooks["on_defence_pre"].append(partial(self.count_hummingbirds, beast=m))

    def put_hook_new(self, played) -> None:
        if MinionClass.Beast in played.classes:
            played.hooks["on_attack_pre"].append(partial(self.count_hummingbirds, beast=played))
            played.hooks["on_defence_pre"].append(partial(self.count_hummingbirds, beast=played))

    def decrease_boost(self) -> None:
        for m in self.army.cards:
            if MinionClass.Beast in m.classes:
                m.humming_bird_boost -= 2
                if self.triplet:
                    m.humming_bird_boost -= 2

    def reset_boost(self) -> None:
        for m in self.army.cards:
            if MinionClass.Beast in m.classes:
                m.humming_bird_boost = 0

    def remove_hook(self) -> None:
        self.army.hooks["on_minion_play"].remove(self.put_hook_new)
        # count_hummingbirds is safe to have in any counts on any beasts
