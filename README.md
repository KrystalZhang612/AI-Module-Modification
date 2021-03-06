# AI-Module-Modification
An AI modification in Python. <br/>
The first is in relation to the exponential heuristic when moving up. <br/>
which implicitly assumes that the best possible path exists on the most direct route, as assumption which does not hold up to scrutiny.<br/>
This can overestimate when delta_h/distance > 1. Consider the following minimal counterexample:<br/> 
delta_h = 3 and distance = 1. This assumes a path cost of 2^3 times 1=8, however the optimal route is taking the roundabout way with a <br/> 
step size of one for three steps. The cost of this route is 2^1 times 3=6.<br/>
For the div heuristic, two key insights are that walking at lower heights costs so much less than walking at high heights and that,<br/>
under the right circumstances, ramping up to high heights can cost very little. Consider the following counterexample:<br/> 
Goal is at height 10, current node 10, and distance between them 100. Your heuristic assumes the cost to be 100 times 10/11,<br/> 
but instead if we got to walk down to height 1, continue down that way for 95 steps, and then move to 2, then 4, then 8, then 10.<br/> 
The total cost there is 1/11+95 times 1/2+1+4/3+8/5+10/9 ~ 52. <br/> 
Finally, the bidirectional is implemented. 
