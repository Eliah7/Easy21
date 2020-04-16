import numpy as np

class Card:
    """
        [Class to represent a card used in the game Easy21]
    """
    def __init__(self, number=0, color="black"):
        """
        Keyword Arguments:
            number {int} -- [number of the card] (default: {0})
            color {str} -- [color of the card] (default: {"black"})
        """
        assert number >=0 and number <= 10, "The number has to be between 0 and 10"
        assert color=="black" or color=="red", "Color can only take the values \'red\' or \'black\'"

        self.number = number
        self.color = color

    def __str__(self):
        card_avatar = "🖤" if self.color == "black" else "❤️"
        return "{0} {1}".format(self.number, card_avatar)

class Deck:
    """
     [Class to represent an infinite deck of cards sampled uniformly to use in the game Easy21]

    All that is needed from this deck of cards in an infinite sample of a single card with 
    replacement meaning that two cards can be sampled with the same number and color.
    """
    def __init__(self, number_limit=10, colors=["black", "red"]):
        self.number_limit = number_limit
        self.colors = colors
    
    def draw(self):
        """[Method used to sample/ draw a card from an infinite deck of cards]
        
        Returns:
            [Card] -- [Returns a random card]
        """
        card_number = np.random.randint(0, self.number_limit+1)
        card_color = self.colors[np.random.choice([0, 1],p=[2/3, 1/3])] # choose black with prob 2/3 and red with prob 1/3
        
        return Card(number=card_number, color=card_color)
    
    def draw_color_card(self, color="black"):
        """[Returns a black card to be used at the initialization phase of the game]
        
        Returns:
            [Card] -- [returns a black card]
        """
        assert color in self.colors, "Color has to be a member of the colors available in the deck"

        card_number = np.random.randint(0, self.number_limit+1)
        return Card(number=card_number, color=color)

class Easy21GameEnvironment:
    def __init__(self):
        # Environment parameters
        self.actions = [0, 1] # 0: stick, 1: hit
        self.action_description = { 0 : "stick", 1 : "hit"}

        self.state_space_shape = (1, 1) # (Dealer's first card, Sum of the players cards)
        self.state_description = "(Dealer's first card, Sum of the players cards)"
        self.state_space_max = (10, 21) # (max card possible, maximum sum of cards before busting)

        # Game parameters
        self.deck = Deck()
        self.dealers_sum = 0 # players sum is part of the state

        # Initializing the game
        self.reset()

    def step(self, action):
        """[Function that the agent uses to interact with the environment]
        
        \nArguments:
            action {[int]} -- [{ 0 : "stick", 1 : "hit"}]
        
        \nReturns:
            [tuple] -- [ reward, next_state, done]
           \n {   
                reward => How much reward for the current state?
                next_state => What state is the environment in now?
                done => Is this the terminal state?
            }
                        
        """
        assert action in self.actions, "Only two actions are possible { 0 : \"stick\", 1 : \"hit\"}"

        if action == 0:  
            self.dealer_acts() 
            reward = self.reward(self.current_state) # collect reward for being in this state
        
        else:
            drawn_card = self.deck.draw()
            self.current_state = (self.current_state[0], self.evaluate_sum(self.current_state[1], drawn_card))
            
            self.dealer_acts()
            
            reward = self.reward(self.current_state) # collect reward for being in this state 
        return reward, self.current_state, self.done

    def evaluate_current_state(self):
        if self.current_state[1] > 21:
            self.done = True
        else:
            self.done = False

    def dealer_acts(self):
        """[Policy for actions that the dealer takes given the current state]
            
            \n=> The player is unaware of the dealers actions as they do not mutate state
        """
        if self.dealers_sum < 17: # hit
            drawn_card = self.deck.draw()
            self.dealers_sum = self.evaluate_sum(self.dealers_sum, drawn_card)
        else: # stay
            return

    def evaluate_sum(self, current_sum, card):
        """[Evaluates the new sum given the type of card that is drawn]
        
        \nArguments:
            current_sum {[int]} -- [Current sum of either the player or the dealer]
            card {[Card]} -- [Card that is drawn from the deck]
        """
        if card.color == "black":
            return (current_sum + card.number)
        else:
            return (current_sum - card.number)

    def reset(self):
        dealers_card = self.deck.draw_color_card(color="black")
        players_card = self.deck.draw_color_card(color="black")
        self.current_state = (dealers_card.number, players_card.number) 
        self.dealers_sum = dealers_card.number
        self.done = False
    
    def reward(self, state):
        """[Function that returns the reward given the state]
            -1 : Player Busts (x, >21) and 
             0 : Draw or game is not over (x, <=21)
            +1 : Player wins (x, <=21) and players_sum > dealers_sum and each has already taken atleast one turn
        \nArguments:
            state {[tuple]} -- [tuple describing the current state of the game check self.state_description for more information]
        \nReturns:
            [int] - [Amount of reward the agent receives]
        """
        if state[1] > 21 and not self.done:
            self.done = True
            return -1

        if not self.done and self.dealers_sum == state[1] and state[1] <= 21:
            self.done = True
            return 0

        if state[1] <= 21 and self.dealers_sum < state[1] and not self.done:
            self.done = True
            return 1

        if state[1] <= 21 and self.dealers_sum > state[1] and not self.done:
            self.done = True
            return 0

        
