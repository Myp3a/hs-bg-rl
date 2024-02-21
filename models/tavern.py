from __future__ import annotations
import logging
from typing import TYPE_CHECKING

import random
from cards.minion import MinionClass
from cards.minions import *
from models.cardset import CardSet


if TYPE_CHECKING:
    from cards.minion import Minion

class Tavern:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Tavern, cls).__new__(cls)
            cls.instance.__initialized = False
        return cls.instance
    
    def __init__(self, loglevel) -> None:
        if(self.__initialized): return
        self.log = logging.getLogger("tavern")
        self.log.setLevel(loglevel)
        logging.basicConfig()
        self.__initialized = True
        self.NOT_SELLABLE = [
            Skeleton,
            Imp,
            Cubling,
            SkyPirate,
            WaterDroplet,
            Crab,
        ]
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
            [WrathWeaver(None) for _ in range(18)] + \
            [BlazingSkyfin(None) for _ in range(15)] + \
            [BriarbackBookie(None) for _ in range(15)] + \
            [BronzeSandspewer(None) for _ in range(15)] + \
            [CogworkCopter(None) for _ in range(15)] + \
            [ColdlightSeer(None) for _ in range(15)] + \
            [CorpseRefiner(None) for _ in range(15)] + \
            [DancingBarnstormer(None) for _ in range(15)] + \
            [DeepSeaAngler(None) for _ in range(15)] + \
            [EternalKnight(None) for _ in range(15)] + \
            [FreedealingGambler(None) for _ in range(15)] + \
            [GraveGobbler(None) for _ in range(15)] + \
            [HummingBird(None) for _ in range(15)] + \
            [ImpulsiveTrickster(None) for _ in range(15)] + \
            [LavaLurker(None) for _ in range(15)] + \
            [Lullabot(None) for _ in range(15)] + \
            [MindMuck(None) for _ in range(15)] + \
            [MoonBaconJazzer(None) for _ in range(15)] + \
            [Murcules(None) for _ in range(15)] + \
            [NerubianDeathswarmer(None) for _ in range(15)] + \
            [OozelingGladiator(None) for _ in range(15)] + \
            [PatientScout(None) for _ in range(15)] + \
            [ReefRiffer(None) for _ in range(15)] + \
            [RipsnarlCaptain(None) for _ in range(15)] + \
            [SewerRat(None) for _ in range(15)] + \
            [SnailCavalry(None) for _ in range(15)] + \
            [SoulRewinder(None) for _ in range(15)] + \
            [Tad(None) for _ in range(15)] + \
            [Thorncaller(None) for _ in range(15)] + \
            [ToughTusk(None) for _ in range(15)] + \
            [TwilightEmissary(None) for _ in range(15)] + \
            [WhelpSmuggler(None) for _ in range(15)] + \
            [Yrel(None) for _ in range(15)]
        self.cards: list[Minion] = []
        self.upgrade_price = [6, 7, 8, 11, 10, 0]
        self.minion_count = [3, 4, 4, 5, 5, 6]
        self.views = []
        self.reset()

    def reset(self) -> None:
        self.log.info("tavern reset")
        available_types = random.sample(list(MinionClass), 5)
        self.log.info(f"available types: {[t.value for t in available_types]}")
        self.cards = [c for c in self.base_cards if any(t in available_types for t in c.classes) or len(c.classes) == 0]
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
    
    def available_cards(self) -> list[Minion]:
        available_cards = [c for c in self.cards if not any(c in view.cards for view in self.views)]
        return available_cards
    
    def roll(self, view: CardSet, count: int) -> list[Minion]:
        view.clear()
        available_cards = self.available_cards()
        chosen = random.sample(available_cards, count)
        for card in chosen:
            view.add(card, len(view))
        return view
    
    def buy(self, card: Minion) -> Minion:
        self.cards.remove(card)
        self.log.debug(f"bought {card}")
        return card
    
    def sell(self, card: Minion) -> None:
        self.log.debug(f"sold {card}")
        card.attack_perm_boost = 0
        card.health_perm_boost = 0
        card.attack_temp_boost = 0
        card.health_temp_boost = 0
        card.clear_hooks()
        if any([isinstance(card, card_class) for card_class in self.NOT_SELLABLE]):
            return
        if card.triplet:
            for c in card.contains:
                self.cards.append(c)
        else:
            self.cards.append(card)
        for c in card.magnited:
            self.cards.append(c)