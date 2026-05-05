# Shut the Box Simulator
WIP
Intended to allow me to simulate a large number of plays of the game Shut the Box using different strategies, generating and saving data about the outcomes of each game (essentially Monte Carlo experiments)

## Steps
1. Writes some steps
2. Simulate a Single Game with the simplest strategy
    - Write high level pseudocode
    - pseudocode for helper functions
    - implement and test the helper functions
    - TODO add the logic to switch from two dice to one
3. Update the code to simulate an arbitrary number of games
    - constant value or command line input the number
    - probably just a for loop over the step two code
4. Save game data to the disk
    - Need to think about what I care to save. Better too much than too little but could start simple
    - pick a format. Probably CSV
    - One table or multiple?