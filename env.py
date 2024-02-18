import numpy as np

from gymnasium import Env
from gymnasium.spaces import Discrete, Box, Dict, Tuple, MultiBinary
import gymnasium.spaces as spaces
from pettingzoo.utils.env import ParallelEnv
from models.game import Game


from models.player import Player
from models.tavern import Tavern

class HSPlayer(Env):
    metadata = {
        "name": "hearthstone_player_environment_v0",
    }

    def __init__(self) -> None:
        super().__init__()
        self.player = Player()
        self.actions = 0
        self._observation_space = Dict({
            "player_data": Dict({
                "level": Box(low=1, high=6),
                "gold": Box(low=0, high=50, dtype=np.int64),
                "health": Box(low=-30, high=50, dtype=np.int64),
                "tavern_not_upgraded_for": Box(low=0, high=50, dtype=np.int64),
                "tavern_upgrade_price": Box(low=0, high=15, dtype=np.int64),
                "turn": Box(low=0, high=50, dtype=np.int64),
                "blood_gem_attack": Box(low=1, high=30, dtype=np.int64),
                "blood_gem_health": Box(low=1, high=30, dtype=np.int64),
                "free_rolls": Box(low=0, high=3, dtype=np.int64),
            }),
            "hand_data": Tuple([
                Dict({
                    "available": Discrete(2),
                    "type": Discrete(3),
                    "minion_id": Discrete(30, start=-1),
                    "spell_id": Discrete(4, start=-1),
                    "card_class": MultiBinary(10),
                    "features": MultiBinary(8),
                    "health": Box(low=-10000, high=10000, dtype=np.int64),
                    "attack": Box(low=-10000, high=10000, dtype=np.int64),
                    "level": Box(low=0, high=6)
                }) for _ in range(10)
            ]),
            "board_data": Tuple([
                Dict({
                    "available": Discrete(2),
                    "type": Discrete(3),
                    "minion_id": Discrete(30, start=-1),
                    "spell_id": Discrete(4, start=-1),
                    "card_class": MultiBinary(10),
                    "features": MultiBinary(8),
                    "health": Box(low=-10000, high=10000, dtype=np.int64),
                    "attack": Box(low=-10000, high=10000, dtype=np.int64),
                    "level": Box(low=0, high=6)
                }) for _ in range(7)
            ]),
            "tavern_data": Tuple([
                Dict({
                    "available": Discrete(2),
                    "type": Discrete(3),
                    "minion_id": Discrete(30, start=-1),
                    "spell_id": Discrete(4, start=-1),
                    "card_class": MultiBinary(10),
                    "features": MultiBinary(8),
                    "health": Box(low=-10000, high=10000, dtype=np.int64),
                    "attack": Box(low=-10000, high=10000, dtype=np.int64),
                    "level": Box(low=0, high=6)
                }) for _ in range(6)
            ])
        })
        self.action_space = Discrete(len(self.player.all_actions))
        assert isinstance(self.action_space, Discrete)
        self.observation_space = spaces.flatten_space(self._observation_space)
        self.observation_space = Dict(
            {
                "action_mask": Box(0.0, 1.0, shape=(self.action_space.n,)),
                "observations": self.observation_space,
            }
        )
        self.valid_actions = [1 if a else 0 for a in self.player.available_actions]

    def start_turn(self) -> None:
        self.player.start_turn()
        self.valid_actions = [1 if a else 0 for a in self.player.available_actions]

    def observation(self) -> dict:
        return {
            "action_mask": np.array([1 if i else 0 for i in self.player.available_actions], dtype=np.float32),
            "observations": np.array(spaces.flatten(self._observation_space, self.player.observation),dtype=np.float32)
        }

    def reset(self, *, seed=None, options=None):
        self.player.tavern.del_view(self.player.view)
        self.player = Player()
        self.start_turn()
        return self._fix_action_mask(self.observation()), {}

    def step(self, action):
        self.actions += 1
        if not self.valid_actions[action]:
            return self.observation(), -1, False, False, {}
            # raise ValueError(
            #     f"Invalid action sent to env! " f"valid_actions={self.valid_actions}" f" sent={action}"
            # )
        self.player.all_actions[action]()
        obs = self.observation()
        rew = 0
        done = True if action == 0 else False
        truncated = False
        info = {}
        self.valid_actions = [1 if a else 0 for a in self.player.available_actions]
        if self.actions > 50:
            self.valid_actions = [0 for a in self.player.available_actions]
            self.valid_actions[0] = 1
        self._fix_action_mask(obs)
        return obs, rew, done, truncated, info
    
    def _fix_action_mask(self, obs):
        # Fix action-mask: Everything larger 0.5 is 1.0, everything else 0.0.
        self.valid_actions = np.round(obs["action_mask"])
        obs["action_mask"] = self.valid_actions

class HSEnv(ParallelEnv):
    metadata = {
        "name": "hearthstone_environment_v0",
    }

    def __init__(self):
        self.player_count = 8
        self.players = {f"player_{i}": HSPlayer() for i in range(self.player_count)}
        self.agents = list(self.players.keys())
        self._agent_ids = self.agents
        self.possible_agents = set(self.agents)
        self.dead = set()
        self.terminateds = set()
        self.truncateds = set()
        self.observation_spaces = {
            i: self.players[i].observation_space for i in self.agents
        }
        self.action_spaces = {
            i: self.players[i].action_space for i in self.agents
        }

    def observation_space(self, agent):
        return self.observation_spaces[agent]

    def action_space(self, agent):
        return self.action_spaces[agent]

    def seed(self, seed):
        pass

    def reset(self, *, seed=None, return_info=True, options=None):
        d = {}
        tav = Tavern()
        tav.reset()
        self.truncateds = set()
        self.terminateds = set()
        self.dead = set()
        for i in self.agents:
            self.players[i].reset()
            d[i] = self.players[i].observation()
        return d, {}
    
    def step(self, action_dict):
        assert len(action_dict) > 0
        # obs - still playing
        obs, rew, terminated, truncated, info = {}, {}, {}, {}, {}
        for i, action in action_dict.items():
            if i in self.dead:
                continue
            obs[i], rew[i], done, truncated[i], _ = self.players[i].step(action)
            if done:
                self.terminateds.add(i)
                obs.pop(i)
            if truncated[i]:
                self.truncateds.add(i)
        terminated["__all__"] = len(self.terminateds) + len(self.dead)== len(self.agents)
        truncated["__all__"] = len(self.truncateds) == len(self.agents)
        if terminated["__all__"]:
            terminated["__all__"] = False
            g = Game([self.players[e].player for e in self.players])
            g.battle()
            for i in self.agents:
                if i in self.dead:
                    continue
                self.players[i].start_turn()
                self.players[i].actions = 0
                obs[i] = self.players[i].observation()
                hmax = max([self.players[i].player.health for i in self.players])
                rew[i] = self.players[i].player.health - hmax + 5
                terminated[i] = self.players[i].player.health <= 0
                if terminated[i]:
                    self.dead.add(i)
                    obs.pop(i)
            self.terminateds = set()
            self.truncateds = set()
        if len(self.dead) == self.player_count - 1:
            terminated["__all__"] = True
            for i in self.agents:
                terminated[i] = True
        return obs, rew, terminated, truncated, info