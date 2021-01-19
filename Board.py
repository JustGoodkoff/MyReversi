class Board:
    def __init__(self):
        self.board = [["-", "-", "-", "-", "-", "-", "-", "-"],
                      ["-", "-", "-", "-", "-", "-", "-", "-"],
                      ["-", "-", "-", "-", "-", "-", "-", "-"],
                      ["-", "-", "-", "0", "1", "-", "-", "-"],
                      ["-", "-", "-", "1", "0", "-", "-", "-"],
                      ["-", "-", "-", "-", "-", "-", "-", "-"],
                      ["-", "-", "-", "-", "-", "-", "-", "-"],
                      ["-", "-", "-", "-", "-", "-", "-", "-"],
                      ]
        self.move = "0"
        self.discs_on_board = 4

    def current_move(self):
        return self.move

    def change_move(self):
        if self.move == "0":
            self.move = "1"
        else:
            self.move = "0"

    def check_pos(self, pos: tuple):
        print(pos[0] // 80, pos[1] // 80)
