from cheatWall import CheatWall
from memory import MemoryManager
from staticInfo import *
from __init__ import *
from gui import PokemonGUI


def main():
    mm = MemoryManager("pokemonAddress.json")
    cheatWall = CheatWall(mm)

    gui = PokemonGUI(cheatWall)


if __name__ == '__main__':
    main()
