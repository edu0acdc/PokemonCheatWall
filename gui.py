import tkinter as tk
from cheatWall import CheatWall


class PokemonGUI():
    def __init__(self, cheatWall: CheatWall):
        self.window = tk.Tk()
        self.window.title("Pokemon Cheat Wall")
        self.window.minsize(height=100, width=300)
        self.frame = tk.Frame(master=self.window)
        self.cw = cheatWall
        self.widgets = []

        tk.Button(master=self.frame, text="Heal All",
                  command=self.cw.healAllPokemon).pack()

        for i in range(1, 7):
            bt = tk.Button(master=self.frame, text="Heal Pokemon Nº" +

                           str(i))
            bt.index = i
            bt['command'] = lambda arg=bt.index: self.cw.healPokemon(arg)
            bt.pack()

        self.frame.pack()
        self.window.mainloop()
