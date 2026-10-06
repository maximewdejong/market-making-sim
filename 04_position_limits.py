import random
random.seed(1)

#------------ PARAMETERS--------
N_TICKS = 200
VOL = 2 #market volatility per tick
HALF_SPREAD = 1.0
TRADE_SIZE = 1
CLIENT_PROB = 0.6 #chance a client shows up each tick
CLIENT_BIAS = 0.5 #willingenss for clients to buy (one-sided flow)
POS_LIMIT = 10 #cannot exceed a certain amount of positions

#------------ STATE (my books)--------
fair = 100.0
position = 0
cash = 0.0
n_trades = 0
n_refused = 0 #trades I had to turn down
max_abs_pos = 0 #biggest position I reached

for t in range(N_TICKS):
    fair += random.gauss(0,VOL)
    bid = fair - HALF_SPREAD
    ask = fair + HALF_SPREAD

    if random.random() < CLIENT_PROB:
        client_value = fair  + CLIENT_BIAS + random.gauss(0,1.5)

        if client_value > ask: #my offer is attractive to him => I SELL, client buys => go short
            if position - TRADE_SIZE >= -POS_LIMIT: #would i stay within limit ?
                position -= TRADE_SIZE
                cash += ask*TRADE_SIZE
                n_trades += 1

            else:
                n_refused += 1

        elif client_value < bid: #my bid is more atrractive => I BUY , client sells
            if position + TRADE_SIZE <= POS_LIMIT: #limit check
                position += TRADE_SIZE
                cash -= bid*TRADE_SIZE
                n_trades += 1

            else:
                n_refused += 1

    max_abs_pos = max(max_abs_pos, abs(position))

    if t%20 == 0:
        pnl = cash + position * fair
        print(f"trade n°{t:3d} | fair= {fair:7.2f} | position= {position:4d} | P&L={pnl:7.2f}")

pnl = cash + position*fair
spread_income = n_trades * HALF_SPREAD * TRADE_SIZE #i.e. profit from spreads
market_pnl = pnl - spread_income #profit from random movement of the market => can be lucky / unlucky

print()
print(f"Trades: {n_trades}   Refused: {n_refused}   Final position: {position}   Max |position|: {max_abs_pos}")
print(f"Spread income: {spread_income:7.2f}")
print(f"Market P&L:    {market_pnl:7.2f}")
print(f"TOTAL P&L:     {pnl:7.2f}")

