import random
import json
import strategies
from inspect import getmembers, isfunction

# get all the strategy funcs from the import in a single list
strategy_list = [s[1] for s in getmembers(strategies, isfunction)]

def find_options(available_numbers, roll_sum):
    # search the set of available numbers to find all combinations that add up to the sum
    # Return the set of all valid combinations as a list of lists
    
    options = []
    # logic assumes the numbers are sorted from small to large
    available_numbers.sort()
    
    # recursively search for valid combinations
    def search(start_index, current_sum, current_option):
        for i in range(start_index, len(available_numbers)):
            current_number = available_numbers[i]
            remaining_target = (roll_sum - current_sum)
            
            if current_number == remaining_target:
                # current number is exactly the right size. Add to the options list
                options.append(current_option[:] + [current_number])
                break
            elif current_number < remaining_target:
                # find all combinations of other numbers that add up to sum - current_number
                # don't need to look at smaller nums since ordered traversal assures their combos were already found
                search(i+1, current_sum + current_number, current_option[:] + [current_number])
            else:
                # current is > target. sorted list means all later numbers are also > so we are done
                break
    
    # run the recursive search to populate the options list
    search(0, 0, [])
    
    return options


def run_game(strategy, game):
    game_index, game_rolls = game
    
    log = {
        "strategy": strategy.__name__,
        "game_index": game_index,
        "rolls": [],
        "knockdowns": [],
        "score": None,
        "strategy_calls": 0
    }

    paddles = { n: True for n in range(1, 11)}
    
    for roll in game_rolls:
        die1 = roll[0]
        die2 = 0
        
        if paddles[7] or paddles[8] or paddles[9]:
            # only roll 1 die if 7/8/9 are all down
            die2 = roll[1]
            
        rolled_sum = die1 + die2
        
        if print_progress: print(f'\nRolled {die1} + {die2} = {rolled_sum}')
        
        log["rolls"].append(rolled_sum)
        
        options = find_options([n for n, is_up in paddles.items() if is_up], rolled_sum)
        
        chosen_option = []
        if len(options) == 0:
            # end the game!
            score = sum([n for n, is_up in paddles.items() if is_up])
            
            if print_progress: print(f'Game Over! Your final score was: {score}\nFinal state:{paddles}')
            
            log["score"] = score
            break
        elif len(options) == 1:
            chosen_option = options[0]
        else:
            # a strategy function should accept the list of possible options and the paddles state and return a single option
            chosen_option = strategy(options, paddles)
            log["strategy_calls"] += 1
        
        if print_progress: print(f'Knocked Down: {", ".join([str(n) for n in chosen_option])}')
        
        log["knockdowns"].append(chosen_option)
        for num in chosen_option:
            paddles[num] = False
            
        if True not in paddles.values():
            # end the game!
            if print_progress: print(f'You managed to Shut The Box\nFinal state:{paddles}')
            
            log["score"] = 0
            break
        
    return log


if __name__ == "__main__":
    # random.seed(1)  # reproducability could be good for testing
    print_progress = False
    
    logs = []
    games = []
    GAME_COUNT = 10000
    
    for game_index in range(GAME_COUNT):
        game_rolls = []
        for i in range(10):
            die1 = random.randint(1, 6)
            die2 = random.randint(1, 6)
            game_rolls.append((die1, die2))
            
        games.append((game_index, game_rolls))
    
    for strategy in strategy_list:
        for game in games:
            if print_progress: print(f'\n\nGAME {game[0]}:\n')
            
            game_log = run_game(strategy, game)
            logs.append(game_log)
    
    FILENAME = "data.json"
    with open(FILENAME, "w") as f:
        json.dump(logs, f)
    
    # alt print when it ends if not printing during run
    if not print_progress: print('Done!')