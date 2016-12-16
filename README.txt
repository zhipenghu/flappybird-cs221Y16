#######################
###Files we modified###
#######################

# flappy.py — none
# visualization.py — none 
# assets folder — none

# initialize_qvalues.py — wrote it all, this is the “warm up” we are discussing in the paper. We dump the qvalues into a json file, look at line 35.

# qvalues.json and folders Qvalue1, Qvalue2 — multiple tests for the initialize_qvalues.py test with json printouts from line 35 of the python file.


# bot.py 
1 - variable additions/modifications: modified and/or added the initialization, learning rate, Flappy’s bounds, weights, and epsilon greedy (lines 18-29)
2 - epsilon greedy instantiation: added (tested static) a dynamic epsilon greedy approach on lines 56-58, 73-79
3 - reduced the state space with the upper/lower bound thresholds to generate a deterministic jump/no jump state-action pair (lines 62-67)
4 - generated warmup feature rewards and weights (lines 109-131)
5 - q-value extractor for feature extraction (add-on feature test which performed poorly after we viewed results), lines 159-169 setup, lines 171-183 extractor

# visualization.py  - generates figure 3 in our paper, wrote all of it 


#######################
### Running the Game###
#######################
Run <python flappy.py> . You’ll need Python 2.7.x and PyGame 1.9.x. 