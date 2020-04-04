from tkinter import *

SIZE_W = 8
SIZE_H = 6
SPACE = 25
SPACE_L = SPACE / 5
SPACE_R = SPACE_L * 4
NUMBER_TO_WIN = 5

class TicTacToe:
    def __init__(self):
        window = Tk()
        window.title("Tic-Tac_Toe Game")

        #Calculate canvas size
        self.width = SIZE_W * SPACE
        self.height = SIZE_H * SPACE

        #Initialize table to store plays
        #0 if not played, 1 if play X, 2 if play O
        self.grid = []
        for i in range(SIZE_H):
            self.grid.append([])
            for j in range(SIZE_W):
                self.grid[i].append(0)

        self.canvas = Canvas(window, width = self.width,
                            height = self.height, bg = "white")
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.processMouseEvent)

        frame0 = Frame(window)
        frame0.pack()
        self.playerLabel = Label(frame0, text = "Play X", fg = "red")
        self.playerLabel.pack()

        frame1 = Frame(window)
        frame1.pack()
        btReset = Button(frame1, text = "Restart", command = self.resetGame)
        btReset.pack()

        #Draw SIZE_H x SIZE_W grid with SPACE apart
        for i in range(0, self.width, SPACE):
            self.canvas.create_line(i, 0, i, self.height, tags = "line")
        for i in range(0, self.height, SPACE):
            self.canvas.create_line(0, i, self.width, i, tags = "line")

        self.resetGame()
        window.mainloop()

    #Play X in red
    def placeX(self):
        self.canvas.create_line(self.x + SPACE_L, self.y + SPACE_L,
            self.x + SPACE_R, self.y + SPACE_R, fill = "red", width = 3, tags = "x")
        self.canvas.create_line(self.x + SPACE_L, self.y + SPACE_R,
            self.x + SPACE_R, self.y + SPACE_L, fill = "red", width = 3, tags = "x")

    #Play O in blue
    def placeO(self):
        self.canvas.create_oval(self.x + SPACE_L, self.y + SPACE_L,
            self.x + SPACE_R, self.y + SPACE_R, outline = "blue", width = 3, tags = "o")

    def processMouseEvent(self, event):
        #Standardize coordinates
        column = event.x // SPACE
        self.x = column * SPACE
        
        row = event.y // SPACE
        self.y = row * SPACE

        if self.endGame == 0:
            if self.grid[row][column] == 0:
                if self.player: #Player 1
                    self.placeX()
                    self.grid[row][column] = 1
                else:   #Player 2
                    self.placeO()
                    self.grid[row][column] = 2

                self.turn += 1
                self.endGame = self.getStatus(row, column)
                self.player = not self.player #Switch player
                self.playerLabel["text"] = "Play X" if self.player else "Play O"
                self.playerLabel["fg"] = "red" if self.player else "blue"

        if self.endGame == 2:
            self.playerLabel["text"] = "Draw"
            self.playerLabel["fg"] = "black"
        elif self.endGame == 1:
            self.playerLabel["text"] = "Winner O" if self.player else "Winner X"
            self.playerLabel["fg"] = "blue" if self.player else "red"

    def getStatus(self, r, c):
        #Current player wins
        if self.turn <= SIZE_W * SIZE_H:
            # Check vertical
            marks = self.countMarks(r, c, -1, 0) + self.countMarks(r, c, 1, 0)
            if marks > NUMBER_TO_WIN:
                return 1    #Winner

            # Check horizontal
            marks = self.countMarks(r, c, 0, -1) + self.countMarks(r, c, 0, 1)
            if marks > NUMBER_TO_WIN:
                return 1

            # Check diagnal \
            marks = self.countMarks(r, c, -1, -1) + self.countMarks(r, c, 1, 1)
            if marks > NUMBER_TO_WIN:
                return 1

            # Check diagnal /
            marks = self.countMarks(r, c, -1, 1) + self.countMarks(r, c, 1, -1)
            if marks > NUMBER_TO_WIN:
                return 1         

        #Draw
        if self.turn == SIZE_W * SIZE_H:
            return 2    

        return 0    #Continue playing
        
            
    #Count countinuos marks in dr, dc direction
    def countMarks(self, r, c, dr, dc):
        counter = 0
        marks = self.grid[r][c]

        while True: #check for boundaries or different marks
            if r < 0 or r > SIZE_H - 1 \
               or c < 0 or c > SIZE_W - 1 \
               or self.grid[r][c] != marks:
                return counter
            else:
                counter += 1
                r += dr
                c += dc

    def resetGame(self):
        self.player = True  #Player 1

        #reset values to 0
        for i in range(SIZE_H):
            for j in range(SIZE_W):
                self.grid[i][j] = 0

        self.endGame = 0
        self.playerLabel["text"] = "Play X"
        self.playerLabel["fg"] = "red"
        self.canvas.delete("x")
        self.canvas.delete("o")
        self.turn = 0
         
TicTacToe()
