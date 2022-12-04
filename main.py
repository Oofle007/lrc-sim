import random
import statistics

dice = [0, 0, 0, 1, 2, 3]


# Keep = 0, left = 1, right = 2, center = 3

def roll_dice():
    output = random.randint(0, 5)
    return dice[output]


def simulate(no_players, no_games, no_seconds):
    next_target_percentage = 1
    all_games = []
    all_times = []
    completed_games = 0
    for i in range(no_games):  # Plays number of games
        players_cash = [3 for i in range(no_players)]
        center_cash = 0
        current_player = -1
        all_rolls = 0
        stop = False
        while not stop:  # 1 Game Running
            if current_player == no_players:  # Setting current player in players_cash list
                current_player = 0
            else:
                current_player += 1
            current_player = current_player % no_players

            if players_cash[current_player] < 4:  # Setting amount of rolls the current player has
                no_rolls = players_cash[current_player]
            else:
                no_rolls = 3

            all_rolls += 1
            for i in range(no_rolls):  # Rolling no_rolls times
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
                    if center_cash == (no_players * 3) - 1 or center_cash >= no_players * 3:  # Stops game
                        all_games.append(all_rolls)
                        stop = True
                if roll_result == 0:  # Rolls Keep
                    if center_cash == (no_players * 3) - 1 or center_cash > no_players * 3:  # Stops game
                        all_games.append(all_rolls)
                        stop = True
        all_times.append(no_seconds * all_rolls)
        completed_games += 1
        percentage_left = round((completed_games / no_games) * 100, 1)  # Percent left in simulation
        if percentage_left >= next_target_percentage and not next_target_percentage > 100:  # Decides when to print %
            print(str(percentage_left) + "%")
            next_target_percentage += 1

    sec = round(statistics.mean(all_times))  # Average Seconds Per Game
    time = ""
    for d, u in [(60, "second"), (60, "minute"), (24, "hour"), (sec, "day")]:
        sec, n = divmod(sec, d)
        if n: time = f"{n} {u}" + "s" * (n > 1) + ", " * bool(time) + time

    return "\n" + "# Of Games Simulated: " + str(no_games) + "\n" + "# Of Players Per Game: " + str(
        no_players) + "\n" + "Time Spent Each Roll: " + str(no_seconds) + "s" + "\n" + "Average Rolls Per Game: " + str(
        round(statistics.mean(all_times))) + "\n" + "Maximum Roll Game: " + str(
        max(all_games)) + "\n" + "Minimum Roll Game: " + str(min(all_games)) + "\n" + "Average Time Per Game: " + str(
        time)


print(simulate(7, 10000, 1))  # Amount Of players, Amount of Games, Seconds Per Roll
