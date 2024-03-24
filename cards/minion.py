from __future__ import annotations
from typing import TYPE_CHECKING

import logging
import random
import string

from enum import Enum
from models.card import Card

if TYPE_CHECKING:
    from models.army import Army

class MinionClass(Enum):
    Beast = "beast"
    Demon = "demon"
    Dragon = "dragon"
    Elemental = "elemental"
    Mech = "mech"
    Murloc = "murloc"
    Naga = "naga"
    Pirate = "pirate"
    Quilboar = "quilboar"
    Undead = "undead"

class Minion(Card):
    def __init__(self, army: Army) -> None:
        super().__init__()
        self.army = army
        self.enemy_army = None
        self.hooks: dict[str, list] = {
            "on_attack_pre": [self.count_hummingbirds],  # (self), target
            "on_attack_post": [],  # (self), target
            "on_defence_pre": [],  # (self), target
            "on_defence_post": [],  # (self), target
            "on_attack_mid": [],  # (self), target
            "on_defence_mid": [],  # (self), target
            "on_take_hit_post": [],  # (self), target
            "on_fight_start": [],  # (self)
            "on_fight_end": [],  # (self)
            "on_turn_start": [self.reset_turn_start],  # (self)
            "on_turn_end": [],  # (self)
            "on_sell": [],  # (self)
            "on_get": [],  # (self)
            "on_play": [],  # (self)
            "on_lose": [],  # (self)
            "on_death": [],  # (self)
            "on_buy": [],  # (self) no more needed?
            "on_temp_values_change": [],  # (self)
            "on_kill": [],  # (self)
            "on_roll": [],  # (self)
            "battlecry": [],  # (self)
            "deathrattle": [],  # (self), position
            "rebirth": [self.reset_turn_start],  # (self)
        }
        self.feature_overrides = {}
        self.clean_overrides()
        self.random_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        self.classes = []
        self.level = 0
        self.base_attack_value = 0
        self.base_health_value = 0
        self.base_divine_shield = False
        self.base_toxic = False
        self.base_rebirth = False
        self.base_taunt = False
        self.base_windfury = False
        self.base_stealth = False
        self.reborn = False
        self.magnetic = False
        self.revealed = True
        self.magnited_to = None
        self.magnited = []
        self.attacked_this_turn = False
        self.triplet = False
        self.immediate_attack = False
        self.contains = []
        self.summoned = False
        self.in_fight = False
        self.humming_bird_boost = 0
        self.sore_loser_boost = 0
        self._attack_temp_boost = 0
        self._health_temp_boost = 0
        self.attack_perm_boost = 0
        self.health_perm_boost = 0
        self.not_sellable = False
        self.immune_attack = False
        self.log = logging.getLogger("minion")
        self.log.setLevel(logging.DEBUG)
        logging.basicConfig()

    def __str__(self) -> str:
        basename = f"{type(self).__name__}:{self.random_id}:{self.attack_value},{self.health_value}"
        name = basename
        if self.triplet:
            name = f"G{name}G"
        if self.taunt:
            name = f"v{name}v"
        if self.rebirth:
            name = f"R{name}R"
        if self.divine_shield:
            name = f"({name})"
        if self.toxic:
            name = f"!{name}!"
        if self.windfury:
            name = f"W{name}W"
        if not self.revealed:
            name = f".{name}."
        return name

    @property
    def attack_value(self) -> int:
        if self.reborn:
            val = self.base_attack_value
        else:
            val = self.base_attack_value + self.attack_perm_boost
        if self.triplet:
            val += self.base_attack_value
        val += self.attack_temp_boost
        return max(0, val)
    
    @property
    def health_value(self) -> int:
        if self.reborn:
            val = self.base_health_value
        else:
            val = self.base_health_value + self.health_perm_boost
        if self.triplet:
            val += self.base_health_value
        val += self.health_temp_boost
        return val

    @property
    def attack_temp_boost(self) -> int:
        return self._attack_temp_boost

    @attack_temp_boost.setter
    def attack_temp_boost(self, new_value) -> None:
        self._attack_temp_boost = new_value
        for hook in self.hooks["on_temp_values_change"]:
            hook()

    @property
    def health_temp_boost(self) -> int:
        return self._health_temp_boost

    @health_temp_boost.setter
    def health_temp_boost(self, new_value) -> None:
        self._health_temp_boost = new_value
        for hook in self.hooks["on_temp_values_change"]:
            hook()

    @property
    def rebirth(self):
        if (overrides := self.feature_overrides["rebirth"]):
            return overrides[-1]["state"]
        return self.base_rebirth
    
    @property
    def divine_shield(self):
        if (overrides := self.feature_overrides["shield"]):
            return overrides[-1]["state"]
        return self.base_divine_shield
    
    @property
    def toxic(self):
        if (overrides := self.feature_overrides["toxic"]):
            return overrides[-1]["state"]
        return self.base_toxic
    
    @property
    def taunt(self):
        if (overrides := self.feature_overrides["taunt"]):
            return overrides[-1]["state"]
        return self.base_taunt
    
    @property
    def windfury(self):
        if (overrides := self.feature_overrides["windfury"]):
            return overrides[-1]["state"]
        return self.base_windfury
    
    @property
    def stealth(self):
        if (overrides := self.feature_overrides["stealth"]):
            return overrides[-1]["state"]
        return self.base_stealth
    
    def reset_turn_start(self) -> None:
        self.attack_temp_boost = 0
        self.health_temp_boost = 0
        for feat in self.feature_overrides:
            for overr in list(self.feature_overrides[feat]):
                if overr["one_turn"]:
                    self.feature_overrides[feat].remove(overr)
        self.reborn = False
        if self.stealth:
            self.revealed = False
        self.in_fight = False
        self.enemy_army = None

    def clean_overrides(self) -> None:
        self.feature_overrides = {
            # Latest one used
            "rebirth": [],
            "shield": [],
            "toxic": [],
            "taunt": [],
            "windfury": [],
            "stealth": [],
        }

    def count_hummingbirds(self, target) -> None:
        bonus = self.army.count_hummingbirds(self)
        self.humming_bird_boost = bonus

    def count_sore_losers(self, target) -> None:
        bonus = self.army.count_sore_losers(self)
        self.sore_loser_boost = bonus

    def death(self) -> None:
        position = self.army.index(self)
        for hook in self.army.hooks["on_minion_death"]:
            hook(self, position)
        for hook in self.hooks["on_death"]:
            hook()
        self.army.dead.append(self)
        self.army.remove(self)
        for hook in self.hooks["deathrattle"]:
            for _ in range(self.army.player.count_rivendare_times()):
                hook(position)
        if self.rebirth:
            self.attack_temp_boost = 0
            self.health_temp_boost = 0
            self.reborn = True
            self.feature_overrides["rebirth"].append({"state": False, "one_turn": True})
            self.army.add(self, position)
            for hook in self.army.hooks["on_minion_summon"]:
                hook(self)

    def attack(self, target: Minion | None) -> None:
        assert self.health_value > 0, "Dead trying to attack! " + str(self)
        if target is None:
            return
        self.attacked_this_turn = True
        if self.stealth:
            self.feature_overrides["stealth"].append({"state": False, "one_turn": True})
        for hook in self.army.hooks["on_attack"]:
            hook(self, target)
        for hook in self.hooks["on_attack_pre"]:
            hook(target)
        for hook in target.army.hooks["on_defence"]:
            hook(target, self)
        for hook in target.hooks["on_defence_pre"]:
            if hook(self):  # If returned value is True, prevent attack
                return
        for hook in self.hooks["on_attack_mid"]:
            hook(target)
        for hook in target.hooks["on_defence_mid"]:
            hook(self)
        if not self.divine_shield and not self.immune_attack:
            self.health_temp_boost -= (target.attack_value
                + (target.humming_bird_boost if MinionClass.Beast in target.classes else 0)
                + (target.sore_loser_boost if MinionClass.Undead in target.classes else 0))
            for hook in self.hooks["on_take_hit_post"]:
                hook(target)
            if target.toxic:
                target.feature_overrides["toxic"].append({"state": False, "one_turn": True})
                for hook in target.hooks["on_kill"]:
                    hook()
                self.death()
        else:
            if not self.immune_attack:
                if target.attack_value > 0:
                    self.feature_overrides["shield"].append({"state": False, "one_turn": True})
                    for hook in self.army.hooks["on_divine_shield_lost"]:
                        hook(self)
        if not target.divine_shield:
            target.health_temp_boost -= (self.attack_value
                + (self.humming_bird_boost if MinionClass.Beast in self.classes else 0)
                + (self.sore_loser_boost if MinionClass.Undead in self.classes else 0))
            for hook in target.hooks["on_take_hit_post"]:
                hook(self)
            if self.toxic:
                self.feature_overrides["toxic"].append({"state": False, "one_turn": True})
                for hook in self.hooks["on_kill"]:
                    hook()
                target.death()
        else:
            if self.attack_value > 0:
                target.feature_overrides["shield"].append({"state": False, "one_turn": True})
                for hook in target.army.hooks["on_divine_shield_lost"]:
                    hook(target)
        for hook in self.hooks["on_attack_post"]:
            hook(target)
        for hook in self.hooks["on_defence_post"]:
            hook(target)
        if self.health_value <= 0:
            for hook in target.hooks["on_kill"]:
                hook()
            self.death()
        if target.health_value <= 0:
            for hook in self.hooks["on_kill"]:
                hook()
            target.death()

    def magnet(self, target: Minion, copy=False) -> None:
        if copy:
            magneting = type(self)(self.army)
            magneting.not_sellable = True
        else:
            magneting = self
        magneting.magnited_to = target
        target.attack_perm_boost += magneting.attack_value
        target.health_perm_boost += magneting.health_value
        if magneting.taunt:
            target.base_taunt = True
        if magneting.divine_shield:
            target.base_divine_shield = True
        if magneting.rebirth:
            target.base_rebirth = True
        if magneting.windfury:
            target.base_windfury = True
        if magneting.toxic:
            target.base_toxic = True
        target.magnited.append(magneting)
