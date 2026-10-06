import random 
random.seed(1)

#------------ PARAMETERS--------
N_TICKS = 200
VOL = 2 #market volatility per tick
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
        if client_value > ask: #I SELL
            position -= TRADE_SIZE
            cash += ask * TRADE_SIZE
            n_trades += 1

        elif client_value < bid: #bid is than client's respect. value => I BUY
            position += TRADE_SIZE
            cash -= bid*TRADE_SIZE
            n_trades += 1

    #4. report every 20 ticks 
    if t % 20 == 0 :
        pnl = cash + position * fair
        print(f"t={t:3d}  fair={fair:7.2f}  position={position:4d}  P&L={pnl:7.2f}")


#------------ FINAL SCORE --------
pnl = cash + position * fair
spread_income = n_trades * HALF_SPREAD * TRADE_SIZE #skill
market_pnl = pnl - spread_income #luck from holding a position
print()
print(f"Trades: {n_trades}   Final position: {position}")
print(f"Spread income: {spread_income:7.2f}")
print(f"Market P&L:    {market_pnl:7.2f}")
print(f"TOTAL P&L:     {pnl:7.2f}")




