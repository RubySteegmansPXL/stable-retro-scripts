# Wrestlemania the arcade game


Train Yokozuna Model:
```
python3 model_trainer.py --env=WWFArcade-Genesis --state=VeryHard_YokozunaVsShawnMicheals --num_timesteps=5000000 --play
```

Train Shawn Micheals Model:
```
python3 model_trainer.py --env=WWFArcade-Genesis --state=VeryHard_ShawnMichealsVsYokozuna --num_timesteps=5000000 --play
```

The models (zip files) should reside in the output directory (by default in the /home directory)


### Pit your two models against each other
```
python3 model_vs_model.py --env=WWFArcade-Genesis --load_p1_model=~/yokozuna.zip --load_p2_model=~/shawn_micheals.zip
```

### Game specific training script to beat WWF (Continental mode)
```
python3 wwf_trainer.py --play
```


### Play pre-trained model
```
python3 model_vs_game.py --env=WWFArcade-Genesis --state=VeryHard_YokozunaVsShawnMicheals --load_p1_model=~/yokozuna.zip
```
