class CheatWall():
    def __init__(self, memoryManager):
        self.memoryManager = memoryManager

    def healAllPokemon(self):
        for pokemon in self.memoryManager.pokemons:
            pokemon.changeFieldHex(
                'current_hp', pokemon.attributes['total_hp'])

        self.memoryManager.writeAll()

    def healPokemon(self, position):
        pokemon = self.memoryManager.pokemons[position-1]
        pokemon.changeFieldHex(
            'current_hp', pokemon.attributes['total_hp'])
        self.memoryManager.writePokemon(position)
