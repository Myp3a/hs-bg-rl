from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass
from cards.spells import *

if TYPE_CHECKING:
    from models.army import Army
    from cards.spell import Spell


class LavaLurker(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 40
        self.classes = [MinionClass.Naga]
        self.level = 2
        self.base_attack_value = 2
        self.base_health_value = 5
        self.saved_changes = 2
        self.hooks["on_turn_start"].append(self.reset_first)
        self.hooks["on_play"].append(self.put_hook)
        self.hooks["on_lose"].append(self.remove_hook)
        
    def put_hook(self) -> None:
        self.army.hooks["on_spell_cast"].append(self.permanent_bonus)

    def remove_hook(self) -> None:
        self.army.hooks["on_spell_cast"].remove(self.permanent_bonus)

    def reset_first(self) -> None:
        if self.triplet:
            self.saved_changes = 2
        else:
            self.saved_changes = 1

    def permanent_bonus(self, casted: Spell, target) -> None:
        if target is self and not self.in_fight and self.saved_changes > 0 and casted.spellcraft:
            self.saved_changes -= 1
            self.attack_temp_boost = 0
            self.health_temp_boost = 0
            match casted:
                # TODO: make "permanent" argument in spell cast?
                case AnglersLure():
                    self.feature_overrides["taunt"].append({"state": True, "one_turn": False})
                    if casted.triplet:
                        hlt_boost = 8
                    else:
                        hlt_boost = 4
                    self.health_perm_boost += hlt_boost
                    for hook in self.army.hooks["on_values_change_perm"]:
                        hook(self, 0, hlt_boost)
                case DeepBlues():
                    if casted.triplet:
                        atk_boost = self.army.player.blues_boost * 2
                        hlt_boost = self.army.player.blues_boost * 2
                    else:
                        atk_boost = self.army.player.blues_boost
                        hlt_boost = self.army.player.blues_boost
                    self.attack_perm_boost += atk_boost
                    self.health_perm_boost += hlt_boost
                    for hook in self.army.hooks["on_values_change_perm"]:
                        hook(self, atk_boost, hlt_boost)
                case DefendToTheDeath():
                    # TODO: what does this do?
                    pass
                case GlowingCrown():
                    self.feature_overrides["shield"].append({"state": True, "one_turn": False})
                case JustKeepSwimming():
                    self.feature_overrides["stealth"].append({"state": True, "one_turn": False})
                    if casted.triplet:
                        atk_boost = 6
                        hlt_boost = 10
                    else:
                        atk_boost = 3
                        hlt_boost = 5
                    self.attack_perm_boost += atk_boost
                    self.health_perm_boost += hlt_boost
                    for hook in self.army.hooks["on_values_change_perm"]:
                        hook(self, atk_boost, hlt_boost)
                case SickRiffs():
                    if casted.triplet:
                        atk_boost = self.army.player.level * 2
                        hlt_boost = self.army.player.level * 2
                    else:
                        atk_boost = self.army.player.level
                        hlt_boost = self.army.player.level
                    self.attack_perm_boost += atk_boost
                    self.health_perm_boost += hlt_boost
                    for hook in self.army.player.army.hooks["on_values_change_perm"]:
                        hook(target, atk_boost, hlt_boost)
                case SurfNSurf():
                    self.hooks["on_turn_start"].remove(casted.remove_hook)
