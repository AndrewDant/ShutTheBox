import random
import functools


# TODO this is probably pretty inefficient
def find_options(available_numbers, sum):
    # search the set of available numbers to find all combinations that add up to the sum
    # Return the set of all valid combinations, maybe as a list of lists
    
    options = []
    
    # assumes the numbers are sorted from small to large
    for i in range(len(available_numbers)):
        current_number = available_numbers[i]
        if current_number == sum:
            options.append([current_number])
        elif current_number < sum:
            # find all combinations of other numbers that add up to sum - current_number
            # don't need to look at smaller nums since ordered traversal assures their combos were already found
            sub_options = find_options(available_numbers[i+1:], sum - current_number)
            for sub in sub_options:
                options.append([current_number] + sub[:])
        else:
            # sorted list means all later numbers are also > so we are done
            break
        
    
    return options


def main():
    # random.seed(1)  # reproducability can be good for testing
    
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
        
        options = find_options([n for n, is_up in paddles.items() if is_up], rolled_sum)
        
        chosen_option = []
        if len(options) == 0:
            # end the game!
            score = sum([n for n, is_up in paddles.items() if is_up])
            print(f'Game Over! Your final score was: {score}\nFinal state:{paddles}')
            game_ongoing = False
            continue
        elif len(options) == 1:
            chosen_option = options[0]
        else:
            # default strategy is to always knock down the highest number possible            
            chosen_option = functools.reduce(lambda x, y: x if max(x) > max(y) else y, options)
        
        print(f'Knocked Down:')
        
        for num in chosen_option:
            paddles[num] = False
            print(num)
            
        if True not in paddles.values():
            # end the game!
            print('You managed to Shut The Box')
            game_ongoing = False
            continue


if __name__ == "__main__":
    main()