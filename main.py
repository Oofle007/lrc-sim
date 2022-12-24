import random
import statistics
import matplotlib.pyplot as plt
import time
import numpy as np

dice = [0, 0, 0, 1, 2, 3]  # Keep = 0, left = 1, right = 2, center = 3


def play_one_game(no_players, no_money, players):
    players_cash = [no_money for _ in range(no_players)]  # Generates list to keep track of each players money
    center_cash = 0
    current_player = 0
    all_rolls = 0  # Keeps track of the total number of rolls
    stop = False  # Variable to stop playing the game
    while not stop:  # 1 Game Running
        current_player = current_player % no_players  # Switches to the beginning index if index is out of range
        if players_cash[current_player] < 4:  # Setting amount of rolls the current player has
            no_rolls = players_cash[current_player]
        else:
            no_rolls = 3
        all_rolls += 1  # Changing amount of rolls to return later
        for j in range(no_rolls):  # Rolling no_rolls times
            output = random.randint(0, 5)
            roll_result = dice[output]
            if roll_result == 1:  # Rolls Left
                players_cash[current_player] -= 1
                players_cash[current_player - 1] += 1
            if roll_result == 2:  # Rolls Right
                players_cash[current_player] -= 1
                players_cash[(current_player + 1) % no_players] += 1
            if roll_result == 3:  # Rolls Center
                players_cash[current_player] -= 1
                center_cash += 1
                if center_cash == (no_players * no_money) - 1 or center_cash >= no_players * no_money:  # Stops game
                    return all_rolls, players[current_player]  # Returns all rolls, and the winner
            if roll_result == 0:  # Rolls Keep
                if center_cash == (no_players * no_money) - 1 or center_cash > no_players * no_money:  # Stops game
                    return all_rolls, players[current_player]  # Returns all rolls, and the winner
        current_player += 1  # Changes to the next player


def check_invalid_params(params): # Function to see if parameters are positive integers
    for param in params:
        if not param > 0 or type(param) != int:
            return True
    return False


def round_seconds(sec):  # Function to make amount of seconds more readable
    timer = ""
    if sec > 0:
        for d, u in [(60, "second"), (60, "minute"), (24, "hour"), (sec, "day")]:
            sec, n = divmod(sec, d)
            if n: timer = f"{n} {u}" + "s" * (n > 1) + ", " * bool(timer) + timer
    else:
        timer = "0 seconds"
    return timer


def simulate(no_players, no_games, no_seconds, no_money, players, isReturningAllStats=True):
    if check_invalid_params((no_games, no_players, no_seconds)):
        return '\nAll inputs need a positive integer value'
    time_start_of_simulation = time.perf_counter()  # Used to determine total simulation time
    if len(players) < no_players:
        while len(players) < no_players:  # Adds blank players to player if the length != no_players
            players.append("")
    if no_players < len(players):  # If you inputted to many players in the list
        return "Too many player names"
    next_target_percentage = 1  # Will be used to print out the percentage
    simulation_seconds_per_game = []  # Used to find average simulation time per game
    all_games = []  # Every roll from every game
    all_players_won = []  # Keeps track of all of the players that have won
    completed_games = 0
    start = time.perf_counter()
    for i in range(no_games):  # Plays number of games
        time_start_each_game = time.perf_counter()
        all_rolls = play_one_game(no_players, no_money, players)[0]
        all_players_won.append(play_one_game(no_players, no_money, players)[1])
        all_games.append(all_rolls)
        completed_games += 1
        if isReturningAllStats:  # Only prints percent when you want; allows to do the "make_graph" function
            percentage_left = round((completed_games / no_games) * 100, 1)  # Percent left in simulation
            if percentage_left >= next_target_percentage and not next_target_percentage > 100:  # Decides when to print %
                time_left = (time.perf_counter() - start) * (100 - percentage_left)
                start = time.perf_counter()
                print(str(percentage_left) + "%" + " Time Left: " + str(round_seconds(round(time_left))))
                next_target_percentage += 1
            simulation_seconds_per_game.append(time.perf_counter() - time_start_each_game)
    if max(set(all_players_won), key=all_players_won.count) == "":  # Finding player who won the most
        player_won = "None Specified"
    else:
        player_won = max(set(all_players_won), key=all_players_won.count)
    times_won = all_players_won.count(player_won)
    time_end_of_simulation = time.perf_counter()
    average_rolls_per_game = statistics.mean(all_games)
    if isReturningAllStats:
        return "\n# Of Games Simulated: " + str(no_games) + "\n# Of Players Per Game: " + str(
            no_players) + "\nTime Spent Each Roll: " + str(no_seconds) + "s\nAverage Rolls Per Game: " + str(
            round(average_rolls_per_game)) + "\nMaximum Roll Game: " + str(
            max(all_games)) + "\nMinimum Roll Game: " + str(min(all_games)) + "\nAverage Time Per Game: " + str(
            round_seconds(round(average_rolls_per_game*no_seconds))) + "\nPlayer Who Won Most: " + player_won + ": " + str(times_won) + " Time(s)\nSimulation Time: " + str(
            round(time_end_of_simulation - time_start_of_simulation, 4)) + "s\nAverage Simulation Time Per Game: " + str(
            round(statistics.mean(simulation_seconds_per_game), 8)) + "s"
    else:
        return round(average_rolls_per_game)


def make_graph(no_simulations, no_games, seconds_per_roll, money_per_player, players):
    st = time.time()
    # 1 list describes no_players to average time
    x1 = []
    y1 = []
    # 2 list describes no_players to time for each simulation
    x2 = []
    y2 = []
    for i in range(1, no_simulations):
        percentage = round(i / (no_simulations - 2) * 100, 2)
        x1.append(i)
        x2.append(i)
        s = time.time()
        y1.append(simulate(i, no_games, seconds_per_roll, money_per_player, players, False))
        e = time.time()
        y2.append((e - s))
        average_times = [round(y2[i] - y2[i - 1], 4) for i in range(len(y2))]
        if average_times[0] < 0:
            del average_times[0]
        average_times = statistics.mean(average_times)
        time_remaining = sum(average_times*k + (e-s) for k in range(no_simulations - i))
        if percentage <= 100:
            print("{}%     {} left".format(percentage, round_seconds(round(time_remaining))))
    print("Simulation Time: {}".format(round_seconds(round(time.time() - st))))  # Total simulation time
    plt.subplot(2, 1, 1)
    plt.plot(x1, y1)
    plt.subplot(2, 1, 2)
    plt.plot(x2, y2)
    plt.suptitle('# Players to Average Rolls; # Players to Time per Simulation')
    plt.xlabel('Number Of Players')
    plt.show()


no_players = 18
no_games = 100
seconds_per_roll = 5
money_per_player = 3
players = []

make_graph_total_simulations = 101

# print(simulate(no_players, no_games, seconds_per_roll, money_per_player, players))
make_graph(make_graph_total_simulations, no_games, seconds_per_roll, money_per_player, players)


# This script is a simulator for the game "Left, Right, Center". Everyone starts with a certain amount of starting
# money "money_per_player". When it's your turn, you roll 3 dice if you have 3 or more dollars, or else you roll dice
# for how much money your have. The dice has 6 sides with 6 options: 3 keep, 1 center, 1 left, and 1 right. If you roll
# a keep, you keep $1. If you have the last dollar, you win that game. If you roll a center, you put $1 in the center.
# If you are the last person with money, you win that game. If you roll a right, you give the person to your right $1.
# If you roll a left, you give the person to your left $1.
