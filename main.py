import os

import ray
from ray.rllib.algorithms.ppo import PPOConfig
from ray.rllib.env.wrappers.pettingzoo_env import ParallelPettingZooEnv
from ray.tune.registry import register_env
from ray import tune
from ray.rllib.models import ModelCatalog

from env import HSEnv
from model import TorchActionMaskModel
from ray.rllib.core.rl_module.rl_module import SingleAgentRLModuleSpec

ray.init()
env = HSEnv()
env_name = "hs_env"
register_env(env_name, lambda config: ParallelPettingZooEnv(env))
ModelCatalog.register_custom_model("HSModel", TorchActionMaskModel)

config = (
        PPOConfig()
        .environment(env=env_name, clip_actions=True, disable_env_checking=False)
        .rollouts(num_rollout_workers=0, rollout_fragment_length="auto")
        .training(
            train_batch_size=2048,
            lr=2e-5,
            gamma=0.99,
            lambda_=0.9,
            use_gae=True,
            clip_param=0.4,
            grad_clip=None,
            entropy_coeff=0.1,
            vf_loss_coeff=0.25,
            sgd_minibatch_size=64,
            num_sgd_iter=10,
            model={
                "custom_model": "HSModel"
            }
        )
        .debugging(log_level="INFO")
        .framework(framework="torch")
        .resources(num_gpus=0)
    )

tune.run(
        "PPO",
        name="PPO",
        stop={"timesteps_total": 5000000},
        checkpoint_freq=10,
        local_dir=os.getcwd() + "/ray_results/" + env_name,
        config=config.to_dict(),
    )