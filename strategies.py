import functools

DOUBLE_DICE_PADDLES = [7, 8, 9]


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