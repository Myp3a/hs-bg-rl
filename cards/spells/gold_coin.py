from cards.spell import Spell


class GoldCoin(Spell):
    def __init__(self, player, triplet=False) -> None:
        super().__init__(player, triplet)
        self.spell_id = 1

    def play(self, target: None) -> None:
        self.player.gold += 1
        for hook in self.player.army.hooks["on_gold_get"]:
            hook(1)
