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
        pass

    def step(self):
        pass

    def reset(self):
        pass