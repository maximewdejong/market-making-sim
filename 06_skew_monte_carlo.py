"""What's new in step 6
Here we'd like to answer the question, which skew is best ?
We find by testing each different setitng on 200 different markets instead of one

What's new: 
1- a function: the whole step 5 simulation goes inside a function so you can call it again and again with different setting
2- two nested loops: for each skew value, run 200 markets
3- statistics: for each skew, compute the average P&L, the risk, the worst case, and the ratio average/risk"""


import random
import statistics

# ---------- PARAMETERS ----------
N_TICKS     = 200
VOL         = 0.5
HALF_SPREAD = 1.0
TRADE_SIZE  = 1
CLIENT_PROB = 0.6
CLIENT_BIAS = 0.5
POS_LIMIT   = 10
N_SIMS      = 200 #new!!!

def run(skew_per_unit,seed):
    """run ONE market with a given skew. Return final P&L and max position"""
    random.seed(seed)
    fair = 100.0
    position = 0
    cash = 0.0
    max_abs_pos = 0

    for t in range(N_TICKS):
        fair += random.gauss(0,VOL)
        skew = -skew_per_unit*position
        bid = fair - HALF_SPREAD + skew
        ask = fair + HALF_SPREAD + skew

        if random.random() < CLIENT_PROB:
            client_value = fair + CLIENT_BIAS + random.gauss(0,1.5)
            if client_value < bid and position + TRADE_SIZE <= POS_LIMIT: #i buy, i go long
                position += TRADE_SIZE
                cash -= bid*TRADE_SIZE

            elif client_value > ask and position - TRADE_SIZE >= -POS_LIMIT:
                position -= TRADE_SIZE
                cash += ask * TRADE_SIZE

        max_abs_pos = max(max_abs_pos, abs(position))
    pnl = cash + position * fair 
    return pnl, max_abs_pos


#---------------COMPARE SKEW SETTINGS------------
print(f"{'skew':>6} {'avg P&L':>9} {'std':>7} {'worst':>8} {'avg/std':>8} {'avg max|pos|':>13}")
for k in [0, 0.05, 0.1,0.15, 0.2, 0.25, 0.3, 0.5]: #skews
    pnls = []
    max_positions = []
    for seed in range(N_SIMS): #different seeds, same 200 markets for every k
        pnl, max_pos = run(k, seed)
        pnls.append(pnl)
        max_positions.append(max_pos)

    avg = statistics.mean(pnls)
    std = statistics.stdev(pnls)
    worst = min(pnls)
    print(f"{k:>6} {avg:>9.1f} {std:>7.1f} {worst:>8.1f} {avg/std:>8.2f} {statistics.mean(max_positions):>13.1f}")

