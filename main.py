import random

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

def play_round(player1, player2):
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

def print_results(round_num, player1, player2):
    print(f"Round {round_num}:")
    print(f"{player1.name} strategy: {player1.history[-1]} | Score: {player1.score}")
    print(f"{player2.name} strategy: {player2.history[-1]} | Score: {player2.score}")
    print()

# Main simulation loop
def main():
    player1 = Player("Player 1", tit_for_tat)
    player2 = Player("Player 2", random_strategy)
    
    num_rounds = 10
    for round_num in range(1, num_rounds + 1):
        play_round(player1, player2)
        print_results(round_num, player1, player2)

if __name__ == "__main__":
    main()
