from random import randint
from math import comb

# Returns a list of 10 distinct random numbers from 1-100
def generate_list():
    nums = []

    while(len(nums) < 10):
        n = randint(1, 100)
        if(n not in nums):
            nums.append(n)

    return nums



class Strategy:
    # This function assumes that there is a valid position to place to number
    # The code simulating the game will determine when there is no valid position and end the game, not calling this function
    def choose_rank(self, num, ranking):
        # Default strategy: choose the digit in tens place of n-1
        rank = (num-1) // 10

        # If that spot is already taken, go above or below it depending on if the new number is greater or less than the number already there
        while(ranking[rank] != 0):
            if(num > ranking[rank]):
                rank += 1
            else:
                rank -= 1

        return rank


class Prob_Strategy(Strategy):

    def probability(self, num, rank, ranking):
        lower_index = -1
        upper_index = 10

        lower_value = 0
        upper_value = 101

        for i in range(10):
            if(ranking[i] != 0):
                    if(ranking[i] < num):
                        lower_index = i
                        lower_value = ranking[i]
                    else:
                        upper_index = i
                        upper_value = ranking[i]
                        break

        # If number can't go into rank specified because it's bigger than a later number or smaller than an earlier number, probability is 0
        if(rank <= lower_index or rank >= upper_index):
            return -1

        # Less than num: choose (rank - lower_index - 1) numbers between lower_value+1 and num-1 (num - lower_value - 1 choices)
        # More than num: choose (upper_index - rank - 1) numbers between num+1 and upper_value-1 (upper_value - num - 1 choices)

        # Total number of choices: (upper_index - lower_index - 2) numbers between lower_value+1 and upper_value-1, excluding num (upper_value - lower_value - 2)

        #print(f"{rank=}, {num=}, {lower_value=}, {upper_value=}, {lower_index=}, {upper_index=}")
        return comb(num - lower_value - 1, rank - lower_index - 1) * comb(upper_value - num - 1, upper_index - rank - 1) / comb(upper_value - lower_value - 2, upper_index - lower_index - 2)


    def choose_rank(self, num, ranking):
        max_prob = 0
        best_rank = 0

        # For each rank, calculate the probability that the number will be in that rank and return the rank with the highest probability
        for i in range(10):
            prob = self.probability(num, i, ranking)
            if(prob > max_prob):
                max_prob = prob
                best_rank = i

        return best_rank


# Takes in the current ranking and the next number, and returns true if the game is lost (no valid place for the number)
# Returns false if the game is not lost
def has_lost(num, ranking):
    if(ranking[0] != 0 and num < ranking[0]):
        # Number is less than the number already in rank 0
        return True

    if(ranking[9] != 0 and num > ranking[9]):
        # Number is greater than the number already in rank 9
        return True

    for i in range(9):
        # Number is in between two numbers in adjacent ranks
        if(ranking[i] != 0 and ranking[i+1] != 0 and num > ranking[i] and num < ranking[i+1]):
            return True
    
    return False

def print_ranking(ranking):
    for i in range(10):
        print(f"{i+1}: {ranking[i] if ranking[i] != 0 else '-'}")

def run_game(strat, debug=False):
    # Runs the blind ranking game using the given strategy
    # Returns the score achieved (how many numbers were placed in the ranking before losing)
    # A score of 10 is a "win" (placed all numbers)

    nums = generate_list()

    ranking = [0] * 10

    for i in range(10):
        current_num = nums[i]
        if(debug):
            print(f"{current_num=}")
            print_ranking(ranking)

        if(has_lost(current_num, ranking)):
            if(debug):
                print("No space for number: Game Over!")
            return i

        rank = strat.choose_rank(current_num, ranking)

        if(debug):
            print(f"Choice: {rank}")

        if(rank < 0 or rank > 9 or ranking[rank] != 0):
            print("Error: invalid choice")
            return i

        ranking[rank] = current_num

    return 10

tens_strat = Strategy()
prob_strat = Prob_Strategy()


# Runs the game n times using the given strategy and returns a tuple containing the portion of games won and teh average score
def test_strategy(strat, n):
    wins = 0
    total_score = 0

    for i in range(n):
        score = run_game(strat)
        if(score == 10):
            wins += 1
        total_score += score

    return (wins / n, total_score / n)

num_games = 100000
tens_win_rate, tens_avg_score = test_strategy(tens_strat, num_games)
prob_win_rate, prob_avg_score = test_strategy(prob_strat, num_games)


print(f"Win rate of '10s place' strategy in {num_games} games: {tens_win_rate}")
print(f"Average score of '10s place' strategy in {num_games} games: {tens_avg_score}")
print(f"Win rate of probability strategy in {num_games} games: {prob_win_rate}")
print(f"Average score of probability strategy in {num_games} games: {prob_avg_score}")
