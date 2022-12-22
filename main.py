import random
import statistics
import matplotlib.pyplot as plt
import time

dice = [0, 0, 0, 1, 2, 3]  # Keep = 0, left = 1, right = 2, center = 3


def play_one_game(no_players, no_money, players):
    players_cash = [no_money for _ in range(no_players)]
    center_cash = 0
    current_player = -1
    all_rolls = 0
    stop = False
    while not stop:  # 1 Game Running
        current_player += 1
        current_player = current_player % no_players  # Setting current player index
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
                    return all_rolls, players[current_player]
            if roll_result == 0:  # Rolls Keep
                if center_cash == (no_players * no_money) - 1 or center_cash > no_players * no_money:  # Stops game
                    return all_rolls, players[current_player]


def check_invalid_params(params):
    for param in params:
        if not param > 0 or type(param) != int:
            return True
    return False


def simulate(no_players, no_games, no_seconds, no_money, players, isReturningAllStats=True):
    if check_invalid_params((no_games, no_players, no_seconds)):
        return '\nAll inputs need a positive integer value'
    import time
    starting = time.perf_counter()
    if len(players) < no_players:
        while len(players) < no_players:
            players.append("")
    if no_players < len(players):
        return "Too many player names"
    next_target_percentage = 1
    simulation_seconds_per_game = []
    all_games = []
    all_times = []
    all_players_won = []
    completed_games = 0
    start = time.perf_counter()
    for i in range(no_games):  # Plays number of games
        started = time.perf_counter()
        all_rolls = play_one_game(no_players, no_money, players)[0]
        all_players_won.append(play_one_game(no_players, no_money, players)[1])
        all_games.append(all_rolls)
        all_times.append(no_seconds * all_rolls)
        completed_games += 1
        if isReturningAllStats:
            percentage_left = round((completed_games / no_games) * 100, 1)  # Percent left in simulation
            if percentage_left >= next_target_percentage and not next_target_percentage > 100:  # Decides when to print %
                end = time.perf_counter()
                time_left = (end - start) * (100 - percentage_left)
                start = time.perf_counter()
                sec = round(time_left)  # Average Seconds Per Game
                timer = ""
                if sec > 0:
                    for d, u in [(60, "second"), (60, "minute"), (24, "hour"), (sec, "day")]:
                        sec, n = divmod(sec, d)
                        if n: timer = f"{n} {u}" + "s" * (n > 1) + ", " * bool(timer) + timer
                else:
                    timer = "0 seconds"
                print(str(percentage_left) + "%" + " Time Left: " + str(timer))
                next_target_percentage += 1
            ended = time.perf_counter()
            simulation_seconds_per_game.append(ended - started)
    sec = round(statistics.mean(all_times))  # Average Seconds Per Game
    timer = ""
    for d, u in [(60, "second"), (60, "minute"), (24, "hour"), (sec, "day")]:
        sec, n = divmod(sec, d)
        if n: timer = f"{n} {u}" + "s" * (n > 1) + ", " * bool(timer) + timer
    if max(set(all_players_won), key=all_players_won.count) == "":  # Finding player who won the most
        player_won = "None Specified"
    else:
        player_won = max(set(all_players_won), key=all_players_won.count)
    times_won = all_players_won.count(player_won)
    ending = time.perf_counter()
    if isReturningAllStats:
        return "\n# Of Games Simulated: " + str(no_games) + "\n# Of Players Per Game: " + str(
            no_players) + "\nTime Spent Each Roll: " + str(no_seconds) + "s\nAverage Rolls Per Game: " + str(
            round(statistics.mean(all_games))) + "\nMaximum Roll Game: " + str(
            max(all_games)) + "\nMinimum Roll Game: " + str(min(all_games)) + "\nAverage Time Per Game: " + str(
            timer) + "\nPlayer Who Won Most: " + player_won + ": " + str(times_won) + " Time(s)\nSimulation Time: " + str(
            round(ending - starting, 4)) + "s\nAverage Simulation Time Per Game: " + str(
            round(statistics.mean(simulation_seconds_per_game), 8)) + "s"
    else:
        return round(statistics.mean(all_games))


no_players = 15
no_games = 100000
seconds_per_roll = 15
money_per_player = 3
players = []


def make_graph(total_players):
    x1 = []
    y1 = []
    x2 = []
    y2 = []
    for i in range(2, total_players):
        x1.append(i)
        x2.append(i)
        s = time.time()
        y1.append(simulate(i, no_games, seconds_per_roll, money_per_player, players, False))
        e = time.time()
        y2.append((e - s)*1000)
        print("{}%   {}".format(str(round(i/(total_players-2)*100, 2)), e - s))
    plt.plot(x1, y1, label="Average Rolls")
    plt.plot(x2, y2, label="Time for simulation of {} games".format(total_players))
    plt.xlabel('Number Of Players')
    plt.ylabel('Average # Of Rolls Per Game')
    plt.title('Graph of # of player to average rolls per game')
    print(x1)
    print(y1)
    plt.show()


print(simulate(no_players, no_games, seconds_per_roll, money_per_player, players))
# make_graph(1000)  # Parameter is how many simulations you want to run

# This script is a simulator for the game "Left, Right, Center". Everyone starts with a certain amount of starting
# money "money_per_player". When it's your turn, you roll 3 dice if you have 3 or more dollars, or else you roll dice
# for how much money your have. The dice has 6 sides with 6 options: 3 keep, 1 center, 1 left, and 1 right. If you roll
# a keep, you keep $1. If you have the last dollar, you win that game. If you roll a center, you put $1 in the center.
# If you are the last person with money, you win that game. If you roll a right, you give the person to your right $1.
# If you roll a left, you give the person to your left $1. When the simulation is running, it will give you the
# percentage of games it has done and the time left in the simulation. When the simulation is done, it will give you
# the average rolls per game, maximum roll game, minimum roll game, and the average time taken each game (taking into
# account the "seconds_per_roll" parameter. You can also put in the names of the players in the game, so you can see who
# won the most.
