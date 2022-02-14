import tkinter as  tk

class Game(tk.Frame):
    def __init__(self, master):
        super(Game, self).__init__(master)
        self.lives = 3
        self.width = 600
        self.height = 400
        self.background = 'aaaaff'
        self.canvas = tk.Canvas(self, width=self.width, height=self.height, bg=self.background)

        self.canvas.pack()
        self.pack()

if __name__ == '__main__':
    root = tk.TK()
    root.title('Pong!')
    game = Game(root)
    game.mainloop()