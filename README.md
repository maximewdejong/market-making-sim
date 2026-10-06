# Market-Making Simulator

A step-by-step Monte Carlo simulation of a single-asset market maker, built to study the trade-off between **spread income** and **inventory risk**, and how **position limits** and **quote skewing** manage that risk.

## The model

At each tick:

1. **The market moves.** Fair value follows a random walk: $P_{t+1} = P_t + \varepsilon_t$, with $\varepsilon_t \sim N(0, \sigma^2)$.
2. **The market maker quotes** a bid and an ask around fair value, shifted by a skew that depends on the current position:

$$\text{skew} = -k \cdot \text{position}, \qquad \text{bid} = P_t - h + \text{skew}, \qquad \text{ask} = P_t + h + \text{skew}$$

3. **A client may arrive** (probability $p$) with a private valuation $v \sim N(P_t + b, 1.5^2)$, where $b$ is a flow bias. The client buys at the ask if $v > \text{ask}$ and sells at the bid if $v < \text{bid}$, provided the trade keeps the position within $\pm L$.
4. **P&L is marked to market:** $\text{P\&L} = \text{cash} + \text{position} \times P_t$, and decomposed into

$$\text{P\&L} = \underbrace{\sum \text{edge per trade}}_{\text{spread income}} + \underbrace{\sum_t \text{position}_t \cdot \Delta P_t}_{\text{market (inventory) P\&L}}$$

## Files

| File | What it adds |
|---|---|
| `01_random_walk.py` | Fair value as a discretised random walk |
| `02_single_trade.py` | One quote, one client, one trade: cash, position and mark-to-market P&L |
| `03_client_flow.py` | Full loop with random client arrivals; splits P&L into spread income vs. market P&L |
| `04_position_limits.py` | Position limit and one-sided (biased) client flow |
| `05_inventory_skew.py` | Inventory-based quote skewing; per-trade edge accounting |
| `06_skew_monte_carlo.py` | Compares skew settings across 200 simulated markets |

Run any file with `python <file>.py`. Only the Python standard library is used.

## Results

200 markets of 200 ticks each, $\sigma = 0.5$, $h = 1$, $L = 10$, same seeds for every setting.

**One-sided flow** (bias $b = 0.5$):

| Skew $k$ | Avg P&L | Std | Worst | Avg / Std | Avg max \|position\| |
|---|---|---|---|---|---|
| 0.0 | 40.8 | 53.3 | −114.4 | 0.77 | 9.9 |
| 0.1 | 56.7 | 32.7 | −29.1 | 1.74 | 8.3 |
| 0.2 | 55.2 | 20.3 | 8.0 | 2.72 | 5.8 |
| 0.5 | 47.7 | 11.6 | 24.7 | 4.10 | 3.5 |

**Balanced flow** (bias $b = 0$):

| Skew $k$ | Avg P&L | Std | Worst | Avg / Std | Avg max \|position\| |
|---|---|---|---|---|---|
| 0.0 | 63.4 | 32.1 | −32.0 | 1.98 | 7.9 |
| 0.1 | 58.9 | 17.0 | 1.9 | 3.47 | 5.2 |
| 0.2 | 56.1 | 13.3 | 17.9 | 4.22 | 4.1 |
| 0.5 | 48.1 | 9.2 | 27.1 | 5.25 | 2.9 |

## Takeaways

- **Spread income is the skill component; inventory P&L is the risk component.** With the same trades, doubling volatility leaves spread income unchanged but scales inventory P&L proportionally.
- **Under one-sided flow, skew pays for itself.** It raises average P&L, removes refused trades at the position limit, and turns the worst case from −114 into a profit.
- **Under balanced flow, skew costs some average P&L** (inventory already mean-reverts on its own) but still halves risk. It acts as insurance.
- **There is a sweet spot.** Too little skew leaves inventory risk; too much gives away edge on every trade.

## Possible extensions

- Informed clients (adverse selection) whose trades predict the next price move
- Random trade sizes and volatility regimes
- Plots of P&L distributions and position paths
- Comparison with the Avellaneda–Stoikov optimal quoting model
