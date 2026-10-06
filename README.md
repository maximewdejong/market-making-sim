# market-making-sim

A small market-making simulation I wrote to understand how a market maker earns the spread and what happens to the position along the way. I built it up one step at a time, so each file adds one thing to the previous one.

## Setup

The fair price follows a random walk, $P_{t+1} = P_t + \varepsilon_t$ with $\varepsilon_t \sim N(0, \sigma^2)$. Every tick I quote a bid and an ask around it, half-spread $h$ on each side. Clients show up at random, each with their own valuation $v \sim N(P_t + b, 1.5^2)$, and buy if $v$ is above my ask or sell if it is below my bid. The bias $b$ lets me make the flow one-sided (more buyers than sellers).

P&L is marked to market, $\text{cash} + \text{position} \times P_t$. I split it into what I earned from the spread and what I made or lost from holding inventory while the price moved.

From step 5 the quotes are skewed by position, $\text{skew} = -k \cdot \text{position}$, so when I'm short both prices move up (more sellers come to me) and when I'm long they move down.

## Files

- `01_random_walk.py` – the price process
- `02_single_trade.py` – one quote, one client, and the bookkeeping (cash, position, P&L)
- `03_client_flow.py` – the full loop, with P&L split into spread and inventory
- `04_position_limits.py` – a position limit and biased client flow
- `05_inventory_skew.py` – skewing quotes based on inventory
- `06_skew_monte_carlo.py` – compares skew values over 200 simulated markets

Standard library only, run with `python <file>.py`.

## What I found

200 markets of 200 ticks, $\sigma = 0.5$, $h = 1$, limit of ±10, same seeds for each setting.

With one-sided flow ($b = 0.5$):

| k | avg P&L | std | worst | avg/std |
|---|---|---|---|---|
| 0 | 40.8 | 53.3 | -114.4 | 0.77 |
| 0.1 | 56.7 | 32.7 | -29.1 | 1.74 |
| 0.2 | 55.2 | 20.3 | 8.0 | 2.72 |
| 0.5 | 47.7 | 11.6 | 24.7 | 4.10 |

With balanced flow ($b = 0$):

| k | avg P&L | std | worst | avg/std |
|---|---|---|---|---|
| 0 | 63.4 | 32.1 | -32.0 | 1.98 |
| 0.1 | 58.9 | 17.0 | 1.9 | 3.47 |
| 0.2 | 56.1 | 13.3 | 17.9 | 4.22 |
| 0.5 | 48.1 | 9.2 | 27.1 | 5.25 |

A few things I didn't expect going in:

- Raising volatility doesn't change the spread income at all (same trades), but the inventory P&L scales with it. Holding a position is where the risk is.
- When flow is one-sided, skewing helps on every measure. Without it I sit at the limit turning clients away and the worst run loses 114.
- When flow is balanced, skewing lowers the average a bit, because the position mostly comes back to zero on its own. It still roughly halves the spread of outcomes, so it works more like insurance.
- Too much skew isn't free either: past a point you're quoting away from fair value and giving up edge on every trade.

## Ideas for later

- Informed clients whose trades predict the next move (adverse selection)
- Random trade sizes, changing volatility
- Plots of the P&L distributions
- Compare against the Avellaneda–Stoikov model
