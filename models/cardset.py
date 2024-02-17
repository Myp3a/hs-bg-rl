from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import MinionClass, Minion

if TYPE_CHECKING:
    from .card import Card
    from .player import Player

class CardSet:
    def __init__(self, player) -> None:
        self.player: Player = player
        self.cards: list[Card] = []
        self.max_len = 0

    def __len__(self) -> int:
        return len(self.cards)
    
    def __getitem__(self, ind):
        return self.cards[ind]
    
    def __str__(self) -> str:
        return " ".join([str(c) for c in self.cards])

    def index(self, card: Card) -> int:
        if card in self.cards:
            return self.cards.index(card)
        return -1
    
    def add(self, card: Card, index: int) -> bool:
        if len(self.cards) >= self.max_len:
            return False
        self.cards.insert(index, card)
        return True
    
    def remove(self, card: Card) -> bool:
        if card in self.cards:
            self.cards.remove(card)
            return True
        return False
    
    def clear(self) -> None:
        self.cards = []

    @property
    def observation(self) -> tuple:
        l = []
        for i in range(self.max_len):
            if i >= len(self.cards):
                l.append({
                    "available": 0,
                    "type": 0,
                    "minion_id": -1,
                    "spell_id": -1,
                    "card_class": [0,0,0,0,0,0,0,0,0,0],
                    "features": [0,0,0,0,0,0,0,0],
                    "health": 0,
                    "attack": 0,
                    "level": 0
                })
            else:
                l.append({
                    "available": 1,
                    "type": 0 if isinstance(self.cards[i], Minion) else 1,
                    "minion_id": self.cards[i].minion_id,
                    "spell_id": self.cards[i].spell_id,
                    "card_class": [
                        MinionClass.Beast in self.cards[i].classes,
                        MinionClass.Demon in self.cards[i].classes,
                        MinionClass.Dragon in self.cards[i].classes,
                        MinionClass.Elemental in self.cards[i].classes,
                        MinionClass.Mech in self.cards[i].classes,
                        MinionClass.Murloc in self.cards[i].classes,
                        MinionClass.Naga in self.cards[i].classes,
                        MinionClass.Pirate in self.cards[i].classes,
                        MinionClass.Quilboar in self.cards[i].classes,
                        MinionClass.Undead in self.cards[i].classes,
                    ] if isinstance(self[i], Minion) else [0,0,0,0,0,0,0,0,0,0],
                    "features": [
                        1 if len(self.cards[i].hooks["battlecry"]) > 0 else 0,
                        1 if len(self.cards[i].hooks["deathrattle"]) > 0 else 0,
                        self.cards[i].taunt,
                        self.cards[i].divine_shield,
                        self.cards[i].toxic,
                        self.cards[i].rebirth,
                        0,
                        0,
                    ] if isinstance(self[i], Minion) else [0,0,0,0,0,0,0,0],
                    "health": self.cards[i].health_value if isinstance(self.cards[i], Minion) else 0,
                    "attack": self.cards[i].attack_value if isinstance(self.cards[i], Minion) else 0,
                    "level": self.cards[i].level if isinstance(self.cards[i], Minion) else 0,
                })