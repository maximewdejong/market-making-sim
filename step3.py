import random 
random.seed(1)

#------------ PARAMETERS--------
N_TICKS = 200
VOL = 0.5 #market volatility per tick
HALF_SPREAD = 1.0
TRADE_SIZE = 1
CLIENT_PROB = 0.6 #chance a client shows up each tick

#------------ STATE (my books)--------
fair = 100.0
position = 0
cash = 0.0
n_trades = 0

for t in range(N_TICKS):
    #1. market moves (step 1)
    fair += random.gauss(0, VOL)

    #2. my quote (no skew yet)
    bid = fair - HALF_SPREAD
    ask = fair + HALF_SPREAD

    #3. maybe a client arrives (step 2, now inside the loop)
    if random.random() < CLIENT_PROB:
        client_value = fair + random.gauss(0,1.5)
        




