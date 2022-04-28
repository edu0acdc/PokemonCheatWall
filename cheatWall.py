from memory import MemoryManager


class CheatWall():
    def __init__(self, memoryManager: MemoryManager):
        self.memoryManager = memoryManager

    def healAllPokemon(self):
        self.memoryManager.refreshPokemon()
        for pokemon in self.memoryManager.pokemons:
            pokemon.changeFieldHex(
                'current_hp', pokemon.attributes['total_hp'])

        self.memoryManager.writeAll()

    def healPokemon(self, position):
        self.memoryManager.refreshPokemon()
        pokemon = self.memoryManager.pokemons[position-1]
        print(pokemon.attributes)
        pokemon.changeFieldHex(
            'current_hp', pokemon.attributes['total_hp'])
        self.memoryManager.writePokemon(position)
