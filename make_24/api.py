"""
API
"""

from make_24.gametree import GameDriver


def make_24(*args, goal=24):
    game = GameDriver(*args, goal=goal)
    game.run()
