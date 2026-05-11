import functools

DOUBLE_DICE_PADDLES = [7, 8, 9]


def highest_numbers(options, paddles):
    # TODO this currently doesn't handle == max's correctly
    # eg consider [[1,4,6], [2,3,6], [5,6]] as options
    # their order cannot tell you which to pick, since 5 > 4 > 3
    
    option_with_highest = lambda aggregate, current: aggregate if max(aggregate) > max(current) else current
    
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
