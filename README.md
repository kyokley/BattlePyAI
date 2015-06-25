# BattlePy AI

This repo provides a starting point for developing an AI strategy to run on the BattlePy engine.

## Getting Started
1. Clone the repo
    git clone https://github.com/kyokley/BattlePyAI.git
    cd BattlePyAI

2. Create a new virtualenv for the game engine
    virtualenv -p python2.7 battlepy
    source battlepy/bin/activate

3. Install the necessary requirements
    pip install -r requirements.txt

4. At this point, you should be able to run main. This will run 1000 games of the RandomPlayer versus itself.
    python main.py

## Creating a new AI
To create a new AI, it is useful to use the RandomPlayer class as a guide. Every AI must inherit from the battlePy.player.Player class. There are a couple of classes that must be defined at a minimum for an AI to be valid.
