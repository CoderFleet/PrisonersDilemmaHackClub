import random
import tkinter as tk
from tkinter import ttk

COOPERATE = 'cooperate'
DEFECT = 'defect'

class Player:
    def __init__(self, name, strategy):
        self.name = name
        self.strategy = strategy
        self.score = 0
        self.history = []
        self.cooperate_count = 0
        self.defect_count = 0
    
    def choose_action(self, opponent):
        action = self.strategy(self, opponent)
        self.history.append(action)
        if action == COOPERATE:
            self.cooperate_count += 1
        else:
            self.defect_count += 1
        return action

def tit_for_tat(player, opponent):
    if opponent.history:
        return opponent.history[-1]
    else:
        return COOPERATE

def random_strategy(player, opponent):
    return random.choice([COOPERATE, DEFECT])

def always_cooperate(player, opponent):
    return COOPERATE

def always_defect(player, opponent):
    return DEFECT

def grim_trigger(player, opponent):
    if DEFECT in opponent.history:
        return DEFECT
    return COOPERATE

def pavlov(player, opponent):
    if len(player.history) == 0:
        return COOPERATE
    if player.history[-1] == COOPERATE and opponent.history[-1] == COOPERATE:
        return COOPERATE
    if player.history[-1] == DEFECT and opponent.history[-1] == DEFECT:
        return COOPERATE
    return DEFECT

def play_round(player1, player2, log_widget):
    action1 = player1.choose_action(player2)
    action2 = player2.choose_action(player1)
    
    if action1 == COOPERATE and action2 == COOPERATE:
        player1.score += 3
        player2.score += 3
    elif action1 == COOPERATE and action2 == DEFECT:
        player1.score += 0
        player2.score += 5
    elif action1 == DEFECT and action2 == COOPERATE:
        player1.score += 5
        player2.score += 0
    elif action1 == DEFECT and action2 == DEFECT:
        player1.score += 1
        player2.score += 1
    
    log_widget.insert(tk.END, f"Round: {len(player1.history)}, {player1.name} action: {action1}, {player2.name} action: {action2}\n")
    log_widget.see(tk.END)

def update_gui(player1, player2, label1, label2, progress1, progress2, history_widget, stats_widget):
    label1.configure(text=f"{player1.name} strategy: {player1.history[-1]} | Score: {player1.score} | Cooperate: {player1.cooperate_count} | Defect: {player1.defect_count}")
    label2.configure(text=f"{player2.name} strategy: {player2.history[-1]} | Score: {player2.score} | Cooperate: {player2.cooperate_count} | Defect: {player2.defect_count}")
    progress1['value'] = player1.score
    progress2['value'] = player2.score
    
    history_widget.delete(1.0, tk.END)
    for i, (action1, action2) in enumerate(zip(player1.history, player2.history)):
        history_widget.insert(tk.END, f"Round {i+1}: {player1.name} - {action1}, {player2.name} - {action2}\n")
    
    stats_widget.delete(1.0, tk.END)
    stats_widget.insert(tk.END, f"{player1.name} - Cooperate: {player1.cooperate_count}, Defect: {player1.defect_count}\n")
    stats_widget.insert(tk.END, f"{player2.name} - Cooperate: {player2.cooperate_count}, Defect: {player2.defect_count}\n")

def simulate_rounds(player1, player2, num_rounds, label1, label2, progress1, progress2, log_widget, history_widget, stats_widget):
    for _ in range(num_rounds):
        play_round(player1, player2, log_widget)
        update_gui(player1, player2, label1, label2, progress1, progress2, history_widget, stats_widget)
        label1.update()
        label2.update()
        progress1.update()
        progress2.update()

def start_simulation(player1, player2, num_rounds_var, label1, label2, progress1, progress2, log_widget, history_widget, stats_widget):
    num_rounds = int(num_rounds_var.get())
    simulate_rounds(player1, player2, num_rounds, label1, label2, progress1, progress2, log_widget, history_widget, stats_widget)

def reset_simulation(player1, player2, label1, label2, progress1, progress2, log_widget, history_widget, stats_widget):
    player1.score = 0
    player2.score = 0
    player1.history = []
    player2.history = []
    player1.cooperate_count = 0
    player2.cooperate_count = 0
    player1.defect_count = 0
    player2.defect_count = 0
    label1.configure(text="")
    label2.configure(text="")
    progress1['value'] = 0
    progress2['value'] = 0
    log_widget.delete(1.0, tk.END)
    history_widget.delete(1.0, tk.END)
    stats_widget.delete(1.0, tk.END)

def get_strategy(strategy_name):
    strategies = {
        "Tit for Tat": tit_for_tat,
        "Random": random_strategy,
        "Always Cooperate": always_cooperate,
        "Always Defect": always_defect,
        "Grim Trigger": grim_trigger,
        "Pavlov": pavlov
    }
    return strategies[strategy_name]

def main():
    root = tk.Tk()
    root.title("Prisoner's Dilemma Simulation")
    
    player1_name = "Player 1"
    player2_name = "Player 2"
    
    strategy1_var = tk.StringVar(value="Tit for Tat")
    strategy2_var = tk.StringVar(value="Random")
    
    strategy1_label = ttk.Label(root, text=f"{player1_name} Strategy:")
    strategy1_label.pack(pady=5)
    strategy1_menu = ttk.Combobox(root, textvariable=strategy1_var, values=["Tit for Tat", "Random", "Always Cooperate", "Always Defect", "Grim Trigger", "Pavlov"])
    strategy1_menu.pack(pady=5)
    
    strategy2_label = ttk.Label(root, text=f"{player2_name} Strategy:")
    strategy2_label.pack(pady=5)
    strategy2_menu = ttk.Combobox(root, textvariable=strategy2_var, values=["Tit for Tat", "Random", "Always Cooperate", "Always Defect", "Grim Trigger", "Pavlov"])
    strategy2_menu.pack(pady=5)
    
    player1 = Player(player1_name, get_strategy(strategy1_var.get()))
    player2 = Player(player2_name, get_strategy(strategy2_var.get()))
    
    label1 = ttk.Label(root, text="")
    label1.pack(pady=10)
    progress1 = ttk.Progressbar(root, orient=tk.HORIZONTAL, length=200, mode='determinate')
    progress1.pack(pady=10)
    
    label2 = ttk.Label(root, text="")
    label2.pack(pady=10)
    progress2 = ttk.Progressbar(root, orient=tk.HORIZONTAL, length=200, mode='determinate')
    progress2.pack(pady=10)
    
    num_rounds_var = tk.StringVar(value="10")
    num_rounds_label = ttk.Label(root, text="Number of Rounds:")
    num_rounds_label.pack(pady=5)
    num_rounds_entry = ttk.Entry(root, textvariable=num_rounds_var)
    num_rounds_entry.pack(pady=5)
    
    log_widget = tk.Text(root, height=10, width=50)
    log_widget.pack(pady=10)
    
    history_widget = tk.Text(root, height=10, width=50)
    history_widget.pack(pady=10)
    
    stats_widget = tk.Text(root, height=5, width=50)
    stats_widget.pack(pady=10)
    
    start_button = ttk.Button(root, text="Start Simulation", command=lambda: start_simulation(
        Player(player1_name, get_strategy(strategy1_var.get())),
        Player(player2_name, get_strategy(strategy2_var.get())),
        num_rounds_var, label1, label2, progress1, progress2, log_widget, history_widget, stats_widget
    ))
    start_button.pack(pady=10)
    
    reset_button = ttk.Button(root, text="Reset Simulation", command=lambda: reset_simulation(
        Player(player1_name, get_strategy(strategy1_var.get())),
        Player(player2_name, get_strategy(strategy2_var.get())),
        label1, label2, progress1, progress2, log_widget, history_widget, stats_widget
    ))
    reset_button.pack(pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    main()
