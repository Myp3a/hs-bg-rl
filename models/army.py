from __future__ import annotations
import logging
from typing import TYPE_CHECKING

import random

from cards.minion import Minion, MinionClass
from cards.minions.audacious_anchor import AudaciousAnchor
from cards.minions.flourishing_frostling import FlourishingFrostling
from cards.minions.free_flying_feathermane import FreeFlyingFeathermane
from cards.minions.humming_bird import HummingBird
from cards.minions.sore_loser import SoreLoser
from cards.minions.zapp_slywick import ZappSlywick

from .cardset import CardSet
if TYPE_CHECKING:
    from .card import Card

class Army(CardSet):
    def __init__(self, player, loglevel) -> None:
        super().__init__(player)
        self.log = logging.getLogger("army")
        self.log.setLevel(loglevel)
        logging.basicConfig()
        self.hooks: dict[str, list] = {
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
            "on_minion_summon": [self.mark_in_fight, self.boost_beast],  # (self), summoned
            "on_gold_spent": [],  # (self), spent
            "on_fight_start": [self.start_fight_all, self.audacious_anchor_fight], # (self), friendly_army, enemy_army
            "on_fight_end": [self.end_fight_all], # (self), friendly_army, dead
            "on_gold_get": [],  # (self), got
            "on_battlecry": []  # (self), cried
        }
        self.max_len = 7
        self.cards: list[Minion] = []
        self.in_fight = False
        self.enemy = None
        self.dead: list[Minion] = []

    @property
    def power(self) -> int:
        return sum([c.level for c in self.cards])
    
    @property
    def attack_power(self) -> int:
        return sum([c.attack_value for c in self.cards])
    
    @property
    def health_power(self) -> int:
        return sum([c.health_value for c in self.cards])
    
    def summon_feathermane(self, dead: Minion, position) -> None:
        if MinionClass.Beast in dead.classes:
            feathermanes = [f for f in self.player.hand if isinstance(f, FreeFlyingFeathermane) and not f.summoned]
            if len(feathermanes) > 0:
                feathermane = feathermanes[0]
                feathermane.log.debug(f"{feathermane} summoning from hand")
                feathermane.summoned = True
                self.add(feathermane, position)
                for hook in self.hooks["on_minion_summon"]:
                    hook(feathermane)

    def boost_undead_attack(self, bought: Minion) -> None:
        if MinionClass.Undead in bought.classes:
            bought.attack_perm_boost += self.player.undead_attack_boost
            bought.log.debug(f"{bought} got undead boost")

    def boost_elemental_values(self, bought: Minion) -> None:
        if MinionClass.Elemental in bought.classes:
            bought.attack_perm_boost += self.player.tavern_elemental_boost
            bought.health_perm_boost += self.player.tavern_elemental_boost
            bought.log.debug(f"{bought} got elemental boost")

    def boost_frostling(self, bought: Minion) -> None:
        if isinstance(bought, FlourishingFrostling):
            atk_boost = self.player.elementals_played
            hlt_boost = self.player.elementals_played
            bought.attack_perm_boost += atk_boost
            bought.health_perm_boost += hlt_boost
            bought.log.debug(f"{bought} got frostling boost")

    def boost_tavern_minion(self, bought: Minion) -> None:
        bought.attack_perm_boost += self.player.tavern_attack_boost
        bought.health_perm_boost += self.player.tavern_health_boost
    
    def audacious_anchor_fight(self, friendly: Army, enemy: Army) -> None:
        for anchor in friendly.cards:
            if isinstance(anchor, AudaciousAnchor):
                position = friendly.index(anchor)
                target_index = min(position, len(enemy.cards) - 1)
                if target_index == -1:
                    continue
                target = enemy.cards[target_index]
                self.log.debug(f"{anchor} battling with {target}")
                while target.health_value > 0 and anchor.health_value > 0:
                    if anchor.health_value > 0:
                        anchor.attack(target)
                    if target.health_value > 0:
                        target.attack(anchor)
                friendly.clean_dead()
                enemy.clean_dead()

    def elemental_play(self, played):
        if MinionClass.Elemental in played.classes:
            self.player.elementals_played += 1

    def start_fight_all(self, friendly: Army, enemy: Army):
        for c in self.cards:
            for hook in c.hooks["on_fight_start"]:
                hook()

    def end_fight_all(self, friendly: Army, dead: list[Minion]):
        for c in self.cards:
            for hook in c.hooks["on_fight_end"]:
                hook()
        for c in self.dead:
            for hook in c.hooks["on_fight_end"]:
                hook()

    def mark_in_fight(self, summoned: Minion):
        summoned.enemy_army = self.enemy
        if self.in_fight:
            summoned.in_fight = True

    def boost_beast(self, summoned: Minion):
        if MinionClass.Beast in summoned.classes:
            summoned.attack_temp_boost += self.player.beast_boost_atk
            summoned.health_temp_boost += self.player.beast_boost_hlt
            summoned.log.debug(f"{summoned} got beast boost")

    def count_hummingbirds(self, asker) -> None:
        boost = 0
        for c in self.cards:
            if isinstance(c, HummingBird) and not c is asker:
                boost += 2
                if c.triplet:
                    boost += 2
        return boost
    
    def count_sore_losers(self, asker) -> None:
        boost = 0
        for c in self.cards:
            if isinstance(c, SoreLoser) and not c is asker:
                boost += self.player.level
                if c.triplet:
                    boost += self.player.level
        return boost

    def attack(self, other: Army, immediate: bool = False) -> None:
        if immediate:
            available_attackers = [c for c in self.cards if c.immediate_attack]
            if not available_attackers:
                return
            attacker = available_attackers[0]
        else:
            available_attackers = [c for c in self.cards if c.attack_value > 0]
            if len(available_attackers) == 0:
                # To bypass stealth defender with no attack. Needs clarifying how it works in real game
                if len(self.cards) > 0:
                    for c in self.cards:
                        c.revealed = True
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
        
        if isinstance(attacker, ZappSlywick):
            target = other.get_target_zapp()
        else:
            target = other.get_target()
        if target is None:
            self.log.debug(f"{attacker} found no targets")
            return  
        self.log.debug(f"def: {target} chosen from {target.army}")
        self.log.debug(f"{attacker} attacks {target}")
        attacker.attack(target)
        self.clean_dead()
        other.clean_dead()
        if attacker.windfury and attacker.health_value > 0:
            target = other.get_target()
            attacker.attack(target)
            self.clean_dead()
            other.clean_dead()
    
    def get_target(self) -> Card | None:
        if len(self) == 0:
            return None
        targets = [t for t in self.cards if t.taunt and t.revealed]
        if len(targets) == 0:
            targets = [t for t in self.cards if t.revealed]
        if len(targets) == 0:
            return None
        target = random.choice(targets)
        return target
    
    def get_target_zapp(self) -> Card | None:
        if len(self) == 0:
            return None
        targets = sorted(self.cards, key=lambda card: card.health_value)
        return targets[0]
    
    def clean_dead(self):
        for c in list(self.cards):
            if c.health_value <= 0:
                c.death()
