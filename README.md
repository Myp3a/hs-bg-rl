# Hearthstone Battlegrounds Reinforcement Learning
A project to make neural-powered Hearthstone Battlegrounds bot.  
> Temporarily frozen at season 6 until TODO is done.

# Features
 - Tier 1-6 minions
 - Shared tavern minion pool with class randomization
 - Battle simulator with player opponents shuffle
 - Ability to create specific battle situations
 - RLlib model training with parallel games and GPU

# Needs checking
 - Features save/restore
 - Triplet hooks management
 - Beast hook order
 - Eternal knight triplet / boost existing
 - Impulsive trickster infight health boost
 - Perm / Temp values gain depending if in battle
 - Mad matador mechanics

# TODO
 - Unify hook function names for getattr
 - Shadow classes
 - Health-depleting actions blocking when 1hp
 - Murozond
 - Logging
 - Chain magnetic deathrattles
 - Targeted battlecry
 - Discover mechanic
 - Tavern spells
 - Heroes
 - Instant attack triggers before deathrattles
 - Tweak reward function
 - CLI interface for playing with AI

# Training notes
### 5 000 000 steps
 - Bots can reach 50+ stats on minions
 - Almost always tavern is upgraded to l3
 - After l3 only half of players upgrade to next tier for every tier respectively
 - Table contains 6-7 minions
 - Cards aren't piling in hand

# How to use
### Training
Install dependencies
```
pip install -r requirements.txt
```
Run command to start training session
```
python main.py
```
To change training steps count or used CPU cores / GPUs, edit values in `main.py`.  
To tweak reward function, edit `env.py` `rew[i]` function at line 204.