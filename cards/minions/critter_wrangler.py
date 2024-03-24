from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass
from cards.spell import TargetedSpell

if TYPE_CHECKING:
    from cards.spell import Spell
    from models.army import Army


class CritterWrangler(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 148
        self.classes = [MinionClass.Naga]
        self.level = 5
        self.base_attack_value = 5
        self.base_health_value = 7
        self.hooks["on_play"].append(self.put_hook)
        self.hooks["on_lose"].append(self.remove_hook)

    def put_hook(self) -> None:
        self.army.hooks["on_spell_cast"].append(self.on_spell_cast)

    def remove_hook(self) -> None:
        self.army.hooks["on_spell_cast"].remove(self.on_spell_cast)

    def on_spell_cast(self, casted: Spell, target: Minion) -> None:
        if isinstance(casted, TargetedSpell):
            self.log.debug(f"{self} found casted {casted}, boosting {target}")
            if self.triplet:
                atk_bonus = 2
                hlt_bonus = 4
            else:
                atk_bonus = 1
                hlt_bonus = 2
            target.attack_perm_boost += atk_bonus
            target.health_perm_boost += hlt_bonus
            for hook in target.army.hooks["on_values_change_perm"]:
                hook(target, atk_bonus, hlt_bonus)
