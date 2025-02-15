# stable-retro scripts

Note: Migrated to pytorch and stable-baselines3. The old tensorflow + original stable-baselines is now in TF1 branch.

* Train models on retro games
* Pit two models against each other on PvP retro games such as NHL94, Mortal Kombat or WWF Wrestlemania: The Arcade Game
* Play against an improved AI opponent


![screenshot 01](./screenshot01.png)
![wwf vs](./vs_screenshot.png)

## Installation

Tested on Ubuntu 22.04 and Windows 11 WSL2 (Ubuntu 22.04 VM)

Requires:
*   Python 3.7 and up
*   stable-baselines3 with gymnasium support
*   stable-retro with gymnasium support (fork of gym-retro)

```
sudo apt update
sudo apt-get install python3 python3-pip git zlib1g-dev libopenmpi-dev ffmpeg cmake

pip3 install git+https://github.com/Farama-Foundation/stable-retro.git
pip3 install "stable_baselines3[extra]" pygame torchsummary

git clone https://github.com/MatPoliquin/stable-retro-scripts.git
cd stable-retro-scripts
```

## Install roms
You need to provide your own roms

In your rom directory exec this command, it will import the roms into stable-retro
```
python3 -m retro.import .
```

Currently there is two NHL 94 env in stable-retro: The original game and the '1 on 1' rom hack which as the name implies is for 1 on 1 matches instead of full teams

## Examples

*   For NHL94 specific page click [here](./NHL94-README.md)
*   For Wrestlemania the arcade game specific page click [here](./WWF-README.md)

### Train a model
Note: Airstriker is a public domain rom and is already included in stable-retro
```bash
python3 model_trainer.py --env=Airstriker-Genesis --num_env=8 --num_timesteps=100_000_000 --play
```


## Devlog

For NHL94:
https://youtube.com/playlist?list=PLmwlWbdWpZVtH6NXqWbrnWOf6SWv9nJBY

NHL94 Discord (with a subgroup dedicated for AI):
https://discord.gg/SDnKEXujDs
