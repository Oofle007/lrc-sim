import random
import statistics

dice = [0, 0, 0, 1, 2, 3]
# Keep = 0, left = 1, right = 2, center = 3


def roll_dice():
    output = random.randint(0, 5)
    return dice[output]


def play_one_game(no_players, no_money, players):
    players_cash = [no_money for i in range(no_players)]
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
        for j in range(no_rolls):  # Rolling no_rolls times
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
                if center_cash == (no_players * no_money) - 1 or center_cash >= no_players * no_money:  # Stops game
                    return all_rolls, players[current_player]
            if roll_result == 0:  # Rolls Keep
                if center_cash == (no_players * no_money) - 1 or center_cash > no_players * no_money:  # Stops game
                    return all_rolls, players[current_player]


def simulate(no_players, no_games, no_seconds, no_money, players):
    if len(players) < no_players:
        while len(players) < no_players:
            players.append("")
    next_target_percentage = 1
    all_games = []
    all_times = []
    all_players_won = []
    completed_games = 0
    for i in range(no_games):  # Plays number of games
        all_rolls = play_one_game(no_players, no_money, players)[0]
        all_players_won.append(play_one_game(no_players, no_money, players)[1])
        all_games.append(all_rolls)
        all_times.append(no_seconds*all_rolls)
        completed_games += 1
        percentage_left = round((completed_games / no_games) * 100, 1)  # Percent left in simulation
        if percentage_left >= next_target_percentage and not next_target_percentage > 100:  # Decides when to print %
            print(str(percentage_left) + "%" + "Time Left: " +)
            next_target_percentage += 1
    sec = round(statistics.mean(all_times))  # Average Seconds Per Game
    time = ""
    for d, u in [(60, "second"), (60, "minute"), (24, "hour"), (sec, "day")]:
        sec, n = divmod(sec, d)
        if n: time = f"{n} {u}" + "s" * (n > 1) + ", " * bool(time) + time
    if max(set(all_players_won), key=all_players_won.count) == "":  # Finding player who won the most
        player_won = "None Specified"
    else:
        player_won = max(set(all_players_won), key=all_players_won.count)
    times_won = all_players_won.count(player_won)
    return "\n" + "# Of Games Simulated: " + str(no_games) + "\n" + "# Of Players Per Game: " + str(
        no_players) + "\n" + "Time Spent Each Roll: " + str(no_seconds) + "s" + "\n" + "Average Rolls Per Game: " + str(
        round(statistics.mean(all_games))) + "\n" + "Maximum Roll Game: " + str(
        max(all_games)) + "\n" + "Minimum Roll Game: " + str(min(all_games)) + "\n" + "Average Time Per Game: " + str(
        time) + "\n" + "Player Who Won Most: " + player_won + ": " + str(times_won) + " Time(s)"

no_players = 7
no_games = 100000
seconds_per_roll = 10
money_per_player = 3
players = ["Aaron", "Alex", "Gage", "Mike", "Mikey", "Bach", "Barbara"]

print(simulate(no_players, no_games, seconds_per_roll, money_per_player, players))
