"""
API
"""

from make_24.gametree import GameDriver


def make_24(*args, goal=24):
    game = GameDriver(*args)
    found = game.run()
    if not found:
        print("No solution was found.")
