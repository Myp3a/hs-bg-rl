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
    def __init__(self, loglevel) -> None:
        self.log = logging.getLogger("tavern")
        self.log.setLevel(loglevel)
        logging.basicConfig()
        self.NOT_SELLABLE = [
            Skeleton,
            Imp,
            Cubling,
            SkyPirate,
            WaterDroplet,
            Crab,
            HalfShell,
            HelpingHand,
            Microbot,
            Smolderwing,
            GoldenMonkey,
            RustedReggie,
            MagtheridonPrime,
            Baltharak,
            Mechorse,
            Mechapony
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
            [CracklingCyclone(None) for _ in range(15)] + \
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
            [Yrel(None) for _ in range(15)] + \
            [AccordOTron(None) for _ in range(13)] + \
            [AmberGuardian(None) for _ in range(13)] + \
            [BloodsailCannoneer(None) for _ in range(13)] + \
            [DeflectOBot(None) for _ in range(13)] + \
            [DiremuckForager(None) for _ in range(13)] + \
            [Dreadbeard(None) for _ in range(13)] + \
            [Eagill(None) for _ in range(13)] + \
            [ElectricSynthesizer(None) for _ in range(13)] + \
            [FacelessDisciple(None) for _ in range(13)] + \
            [Felemental(None) for _ in range(13)] + \
            [FreeFlyingFeathermane(None) for _ in range(13)] + \
            [GunpowderCourier(None) for _ in range(13)] + \
            [HandlessForsaken(None) for _ in range(13)] + \
            [LegionOverseer(None) for _ in range(13)] + \
            [LivingConstellation(None) for _ in range(13)] + \
            [MangledBandit(None) for _ in range(13)] + \
            [MonstrousMacaw(None) for _ in range(13)] + \
            [MoonBaconJazzer(None) for _ in range(13)] + \
            [Mummifier(None) for _ in range(13)] + \
            [NetherDrake(None) for _ in range(13)] + \
            [PaintSmudger(None) for _ in range(13)] + \
            [PartyElemental(None) for _ in range(13)] + \
            [PashmarTheVengeful(None) for _ in range(13)] + \
            [PhaerixWrathOfTheSun(None) for _ in range(13)] + \
            [PricklyPiper(None) for _ in range(13)] + \
            [RecyclingWraith(None) for _ in range(13)] + \
            [ReplicatingMenace(None) for _ in range(13)] + \
            [SoreLoser(None) for _ in range(13)] + \
            [SprightlyScarab(None) for _ in range(13)] + \
            [TheGladIator(None) for _ in range(13)] + \
            [VengefulSlitherer(None) for _ in range(13)] + \
            [WildfireElemental(None) for _ in range(13)] + \
            [ZestyShaker(None) for _ in range(13)] + \
            [AnnoyOModule(None) for _ in range(11)] + \
            [AnubarakNerubianKing(None) for _ in range(11)] + \
            [AudaciousAnchor(None) for _ in range(11)] + \
            [Bannerboar(None) for _ in range(11)] + \
            [Bassgill(None) for _ in range(11)] + \
            [BazaarDealer(None) for _ in range(11)] + \
            [BladeCollector(None) for _ in range(11)] + \
            [BreamCounter(None) for _ in range(11)] + \
            [DaggerspineThrasher(None) for _ in range(11)] + \
            [DeepBlueCrooner(None) for _ in range(11)] + \
            [DisguisedGraverobber(None) for _ in range(11)] + \
            [EmergentFlame(None) for _ in range(11)] + \
            [FloatingWatcher(None) for _ in range(11)] + \
            [FlourishingFrostling(None) for _ in range(11)] + \
            [GeomagusRoogug(None) for _ in range(11)] + \
            [LandLubber(None) for _ in range(11)] + \
            [LighterFighter(None) for _ in range(11)] + \
            [LivingAzerite(None) for _ in range(11)] + \
            [LovesickBalladist(None) for _ in range(11)] + \
            [MalchezaarPrinceOfDance(None) for _ in range(11)] + \
            [MamaBear(None) for _ in range(11)] + \
            [MenagerieJug(None) for _ in range(11)] + \
            [MysticSporebat(None) for _ in range(11)] + \
            [OutbackSmolderer(None) for _ in range(11)] + \
            [PeckishFeldrake(None) for _ in range(11)] + \
            [PeggySturdybone(None) for _ in range(11)] + \
            [PrimalfinLookout(None) for _ in range(11)] + \
            [RazorgoreTheUntamed(None) for _ in range(11)] + \
            [RendleTheMistermind(None) for _ in range(11)] + \
            [RylakMetalhead(None) for _ in range(11)] + \
            [SaloonDancer(None) for _ in range(11)] + \
            [SilentSwimmer(None) for _ in range(11)] + \
            [SindoreiStraightShot(None) for _ in range(11)] + \
            [SlyRaptor(None) for _ in range(11)] + \
            [SnarlingConductor(None) for _ in range(11)] + \
            [SteadfastSpirit(None) for _ in range(11)] + \
            [StrongshellScavenger(None) for _ in range(11)] + \
            [TreasureSeekerElise(None) for _ in range(11)] + \
            [TunnelBlaster(None) for _ in range(11)] + \
            [UtilityDrone(None) for _ in range(11)] + \
            [WaywardGrimscale(None) for _ in range(11)] + \
            [AugmentedLaborer(None) for _ in range(9)] + \
            [BananaSlamma(None) for _ in range(9)] + \
            [BongoBopper(None) for _ in range(9)] + \
            [BrannBronzebeard(None) for _ in range(9)] + \
            [BristlebackKnight(None) for _ in range(9)] + \
            [ChampionOfThePrimus(None) for _ in range(9)] + \
            [CorruptedMyrmidon(None) for _ in range(9)] + \
            [CritterWrangler(None) for _ in range(9)] + \
            [DrakkariEnchanter(None) for _ in range(9)] + \
            [EnsorcelledFungus(None) for _ in range(9)] + \
            [GeneralDrakkisath(None) for _ in range(9)] + \
            [GentleDjinni(None) for _ in range(9)] + \
            [Glowscale(None) for _ in range(9)] + \
            [HungeringAbomination(None) for _ in range(9)] + \
            [HunterOfGatherers(None) for _ in range(9)] + \
            [InsatiableUrzul(None) for _ in range(9)] + \
            [KangorsApprentice(None) for _ in range(9)] + \
            [KingBagurgle(None) for _ in range(9)] + \
            [MadMatador(None) for _ in range(9)] + \
            [MasterOfRealities(None) for _ in range(9)] + \
            [MechanizedGiftHorse(None) for _ in range(9)] + \
            [MoroesStewardOfDeath(None) for _ in range(9)] + \
            [Murozond(None) for _ in range(9)] + \
            [OperaticBelcher(None) for _ in range(9)] + \
            [RapscallionRecruiter(None) for _ in range(9)] + \
            [RecordSmuggler(None) for _ in range(9)] + \
            [RodeoPerformer(None) for _ in range(9)] + \
            [SandstoneDrake(None) for _ in range(9)] + \
            [ScrapScraper(None) for _ in range(9)] + \
            [SpellboundSeafarer(None) for _ in range(9)] + \
            [Tichondrius(None) for _ in range(9)] + \
            [TitusRivendare(None) for _ in range(9)] + \
            [TortollanBlueShell(None) for _ in range(9)] + \
            [TransmutedBramblewitch(None) for _ in range(9)] + \
            [UnderhandedDealer(None) for _ in range(9)] + \
            [AdmiralElisaGoreblade(None) for _ in range(6)] + \
            [ArchlichKelthuzad(None) for _ in range(6)] + \
            [Bristlebach(None) for _ in range(6)] + \
            [Charlga(None) for _ in range(6)] + \
            [ChoralMrrrglr(None) for _ in range(6)] + \
            [CultistSthara(None) for _ in range(6)] + \
            [Deadstomper(None) for _ in range(6)] + \
            [ElementalOfSurprise(None) for _ in range(6)] + \
            [EternalSummoner(None) for _ in range(6)] + \
            [FamishedFelbat(None) for _ in range(6)] + \
            [Felboar(None) for _ in range(6)] + \
            [FleetAdmiralTethys(None) for _ in range(6)] + \
            [FoeReaper4000(None) for _ in range(6)] + \
            [Ghastcoiler(None) for _ in range(6)] + \
            [GoldrinnTheGreatWolf(None) for _ in range(6)] + \
            [HawkstriderHerald(None) for _ in range(6)] + \
            [IgnitionSpecialist(None) for _ in range(6)] + \
            [KalecgosArcaneAspect(None) for _ in range(6)] + \
            [MantidQueen(None) for _ in range(6)] + \
            [MotleyPhalanx(None) for _ in range(6)] + \
            [Murky(None) for _ in range(6)] + \
            [NalaaTheRedeemer(None) for _ in range(6)] + \
            [OmegaBuster(None) for _ in range(6)] + \
            [PolarizingBeatboxer(None) for _ in range(6)] + \
            [RockRock(None) for _ in range(6)] + \
            [SilivazTheVindictive(None) for _ in range(6)] + \
            [SlitherspearLordOfGains(None) for _ in range(6)] + \
            [TheWalkingFort(None) for _ in range(6)] + \
            [Warpwing(None) for _ in range(6)] + \
            [WhirlingLassOMatic(None) for _ in range(6)] + \
            [YoungMurkeye(None) for _ in range(6)] + \
            [ZappSlywick(None) for _ in range(6)]
        self.cards: list[Minion] = []
        self.upgrade_price = [6, 7, 8, 11, 10, 0]
        self.minion_count = [3, 4, 4, 5, 5, 6]
        self.views = []
        self.log.info("tavern init")
        self.available_types = random.sample(list(MinionClass), 5)
        self.log.info(f"available types: {[t.value for t in self.available_types]}")
        self.cards = [c for c in self.base_cards if any(t in self.available_types for t in c.classes) or len(c.classes) == 0]
        self.views = []

    def check_duplicates(self) -> None:
        seen = set()
        dupes = []
        for x in self.cards:
            if x in seen:
                dupes.append(x)
            else:
                seen.add(x)
        assert len(self.cards) == len(set(self.cards)), "Duplicate card in tavern! " + str([str(obj) for obj in dupes])
        
    def new_view(self, player) -> CardSet:
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
    
    def roll(self, view: CardSet, count: int, level: int) -> CardSet:
        self.check_duplicates()
        view.clear()
        available_cards = [c for c in self.available_cards() if c.level <= level]
        chosen = random.sample(available_cards, count)
        for card in chosen:
            view.add(card, len(view))
        return view
    
    def clean_card(self, card: Minion):
        card.reset_turn_start()
        card.clean_overrides()
        return card

    def buy(self, card: Minion) -> Minion:
        self.log.debug(f"bought {card}")
        self.clean_card(card)  # In case if was summoned (rylak + faceless)
        if isinstance(card, GoldenMonkey):  # Not in tavern, but can be bought
            return card
        self.cards.remove(card)
        return card
    
    def sell(self, card: Minion) -> None:
        self.log.debug(f"sold {card}")
        self.clean_card(card)
        if any([isinstance(card, card_class) for card_class in self.NOT_SELLABLE]) or card.not_sellable:
            return
        for c in card.contains:
            self.sell(c)
        card.contains = []
        if not card.triplet:
            self.cards.append(card)
        for c in card.magnited:
            c.magnited_to = None
            self.sell(c)
        card.magnited = []
        self.check_duplicates()
