import random
import functools
import simulator

DOUBLE_DICE_PADDLES = [7, 8, 9]


def random_choice(options, paddles):
    return random.choice(options)


def highest_numbers(options, paddles):
    # solution has to look at all numbers since max # in an array could be equal and order isn't helpful
    # eg consider [[1,4,6], [2,3,6], [5,6]] as options
    # their order cannot tell you which to pick, since 5 > 4 > 3
    def option_with_highest(aggregate, current):
        result = aggregate
        
        for i in range(1, min(len(aggregate), len(current)) + 1):
            # work backwards since the arrays are sorted.
            if current[-i] != aggregate[-i]:
                result = current if current[-i] > aggregate[-i] else aggregate
                break
        
        return result
    
    # always knock down the highest number possible
    return functools.reduce(option_with_highest, options)


def highest_preserve_double(options, paddles):
    remaining_double_dice_paddles = [n for n in DOUBLE_DICE_PADDLES if paddles[n]]
    
    # retain a list of options o if there is a # in the remaining double dice paddles that is not in o
    # aka chuck each list o such that ALL #'s in the remaining double dice paddles are in o
    def preserves_double(option):
        preserves = False
        
        for paddle in remaining_double_dice_paddles:
            if paddle not in option:
                preserves = True
                break
        
        return preserves
    
    # the list of options which will use 2 dice on following rolls
    options_retaining_double = []
    if len(remaining_double_dice_paddles) > 0:
        options_retaining_double = [option for option in options if preserves_double(option)]
    
    if len(options_retaining_double) > 0:
        return highest_numbers(options_retaining_double, paddles)
    else:
        return highest_numbers(options, paddles)


def preserve_double_until_10_is_down(options, paddles):
    # if the 10 is still up try to preserve double dice. Once it's down just knock the highest
    if paddles[10]:
        return highest_preserve_double(options, paddles)
    else:
        return highest_numbers(options, paddles)


# minimizes the NUMBER of possible dead rolls next turn (not the odds of a dead roll)
def minimize_dead_rolls(options, paddles):
    # TODO duplicated logic for checking doubles preservation
    
    remaining_double_dice_paddles = [n for n in DOUBLE_DICE_PADDLES if paddles[n]]
    
    # retain a list of options o if there is a # in the remaining double dice paddles that is not in o
    # aka chuck each list o such that ALL #'s in the remaining double dice paddles are in o
    def preserves_double(option):
        preserves = False
        
        for paddle in remaining_double_dice_paddles:
            if paddle not in option:
                preserves = True
                break
        
        return preserves
    
    # the list of options which will use 2 dice on following rolls
    options_retaining_double = []
    if len(remaining_double_dice_paddles) > 0:
        options_retaining_double = [option for option in options if preserves_double(option)]
    
    min_dead_rolls = 10 # equivalent to int max for this use case
    best_options = []
    
    # possible rolls depends on whether rolling 1 or 2 dice, so we need separate logic for options in each case
    for option in options_retaining_double:
        dead_rolls = 0
        available_numbers = [n for n, is_up in paddles.items() if is_up and n not in option]
        
        # with 2 dice the possible rolls are 2 - 12
        for sum in range(2, 13):
            new_options = simulator.find_options(available_numbers, sum)
            if len(new_options) == 0:
                dead_rolls += 1
        
        if dead_rolls < min_dead_rolls:
            # new best so we restart the list
            best_options = [option]
            min_dead_rolls = dead_rolls
        elif dead_rolls == min_dead_rolls:
            best_options.append(option)
    
    # the list of options which will use only 1 die on following rolls (if not already)
    non_doubles_options = [option for option in options if option not in options_retaining_double]
    
    for option in non_doubles_options:
        dead_rolls = 0
        available_numbers = [n for n, is_up in paddles.items() if is_up and n not in option]
        
        # with 1 die the possible rolls are 1 - 6
        for sum in range(1, 7):
            new_options = simulator.find_options(available_numbers, sum)
            if len(new_options) == 0:
                dead_rolls += 1
        
        if dead_rolls < min_dead_rolls:
            # new best so we restart the list
            best_options = [option]
            min_dead_rolls = dead_rolls
        elif dead_rolls == min_dead_rolls:
            best_options.append(option)
    
    # need a tiebreaker of some kind
    return highest_preserve_double(best_options, paddles)