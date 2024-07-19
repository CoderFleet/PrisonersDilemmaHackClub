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
    
    def choose_action(self, opponent):
        action = self.strategy(self, opponent)
        self.history.append(action)
        return action

def tit_for_tat(player, opponent):
    if opponent.history:
        return opponent.history[-1]
    else:
        return COOPERATE

def random_strategy(player, opponent):
    return random.choice([COOPERATE, DEFECT])

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

def update_gui(player1, player2, label1, label2, progress1, progress2):
    label1.configure(text=f"{player1.name} strategy: {player1.history[-1]} | Score: {player1.score}")
    label2.configure(text=f"{player2.name} strategy: {player2.history[-1]} | Score: {player2.score}")
    progress1['value'] = player1.score
    progress2['value'] = player2.score

def simulate_rounds(player1, player2, num_rounds, label1, label2, progress1, progress2, log_widget):
    for _ in range(num_rounds):
        play_round(player1, player2, log_widget)
        update_gui(player1, player2, label1, label2, progress1, progress2)
        label1.update()
        label2.update()
        progress1.update()
        progress2.update()

def start_simulation(player1, player2, num_rounds_var, label1, label2, progress1, progress2, log_widget):
    num_rounds = int(num_rounds_var.get())
    simulate_rounds(player1, player2, num_rounds, label1, label2, progress1, progress2, log_widget)

def reset_simulation(player1, player2, label1, label2, progress1, progress2, log_widget):
    player1.score = 0
    player2.score = 0
    player1.history = []
    player2.history = []
    label1.configure(text="")
    label2.configure(text="")
    progress1['value'] = 0
    progress2['value'] = 0
    log_widget.delete(1.0, tk.END)

def main():
    player1 = Player("Player 1", tit_for_tat)
    player2 = Player("Player 2", random_strategy)
    
    root = tk.Tk()
    root.title("Prisoner's Dilemma Simulation")
    
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
    
    start_button = ttk.Button(root, text="Start Simulation", command=lambda: start_simulation(player1, player2, num_rounds_var, label1, label2, progress1, progress2, log_widget))
    start_button.pack(pady=10)
    
    reset_button = ttk.Button(root, text="Reset Simulation", command=lambda: reset_simulation(player1, player2, label1, label2, progress1, progress2, log_widget))
    reset_button.pack(pady=10)
    
    log_widget = tk.Text(root, height=10, width=50)
    log_widget.pack(pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    main()
