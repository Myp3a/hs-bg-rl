from __future__ import annotations
from functools import partial
import random
import logging
import string
from typing import TYPE_CHECKING, Callable

from cards.minion import Minion, MinionClass
from cards.minions.brann_bronzebeard import BrannBronzebeard
from cards.minions.drakkari_enchanter import DrakkariEnchanter
from cards.minions.elemental_of_surprise import ElementalOfSurprise
from cards.minions.malchezaar_prince_of_dance import MalchezaarPrinceOfDance
from cards.minions.titus_rivendare import TitusRivendare
from cards.spell import Spell, TargetedSpell

if TYPE_CHECKING:
    from models.card import Card


from .army import Army
from .hand import Hand
from .tavern import Tavern

class Player:
    def __init__(self, tavern: Tavern, loglevel) -> None:
        self.log = logging.getLogger("player")
        self.log.setLevel(loglevel)
        logging.basicConfig()
        self.army: Army = Army(self, loglevel)
        self.hand: Hand = Hand(self)
        self.player_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
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
        self.tavern = tavern
        self.tavern_discount = 0
        self.free_rolls = 0
        self.turn = 0
        self.tavern_elemental_boost = 0
        self.knights_died = 0
        self.undead_attack_boost = 0
        self.tavern_attack_boost = 0
        self.tavern_health_boost = 0
        self.blues_boost = 1
        self.rolls_on_turn = 0
        self.elementals_played = 0
        self.gold_spent_on_turn = 0
        self.damaged_for_roll = False
        self.cards_played_on_turn = 0
        self.lost_last_turn = False
        self.beast_boost_atk = 0
        self.beast_boost_hlt = 0
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
        if self.health > 0:
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
        else:
            for _ in range(134):
                actions.append(False)
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
        d["tavern_attack_boost"] = self.tavern_attack_boost
        d["tavern_health_boost"] = self.tavern_health_boost
        d["blues_boost"] = self.blues_boost
        d["rolls_on_turn"] = self.rolls_on_turn
        d["elementals_played"] = self.elementals_played
        d["gold_spent_on_turn"] = self.gold_spent_on_turn
        return {
            "player_data": d, 
            "hand_data": self.hand.observation,
            "board_data": self.army.observation,
            "tavern_data": self.view.observation,
        }
    
    def __str__(self) -> str:
        return f"Player {self.player_id} L={self.level} H={self.health} G={self.gold}"

    def all_visible_cards(self) -> list[Card]:
        l = self.army.cards + self.hand.cards + self.view.cards
        return l

    def act_random(self) -> None:
        action_id = -1
        while action_id != 0:
            possible = False
            while not possible:
                action_id = random.randint(0, len(self.all_actions)-1)
                possible = self.available_actions[action_id]
            self.log.debug(f"{self} doing action {self.all_actions[action_id]}")
            self.all_actions[action_id]()

    def count_brann_times(self):
        times = 1
        for c in self.army.cards:
            if isinstance(c, BrannBronzebeard):
                if c.triplet:
                    times = 3
                elif times < 2:
                    times = 2
        return times
    
    def count_drakkari_times(self):
        times = 1
        for c in self.army.cards:
            if isinstance(c, DrakkariEnchanter):
                if c.triplet:
                    times = 3
                elif times < 2:
                    times = 2
        return times
    
    def count_rivendare_times(self):
        times = 1
        for c in self.army.cards:
            if isinstance(c, TitusRivendare):
                if c.triplet:
                    times += 2
                else:
                    times += 1
        return times
    
    def count_malchezaar_rolls(self):
        rolls = 0
        for c in self.army.cards:
            if isinstance(c, MalchezaarPrinceOfDance):
                rolls += c.rolls
        return rolls
    
    def check_triplets(self) -> None:
        cards = [c for c in self.army.cards + self.hand.cards if isinstance(c, Minion) and not c.triplet]
        cntr = 0
        for card in cards:
            card_type = type(card)
            cntr = 0
            for another_card in cards:
                if (
                    isinstance(another_card, card_type)
                    or MinionClass.Elemental in card.classes and isinstance(another_card, ElementalOfSurprise)
                ):
                    cntr += 1
                if cntr >= 3:
                    break
        if cntr == 3:
            contains = []
            perm_attack = 0
            perm_health = 0
            for card in list(self.army.cards):
                if (
                    isinstance(card, card_type)
                    or MinionClass.Elemental in card.classes and isinstance(card, ElementalOfSurprise)
                ) and not card.triplet:
                    perm_attack += card.attack_perm_boost
                    perm_health += card.health_perm_boost
                    self.army.remove(card)
                    for hook in card.hooks["on_lose"]:
                        hook()
                    contains.append(card)
            for card in list(self.hand.cards):
                if isinstance(card, Minion):
                    if (
                        isinstance(card, card_type)
                        or MinionClass.Elemental in card.classes and isinstance(card, ElementalOfSurprise)
                    ) and not card.triplet:
                        perm_attack += card.attack_perm_boost
                        perm_health += card.health_perm_boost
                        self.hand.remove(card)
                        contains.append(card)
            triplet = card_type(contains[0].army)
            self.log.debug(f"{self} tripleted {triplet}")
            triplet.triplet = True
            triplet.contains = contains
            for hook in triplet.hooks["on_get"]:
                hook()
            triplet.attack_perm_boost += perm_attack
            triplet.health_perm_boost += perm_health
            self.hand.add(triplet, len(self.hand))
            discover = [c for c in self.tavern.available_cards() if c.level == min(triplet.level + 1, 4)]
            bonus = random.choice(discover)
            if len(self.hand.cards) == 10:
                return
            bonus.army = self.army
            self.tavern.buy(bonus)
            for hook in bonus.hooks["on_get"]:
                hook()
            self.hand.add(bonus, len(self.hand.cards))

    def start_turn(self) -> None:
        self.log.debug(f"{self} turn start")
        if self.health > 0:
            self.turn += 1
            self.base_gold += 1
            self.gold = min(self.base_gold, 10)
            for hook in self.army.hooks["on_gold_get"]:
                hook(self.gold)
            self.view = self.tavern.roll(self.view, self.tavern.minion_count[self.level-1], self.level)
            self.tavern_discount += 1
            self.rolls_on_turn = 0
            self.gold_spent_on_turn = 0
            self.free_rolls = 0
            self.cards_played_on_turn = 0
            self.beast_boost_atk = 0
            self.beast_boost_hlt = 0
            for card in list(self.army.cards):
                for hook in card.hooks["on_turn_start"]:
                    hook()
                for c in card.magnited:
                    for hook in c.hooks["on_turn_start"]:
                        hook()
            for hook in self.hand.hooks["on_turn_start"]:
                hook()
        else:
            for c in self.army.cards:
                c.reset_turn_start()
            for c in self.hand.cards:
                if isinstance(c, Minion):
                    c.reset_turn_start()
        for c in self.army.cards:
            assert c.health_value > 0, "Army minion found dead at turn start! " + str(c)
            assert not c.in_fight, "in_fight wasn't reset for " + str(c)
        for c in self.hand.cards:
            if isinstance(c, Minion):
                assert c.health_value > 0, "Hand minion found dead at turn start! " + str(c)
                assert not c.in_fight, "in_fight wasn't reset for " + str(c)

    def end_turn(self) -> None:
        self.log.debug(f"{self} turn end")
        if self.health > 0:
            for _ in range(self.count_drakkari_times()):
                for card in self.army.cards:
                    for hook in card.hooks["on_turn_end"]:
                        hook()
                    for c in card.magnited:
                        for hook in c.hooks["on_turn_end"]:
                            hook()
                for hook in self.hand.hooks["on_turn_end"]:
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
            for hook in self.army.hooks["on_gold_spent"]:
                hook(tav_price)
            self.gold_spent_on_turn += tav_price
            self.level += 1
            self.tavern_discount = 0
            return True
        return False
    
    def roll_possible(self) -> bool:
        if self.gold >= self.roll_price or self.free_rolls > 0 or (self.count_malchezaar_rolls() > 0 and self.health > 1):
            return True
        return False
    
    def roll(self) -> bool:
        if self.roll_possible():
            self.damaged_for_roll = False
            malchezaar_rolls = self.count_malchezaar_rolls()
            if malchezaar_rolls == 0:
                if self.free_rolls == 0:
                    self.gold -= self.roll_price
                    for hook in self.army.hooks["on_gold_spent"]:
                        hook(self.roll_price)
                    self.gold_spent_on_turn += self.roll_price
            self.view = self.tavern.roll(self.view, self.tavern.minion_count[self.level-1], self.level)
            for c in self.army.cards:
                for hook in c.hooks["on_roll"]:
                    hook()
            if malchezaar_rolls == 0:
                if self.free_rolls > 0:
                    self.free_rolls -= 1
            self.rolls_on_turn += 1
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
            for hook in self.army.hooks["on_gold_spent"]:
                hook(self.buy_price)
            self.gold_spent_on_turn += self.buy_price
            card = self.tavern.buy(self.view[index])
            card.army = self.army
            self.view.remove(card)
            self.hand.add(card, len(self.hand))
            self.log.debug(f"{self} bought {card}, hand = {self.hand}")
            for hook in card.hooks["on_get"]:
                hook()
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
            for hook in card.hooks["on_lose"]:
                hook()
            for hook in card.hooks["on_sell"]:
                hook()
            self.tavern.sell(card)
            card.army = None
            self.gold += self.sell_price
            for hook in self.army.hooks["on_gold_get"]:
                hook(self.sell_price)
            self.army.remove(card)
            self.log.debug(f"{self} sold {card}, army = {self.army}")
            return True
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
                self.cards_played_on_turn += 1
                if card.magnetic:
                    if place_to_play < len(self.army):
                        if MinionClass.Mech in self.army[place_to_play].classes:
                            for hook in card.hooks["on_play"]:
                                hook()
                            for hook in card.hooks["battlecry"]:
                                for _ in range(self.count_brann_times()):
                                    hook()
                            for hook in self.army.hooks["on_minion_play"]:
                                hook(card)
                            self.log.debug(f"{self} played {card}, magnited to {self.army[place_to_play]}")
                            return card.magnet(self.army[place_to_play])
                self.army.add(card, place_to_play)
                self.log.debug(f"{self} played {card}, army = {self.army}")
                for hook in card.hooks["on_play"]:
                    hook()
                for hook in card.hooks["battlecry"]:
                    for _ in range(self.count_brann_times()):
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
            self.cards_played_on_turn += 1
            if isinstance(card, Spell):
                if place_to_play < len(self.army):
                    target = self.army[place_to_play]
                else:
                    target = None
                self.log.debug(f"{self} played {card}, target = {target}")
                card.play(target)
                for hook in self.army.hooks["on_spell_cast"]:
                    hook(card, target)
                return True
        return False
    
    def play_spell_minion(self, card, place_to_play) -> bool:
        if isinstance(card, Spell):
            target = self.army[place_to_play]
            self.log.debug(f"{self} minion played {card}, target = {target}")
            card.play(target)
            for hook in self.army.hooks["on_spell_cast"]:
                hook(card, target)
    
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