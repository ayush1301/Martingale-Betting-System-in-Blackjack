# Martingale Betting System in Blackjack
 
 ## Introduction
 ### Code
 This project is a self-playing blackjack program applying the Martingale betting strategy along with the blackjack basic strategy. It is known that the secret to winning blackjack is:
1. Using blackjack basic strategy to decide what action to take in response to the dealer's cards
2. Using card counting to determine how much to bet in a round
Having learnt the basic strategy, I wished to try different methods of determining the 'bet' in a round. Professional card counters seriously advise against the martingale betting method, since doubling the bet quickly escalates the amount leading to the risk of losing everything. However, these statements were made with lack of any evidence and just fear of losing large sums of money.

I hypothesised that if the minimum bet for a person is 1/1000 th of the original amount, the person will never lose since he will have to lose the game 9 times in a row to lose all of his money (which seemed like a highly unlikely event). Playing hundreds of these games on my own, I realised that the hypothesis was incorrect. However, trying the same hypothesis for 1/10000 of the original amount and so on would be extremely tiring. 

Thus, I have written this code, which simulates player(s) playing perfect blackjack basic strategy with the martingale betting strategy, where one can set the fraction of money used as the minimum bet. Using the code, the same games that I spent hours playing on my own could be replayed in less than a second! To simulate real games in a casino, various options such as H17 and S17 games etc can be chosen. (These terms and other options are explained later). 

 
 ### Martingale Betting Strategy
 In this strategy, the player first chooses a minimum betting amount. Every time the player loses, he doubles his bet, until the game is won. After winning, the player again bets the minimum bet chosen.

 Originally used in roulette, this strategy ensures that if a person has enough money, they'll always have a net gain, as the amount that the player is left with after finally winning equals the original sum + minimum bet.

 Although the betting system is fairly simple, some modifications had to be made to make it suitable for the game of blackjack. These modifications are mentioned in the next section. 

 ## How to Use the Code
The important files in the code are:
1. blackjack python file
2. All .csv files containing the basic strategy
These files are explained below:

### Python code - IMPORTANT
At the top of the file, under the "Variable constants" section, are all the variables that one can vary before running the program to produce the specific results. These are:
1. 'decks' - This determines the number of decks which will be used in a game. Most casinos use around 4/6 decks. Thus, this flexibility is provided to simulate games with different numbers of decks used. Once the given decks are used up, the program automatically reshuffles them as needed until the game is over.
2. 'fraction' - This is a variable such that its value n sets the martingale minimum bet to (1/n) of total money 
3. 'max_money' - This determines the starting amount for a player
4. 'maximum_splits_allowed' - Some casinos limit the number of splits a player can do at a time. The most common is 3. This means that in a given round the player can't have more than 4 hands (3 splits and one original). In case you do not want to have such a limit, just convert this line into a comment. A try-except block will deal with the rest.
5. 'num_players' - This simply represents the players on one table. All of them will have the starting balance 'max_money' and play the same strategy. With this variable, one can test if it is economical to participate in this strategy in teams.
6. 'rounds' - This represents the number of games played. This variable has been coded in a way that if a player is currently losing money in the last round, the number of rounds will be extended until the player wins. (Logically, if you decide to play 100 rounds and are on a losing streak on the 100th round, you are likely to play a few more rounds until you have recouped your money from the round. Thus, don't be surprised if the code runs for a few more rounds than indicated by you)
7. 'currency' - Add the currency symbol of your choice. This variable has no functionality. It is just for aesthetics in the graphs
8. 'game_type' - This is not an explicitly declared global variable. If the program is run without any command line arguments, the default game is set to 'H17', which means "Hit Soft 17" (The dealer hits on a soft 17). To simulate a different type of casino, where the dealer stands on a soft 17, enter the command line argument S17 when executing the program. 
9. 'show_plot' - Set this variable to true if you want to show the graph of the player's money V the number of rounds played
10. 'print_result' - Set this variable to True if you wish to see the result of each round printed

### Code output
#### Graph
The graph is pretty self-explanatory; however, a point to note is that the start, end, min and max values are annotated. If game is run with many players, these annotations can get clustered and make it to hard to read them.

#### Print
The print shows these values:
1. Round number
2. Player number
3. Player cards as a list
4. Card value
5. Bet value in that round
6. Money left with the player AFTER the round is over
7. Loss in the current martingale cycle (-ve value indicates the profit made in that cycle)
8. Dealer net - Showing the money lost or gained by dealer since the game began

### Python Code - certain corner cases and program behaviour (Read only if interested in working of the program)
Some corner cases in the code include:
    1. Winning after a huge losing streak - If a person is playing with 1000$ and has already lost more than 500$, the player is forced to bet all of the remaining money and the maximum amount of money he can have after winning is twice of the bet. Since bet < 500$, thus, money after winning < 1000$. Unlike other cases, the player **DOES NOT** recoup all the money after this win. Simulating real human behaviour, this is considered as a full win and the player restarts by betting the minimum amount (accepting the lost amount). 

### .csv files (Read only if interested in working of the program)
The .csv files represent the blackjack basic strategy. There are 3 csv files per game type. The hard or soft file is used if the player has a hard or soft total respectively. Each row represents the player's sum total and each column represents the dealer's sum total. Thus, a specific cell can be located and the appropriate action is determined. 'H' represents hit, 'S' represents stand, 'D' represents Double Down, 'Y' represents yes to splitting, and 'N' represents no to splitting. 

## Observed Results
I have run this test multiple times with different values of 'fraction'. It was observed that with 'fraction' = 1000, it took less than 1000 rounds for the player to lose all his money. In many cases, if the person began with a 1000$, his net gain was around 80 - 150$ after 100 rounds. For 'fraction' = 10,000, it took less than 10,000 rounds for the player to lose all his money. The player lost all the money with 'fraction' = 100,000 too. For fractions greater than 100,000, the return on investment is too low and were thus not tested. 

Thus, in the long run, a person playing the martingale betting strategy in blackjack is almost bound to **LOSE** all his money. 

## Future scope and updates
In addition to the variables present above, few more can be integrated into the code to allow it to resemble more and more casinos. These include:
1. Surrender- Surrendering is a part of the blackjack basic strategy and can be incorporated in the csv files and later the code
2. Limit on doubling after splitting and so on- Some casinos do not allow a double down after a split. A global variable representing this can be added to the code
3. Blackjack reward- Most casinos offer a 2:3 reward for scoring a blackjack. However, some offer only 1:1
4. Changing bets as amount increases- If one's original money is 1000$ and after playing a few rounds, the money increases to an amount > 2048$, the minimum amount can be doubled and the risk of losing all the money will remain the same. This feature is absent as of now.

 ## Author
 This project was written by Ayush Agarwal, Engineering student at the University of Cambridge.
