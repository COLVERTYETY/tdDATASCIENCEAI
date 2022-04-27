from multiprocessing.dummy import current_process
import tkinter as tk
import gommoku as gm

players = ["red","blue"]
current_player = 0
game_grid = {}
history = []

class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Gommoku !!!")
        self.geometry("500x500")
        self.resizable(0, 0)
        self.configure(bg="lightgrey")

        ### divide the app in 2 frames
        ## upper frame takes 2/3 of the app
        self.upper_frame = tk.Frame(self, bg="lightgrey")
        self.upper_frame.pack(side="top", fill="both", expand=True)
        ## lower frame takes 1/3 of the app
        self.lower_frame = tk.Frame(self, bg="white")
        self.lower_frame.pack(side="bottom", fill="both", expand=True)

        ### divide the uppper frame in a grid of 12*12
        self.upper_frame_grid = tk.Frame(self.upper_frame, bg="lightgrey")
        self.upper_frame_grid.pack(side="top", fill="both", expand=True)
        for i in range(12):
            self.upper_frame_grid.grid_columnconfigure(i, weight=1)
        for i in range(12):
            self.upper_frame_grid.grid_rowconfigure(i, weight=1)
        ### highlight each cell of the grid on mouse over
        global game_grid
        for i in range(12):
            for j in range(12):
                game_grid[(i,j)] = -1
                cell = tk.Label(self.upper_frame_grid, bg="white", text=str(i).rjust(2)+":"+str(j).rjust(2))
                cell.grid(row=i, column=j)
                cell.bind("<Enter>", lambda event, button=cell, pos=(i,j): self.on_enter(event, button, pos))
                cell.bind("<Leave>", lambda event, button=cell, pos=(i,j) : self.on_leave(event, button, pos))
                cell.bind("<Button-1>", lambda event, button=cell, pos=(i,j) : self.on_click(event, button, pos))

        ### divide the lower frame in a grid of 1*4
        self.lower_frame_grid = tk.Frame(self.lower_frame, bg="white")
        self.lower_frame_grid.pack(side="top", fill="both", expand=True)
        for i in range(4):
            self.lower_frame_grid.grid_columnconfigure(i, weight=1)
        for i in range(1):
            self.lower_frame_grid.grid_rowconfigure(i, weight=1)
        ### create a button to toggle between players
        self.player_btn = tk.Button(self.lower_frame_grid, text=f"{players[current_player]}", bg=players[current_player], command=self.change_player)
        self.player_btn.grid(row=0, column=0)
        ### create a button to step back in the history
        self.history_button = tk.Button(self.lower_frame_grid, text="step back", bg="white", command=self.step_back)
        self.history_button.grid(row=0, column=1)
        ### create a button to reset the game
        self.reset_btn = tk.Button(self.lower_frame_grid, text="Reset", bg="white", command=self.reset)
        self.reset_btn.grid(row=0, column=2)
        ### create a button to sove the game (not implemented yet)
        self.solve_btn = tk.Button(self.lower_frame_grid, text="computer", bg="white", command=self.solve)
        self.solve_btn.grid(row=0, column=3)

    def step_back(self):
        global history
        if len(history) > 0:
            pos = history.pop()
            cell = self.upper_frame_grid.grid_slaves(row=pos[0], column=pos[1])[0]
            cell["bg"] = "white"
            game_grid[pos] = -1
            self.change_player()

    def solve(self):
        print("not implemented yet")

    def reset(self):
        global game_grid, history
        history = []
        for i in range(12):
            for j in range(12):
                game_grid[(i,j)] = -1
                cell = self.upper_frame_grid.grid_slaves(row=i, column=j)[0]
                cell["bg"] = "white"
        self.upper_frame_grid.configure(bg="lightgrey")
        

    def on_click(self, e, btn, pos):
        global players, current_player, game_grid, history
        if game_grid[pos] == -1:
            game_grid[pos] = current_player
            btn["bg"] = players[current_player]
            history.append(pos)
            ### now change the player
            self.change_player()
        self.check_victory()

    def change_player(self):
        global players, current_player
        current_player = (current_player + 1) % 2
        self.player_btn["text"] = f"{players[current_player]}"
        self.player_btn["bg"] = players[current_player]
        
    def on_enter(self, e, btn, pos):
        global players, current_player, game_grid
        if game_grid[pos] == -1:
            btn["bg"] = players[current_player]
    
    def on_leave(self, e, btn, pos):
        global players, current_player, game_grid
        if game_grid[pos] == -1:
            btn["bg"] = "white"
        else:
            btn["bg"] = players[game_grid[pos]]

    def check_victory(self):
        global game_grid
        temp=[]
        for i in range(12):
            for j in range(12):
                temp.append(game_grid[(i,j)])
        t = gm.game_over(temp)
        # print(t)
        if t == 0:
            # print("red wins")
            # change the background of the self.upper_frame_grid
            self.upper_frame_grid.configure(bg="pink")
        elif t == 1:
            # print("blue wins")
            # change the background of the self.upper_frame_grid
            self.upper_frame_grid.configure(bg="lightblue")




if __name__ == '__main__':
    ### test that the module is working
    # print(gm.working_module())
    app = App()
    app.mainloop()