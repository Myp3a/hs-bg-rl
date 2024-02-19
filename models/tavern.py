from __future__ import annotations
from typing import TYPE_CHECKING

import random
from cards.minion import MinionClass
from cards.minions import *
from models.cardset import CardSet


if TYPE_CHECKING:
    from cards.minion import Minion

class Tavern:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Tavern, cls).__new__(cls)
            cls.instance.__initialized = False
        return cls.instance
    
    def __init__(self) -> None:
        if(self.__initialized): return
        self.__initialized = True
        self.base_cards: list[Minion] = \
            [AnnoyOTron(None) for _ in range(18)] + \
            [BeleagueredBattler(None) for _ in range(18)] + \
            [EmeraldProtoWhelp(None) for _ in range(18)] + \
            [HarmlessBonehead(None) for _ in range(18)] + \
            [Imprisoner(None) for _ in range(18)] + \
            [Manasaber(None) for _ in range(18)] + \
            [MicroMummy(None) for _ in range(18)] + \
            [PickyEater(None) for _ in range(18)] + \
            [RazorfenGeomancer(None) for _ in range(18)] + \
            [RefreshingAnomaly(None) for _ in range(18)] + \
            [RisenRider(None) for _ in range(18)] + \
            [RockpoolHunter(None) for _ in range(18)] + \
            [Scallywag(None) for _ in range(18)] + \
            [Sellemental(None) for _ in range(18)] + \
            [ShellCollector(None) for _ in range(18)] + \
            [SouthseaBusker(None) for _ in range(18)] + \
            [SunBaconRelaxer(None) for _ in range(18)] + \
            [SurfNSurf(None) for _ in range(18)] + \
            [Swampstriker(None) for _ in range(18)] + \
            [UpbeatFrontdrake(None) for _ in range(18)] + \
            [WrathWeaver(None) for _ in range(18)]
        self.cards: list[Minion] = []
        self.upgrade_price = [6, 7, 8, 11, 10, 0]
        self.minion_count = [3, 4, 4, 5, 5, 6]
        self.views = []
        self.reset()

    def reset(self) -> None:
        available_types = random.sample(list(MinionClass), 10)
        self.cards = [c for c in self.base_cards if any(t in available_types for t in c.classes)]
        self.views = []
        
    def new_view(self, player) -> list[Minion]:
        view = CardSet(player)
        view.max_len = 6
        self.views.append(view)
        return view
    
    def del_view(self, view) -> bool:
        if view in self.views:
            self.views.remove(view)
            return True
        return False
    
    def roll(self, view: CardSet, count: int) -> list[Minion]:
        view.clear()
        available_cards = [c for c in self.cards if not any(c in view.cards for view in self.views)]
        chosen = random.sample(available_cards, count)
        for card in chosen:
            view.add(card, len(view))
        return view
    
    def buy(self, card: Minion) -> Minion:
        self.cards.remove(card)
        return card
    
    def sell(self, card: Minion) -> None:
        if card.triplet:
            for c in card.contains:
                self.cards.append(c)
        else:
            self.cards.append(card)