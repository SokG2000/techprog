from tkinter import *
from abc import ABC, abstractmethod
import battle
wait_time = 1

class TurnStrategy(ABC):
    def config(self, player):
        self.player = player
    @abstractmethod
    def make_turn(self, game):
        pass
    def move(self, game, from_, to):
        if from_ < 0 or from_ > game.player_num or to < 0 or to > game.player_num or self.player.armies[from_] is None:
            return
        if from_ != game.player_num and to != game.player_num:
            return
        army = self.player.armies[from_]
        self.player.armies[from_] = None
        self.move_army(game, army, to)
    def move_army(self, game, army, where):
        if self.player.armies[where] is None:
            self.player.armies[where] = army
            self.player.armies[where].cell = where
            for player in game.players:
                if player.index != self.player.index:
                    if player.armies[where] is not None:
                        b = battle.Battle(self.player, player, where)
                        battle_res = b.start_battle()
                        if battle_res:
                            self.player.armies[where] = army
                            game.lands[where] = self.player.index
                            player.armies[where] = None
                            if where == player.index:
                                player.died = True
                        else:
                            self.player.armies[where] = None
                        return
            game.lands[where] = self.player.index
            if where != self.player.index and where != game.player_num:
                game.players[where].died = True
        else:
            self.player.armies[where].merge_armies(army)
        
    
class ComputerTurnStrategy(TurnStrategy):
    def __init__(self):
        self.turns_rest = wait_time
    def make_turn(self, game):
        if self.player.died:
            return
        self.turns_rest -= 1
        if self.turns_rest == -2:
            self.turns_rest = wait_time
        if self.turns_rest > 0:
            return
        if game.lands[game.player_num] is None or game.players[game.lands[game.player_num]].armies[game.player_num] is None or game.is_man[game.lands[game.player_num]]:
            self.move(game, self.player.index, game.player_num)
            return
        if game.lands[game.player_num] == self.player.index:
            for player in game.players:
                if game.is_man[player.index]:
                    self.move(game, game.player_num, player.index)
                    return

class ManTurnStrategy(TurnStrategy):
    def make_turn(self, game):
        if self.player.died:
            return
        root = Tk()
        x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2
        y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2
        root.wm_geometry("+%d+%d" % (x, y))
        from_label = Label(root, text='From')
        from_label.grid(row=0, column=0)
        variants = (i for i in range(game.player_num + 1))
        from_var = StringVar(root)
        from_var.set("Not move")
        from_option = OptionMenu(root, from_var, "Not move", *variants)
        from_option.grid(row=1, column=0)
        to_label = Label(root, text='To')
        to_label.grid(row=0, column=1)
        variants = (i for i in range(game.player_num + 1))
        to_var = StringVar(root)
        to_var.set("Not move")
        to_option = OptionMenu(root, to_var, "Not move", *variants)
        to_option.grid(row=1, column=1)
        execute_button = Button(root, text='execute', command=root.quit)
        execute_button.grid(row=2)
        root.mainloop()
        root.destroy()
        self.execute_move(game, root, from_var.get(), to_var.get())
        return
    def execute_move(self, game, root, from_, to):
        if from_ == "Not move":
            from_ = "-1"
        if to == "Not move":
            to = "-1"
        self.move(game, int(from_), int(to))
        print(from_, to)

if __name__ == '__main__':
    import main
    main.main()
    