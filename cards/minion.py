from __future__ import annotations
from typing import TYPE_CHECKING

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
        self.classes = []
        self.level = 0
        self.base_attack_value = 0
        self.base_health_value = 0
        self.base_divine_shield = False
        self.base_toxic = False
        self.base_rebirth = False
        self.is_dead = False
        self.rebirth = False
        self.reborn = False
        self.divine_shield = False
        self.toxic = False
        self.taunt = False
        self.magnetic = False
        self.windfury = False
        self.magnited_to = None
        self.magnited = []
        self.attacked_this_turn = False
        self.triplet = False
        self.immediate_attack = False
        self.contains = []
        self.humming_bird_boost = 0
        self._attack_temp_boost = 0
        self._health_temp_boost = 0
        self.attack_perm_boost = 0
        self.health_perm_boost = 0
        self.clear_hooks()

    def __str__(self) -> str:
        basename = f"{type(self).__name__}{self.attack_value},{self.health_value}"
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
        return val
    
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
    
    def clear_hooks(self) -> None:
        self.hooks = {
            "on_attack_pre": [],  # (self), target
            "on_attack_post": [],  # (self), target
            "on_defence_pre": [],  # (self), target
            "on_defence_post": [],  # (self), target
            "on_fight_start": [],  # (self)
            "on_turn_start": [self.reset_temp_bonuses, self.restore_features],  # (self)
            "on_turn_end": [self.snapshot_features],  # (self)
            "on_sell": [],  # (self)
            "on_play": [],  # (self)
            "on_death": [],  # (self)
            "on_temp_values_change": [],  # (self)
            "on_kill": [],  # (self)
            "battlecry": [],  # (self)
            "deathrattle": [],  # (self)
            "rebirth": [self.restore_features],  # (self)
        }

    def snapshot_features(self) -> None:
        self.base_divine_shield = self.divine_shield
        self.base_toxic = self.toxic
        self.base_rebirth = self.rebirth
    
    def restore_features(self) -> None:
        self.divine_shield = self.base_divine_shield
        self.toxic = self.base_toxic
        self.rebirth = self.base_rebirth

    def reset_temp_bonuses(self) -> None:
        self.attack_temp_boost = 0
        self.health_temp_boost = 0
        self.is_dead = False
        if self.reborn:
            self.rebirth = True
            self.reborn = False

    def death(self) -> None:
        if self.is_dead:
            return
        self.is_dead = True
        position = self.army.index(self)
        for hook in self.army.hooks["on_minion_death"]:
            hook(self)
        for hook in self.hooks["on_death"]:
            hook()
        self.army.remove(self)
        for hook in self.hooks["deathrattle"]:
            hook(position)
        if self.rebirth:
            self.rebirth = False
            self.reborn = True
            self.is_dead = False
            self.army.add(self, position)
            for hook in self.hooks["on_play"]:
                hook()
        else:
            self.is_dead = True

    def attack(self, target: Minion | None) -> None:
        if target is None:
            return
        for hook in self.army.hooks["on_attack"]:
            hook(self, target)
        for hook in self.hooks["on_attack_pre"]:
            hook(target)
        for hook in target.army.hooks["on_defence"]:
            hook(target, self)
        for hook in target.hooks["on_defence_pre"]:
            hook(target)        
        if not self.divine_shield:
            self.health_temp_boost -= target.attack_value + target.humming_bird_boost
            if target.toxic:
                target.toxic = False
                for hook in target.hooks["on_kill"]:
                    hook()
                self.death()
        else:
            if target.attack_value > 0:
                self.divine_shield = False
                for hook in self.army.hooks["on_divine_shield_lost"]:
                    hook(self)
        if not target.divine_shield:
            target.health_temp_boost -= self.attack_value + self.humming_bird_boost
            if self.toxic:
                self.toxic = False
                for hook in self.hooks["on_kill"]:
                    hook()
                target.death()
        else:
            if self.attack_value > 0:
                target.divine_shield = False
                for hook in target.army.hooks["on_divine_shield_lost"]:
                    hook(target)
        for hook in self.hooks["on_attack_post"]:
            hook(target)
        for hook in self.hooks["on_defence_post"]:
            hook(target)
        if self.health_value <= 0 and not self.is_dead:
            for hook in target.hooks["on_kill"]:
                hook()
            self.death()
        if target.health_value <= 0 and not target.is_dead:
            for hook in self.hooks["on_kill"]:
                hook()
            target.death()

    def magnet(self, target: Minion) -> None:
        self.magnited_to = target
        target.attack_perm_boost += self.attack_value
        target.health_perm_boost += self.health_value
        if self.taunt:
            target.taunt = True
        if self.divine_shield:
            target.divine_shield = True
        if self.rebirth:
            target.rebirth = True
        if self.windfury:
            target.windfury = True
        if self.toxic:
            target.toxic = True
        target.magnited.append(self)
