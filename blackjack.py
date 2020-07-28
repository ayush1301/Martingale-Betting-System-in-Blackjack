import csv
import sys
import random
import matplotlib.pyplot as plt

#for efficiency, consider using lists instead of dictionaries
#for efficiency, consider addinf the indeces of all 11s in a list to make searching easier

    #"Variable constants"
#number of decks of cards played with
decks = 6
#n such that (1/n) of total money represents min bet --- (Most important)
fraction = 1000
max_money = 1000
#maximum_splits_allowed = 3
num_players = 2
rounds = 1000
currency = '$'
show_plot = True
print_result = True
#'£' '₹' '€' '¥' '$'

    #Other important global variables
shoe = []
players = []
game_type = None
soft_data = None
hard_data = None
split_data = None
dealer = None
decks_played = 0
#all data is a dictionary in form -- variable['player number']['dealer number']

def main():
    game()

def game():
    global game_type, soft_data, hard_data, split_data, dealer, rounds, decks_played
    if len(sys.argv) == 1 or sys.argv[1].upper() == 'H17':
        game_type = 'H17'
        get_data()
    elif sys.argv[1].upper() == 'S17':
        game_type = 'S17'
        get_data()
    else:
        print("Enter correct command line arguments")
        sys.exit(1)

    #pre-trial setup
    for i in range(num_players):
        players.append(Player(max_money))
    dealer = Dealer()
    
    #setup for plotting
    x = [0]
    y = {f'Player {i + 1}': [max_money] for i in range(len(players))}

    round_num = 1
    while round_num <= rounds:
        #dealing two cards to each player and 1 to dealer
        for player in players:
            if player.paused:
                continue
            player.add_hand(None)
            player.hands[0].deal()
        dealer.hand.deal()
        for player in players:
            if player.paused:
                continue
            player.hands[0].deal()
        
        #players playing the basic strategy
        for player in players:
            if player.paused:
                continue
            for hand in player.hands:
                hand.action()
        dealer.hand.action()
       
        #calculating results of all hands
        for n, player in enumerate(players):
            if player.paused:
                continue
            for hand in player.hands:
                hand.result()
                if print_result:
                    print(f'Round {round_num}: Player {n + 1} ', end="")
                    hand.print_all()
        if print_result:
            print(f'Round {round_num}: ', end="")
            dealer.hand.print_all()

        #plotting updates
        x.append(round_num)
        for i in range(len(players)):
            y[f'Player {i + 1}'].append(players[i].money_left)

        #preparing for next round
        for player in players:
            if player.paused:
                continue
            player.reset()
        dealer.reset()

        #pausing players if they're out of money
        for player in players:
            if player.money_left == 0:
                player.paused = True

        #ending game if all players are out
        if all(player.money_left == 0 for player in players):
            print('All players lost')
            break
        
        #extending rounds until the player wins the current martingale game
        if round_num == rounds:
            for player in players:
                if player.current_loss <= 0:
                    player.paused = True
            rounds += 1
        
        #finishing game if no players have a loss in the current martingale game
        if all(player.paused for player in players):
            print('Game successfully over')
            break

        # while loop continuation
        if round_num < rounds:
            round_num += 1

    #Printing Final stats
    print(f'Rounds played = {round_num}, Decks finished <= {decks_played}')

    #Plotting graph
    if show_plot:
        for player, f in sorted(y.items()):
            fmax = max(f)
            fmax_indeces = [index for index, item in enumerate(f) if item == fmax]
            fmin = min(f)
            if fmin == 0:
                fmin_indeces = [f.index(fmin)]
            else:
                fmin_indeces = [index for index, value in enumerate(f) if value == fmin]
            #Critical in order [start, end, max, min]
            critical = [x[0], x[-1], x[fmax_indeces[-1]], x[fmin_indeces[-1]]]
            plt.plot(x, f, '-o', markevery=critical, label=player)
            plt.annotate(f'({x[0]}, {f[0]:.2f})', (x[0], f[0]), ha='center', xytext=(0, 5), textcoords='offset points')
            plt.annotate(f'({x[-1]}, {f[-1]:.2f})', (x[-1], f[-1]), ha='center', xytext=(0, 5), textcoords='offset points')
            plt.annotate(f'({critical[2]}, {fmax:.2f})', (critical[2], fmax), ha='center', xytext=(0, 5), textcoords='offset points')
            plt.annotate(f'({critical[3]}, {fmin:.2f})', (critical[3], fmin), ha='center', xytext=(0, 5), textcoords='offset points')
        plt.title(f'Martingale Betting Strategy Applied to {game_type} Blackjack Game')
        plt.xlabel('Number of Rounds')
        plt.ylabel(f'Money in {currency} with Player')
        plt.legend()
        plt.show()
    
            
def get_data():
    global soft_data, hard_data, split_data
    soft_data = form_dict(f'{game_type} Soft.csv')
    hard_data = form_dict(f'{game_type} Hard.csv')
    split_data = form_dict(f'{game_type} Split.csv')   

def form_dict(file_name):
    file = open(file_name, encoding='utf-8-sig')
    return {row['Input'] : row for row in csv.DictReader(file)}

class Player:
    def __init__(self, money):
        self.hands = []
        self.money_left = money
        self.current_loss = 0
        self.min_bet = money / fraction
        self.paused = False
        self.dying = False
    
    def add_hand(self, bet):
        if bet == None:
            bet = self.decide_bet()
        self.hands.append(Hand(self, bet))
        self.money_left -= bet
        self.current_loss += bet
        return self.hands[-1]

    def decide_bet(self):
        if self.current_loss < 0:
            self.current_loss = 0
        bet = self.current_loss + self.min_bet
        if bet > self.money_left:
            self.dying = True
            return self.money_left
        else:
            return bet

    def reset(self):
        self.hands.clear()
        self.dying = False
     
class Dealer(Player):
    def __init__(self):
        self.net = 0
        self.hand = DealerHand(self)
        
    def reset(self):
        self.hand = DealerHand(self)
        

class Hand:
    def __init__(self, player, bet):
        self.bet = bet
        self.player = player
        self.hand_setup()

    def hand_setup(self):
        self.cards = []
        self.aces_dealt = 0
        self.type = 'hard'
        self.value = 0
        self.is_split = False

    def deal(self):
        while True:
            if len(shoe) == 0:
                global decks_played
                decks_played += decks
                for i in range(decks * 4):
                    shoe[len(shoe):] = [2,3,4,5,6,7,8,9,10,10,10,10,11]
            else:
                new_card = shoe.pop(random.randint(0, len(shoe) - 1))
                if new_card == 11:
                    self.aces_dealt += 1
                self.cards.append(new_card)
                if self.aces_dealt:
                    self.hand_type()
                self.hand_value()
                break

    #only for testig purposes

    ###############
    def deal_particular_card(self, card):
        self.cards.append(card)
        if card == 11:
            self.aces_dealt += 1
        self.update()
    ##############


    def print_all(self):
        print(f'cards = {self.cards}, value = {self.value}, bet = {self.bet:.2f}{currency}, ', end="")
        print(f'money_left = {self.player.money_left:.2f}{currency}, current_loss = {self.player.current_loss:.2f}{currency}')

    def hand_type(self):
        if self.aces_dealt:
            self.type = 'soft'
        else:
            self.type = 'hard'

    def hand_value(self):
        value = sum(self.cards)
        if len(self.cards) == 2 and value == 21 and not self.is_split: #len(self.player.hands) == 1
            self.value = 'blackjack'
        elif value <= 21:
            self.value = value
        else:
            if self.type == 'hard':
                self.value = 'bust'
            else:
                if self.aces_dealt:
                    for i in range(len(self.cards)):
                        if self.cards[i] == 11:
                            self.cards[i] = 1
                            self.aces_dealt -= 1
                            self.update()
                            break
                    
    def update(self):
        #efficiency improvement opportunity
        self.hand_type()
        self.hand_value()

    def response_val(self, data):
        return data[str(self.value)][str(dealer.hand.value)]

    def response(self, data_type):
        if self.response_val(data_type) == 'D':
            if self.player.money_left < self.bet: #check logic
                if not self.value in range(18, 20):
                    self.deal()
                    self.action()
                    return 
                else:
                    return
            self.player.money_left -= self.bet
            self.player.current_loss += self.bet
            self.bet *= 2
            self.deal()
        elif self.response_val(data_type) == 'H':
            self.deal()
            self.action()
        elif self.response_val(data_type) == 'S':
            pass
        else:
            print('Error in response')
            sys.exit(3)

    def split_max_check(self):
        try:
            if len(self.player.hands) > maximum_splits_allowed:
                self.response(hard_data)
                #return
            else:
                self.split()
                self.action()
                #return
        except NameError:
            self.split()
            self.action()

    def action(self):
        if isinstance(self.value, str):
            return
        if self.is_split:
            self.deal()
            self.is_split = False
        if len(self.cards) == 2:
            if self.cards[0] == self.cards[1]:
                if self.response_val(split_data) == 'Y':
                    #add max split error block
                    if self.player.money_left < self.bet: #or len(self.player.hands) > maximum_splits_allowed:
                        self.response(hard_data)
                        #return
                    else:
                        self.split_max_check()
                    return
            elif self.cards[0] == 1 and self.cards[1] == 11:
                if self.player.money_left < self.bet: #or len(self.player.hands) > maximum_splits_allowed: # check logic
                    self.response(hard_data)
                    #return
                else:
                    self.split_max_check()
                return
        if self.type == 'soft':
            self.response(soft_data)
        elif self.type == 'hard':
            self.response(hard_data)

    def split(self):
        new_hand = self.player.add_hand(self.bet)
        new_hand.cards.append(self.cards.pop(1))
        if 1 in self.cards:
            self.cards[0] = 11
            self.aces_dealt = 1
            new_hand.aces_dealt = 1
        self.update()
        self.is_split = True
        new_hand.is_split = True
        new_hand.update()

    #need to check
    def result(self):
        #efficiency improvement opportunity
        if self.value == 'bust':
            self.lose()
        elif self.value == 'blackjack':
            if dealer.hand.value == 'blackjack':
                self.push()
            else:
                self.win()
        elif isinstance(dealer.hand.value, str):
            if dealer.hand.value == 'blackjack':
                self.lose()
            else:
                self.win()
        elif dealer.hand.value > self.value:
            self.lose()
        elif dealer.hand.value < self.value:
            self.win()
        elif dealer.hand.value == self.value:
            self.push()
        else:
            print('Logic error in result function')
            sys.exit(2)

    def win(self):
        if self.value == 'blackjack':
            self.player.money_left += 2.5 * self.bet
            self.player.current_loss -= 2.5 * self.bet
            dealer.net -= 1.5 * self.bet
        else:
            self.player.money_left += 2 * self.bet
            self.player.current_loss -= 2 * self.bet
            dealer.net -= self.bet
        if self.player.dying:
            self.player.current_loss = 0
        #add change to betting

    def lose(self):
        dealer.net += self.bet

    def push(self):
        self.player.money_left += self.bet
        self.player.current_loss -= self.bet
    
class DealerHand(Hand):
    def __init__(self, player): #think if is_split affects dealer
        self.hand_setup()
        self.dealer = player

    def action(self):
        while True:
            if isinstance(self.value, str):
                break
            elif self.value < 17:
                self.deal()
            elif self.value > 17:
                break
            elif self.value == 17:
                if self.type == 'hard':
                    break
                else:
                    if game_type == 'H17':
                        self.deal()
                    else:
                        break
    
    def print_all(self):
        print(f'Dealer cards = {self.cards}, value = {self.value}, net = {self.dealer.net:.2f}{currency}')

main()