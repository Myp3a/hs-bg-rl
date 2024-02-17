from cards.spell import Spell


class GoldCoin(Spell):
    def __init__(self, player) -> None:
        super().__init__(player)

    def play(self, target: None) -> None:
        self.player.gold += 1