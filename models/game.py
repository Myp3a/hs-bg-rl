import random

from .field import Field
from .player import Player


class Game:
    players: list[Player]
    alive_players: list[Player]
    dead_players: list[Player]
    def __init__(self,players) -> None:
        self.players = players
        self.sort()

    def sort(self) -> None:
        self.alive_players = sorted([p for p in self.players if p.health > 0], key=lambda p: p.health, reverse=True)
        self.dead_players = sorted([p for p in self.players if p.health <= 0], key=lambda p: p.turn, reverse=True)

    def prepare(self) -> None:
        for p in self.players:
            if p.health > 0:
                p.start_turn()
                p.act_random()

    def battle(self) -> None:
        player_ids = [self.players.index(p) for p in self.alive_players]
        random.shuffle(player_ids)
        if len(player_ids) % 2 == 1:
            player_ids.append(self.players.index(self.dead_players[0]))
        for i in range(int(len(player_ids) / 2)):
            p1 = self.players[player_ids[i*2]]
            p2 = self.players[player_ids[i*2+1]]
            p1.end_turn()
            p2.end_turn()
            b = Field(p1, p2)
            b.fight()
                
        # for i in range(len(self.players)):
        #     print(f"player {i}: {self.players[i].health} hp")

    def run(self) -> None:
        while len(self.alive_players) > 1:
            self.prepare()
            self.battle()
            self.sort()
