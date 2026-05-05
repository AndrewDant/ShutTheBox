"""

def roll_dice():
    return two randomly generated dice results

def find_options(available_numbers, sum):
    search the set of available numbers to find all combinations that add up to the sum
    Return the set of all valid combinations, maybe as a list of lists

def main():
    paddles = { 1: True, 2: True, ..., 10: True}
    
    game_ongoing = True
    while game_ongoing:
        die1, die2 = roll_dice()
        sum = die1 + die2
        
        print(f'\nRolled {die1} + {die2} = {sum}')
        
        options = find_options([n for n, up in paddles.items() if up], sum)
        
        chosen_option = []
        if len(options) == 0:
            # end the game!
            game_ongoing = False
            continue
        elif len(options) == 1:
            chosen_option = options[0]
        else:
            chosen_option = ... # some logic to implement the strategy of choice
        
        print(f'Knocked Down:')
        
        for num in chosen_option:
            paddles[num] = False
            print(num)
            
        if True not in paddles.values():
            # TODO seems a bit inefficient to check them all every time
            # end the game!
            game_ongoing = False
            continue

"""