Title: Google Code Jam 2014 - Qualification Round
Date: 2014-04-17
Category: Programming
Tags: python, google-code-jam, programming, puzzles
Slug: google-code-jam-2014-qualification
Author: Gerard Madorell
Summary: Explanation of how I solved the Google Code Jam 2014 Qualification Round challenges, using Python.


The 2014 qualification round of this fantastic competition was held last week. I didn't have much time to do it at the "oficial" time, so I decided to give it a shot during my free time this week.

Google code jam is a competition in which programmers world wide participate against the clock in order to solve hard problems. It consists of a set of rounds, the first of which is the qualification one.

The qualification round this year consisted of 4 different problems, with different difficulties. So, without further ado, let's solve them!

(Btw, if you can't wait, you can always visit the github repo: https://github.com/Skabed/programming-challenges/tree/master/google_code_jam/2014/qualification)

## Magic trick
We are watching a magician doing a trick. It basically consists of:

1. Magician arranges 16 different cards in a 4x4 grid.
2. He asks for someone to choose a card at will, telling at which row it's located.
3. The magician rearranges the cards in a new distribution.
4. He now asks the same person in which row the card is located, and proceeds to tell which card is it.

Our goal is basically to understand how the trick works, using an algorithm.

We're given as input both grid distributions (after and before the first row is said) and also the two rows in which the volunteer said the card is located.

We need to say which card is the chosen one if there's only one possibility, "Bad magician!" if there's more than one card possibility or "Volunteer cheated!" if no card is possible.

This exercise was actually quite easy. We can simply count how many cards were in both rows, and use that number to find the answer directly.

I solved it using Python (all the file parsing is excluded):

    #!python
    class MagicTrickSolver(JamSolver):
        def solve_instance(self, instance):
            # Strategy: count how many numbers can be in both the rows the player said.

            first_row = instance.first_cards[instance.first_row - 1]
            second_row = instance.second_cards[instance.second_row - 1]

            possible_cards = []
            for card in first_row:
                if card in second_row:
                    possible_cards.append(card)

            return self.craft_solution(possible_cards)

        def craft_solution(self, possible_cards):
            if len(possible_cards) == 1:
                return str(possible_cards[0])
            elif len(possible_cards) > 1:
                return "Bad magician!"
            else:
                return "Volunteer cheated!"

## Cookie Clicker Alpha
This problem was quite more interesting than the last one.

It's based on a very popular game (http://orteil.dashnet.org/cookieclicker/) in which you basically earn cookies via clicks, and you can then spend those cookies on various cookie generators such as farms or aunts. Beware! It's quite addictive :P.

In this simplified version. We only have farms and a static production of 2 cookies/second.

We're given a goal of *X* cookies, the cost of the farms *C* and the amount of cookies produced by the farms *F*. Our job is to optimize cookie production in order to find the minimum amount of time needed to get to the goal of *X* cookies.

The code for the solution comes below, with the strategy explained in the comments:

	#!python
    class SuperCookieSolver(JamSolver):
        def solve_instance(self, instance):
            production = 2
            cost = instance.farm_cost
            farm_production = instance.farm_production
            objective = instance.objective
            elapsed_time = 0

            while True:
                # Need to calculate how much time do we need if we buy the farm.
                # And also how much time do we need if we don't do anything.

                # If time_buying < time_without_buying,
                #   then buy a farm and iterate again.
                # Else
                #   simply return how much time we need until we get to the objective.

                time_next_farm = cost / production

                time_buying_farm = time_next_farm + elapsed_time + objective / (production + farm_production)

                time_without_buying = elapsed_time + objective / production

                if time_buying_farm < time_without_buying:
                    elapsed_time += time_next_farm
                    production += farm_production
                else:
                    elapsed_time += objective / production
                    return elapsed_time

## Minesweeper Master
This one was the hardest challenge of this round by far! At the time of this writing, google code jam statistics show that only 45% of the people were able to get it right on the small input, which is quite a small percentage.

I had quite a lot of trouble solving this one, and, even though my solution is not the most elegant one, I still managed to get it working, so everything is fine.

In this problem we are given as input the number of rows, columns and mines that form a minesweeper grid configuration. Our job is to place the mines in such a way that we can win using only one click (remember that if you click in a cell that doesn't have any mines nearby it expands, recursively). If winning with one click isn't possible, we should say that.

For example, for this input:

	10 10 82
Which indicates a 10x10 grid with 82 mines inside, a possible solution would be:

	**********
    **********
    **********
    ****....**
    ***.....**
    ***.c...**
    ***....***
    **********
    **********
    **********

With "\*" denoting mines, "." denoting empty cells and *c* being the cell in which we click in order to win in a single click.

The solution isn't included here simply because it's too long (about 200 lines of code).

The strategy I used was:

* Deal with the edge case in which all are mines except one. Simply click on any cell and you just win.
* If that fails, try to fill the board with mines by diagonals from bottom right to top left.
* If that fails, then try to fill the board with empty cells starting from the center moving to the exterior of the grid.
* If that also fails, then try to fill the board with empty spaces horizontally, and then vertically if that fails as well.
* As our last chance, I tryed to fill the board by diagonals using grids of empty cells, starting from bot right moving to top left.
* If that also fails, we assume that the instance is insolvable and thus we return "Impossible".

You can always check the solution in code at: https://github.com/Skabed/programming-challenges/blob/master/google_code_jam/2014/qualification/c_minesweeper_master/minesweeper_master.py


## Deceitful War
In this problem we are faced with an interesting situation. Two friends, Ken and Naomi play a game called War.

In this game, they're both given N identical-looking blocks, each of them of different weights. They know their own weights but not the wights of the opponent.

The game consists of Naomi choosing a block, Ken choosing another one and then the one with the heavier block wins a point. They repeat that until all blocks are used.

This was the basic version of War. In this one, Ken will always choose it's lightest block if he can't win Naomi's weight and the block with an immediate heavier weight if he can win.

On the second version of the game, called Deceitful War, Naomi knows all weights and can therefore trick Ken in order to win. She can't break the rules or she will be discovered though. For example, if she says that a block weights 0.5 and then Ken uses a block that weights 0.6 and loses, Naomi is discovered, which is something she needs to evade as well.

Our goal is to calculate how many points will Naomi earn in both versions of the game given the weights of the blocks of both players.

As always, I endorse my solution that has my solution explained in it:

    #!python
    class DeceitfulWarSolver(JamSolver):

        def solve_instance(self, instance):
            war_result = self.calculate_war_result(instance)
            deceitful_war_result = self.calculate_deceitful_war_result(instance)
            return "{0} {1}".format(deceitful_war_result, war_result)

        def calculate_war_result(self, instance):
            # Strategy:
            #   Choose heaviest naomi block and then:
            #       - Choose max ken block if he can beat that score.
            #       - Choose min ken block if he cannot beat the score.

            points = 0
            naomi = copy.copy(instance.naomi)
            ken = copy.copy(instance.ken)
            for i in range(instance.amount_blocks):
                chosen_naomi = max(naomi)

                can_ken_beat_that = chosen_naomi < max(ken)
                if can_ken_beat_that:
                    naomi.remove(chosen_naomi)
                    ken.remove(max(ken))
                else:
                    naomi.remove(chosen_naomi)
                    ken.remove(min(ken))
                    points += 1

            return points

        def calculate_deceitful_war_result(self, instance):
            # Strategy:
            #   Naomi always takes its lightest block.
            #   - If lightest naomi is lighter than lightest ken:
            #       Then Naomi tells that her block is just lighter than the heaviest Ken's block.
            #       Ken then will choose its heaviest block to counter the choice.
            #       Result: Ken wins, Ken heaviest block and Naomi lightest one get discarded.
            #   - Else If lightest naomi is heavier than lightest ken:
            #       Then Naomi tells that her block is heavier than the heaviest Ken's block.
            #       In consequence, Ken chooses its lightest block because he can't win.
            #       Result: Naomi wins, Ken and Naomi's lightest blocks get discarded.

            points = 0
            naomi = copy.copy(instance.naomi)
            ken = copy.copy(instance.ken)

            for i in range(instance.amount_blocks):
                min_naomi = min(naomi)
                min_ken = min(ken)

                if min_naomi > min_ken:
                    naomi.remove(min_naomi)
                    ken.remove(min_ken)
                    points += 1
                else:
                    ken.remove(max(ken))
                    naomi.remove(min_naomi)

            return points

## Conclusion
Overall, it was a lot of fun to do it and I look forward to the next rounds!





























