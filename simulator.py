import random
import json
import strategies

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


def run_game(strategy):
    log = {
        "strategy": strategy.__name__,
        "rolls": [],
        "knockdowns": [],
        "score": None
        }

    paddles = { n: True for n in range(1, 11)}
    
    game_ongoing = True
    while game_ongoing:
        # return two randomly generated dice results
        die1 = random.randint(1, 6)
        die2 = 0
        
        if paddles[7] or paddles[8] or paddles[9]:
            # only roll 1 die if 7/8/9 are all down
            die2 = random.randint(1, 6)
            
        rolled_sum = die1 + die2
        
        print(f'\nRolled {die1} + {die2} = {rolled_sum}')
        log["rolls"].append(rolled_sum)
        
        options = find_options([n for n, is_up in paddles.items() if is_up], rolled_sum)
        
        chosen_option = []
        if len(options) == 0:
            # end the game!
            score = sum([n for n, is_up in paddles.items() if is_up])
            print(f'Game Over! Your final score was: {score}\nFinal state:{paddles}')
            game_ongoing = False
            log["score"] = score
            continue
        elif len(options) == 1:
            chosen_option = options[0]
        else:
            # default strategy is to always knock down the highest number possible            
            chosen_option = strategy(options, paddles)
        
        print(f'Knocked Down:')
        log["knockdowns"].append(chosen_option)
        for num in chosen_option:
            paddles[num] = False
            print(num)
            
        if True not in paddles.values():
            # end the game!
            print('You managed to Shut The Box')
            game_ongoing = False
            log["score"] = 0
            continue
        
    return log


if __name__ == "__main__":
    # random.seed(1)  # reproducability could be good for testing
    
    logs = []
    GAME_COUNT = 100
    
    for game in range(GAME_COUNT):
        print(f'\n\nGAME {game}:\n')
        game_log = run_game(strategies.highest_preserve_double)
        logs.append(game_log)
    
    FILENAME = "data.json"
    with open(FILENAME, "w") as f:
        json.dump(logs, f)
    
    print(game_log)