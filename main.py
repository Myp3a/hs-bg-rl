import os
import logging

import ray
from ray.rllib.algorithms.ppo import PPOConfig
from ray.rllib.env.wrappers.pettingzoo_env import ParallelPettingZooEnv
from ray.tune.registry import register_env
from ray import tune
from ray.rllib.models import ModelCatalog

from env import HSEnv
from model import TorchActionMaskModel

ray.init(num_gpus=1)

env = HSEnv(logging.DEBUG)
env_name = "hs_env"
register_env(env_name, lambda config: env)
ModelCatalog.register_custom_model("HSModel", TorchActionMaskModel)

config = (
        PPOConfig()
        .environment(env=env_name, clip_actions=True, disable_env_checking=True)
        .rollouts(num_rollout_workers=10, rollout_fragment_length="auto")
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
        .debugging(log_level="DEBUG")
        .framework(framework="torch")
        .resources(num_gpus=1)
    )

tune.run(
        "PPO",
        name="PPO",
        stop={"timesteps_total": 5000000},
        checkpoint_freq=10,
        config=config.to_dict(),
        resume="AUTO",
        #log_to_file=True,  # Doesn't work, logs are stored in /tmp/ray | %TEMP%\ray
        local_dir=os.getcwd() + "/ray_results/" + env_name,  # Disable saving to ~/ray_results
        storage_path=os.getcwd() + "/ray_results/" + env_name,  # Proper way of setting storage path
    )