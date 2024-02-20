from __future__ import annotations
from functools import partial
import random
from typing import TYPE_CHECKING, Callable

from cards.minion import Minion, MinionClass
from cards.spell import Spell, TargetedSpell


from .army import Army
from .hand import Hand
from .tavern import Tavern


class Player:
    def __init__(self) -> None:
        self.army: Army = Army(self)
        self.hand: Hand = Hand(self)
        self.level = 1
        self.health = 30
        self.armor = 0
        self.base_gold = 2
        self.gold = 2
        self.roll_price = 1
        self.buy_price = 3
        self.sell_price = 1
        self.blood_gem_attack = 1
        self.blood_gem_health = 1
        self.tavern: Tavern = Tavern()
        self.tavern_discount = 0
        self.free_rolls = 0
        self.turn = 0
        self.tavern_elemental_boost = 0
        self.knights_died = 0
        self.undead_attack_boost = 0
        self.view = self.tavern.new_view(self)

    @property
    def tavern_upgrade_price(self) -> int:
        return max(0, self.tavern.upgrade_price[self.level-1] - self.tavern_discount)

    @property
    def all_actions(self) -> list[Callable]:
        actions = []
        actions.append(lambda: None) # 0, nothing
        for tavern_index in range(6): # 1-6, buy card from tavern
            actions.append(partial(self.buy, tavern_index))
        for inhand_index in range(10): # 7-76, play card from hand to table position
            for table_index in range(7):
                actions.append(partial(self.play, inhand_index, table_index))
        for source_position in range(7): # 77-125, reorder cards on board
            for target_position in range(7):
                actions.append(partial(self.reorder, source_position, target_position))
        for table_index in range(7): # 126-132, sell minion from board
            actions.append(partial(self.sell, table_index))
        actions.append(partial(self.roll)) # 133, roll tavern
        actions.append(partial(self.upgrade_tavern)) # 134, upgrade tavern
        return actions
    
    @property
    def available_actions(self) -> list[bool]:
        actions = []
        actions.append(True) # 0, nothing
        for tavern_index in range(6): # 1-6, buy card from tavern
            actions.append(self.buy_possible(tavern_index))
        for inhand_index in range(10): # 7-76, play card from hand to table position
            for table_index in range(7):
                actions.append(self.play_possible(inhand_index, table_index))
        for source_position in range(7): # 77-125, reorder cards on board
            for target_position in range(7):
                actions.append(self.reorder_possible(source_position, target_position))
        for table_index in range(7): # 126-132, sell minion from board
            actions.append(self.sell_possible(table_index))
        actions.append(self.roll_possible()) # 133, roll tavern
        actions.append(self.upgrade_possible()) # 134, upgrade tavern
        return actions

    @property
    def observation(self) -> dict:
        d = {}
        d["level"] = self.level
        d["gold"] = self.gold
        d["health"] = self.health
        d["tavern_not_upgraded_for"] = self.tavern_discount
        d["tavern_upgrade_price"] = self.tavern_upgrade_price
        d["turn"] = self.turn
        d["blood_gem_attack"] = self.blood_gem_attack
        d["blood_gem_health"] = self.blood_gem_health
        d["free_rolls"] = self.free_rolls
        d["tavern_elemental_boost"] = self.tavern_elemental_boost
        d["knights_died"] = self.knights_died
        d["undead_attack_boost"] = self.undead_attack_boost
        return {
            "player_data": d, 
            "hand_data": self.hand.observation,
            "board_data": self.army.observation,
            "tavern_data": self.view.observation,
        }
    
    def __str__(self) -> str:
        return f"Player level={self.level} health={self.health} gold={self.gold}"

    def act_random(self) -> None:
        action_id = -1
        while action_id != 0:
            possible = False
            while not possible:
                action_id = random.randint(0, len(self.all_actions)-1)
                possible = self.available_actions[action_id]
            self.all_actions[action_id]()

    def check_triplets(self) -> None:
        cards = self.army.cards + self.hand.cards
        for card in cards:
            card_type = type(card)
            cntr = 0
            for another_card in cards:
                if isinstance(another_card, card_type):
                    cntr += 1
                if cntr >= 3:
                    break
        if cntr == 3:
            contains = []
            perm_attack = 0
            perm_health = 0
            for card in list(self.army.cards):
                if isinstance(card, card_type):
                    perm_attack += card.attack_perm_boost
                    perm_health += card.health_perm_boost
                    self.army.remove(card)
                    contains.append(card)
            for card in list(self.hand.cards):
                if isinstance(card, Minion):
                    if isinstance(card, card_type):
                        perm_attack += card.attack_perm_boost
                        perm_health += card.health_perm_boost
                        self.hand.remove(card)
                        contains.append(card)
            triplet = card_type(card.army)
            triplet.triplet = True
            triplet.contains = contains
            triplet.attack_perm_boost += perm_attack
            triplet.health_perm_boost += perm_health
            self.hand.add(triplet, len(self.hand))

    def start_turn(self) -> None:
        self.turn += 1
        self.base_gold += 1
        self.gold = min(self.base_gold, 10)
        self.view = self.tavern.roll(self.view, self.tavern.minion_count[self.level-1])
        self.tavern_discount += 1
        for card in self.army.cards:
            for hook in card.hooks["on_turn_start"]:
                hook()
            for c in card.magnited:
                for hook in c.hooks["on_turn_start"]:
                    hook()

    def end_turn(self) -> None:
        for card in self.army.cards:
            for hook in card.hooks["on_turn_end"]:
                hook()
            for c in card.magnited:
                for hook in c.hooks["on_turn_end"]:
                    hook()

    def upgrade_possible(self) -> bool:
        if self.level < 6:
            if self.gold >= self.tavern_upgrade_price:
                return True
        return False

    def upgrade_tavern(self) -> bool:
        if self.upgrade_possible():
            tav_price = self.tavern_upgrade_price
            self.gold -= tav_price
            self.level += 1
            self.tavern_discount = 0
            return True
        return False
    
    def roll_possible(self) -> bool:
        if self.gold >= self.roll_price or self.free_rolls > 0:
            return True
        return False
    
    def roll(self) -> bool:
        if self.roll_possible():
            if self.free_rolls > 0:
                self.free_rolls -= 1
            else:
                self.gold -= self.roll_price
            self.view = self.tavern.roll(self.view, self.tavern.minion_count[self.level-1])
            return True
        return False
    
    def buy_possible(self, index: int) -> bool:
        if index < len(self.view):
            if self.gold >= self.buy_price:
                if len(self.hand) < self.hand.max_len:
                    return True
        return False
    
    def buy(self, index: int) -> bool:
        if self.buy_possible(index):
            self.gold -= self.buy_price
            card = self.tavern.buy(self.view[index])
            card.army = self.army
            self.view.remove(card)
            self.hand.add(card, len(self.hand))
            for hook in self.army.hooks["on_minion_buy"]:
                hook(card)
            self.check_triplets()
            return True
        return False
    
    def sell_possible(self, index: int) -> bool:
        if index < len(self.army):
            return True
        return False

    def sell(self, index: int) -> bool:
        if self.sell_possible(index):
            card = self.army[index]
            for hook in card.hooks["on_sell"]:
                hook()
            self.tavern.sell(card)
            card.army = None
            self.gold += self.sell_price
            return self.army.remove(card)
        return False
    
    def play_possible(self, index, place) -> bool:
        if index < len(self.hand):
            if place <= len(self.army):
                card = self.hand[index]
                if isinstance(card, Minion):
                    return self.play_minion_possible(index, place)
                if isinstance(card, Spell):
                    return self.play_spell_possible(index, place)
        return False
    
    def play(self, index, place) -> bool:
        card = self.hand[index]
        if isinstance(card, Minion):
            return self.play_minion(index, place)
        if isinstance(card, Spell):
            return self.play_spell(index, place)
        return False
    
    def play_minion_possible(self, index, place) -> bool:
        if index < len(self.hand):
            if len(self.army) < 7 or self.hand[index].magnetic:
                if place <= len(self.army):
                    return True
        return False
    
    def play_minion(self, card_to_play_ind, place_to_play) -> bool:
        if self.play_minion_possible(card_to_play_ind, place_to_play):
            card = self.hand[card_to_play_ind]
            if isinstance(card, Minion):
                self.hand.remove(card)
                if card.magnetic:
                    if place_to_play < len(self.army):
                        if MinionClass.Mech in self.army[place_to_play].classes:
                            for hook in card.hooks["on_play"]:
                                hook()
                            for hook in card.hooks["battlecry"]:
                                hook()
                            for hook in self.army.hooks["on_minion_play"]:
                                hook(card)
                            return card.magnet(self.army[place_to_play])
                self.army.add(card, place_to_play)
                for hook in card.hooks["on_play"]:
                    hook()
                for hook in card.hooks["battlecry"]:
                    hook()
                for hook in self.army.hooks["on_minion_play"]:
                    hook(card)
                return True
        return False
    
    def play_spell_possible(self, index, place) -> bool:
        if index < len(self.hand):
            if place < len(self.army) or not isinstance(self.hand[index], TargetedSpell):
                return True
        return False
    
    def play_spell(self, card_to_play_ind, place_to_play) -> bool:
        if self.play_spell_possible(card_to_play_ind, place_to_play):
            card = self.hand[card_to_play_ind]
            self.hand.remove(card)
            if isinstance(card, Spell):
                if place_to_play < len(self.army):
                    target = self.army[place_to_play]
                else:
                    target = None
                for hook in self.army.hooks["on_spell_cast"]:
                    hook(card, target)
                return True
        return False
    
    def reorder_possible(self, source_index, target_index) -> bool:
        if source_index < len(self.army):
            if target_index < len(self.army):
                return True
        return False

    def reorder(self, source_index, target_index) -> bool:
        if self.reorder_possible(source_index, target_index):
            card = self.army[source_index]
            self.army.remove(card)
            self.army.add(card, target_index)
            return True
        return False