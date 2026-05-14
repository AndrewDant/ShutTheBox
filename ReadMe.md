# Shut the Box Simulator
WIP
Intended to allow me to simulate a large number of plays of the game Shut the Box using different strategies, generating and saving data about the outcomes of each game (essentially Monte Carlo experiments)

## Steps
1. Writes some steps
2. Simulate a Single Game with the simplest strategy
    - Write high level pseudocode
    - pseudocode for helper functions
    - implement and test the helper functions
3. Save game data to the disk
    - Need to think about what I care to save. Better too much than too little but could start simple
    - pick a format. Probably CSV
    - One table or multiple?
4. Update the code to simulate an arbitrary number of games
    - constant value or command line input the number
    - probably just a for loop over the step two code
5. Define multiple game strategies and update the game simulator to use a chosen one

6. Write steps for EDA
7. Start with a separate .ipynb file
8. import the json data
    - read the file into memory
    - convert it into a pandas DataFrame?