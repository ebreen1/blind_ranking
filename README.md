# blind_ranking
A simulation of a blind ranking game with different strategies

Inspired by [this Jetpunk quiz](https://www.jetpunk.com/user-quizzes/234916/10-random-numbers-1-100-blind-ranking)


## The Game
You are given 10 random numbers from 1-100 consecutively without knowing what's next. You need to place each number in a rank from 1-10 and try to order them all correctly.

Your score is how many numbers you managed to place before getting one that doesn't fit in any remaining ranks.

If you place all 10 numbers, you win.

## Strategies
<ul>
  <li>"Tens" strategy: Place each number N based on the digits in the tens place of N-1 (so 1-10 go in rank 1, 11-20 go in rank 2, etc.). If that rank is taken, take the closest available one (go up if the number already there is less than the new number, down if it's greater) 
  <ul>
    <li> Win rate: 18.04% </li>
    <li> Average score: 5.828 </li>
  </ul>
  </li>
  <li>Probability strategy: When given a number, calculate the probability that it will fall into each rank, assuming that all previous numbers have been placed correctly. Choose the rank with the highest probability. 
  <ul>
    <li> Win rate: 21.32% </li>
    <li> Average score: 6.032 </li>
  </ul>
  </li>
</ul>

