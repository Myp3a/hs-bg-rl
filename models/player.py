from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion
from cards.spell import Spell


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
        self.view = self.tavern.new_view()

    def __str__(self) -> str:
        return f"Player level={self.level} health={self.health} gold={self.gold}"

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
            perm_attack = 0
            perm_health = 0
            for card in list(self.army.cards):
                if isinstance(card, card_type):
                    perm_attack += card.attack_value - card.base_attack_value
                    perm_health += card.health_value - card.base_health_value
                    self.army.remove(card)
            for card in list(self.hand.cards):
                if isinstance(card, Minion):
                    if isinstance(card, card_type):
                        perm_attack += card.attack_value - card.base_attack_value
                        perm_health += card.health_value - card.base_health_value
                        self.hand.remove(card)
            triplet = card_type(card.army)
            triplet.triplet = True
            triplet.base_attack_value *= 2
            triplet.base_health_value *= 2
            triplet.attack_value = triplet.base_attack_value
            triplet.health_value = triplet.base_health_value
            triplet.attack_value += perm_attack
            triplet.health_value += perm_health
            self.hand.add(triplet, len(self.hand))

    def start_turn(self) -> None:
        self.base_gold += 1
        self.gold = min(self.base_gold, 10)
        self.view = self.tavern.roll(self.view, self.tavern.minion_count[self.level-1])
        self.tavern_discount += 1
        for card in self.army.cards:
            for hook in card.hooks["on_turn_start"]:
                hook()

    def end_turn(self) -> None:
        for card in self.army.cards:
            for hook in card.hooks["on_turn_end"]:
                hook()

    def upgrade_tavern(self) -> bool:
        if self.gold >= (tav_price := max(0, self.tavern.upgrade_price[self.level-1] - self.tavern_discount)):
            self.gold -= tav_price
            self.level += 1
            self.tavern_discount = 0
            return True
        return False
    
    def roll(self) -> bool:
        if self.gold >= self.roll_price or self.free_rolls > 0:
            if self.free_rolls > 0:
                self.free_rolls -= 1
            else:
                self.gold -= self.roll_price
            self.view = self.tavern.roll(self.view, self.tavern.minion_count[self.level-1])
            return True
        return False
    
    def buy(self, index: int) -> bool:
        if index < len(self.view):
            if self.gold >= self.buy_price:
                if len(self.hand) < self.hand.max_len:
                    self.gold -= self.buy_price
                    card = self.tavern.buy(self.view[index])
                    card.army = self.army
                    self.view.remove(card)
                    self.hand.add(card, len(self.hand))
                    self.check_triplets()
                    return True
        return False
    
    def sell(self, index: int) -> bool:
        if index < len(self.army):
            card = self.army[index]
            card.army = None
            self.tavern.sell(card)
            for hook in card.hooks["on_sell"]:
                hook()
            self.gold += self.sell_price
            return self.army.remove(card)
        return False
    
    def play_minion(self, card_to_play_ind, place_to_play) -> bool:
        if card_to_play_ind < len(self.hand):
            if place_to_play <= len(self.army):
                card = self.hand[card_to_play_ind]
                if isinstance(card, Minion):
                    self.army.add(card, place_to_play)
                    for hook in card.hooks["battlecry"]:
                        hook()
                    for hook in self.army.hooks["on_minion_play"]:
                        hook(card)
                    return True
        return False
    
    def play_spell(self, card_to_play_ind, place_to_play) -> bool:
        if card_to_play_ind < len(self.hand):
            if place_to_play < len(self.army):
                card = self.hand[card_to_play_ind]
                if isinstance(card, Spell):
                    card.play(card, place_to_play)
                    return True
        return False