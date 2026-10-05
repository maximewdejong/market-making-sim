#step 2: one quote, one client, one trade
#this teaches the bookkeeping: how a trade changes your position and cash, and how you compute P&L

import random
random.seed(5)

#------------ 1 THE MARKET ----------
fair = 100.0 #fair value right now
half_spread = 1.0

#------------ 2 MY QUOTE ----------
#we quote symmetrically around fair value
bid = fair - half_spread # bid < ask
ask = fair + half_spread
print(f"My quote : {bid} / {ask}")

#------------ 3 MY BOOKS ----------
#we initialise my position and cash
position = 0 #+1 = long 1 unit; -1 = short 1 unit
cash = 0.0 #money in (selling) minus money out (buying)

#------------ 4 A CLIENT ARRIVES ----------
client_value = fair + random.gauss(0,1.5) #what the client thinks it's worth
print(f"Client values it at {client_value:.2f}")

if client_value > ask: #client think it is worth more than i do => my ask looks cheap to them => they BUY from me 
    position -=1 #i sold => i'm short
    cash += ask #i receive the ask price
    print(f"Client BUYS from me at {ask}")

elif client_value < bid: #my bid looks generous to them => they SELL to me
    position += 1 #i bought => i'm long
    cash -= bid #I pay the bid price
    print(f"Client SELLS to me at {bid}")

else:
    print("No trade")

#------------ 5 MARKETS MOVES, THEN MARK TO MARKET ----------
fair += random.gauss(0, 0.5)
pnl = cash + position * fair
print(f"New fair {fair:.2f} | position {position} | cash {cash:.2f} | P&L {pnl:.2f}")





