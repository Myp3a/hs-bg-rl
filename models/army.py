from __future__ import annotations
import logging
from typing import TYPE_CHECKING

import random

from cards.minion import Minion, MinionClass
from cards.minions.audacious_anchor import AudaciousAnchor
from cards.minions.flourishing_frostling import FlourishingFrostling
from cards.minions.free_flying_feathermane import FreeFlyingFeathermane

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
            "on_minion_play": [self.elemental_play],  # (self), played
            "on_divine_shield_lost": [],  # (self), lost
            "on_minion_death": [self.summon_feathermane],  # (self), dead, position
            "on_spell_cast": [],  # (self), casted, target
            "on_hero_damage": [],  # (self), damage
            "on_values_change_perm": [],  # (self), target, attack_boost, health_boost
            "on_values_change_temp": [],  # (self), target, attack_boost, health_boost
            "on_minion_buy": [self.boost_undead_attack, self.boost_elemental_values, self.boost_tavern_minion, self.boost_frostling],  # (self), bought
            "on_minion_summon": [],  # (self), summoned
            "on_gold_spent": [],  # (self), spent
            "on_fight_start": [self.audacious_anchor_fight], # (self), friendly_army, enemy_army
        }
        self.max_len = 7
        self.cards: list[Minion] = []

    @property
    def power(self) -> int:
        return sum([c.level for c in self.cards])
    
    @property
    def attack_power(self) -> int:
        return sum([c.attack_value for c in self.cards])
    
    def summon_feathermane(self, dead: Minion, position) -> None:
        if MinionClass.Beast in dead.classes:
            feathermanes = [f for f in self.player.hand if isinstance(f, FreeFlyingFeathermane) and not f.summoned]
            if len(feathermanes) > 0:
                feathermane = feathermanes[0]
                feathermane.summoned = True
                self.add(feathermane, position)
                for hook in self.hooks["on_minion_summon"]:
                    hook(feathermane)

    def boost_undead_attack(self, bought: Minion) -> None:
        if MinionClass.Undead in bought.classes:
            bought.attack_perm_boost += self.player.undead_attack_boost
    
    def boost_elemental_values(self, bought: Minion) -> None:
        if MinionClass.Elemental in bought.classes:
            bought.attack_perm_boost += self.player.tavern_elemental_boost
            bought.health_perm_boost += self.player.tavern_elemental_boost

    def boost_frostling(self, bought: Minion) -> None:
        if isinstance(bought, FlourishingFrostling):
            atk_boost = self.player.elementals_played
            hlt_boost = self.player.elementals_played
            bought.attack_perm_boost += atk_boost
            bought.health_perm_boost += hlt_boost

    def boost_tavern_minion(self, bought: Minion) -> None:
        bought.attack_perm_boost += self.player.tavern_attack_boost
        bought.attack_perm_boost += self.player.tavern_health_boost
    
    def audacious_anchor_fight(self, friendly: Army, enemy: Army) -> None:
        for anchor in friendly.cards:
            if isinstance(anchor, AudaciousAnchor):
                position = friendly.index(anchor)
                target_index = min(position, len(enemy.cards) - 1)
                if target_index == -1:
                    continue
                target = enemy.cards[target_index]
                while target.health_value > 0 and anchor.health_value > 0:
                    if anchor.health_value > 0:
                        anchor.attack(target)
                    if target.health_value > 0:
                        target.attack(anchor)

    def elemental_play(self, played):
        if MinionClass.Elemental in played.classes:
            self.player.elementals_played += 1

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
        self.log.debug(f"def: {target} chosen from {target.army}")
        self.log.debug(f"{attacker} attacks {target}")
        attacker.attack(target)
        if attacker.windfury and attacker.health_value > 0:
            target = other.get_target()
            attacker.attack(target)
    
    def get_target(self) -> Card | None:
        if len(self) == 0:
            return None
        targets = [t for t in self.cards if t.taunt and t.revealed]
        if len(targets) == 0:
            targets = [t for t in self.cards if t.revealed]
        target = random.choice(targets)
        return target