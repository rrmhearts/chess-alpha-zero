# About

Chess reinforcement learning by [AlphaGo Zero](https://deepmind.com/blog/alphago-zero-learning-scratch/) methods.

This project is based in two main resources:
1) DeepMind's Oct19th publication: [Mastering the Game of Go without Human Knowledge](https://www.nature.com/articles/nature24270.epdf?author_access_token=VJXbVjaSHxFoctQQ4p2k4tRgN0jAjWel9jnR3ZoTv0PVW4gB86EEpGqTRDtpIz-2rmo8-KG06gqVobU5NSCFeHILHcVFUeMsbvwS-lxjqQGg98faovwjxeTUgZAUMnRQ).
2) The <b>great</b> Reversi development of the DeepMind ideas that @mokemokechicken did in his repo: https://github.com/mokemokechicken/reversi-alpha-zero

Note: <b>This project is still under construction!!</b>

## Environment

* Python 3.5
* tensorflow-gpu
* Keras

### Setup

#### install libraries
```bash
pip install -r requirements.txt
```

If you want use GPU,

```bash
pip install tensorflow-gpu
```

#### set environment variables (if necessary)
Create `.env` file and write this.

```text:.env
KERAS_BACKEND=tensorflow
```
## News

DeepMind just released today a new version of thr AlphaGo Zero idea (named now AlphaZero) where they mastering chess from scratch: 
https://arxiv.org/pdf/1712.01815.pdf. In fact, AlphaZero outperformed Stockfish after just 4 hours (300k steps).

There are new ideas we have to take into account for this project. It seems, for example, that two planes for feeding the input model are not enough.

### New Distributed Training Pipeline

Now it's possible to train the model in a distributed way. The only thing needed is to use the new parameter:

* `--type distributed`: use mini config for testing, (see `src/chess_zero/configs/distributed.py`)

So, in order to contribute to the distributed team you just need to run the three workers locally like this:

```bash
python src/chess_zero/run.py self --type distributed (or python src/chess_zero/run.py sl --type distributed)
python src/chess_zero/run.py opt --type distributed
python src/chess_zero/run.py eval --type distributed
```

# System Overview
## Supervised Learning

This allows the system to use data from pgn files to pretrain weights before gradient descent.
```bash
python src/chess_zero/run.py sl
```
I've done a supervised learning new pipeline step (to use those human games files "PGN" we can find in internet as play-data generator).
This SL step was also used in the first and original version of AlphaGo and maybe chess is a some complex game that we have to pre-train first the policy model before starting the self-play process (i.e., maybe chess is too much complicated for a self training alone).

To use the new SL process is so simple as running in the beginning instead of the worker "self" the new worker "sl".
Once the model converges enough with SL play-data we just stop the worker "sl" and start the worker "self" so the model will start improving now due to self-play data.

If you want to use this new SL step you will have to download from internet big PGN files (chess files) and paste them into the "data/play_data" folder.

## Reinforcement Learning

This AlphaGo Zero implementation consists of three worker `self`, `opt` and `eval`.

* `self` is Self-Play to generate training data by self-play using BestModel.
* `opt` is Trainer to train model, and generate next-generation models.
* `eval` is Evaluator to evaluate whether the next-generation model is better than BestModel. If better, replace BestModel.

## Evaluation

For evaluation, you can play chess with the BestModel. Command prompt move input with ascii visualization. Type 'exit' to leave game.

* `play_gui` is Play Game vs BestModel using ASCII character encoding.

## Data

* `data/model/model_best_*`: BestModel.
* `data/model/next_generation/*`: next-generation models.
* `data/play_data/play_*.json`: generated training data.
* `logs/main.log`: log file.
  
If you want to train the model from the beginning, delete the above directories.

# How to use

## Basic Usage

For training model, execute `Self-Play`, `Trainer` and `Evaluator`. 

### Self-Play

```bash
python src/chess_zero/run.py self
```

When executed, Self-Play will start using BestModel.
If the BestModel does not exist, new random model will be created and become BestModel.

#### options
* `--new`: create new BestModel
* `--type mini`: use mini config for testing, (see `src/chess_zero/configs/mini.py`)

### Trainer

```bash
python src/chess_zero/run.py opt
```

When executed, Training will start.
A base model will be loaded from latest saved next-generation model. If not existed, BestModel is used.
Trained model will be saved every 2000 steps(mini-batch) after epoch. 

#### options
* `--type mini`: use mini config for testing, (see `src/chess_zero/configs/mini.py`)
* `--total-step`: specify total step(mini-batch) numbers. The total step affects learning rate of training. 

### Evaluator

```bash
python src/chess_zero/run.py eval
```

When executed, Evaluation will start.
It evaluates BestModel and the latest next-generation model by playing about 200 games.
If next-generation model wins, it becomes BestModel. 

#### options
* `--type mini`: use mini config for testing, (see `src/chess_zero/configs/mini.py`)

### Play Game

```bash
python src/chess_zero/run.py play_gui
```

When executed, ordinary chess board will be displayed in ASCII code and you can play against BestModel.

# Model Performance (unfinished)

The following table is records of the best models.

|best model generation|winning percentage to best model|Time Spent(hours)|note|
|-----|-----|-----|-----|
|1|-|-|　|

## First "good" results

Using the new supervised learning step I created, I've been able to train a model to the point that seems to be learning the openings of chess. Also it seems the model starts to avoid losing naively pieces.

Here you can see an example of a game played for me against this model (AI plays black):
 
![partida1](https://user-images.githubusercontent.com/17341905/33597844-ea53c8ae-d9a0-11e7-8564-4b9b0f35a221.gif)

This model plays in this way after only 5 epoch iterations of the 'opt' worker, the 'eval' worker changed 4 times the best model (4 of 5). At this moment the loss of the 'opt' worker is 5.1 (and still seems to be converging very well).

As I have not GPU, I had to evaluate ('eval') using only "self.simulation_num_per_move = 10" and only 10 files of play data for the 'opt' worker. I'm pretty sure if anybody is able to run in a good GPU with a more powerful configuration the results after complete convergence would be really good.
