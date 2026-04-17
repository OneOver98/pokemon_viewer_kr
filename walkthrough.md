# PvPoke RL Environment - Walkthrough

## Overview

We have successfully bridged the open-source Pokémon GO battle simulator (PvPoke) into a Python-native Reinforcement Learning environment using `stable-baselines3`, `Gymnasium`, and `Node.js`.

### Changes Made

1. **[NEW] [ai_pipeline/pvpoke_env.js](file:///c:/Users/jake/ai_1o/ai_pipeline/pvpoke_env.js)**: 
   A headless wrapper running in Node.js. It reads the source JS files from `pvpoke/src/js/` and utilizes `vm.runInContext` to evaluate the globals (`Battle`, `Pokemon`, `GameMaster`). It overrides `$.ajax` to synchronously fetch `GameMaster` definitions from `pvpoke/src/data/`. Afterwards, it loops over `process.stdin`, parsing JSON action commands from Python, issuing `battle.queueAction`, advancing `battle.step()`, and replying with the JSON state (HP, Energy, Shields, Cooldowns, Buffs).

2. **[NEW] `ai_pipeline/pvpoke_gym.py`**:
   A Gymnasium `Env` class that spawns `node pvpoke_env.js` as a subprocess. It maps RL actions (spaces.Discrete) into PvPoke JSON payloads and scales the state down to a normalized `spaces.Box` observation (scale of 0.0 to 1.0). The reward correctly utilizes HP differential. 

3. **[NEW] `ai_pipeline/train.py`**:
   A training script leveraging `stable-baselines3`'s `PPO`. It creates parallel environments scaling horizontally with the user's multi-core CPU via `SubprocVecEnv` (up to 8 environments). The network inherently delegates PyTorch computation to the RTX 3060 CUDA GPU.

### Verification Results

The test execution of `python train.py` revealed:

1. **Successful Initialization**: Node.js processes properly booted, loading 1710 Pokémon species into the `GameMaster` state completely headlessly (without needing browser APIs).
2. **Synchronous Multiprocessing**: Handshaking was successful across 8 vectorized Gym instances simultaneously. 
3. **Training Iteration**: Python properly batched inputs and outputs using IO pipes, converting JSON into Float32 observation Tensors, executing steps seamlessly.

> [!NOTE]
> Currently, PyTorch in this venv is defaulting to the `cpu` variant. To utilize your RTX 3060 fully, simply install the `cu118` or `cu121` wheel of PyTorch inside your `ai_pipeline` working directory:  
> `pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118`
> The `train.py` script possesses `device="cuda" if torch.cuda.is_available() else "cpu"`, so it will automatically run on the GPU after installing the `cu118` version.

### Future Work

The current script uses Azumarill vs Skarmory as standard fixed Pokémon, and only Fast / Charged Attack actions. You can extend `pvpoke_gym.py` later to cover `Switch` mechanics or randomize matchups in `reset()`.
