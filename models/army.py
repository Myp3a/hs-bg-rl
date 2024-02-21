from __future__ import annotations
import logging
from typing import TYPE_CHECKING

import random

from cards.minion import Minion, MinionClass

from .cardset import CardSet
if TYPE_CHECKING:
    from .card import Card

class Army(CardSet):
    def __init__(self, player, loglevel) -> None:
        super().__init__(player)
        self.log = logging.getLogger("army")
        self.log.setLevel(loglevel)
        logging.basicConfig()
        self.hooks = {
            "on_attack": [],  # (self), attacker, defender
            "on_defence": [],  # (self), defender, attacker
            "on_minion_play": [],  # (self), played
            "on_divine_shield_lost": [],  # (self), lost
            "on_minion_death": [],  # (self), dead
            "on_spell_cast": [],  # (self), casted, target
            "on_hero_damage": [],  # (self), damage
            "on_values_change_perm": [],  # (self), target, attack_boost, health_boost
            "on_values_change_temp": [],  # (self), target, attack_boost, health_boost
            "on_minion_buy": [self.boost_undead_attack, self.boost_elemental_values],  # (self), bought
        }
        self.max_len = 7
        self.cards: list[Minion] = []

    @property
    def power(self) -> int:
        return sum([c.level for c in self.cards])
    
    @property
    def attack_power(self) -> int:
        return sum([c.attack_value for c in self.cards])
    
    def boost_undead_attack(self, bought: Minion) -> None:
        if MinionClass.Undead in bought.classes:
            bought.attack_perm_boost += self.player.undead_attack_boost
    
    def boost_elemental_values(self, bought: Minion) -> None:
        if MinionClass.Undead in bought.classes:
            bought.attack_perm_boost += self.player.tavern_elemental_boost
            bought.health_perm_boost += self.player.tavern_elemental_boost

    def attack(self, other: Army) -> None:
        available_attackers = [c for c in self.cards if c.attack_value > 0]
        if len(available_attackers) == 0:
            return
        if len(other.cards) == 0:
            return
        for attacker in available_attackers:
            if not attacker.attacked_this_turn:
                break
        if attacker.attacked_this_turn:
            for attacker in available_attackers:
                attacker.attacked_this_turn = False
            attacker = available_attackers[0]
        self.log.debug(f"atk: {attacker} chosen from {attacker.army}")
        
        target = other.get_target()
        self.log.debug(f"def: {attacker} attacks {target}")
        attacker.attack(target)
        if attacker.windfury:
            target = other.get_target()
            attacker.attack(target)
    
    def get_target(self) -> Card | None:
        if len(self) == 0:
            return None
        targets = [t for t in self.cards if t.taunt]
        if len(targets) == 0:
            targets = [t for t in self.cards]
        target = random.choice(targets)
        self.log.debug(f"{target} chosen from {target.army}")
        return target