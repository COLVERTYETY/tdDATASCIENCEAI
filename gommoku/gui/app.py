import tkinter as tk
import gommoku as gm
import numpy as np
import time 
import node as nd
import time

players = ["red","blue"]
players2 = ["pink","lightblue"]
current_player = 0
game_grid = {}
history = []

class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Gommoku !!!")
        self.geometry("600x600")
        self.resizable(0, 0)
        self.configure(bg="lightgrey")

        ### divide the app in 2 frames
        ## upper frame takes 2/3 of the app
        self.upper_frame = tk.Frame(self, bg="lightgrey")
        self.upper_frame.pack(side="top", fill="both", expand=True)
        ## lower frame takes 1/3 of the app
        self.lower_frame = tk.Frame(self, bg="white")
        self.lower_frame.pack(side="bottom", fill="both", expand=True)

        ### divide the uppper frame in a grid of 15*15
        self.upper_frame_grid = tk.Frame(self.upper_frame, bg="lightgrey")
        self.upper_frame_grid.pack(side="top", fill="both", expand=True)
        for i in range(15):
            self.upper_frame_grid.grid_columnconfigure(i, weight=1)
        for i in range(15):
            self.upper_frame_grid.grid_rowconfigure(i, weight=1)
        ### highlight each cell of the grid on mouse over
        global game_grid
        for i in range(15):
            for j in range(15):
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

    def update_colors(self):
        global game_grid
        for i in range(15):
            for j in range(15):
                cell = self.upper_frame_grid.grid_slaves(row=i, column=j)[0]
                if game_grid[(i,j)] == -1:
                    cell["bg"] = "white"
                else:
                    cell["bg"] = players[game_grid[(i,j)]]

    def step_back(self):
        global history
        if len(history) > 0:
            pos = history.pop()
            cell = self.upper_frame_grid.grid_slaves(row=pos[0], column=pos[1])[0]
            cell["bg"] = "white"
            game_grid[pos] = -1
            self.change_player()
            self.upper_frame_grid.configure(bg="lightgrey")
            self.check_victory()

    def solve(self):
        global game_grid, history
        # temp=[]
        # for i in range(15):
        #     for j in range(15):
        #         temp.append(game_grid[(i,j)])
        # check if there is a move in teh history
        temp=[[0 for i in range(15)] for j in range(15)]
        for i in range(15):
            for j in range(15):
                temp.append(game_grid[(i,j)])
                # if game_grid[(i,j)] == -1:
                #     temp[i][j]=0
                # elif game_grid[(i,j)] == 0:
                #     temp[i][j]=1
                # elif game_grid[(i,j)] == 1:
                #     temp[i][j]=-1
        print(temp)
        cp = 0
        if current_player == 0:
            cp = -1
        elif current_player == 1:
            cp = 1
        # root = nd.Node(np.array([7,7]), None, cp, 120)
        if len(history) > 0:
            pos = history[-1]
        else:
            pos = (7,7)
        # check if the game is already solved
        if self.check_victory():
            return
        # we play
        start = time.time()
        # (moves,(score,x,y)) = gm.solve(temp,current_player,pos[0],pos[1])
        k = gm.solve_mcts(temp,current_player)
        print(type(k),k)
        (x,y) = k
        # (x,y) = nd.Node.mcts(np.array(temp),np.array(temp.copy()),root)
        # (x,y) = nd.solve(np.array(temp),cp,pos[0],pos[1])
        stop = time.time()
        print(f"time taken : {stop-start}s")
        # print("move score is",score)
        # display the potential moves
        self.update_colors()
        # for move in moves:
        #     if move[0] != -1 and move[1] != -1 and (move[0],move[1]) not in history:
        #         cell = self.upper_frame_grid.grid_slaves(row=move[0], column=move[1])[0]
        #         cell["bg"] = players2[current_player]
        # we update the game grid
        game_grid[(x,y)] = current_player
        # we update the gui
        cell = self.upper_frame_grid.grid_slaves(row=x, column=y)[0]
        cell["bg"] = players[current_player]
        # we update the history
        history.append((x,y))
        # we change the player
        self.change_player()
        # we check if the game is solved
        self.check_victory()


    def reset(self):
        global game_grid, history
        history = []
        for i in range(15):
            for j in range(15):
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
            ## check victory
            self.check_victory()
            ### now change the player
            self.change_player()
        self.update_colors()

    def change_player(self):
        global players, current_player
        current_player = (current_player + 1) % 2
        self.player_btn["text"] = f"{players[current_player]}"
        self.player_btn["bg"] = players[current_player]
        # get the evaluation of the board
        temp=[]
        for i in range(15):
            for j in range(15):
                temp.append(game_grid[(i,j)])
        evaluation = gm.evaluate_board(temp,current_player)
        print(f"evaluation for player {players[current_player]} is:",evaluation)

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
        temp=[[-1 for i in range(15)] for j in range(15)]
        for i in range(15):
            for j in range(15):
                # temp.append(game_grid[(i,j)])
                if game_grid[(i,j)] == -1:
                    temp[i][j]=0
                elif game_grid[(i,j)] == 0:
                    temp[i][j]=1
                elif game_grid[(i,j)] == 1:
                    temp[i][j]=-1
        start = time.time()
        t = nd.get_winner(np.array(temp))
        # t = nd.winning_move(np.array(temp),np.array(history[-1]))
        stop = time.time()
        print(f"time taken for w: {stop-start}s", t)
        if t == 0:
            t=-1
        elif t == -1:
            t=1
        else:
            t=0
        print(f"winner is {t}")
        if t != -1:
            self.upper_frame_grid.configure(bg=players2[t])




if __name__ == '__main__':
    ### test that the module is working
    # print(gm.working_module())
    app = App()
    app.mainloop()