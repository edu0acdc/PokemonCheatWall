import json
from core import Pokemon
from pymem import Pymem


class MemoryManager():
    def __init__(self, filePath):
        f = open(filePath)
        self.memoryInfo = json.load(f)
        f.close()
        self.firstPokemonAdress = -1
        self.pokemons = []
        self.pm = Pymem('VisualBoyAdvance.exe')
        self.getFirstPokemonAddress()
        self.createPokemons()

    def writePokemon(self, position=1):
        print(int.from_bytes(self.pm.read_bytes(int('0x19F23E', 16), 1), 'little'))
        position -= 1
        pokemon = self.pokemons[position]
        pokemonOffset = 100*position
        for attr in self.memoryInfo['attributes']:
            attr_offset = int(
                self.memoryInfo['attributes'][attr]['offset'])
            addr = self.firstPokemonAdress + attr_offset + pokemonOffset
            attr_size = int(
                self.memoryInfo['attributes'][attr]['size'])
            val = int(pokemon.attributes[attr], 16).to_bytes(
                attr_size, 'little')
            self.pm.write_bytes(addr, val, attr_size)

    def writeAll(self):
        pokemonOffset = 0
        for pokemon in self.pokemons:
            for attr in self.memoryInfo['attributes']:
                attr_offset = int(
                    self.memoryInfo['attributes'][attr]['offset'])
                addr = self.firstPokemonAdress + attr_offset + pokemonOffset
                attr_size = int(
                    self.memoryInfo['attributes'][attr]['size'])
                val = int(pokemon.attributes[attr], 16).to_bytes(
                    attr_size, 'little')
                self.pm.write_bytes(addr, val, attr_size)
            pokemonOffset += 100

    def getFirstPokemonAddress(self):
        baseAddress = self.pm.read_bytes(
            self.pm.base_address + int(self.memoryInfo['pointer']['baseOffset'], 16), 4)
        self.firstPokemonAdress = int.from_bytes(baseAddress, 'little') + \
            int(self.memoryInfo['pointer']['offset'], 16)

    def createPokemons(self):
        for i in range(6):
            pokemonOffset = i*100
            pokemon_attr = {}
            for attr in self.memoryInfo['attributes']:
                bytes = self.pm.read_bytes(self.firstPokemonAdress +
                                           int(self.memoryInfo['attributes'][attr]['offset']) + pokemonOffset, int(self.memoryInfo['attributes'][attr]['size']))
                # read_mode = 'big' if attr == 'data' else 'little'
                pokemon_attr[attr] = hex(int.from_bytes(bytes, 'little'))
            self.pokemons.append(Pokemon(pokemon_attr))
