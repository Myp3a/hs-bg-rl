from __future__ import annotations
from typing import TYPE_CHECKING

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