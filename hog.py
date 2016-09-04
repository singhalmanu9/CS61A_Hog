"""CS 61A Presents The Game of Hog."""

from dice import four_sided, six_sided, make_test_dice
from ucb import main, trace, log_current_line, interact
from math import sqrt

GOAL_SCORE = 100  # The goal of Hog is to score 100 points.


######################
# Phase 1: Simulator #
######################

def roll_dice(num_rolls, dice=six_sided):
    """Simulate rolling the DICE exactly NUM_ROLLS>0 times. Return the sum of
    the outcomes unless any of the outcomes is 1. In that case, return the
    number of 1's rolled.
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'

    number_of_ones = 0;
    sum = 0;
    for i in range(num_rolls):
        roll = dice()
        if roll == 1:
            number_of_ones += 1

        sum += roll

    if not number_of_ones == 0:
        return number_of_ones
    else:
        return sum


def free_bacon(opponent_score):
    """Return the points scored from rolling 0 dice (Free Bacon)."""

    first_digit = opponent_score // 10
    last_digit = opponent_score % 10
    return max(first_digit, last_digit) + 1


# Write your prime functions here!
def is_prime(n):


    """Determines that N is prime and makes sure that 1 returns False"""
    if n == 1:
        return False

    # Makes sure 2 is considered prime, to fix bug with n % 2 statement
    if n == 2:
        return True

    # A simple check to improve efficiency
    if n % 2 == 0:
        return False

    # Checks every number between 3 and the sqrt of the number
    for i in range(int(sqrt(n) // 1), 2, -1):
        if n % i == 0:
            return False

    # If it's gotten this far, it must be prime
    return True

def next_prime(n):
    i = n + 1
    while not is_prime(i):
        i += 1
    return i


def hogtimus_prime(n):
    if is_prime(n):
        return next_prime(n)
    else:
        return n

def when_pigs_fly(score,num_rolls):
    limit = 25 - num_rolls
    return min(limit, score)

def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free Bacon).
    Return the points scored for the turn by the current player. Also
    implements the Hogtimus Prime and When Pigs Fly rules.

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function of no args that returns an integer outcome.
    """
    # Leave these assert statements here; they help check for errors.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice in take_turn.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < 100, 'The game should be over.'

    score = 0

    #test to see if free_bacon
    if num_rolls == 0:
        score = free_bacon(opponent_score)
    else:
        score = roll_dice(num_rolls, dice)

    #implement Hogtimus Prime
    score = hogtimus_prime(score)

    #implements when Pigs Fly rules
    score = when_pigs_fly(score, num_rolls)

    return score


def reroll(dice):
    """Return dice that return even outcomes and re-roll odd outcomes of DICE."""
    def rerolled():
        "*** REPLACE THIS LINE ***"
        roll = dice()
        if roll % 2 == 1:
            roll = dice()

        return roll

    return rerolled


def select_dice(score, opponent_score, dice_swapped):
    """Return the dice used for a turn, which may be re-rolled (Hog Wild) and/or
    swapped for four-sided dice (Pork Chop).

    DICE_SWAPPED is True if and only if four-sided dice are being used.
    """

    if dice_swapped:
        dice = four_sided
    else:
        dice = six_sided

    if (score + opponent_score) % 7 == 0:
        dice = reroll(dice)
    return dice


def other(player):
    """Return the other player, for a player PLAYER numbered 0 or 1.

    >>> other(0)
    1
    >>> other(1)
    0
    """
    return 1 - player

def pork_chop(dice_swapped, strategy0, strategy1, score0, score1, player):
    if player == 0:
        if strategy0(score0, score1) == -1:
            return not dice_swapped, score0 + 1
        else:
            return dice_swapped, score0
    else:
        if strategy1(score1, score0) == -1:
            return not dice_swapped, score1
        else:
            return False, score1

def swine_swap(score0, score1):
    if score0 == 2* score1 or score1 == 2* score0:
        score0, score1 = score1, score0
    return score0, score1

def play(strategy0, strategy1, score0=0, score1=0, goal=GOAL_SCORE):
    """Simulate a game and return the final scores of both players, with
    Player 0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first
    strategy1:  The strategy function for Player 1, who plays second
    score0   :  The starting score for Player 0
    score1   :  The starting score for Player 1
    """
    player = 0  # Which player is about to take a turn, 0 (first) or 1 (second)
    dice_swapped = False  # Whether 4-sided dice have been swapped for 6-sided
    num_rolls = 0

    while max(score0, score1) < goal:
        if player == 0:
            num_rolls = strategy0(score0, score1)

            #implements porkchop by calling pork_chop function to apply porkchop conditions and to end turn
            if num_rolls == -1:
                dice_swapped, score0 = pork_chop(dice_swapped, strategy0, strategy1, score0, score1, player)
            else:
                score0 += take_turn(num_rolls,score1, select_dice(score0, score1, dice_swapped))


        else:
            num_rolls = strategy1(score1, score0)

            if num_rolls == -1:
                dice_swapped, score1 = pork_chop(dice_swapped,strategy0, strategy1, score0, score1, player)
            else:
                score1 += take_turn(num_rolls,score0, select_dice(score1, score0, dice_swapped))


        #implementation of swine_swap
        score0, score1 = swine_swap(score0, score1)

        #switches player
        player = other(player)

    return score0, score1


#######################
# Phase 2: Strategies #
#######################

def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
        return n
    return strategy


def check_strategy_roll(score, opponent_score, num_rolls):
    """Raises an error with a helpful message if NUM_ROLLS is an invalid
    strategy output. All strategy outputs must be integers from -1 to 10.

    >>> check_strategy_roll(10, 20, num_rolls=100)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(10, 20) returned 100 (invalid number of rolls)

    >>> check_strategy_roll(20, 10, num_rolls=0.1)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(20, 10) returned 0.1 (not an integer)

    >>> check_strategy_roll(0, 0, num_rolls=None)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(0, 0) returned None (not an integer)
    """
    msg = 'strategy({}, {}) returned {}'.format(
        score, opponent_score, num_rolls)
    assert type(num_rolls) == int, msg + ' (not an integer)'
    assert -1 <= num_rolls <= 10, msg + ' (invalid number of rolls)'


def check_strategy(strategy, goal=GOAL_SCORE):
    """Checks the strategy with all valid inputs and verifies that the
    strategy returns a valid input. Use `check_strategy_roll` to raise
    an error with a helpful message if the strategy returns an invalid
    output.

    >>> def fail_15_20(score, opponent_score):
    ...     if score != 15 or opponent_score != 20:
    ...         return 5
    ...
    >>> check_strategy(fail_15_20)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(15, 20) returned None (not an integer)
    >>> def fail_102_115(score, opponent_score):
    ...     if score == 102 and opponent_score == 115:
    ...         return 100
    ...     return 5
    ...
    >>> check_strategy(fail_102_115)
    >>> fail_102_115 == check_strategy(fail_102_115, 120)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(102, 115) returned 100 (invalid number of rolls)
    """
    # BEGIN PROBLEM 6
    for i in range(goal + 1):
        for j in range(goal + 1):
            check_strategy_roll(i, j, strategy(i, j))
    # END PROBLEM 6


# Experiments

def make_averaged(fn, num_samples=1000):
    """Return a function that returns the average_value of FN when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(3, 1, 5, 6)
    >>> averaged_dice = make_averaged(dice, 1000)
    >>> averaged_dice()
    3.75
    """
    def averager(*args):
        total = 0
        counter = 1
        while counter <= num_samples:
            total += fn(*args)
            counter += 1
        return total / num_samples

    return averager



def max_scoring_num_rolls(dice=six_sided, num_samples=1000):
    """Return the number of dice (1 to 10) that gives the highest average turn
    score by calling roll_dice with the provided DICE over NUM_SAMPLES times.
    Assume that the dice always return positive outcomes.

    >>> dice = make_test_dice(3)
    >>> max_scoring_num_rolls(dice)
    10
    """

    num_roles = 1
    best_num_roles = 10
    average_score = 0

    current_num_rolls_score = lambda num_roles: make_averaged(roll_dice,num_samples)(num_roles,dice)


    while num_roles <= 10:
        if current_num_rolls_score (num_roles) >  average_score:
            average_score = current_num_rolls_score(num_roles)
            best_num_roles = num_roles
        elif current_num_rolls_score (num_roles) == average_score:
            best_num_roles = min(num_roles, best_num_roles)
        num_roles += 1

    return best_num_roles


def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1


def average_win_rate(strategy, baseline=always_roll(4)):
    """Return the average win rate of STRATEGY against BASELINE. Averages the
    winrate when starting the game as player 0 and as player 1.
    """
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)

    return (win_rate_as_player_0 + win_rate_as_player_1) / 2


def run_experiments():
    """Run a series of strategy experiments and report results."""
    if True:  # Change to False when done finding max_scoring_num_rolls
        six_sided_max = max_scoring_num_rolls(six_sided)
        print('Max scoring num rolls for six-sided dice:', six_sided_max)
        rerolled_max = max_scoring_num_rolls(reroll(six_sided))
        print('Max scoring num rolls for re-rolled dice:', rerolled_max)

    if False:  # Change to True to test always_roll(8)
        print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    if False:  # Change to True to test bacon_strategy
        print('bacon_strategy win rate:', average_win_rate(bacon_strategy))

    if False:  # Change to True to test swap_strategy
        print('swap_strategy win rate:', average_win_rate(swap_strategy))

    "*** You may add additional experiments as you wish ***"


# Strategies

def bacon_strategy(score, opponent_score, margin=8, num_rolls=4):
    """This strategy rolls 0 dice if that gives at least MARGIN points,
    and rolls NUM_ROLLS otherwise.
    """

    if hogtimus_prime(free_bacon(opponent_score)) >= margin:
        return 0
    else:
        return num_rolls

check_strategy(bacon_strategy)


def swap_strategy(score, opponent_score, margin=8, num_rolls=4):
    """This strategy rolls 0 dice when it triggers a beneficial swap. It also
    rolls 0 dice if it gives at least MARGIN points. Otherwise, it rolls
    NUM_ROLLS.
    """
    # BEGIN PROBLEM 10
    if hogtimus_prime(free_bacon(opponent_score)) == 2*opponent_score:
        return 0
    elif hogtimus_prime(free_bacon(opponent_score)) >= margin:
        return 0
    else:
        return num_rolls
    # END PROBLEM 10

check_strategy(swap_strategy)


def final_strategy(score, opponent_score):
    """Write a brief description of your final strategy.

    ALGORITHIM BRUH:

    this is all based around swap_strategy and giving it optimum variables

    TO DO:
        -think about pork chop as optimizing the dice rolled

    What it is doing already:
        -num_rolls is optimized using max_scoring_num_rolls function already written
        -HELLO


    *** YOUR DESCRIPTION HERE ***
    """
    # BEGIN PROBLEM 11




    """ This line is broken, so this I commented it out"""
    # swap_strategy(score, opponent_score, margin = 8, max_scoring_num_rolls(dice=six_sided, num_samples=1000))


    # END PROBLEM 11

# check_strategy(final_strategy)


##########################
# Command Line Interface #
##########################

# NOTE: Functions in this section do not need to be changed. They use features
# of Python not yet covered in the course.

@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions.

    This function uses Python syntax/techniques not yet covered in this course.
    """
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')

    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()
