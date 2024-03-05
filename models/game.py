import logging
import random

from .tavern import Tavern

from .field import Field
from .player import Player

class Game:
    players: list[Player]
    alive_players: list[Player]
    dead_players: list[Player]
    def __init__(self, players, loglevel) -> None:
        self.loglevel = loglevel
        self.log = logging.getLogger("game")
        self.log.setLevel(loglevel)
        logging.basicConfig()
        self.players = players
        self.sort()

    def sort(self) -> None:
        self.alive_players = sorted([p for p in self.players if p.health > 0], key=lambda p: p.health, reverse=True)
        self.dead_players = sorted([p for p in self.players if p.health <= 0], key=lambda p: p.turn, reverse=True)

    def prepare(self) -> None:
        for p in self.players:
            p.start_turn()
            if p.health > 0:
                p.act_random()

    def battle(self) -> None:
        self.check_duplicates()
        player_ids = [self.players.index(p) for p in self.alive_players]
        random.shuffle(player_ids)
        if len(player_ids) % 2 == 1:
            player_ids.append(self.players.index(self.dead_players[0]))
        for i in range(int(len(player_ids) / 2)):
            p1 = self.players[player_ids[i*2]]
            p2 = self.players[player_ids[i*2+1]]
            p1.end_turn()
            p2.end_turn()
            b = Field(p1, p2, self.loglevel)
            b.fight()
                
        # for i in range(len(self.players)):
        #     print(f"player {i}: {self.players[i].health} hp")

    def run(self) -> None:
        self.log.info("starting new game")
        while len(self.alive_players) > 1:
            self.log.debug("starting turn")
            self.prepare()
            self.battle()
            self.sort()
            self.log.debug("turn end")
            self.log.info(f"alive: {[p for p in self.alive_players]}")
            self.log.info(f"dead: {[p for p in self.dead_players]}")

    def check_duplicates(self) -> None:
        l = []
        t = Tavern(self.loglevel)
        for p in self.players:
            l += p.all_visible_cards()
        l += t.available_cards()
        seen = set()
        dupes = []
        for x in l:
            if x in seen:
                dupes.append(x)
            else:
                seen.add(x)
        assert len(set(l)) == len(l), "Duplicate card found! " + str([str(obj) for obj in dupes])