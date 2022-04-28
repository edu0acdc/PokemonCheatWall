import tkinter as tk


class PokemonGUI():
    def __init__(self, cheatWall):
        self.window = tk.Tk()
        self.frame = tk.Frame(master=self.window)
        self.cw = cheatWall
        self.widgets = []

        tk.Button(master=self.frame, text="Heal All",
                  command=self.cw.healAllPokemon).pack()

        self.frame.pack()
        self.window.mainloop()
