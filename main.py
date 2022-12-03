import random

dice = [0, 0, 0, 1, 2, 3]

# Keep = 0, left = 1, right = 2, center = 3

def roll_dice():
    output = random.randint(0, 5)
    return dice[output]


def simulate(no_players, no_games):
    next_target_percentage = 1
    all_games_length = []
    percentage_left = 0
    for i in range(no_games):  # Plays number of games
        players_cash = [3 for i in range(no_players)]
        center_cash = 0
        current_player = -1
        all_rolls = 0
        stop = False
        while not stop:  # 1 Game Running

            if current_player == no_players:
                current_player = 0
            else:
                current_player += 1

            current_player = current_player % no_players

            if players_cash[current_player] < 4:
                no_rolls = players_cash[current_player]
            else:
                no_rolls = 3

            # print(no_rolls)
            all_rolls += 1
            for i in range(no_rolls):
                roll_result = roll_dice()
                if roll_result == 1:  # Rolls Left
                    players_cash[current_player] -= 1
                    players_cash[current_player - 1] += 1
                if roll_result == 2:  # Rolls Right
                    players_cash[current_player] -= 1
                    players_cash[(current_player + 1) % no_players] += 1
                if roll_result == 3:  # Rolls Center
                    players_cash[current_player] -= 1
                    center_cash += 1
                    if center_cash == (no_players * 3) - 1 or center_cash >= no_players * 3:
                        all_games_length.append(all_rolls)
                        stop = True
                if roll_result == 0:  # Rolls Keep
                    if center_cash == (no_players * 3) - 1 or center_cash > no_players * 3:
                        all_games_length.append(all_rolls)
                        stop = True
        percentage_left = round((len(all_games_length) / no_games) * 100, 2)
        if percentage_left >= next_target_percentage and not next_target_percentage > 100:
            print(str(percentage_left) + "%")
            next_target_percentage += 1
    every_roll = 0
    for i in all_games_length:
        every_roll += i
    return "\n" + "# Of Games Simulated: " + str(no_games) + "\n" + "# Of Players Per Game: " + str(
        no_players) + "\n" + "Average Rolls Per Game: " + str(
        round(every_roll / no_games)) + "\n" + "Maximum Roll Game: " + str(max(all_games_length)) + "\n" + "Minimum Roll Game: " + str(min(all_games_length))


print(simulate(8, 100))  # Amount Of players, Amount of Games
