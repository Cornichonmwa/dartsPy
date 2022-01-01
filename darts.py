

QUIT_MOVE = "quit"
UNDO_MOVE = "undo"
ILLEGAL_MOVE = "illegal"

class Game():
    def __init__(self, nb_players):
        self.nb_players = nb_players
        self.history = []
        self.scores = {i: 0 for i in range (nb_players)}
        self.active_player = 0

    def __str__(self):
        # return f"Scores:\n{self.scores}\nHisto"
        return str(self.scores)

    def play(self, move):
        self.history += [move]

    def start(self):
        while(True):
            move = self.get_move()
            if move == QUIT_MOVE:
                break
            elif move == UNDO_MOVE:
                print("Undoing last move")
                self.undo()
                continue
            if self.play(move) == ILLEGAL_MOVE:
                print("Illegal move")
            self.active_player = (self.active_player + 1) % self.nb_players
            print(self)
            if self.win_condition():
                break

    def undo(self):
        last_move = self.history[-1]
        self.history = self.history[:-1]
        self.active_player = (self.active_player - 1) % self.nb_players
        return last_move

    def game_over(self):
        print("game over")

class Darts501(Game):
    def __init__(self, nb_players):
        super().__init__(nb_players)

    def play(self, move):
        total = 0
        for m in move:
            total += self._move_to_score(m)
        if self.scores[self.active_player] + total < 501:
            self.scores[self.active_player] += total
            super().play(move)

        elif self.scores[self.active_player] + total == 501 :
            if move[-1][0] == "t" or move[-1][0] == "d" :
                self.scores[self.active_player] += total
                super().play(move)
            return ILLEGAL_MOVE

        else :
            return ILLEGAL_MOVE


    def undo(self):
        last_move = super().undo()
        total = 0
        for m in last_move :
            total += self._move_to_score(m)
        self.scores[self.active_player] -= total

    def _move_to_score(self, move):
        (type, score) = move
        if type == "d":
            mul = 2
        elif type == "t":
            mul = 3
        else:
            mul = 1
        return score * mul

    
    def get_move(self):
        d = 1
        volley = []
        while(d <= 3):
            raw = input(f"Move for player {self.active_player} ? : ")
            try:
                move = parse_move(raw)
            except:
                print("Invalid move")
            else:
                if move == QUIT_MOVE :
                    return QUIT_MOVE
                if move == UNDO_MOVE :
                    return UNDO_MOVE
                if move[1] > 0:
                    volley.append(move)
                d += 1
        return volley

    def win_condition(self):
        for k, v in self.scores.items():
            if v == 501:
                print(f"{k} wins")
                return True
        return False


class DartsDumb(Game):
    def __init__(self, nb_players):
        super().__init__(nb_players)
        
    def play(self, move):
        super().play(move)
        self.scores[self.active_player] += self._move_to_score(move)

    def undo(self):
        last_move = super().undo()
        self.scores[self.active_player] -= self._move_to_score(last_move)

    def _move_to_score(self, move):
        (type, score) = move
        if type == "d":
            mul = 2
        elif type == "t":
            mul = 3
        else:
            mul = 1
        return score * mul

    
    def get_move(self):
        while(True):
            raw = input(f"Move for player {self.active_player} ? : ")
            try:
                move = parse_move(raw)
            except:
                print("Invalid move")
            else:
                return move

    def win_condition(self):
        for k, v in self.scores.items():
            if v > 100:
                print(f"{k} wins")
                return True
        return False

def parse_move(raw):
    prefix = raw[0]
    if prefix in ["d", "t"]:
        return (prefix, int(raw[1:]))
    elif prefix == "q":
        return QUIT_MOVE
    elif prefix == "u":
        return UNDO_MOVE
    else:
        return ("s", int(raw))

def main():
    game = Darts501(2)
    game.start()

    print(game.history)

if __name__ == "__main__":
    main()