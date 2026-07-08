# Entropy Trading Strategy

A Python implementation of the entropy-assisted pattern identification framework proposed in the paper **"Entropy-Assisted Quality Pattern Identification in Finance"** (Gupta et al., 2025). This project reproduces the core trading strategy described in the paper, integrates it with historical market data and the Alpaca API, and evaluates its behavior through historical backtesting.

> **Status:** Archived (Completed Learning Project)

---

## Overview

This project began as an attempt to better understand how quantitative trading strategies are developed from academic research.

Rather than inventing a trading strategy from scratch, I selected a recently published entropy-assisted framework and implemented the trading pipeline myself. Along the way, I built supporting infrastructure for data ingestion, portfolio management, backtesting, broker integration, logging, and performance evaluation.

Although this project is no longer under active development, it served as my first substantial software engineering project and introduced me to modular application design, reproducible experimentation, and algorithmic trading systems.

---

## Paper

This implementation is based on:

> Gupta, R., Gupta, S., Singh, J., & Kais, S.
> **Entropy-Assisted Quality Pattern Identification in Finance**
> arXiv:2503.06251 (2025)

The paper proposes using entropy as an information-theoretic measure to identify high-quality trading patterns by balancing information gain and historical profitability. Rather than relying solely on clustering methods like K-Means or Gaussian Mixture Models, the approach removes ambiguous patterns and retains those with both low entropy and historically consistent outcomes.  [oai_citation:1‡2503.06251v1.pdf](sediment://file_00000000b468720c9e0626cb2fa8c2e7)

---

## Features

- Historical market data ingestion
- Entropy-based signal generation
- Portfolio simulation and tracking
- Historical backtesting
- Alpaca API integration
- Trade logging
- Modular strategy implementation

---

## Motivation

Academic trading strategies are often described at a high level but rarely accompanied by complete implementations.

My goal was to understand both the research and the engineering required to translate a published quantitative strategy into executable software.

This project explores questions like:

- How do you transform an academic algorithm into production-style Python code?
- How should trading logic be separated from brokerage infrastructure?
- How can historical performance be evaluated reproducibly?

---

## Architecture

```
Historical Market Data
          │
          ▼
 Entropy Strategy
          │
          ▼
 Portfolio Manager
          │
          ▼
 Broker Interface
     (Alpaca API)
          │
          ▼
 Performance Logging
          │
          ▼
 Backtest Results
```

Repository structure:

```
entropy-trading-strategy/
│
├── src/
│   ├── trading_strategy.py
│   ├── portfolio_manager.py
│   ├── alpaca_client.py
│   ├── logger.py
│   ├── config.py
│   └── ...
│
├── data/
├── logs/
├── notebooks/
├── requirements.txt
└── README.md
```

---

## Technologies

| Category | Technologies |
|----------|--------------|
| Language | Python |
| APIs | Alpaca Trading API |
| Data Analysis | pandas, NumPy |
| Visualization | Matplotlib |
| Development | Jupyter Notebook, Git |

---

## Installation

Clone the repository

```bash
git clone https://github.com/eykzhang/entropy-trading-strategy.git
cd entropy-trading-strategy
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run

```bash
python src/main.py
```

---

## Engineering Challenges

Some of the engineering challenges explored during this project included:

- Translating an academic algorithm into modular Python software
- Separating trading strategy logic from brokerage interactions
- Managing portfolio state throughout historical backtests
- Organizing reusable components to support strategy experimentation
- Building a reproducible experimentation workflow

---

## Lessons Learned

This project was my introduction to building larger Python applications.

More importantly, it taught me that implementing an idea from a paper is often much harder than understanding the paper itself. Many engineering decisions—configuration management, portfolio bookkeeping, logging, API interactions, and software organization—are left to the implementer.

Those lessons directly influenced the architecture of my later projects.

---

## Looking Back

If I were rebuilding this project today, I would make several significant improvements.

- Separate research notebooks from the production codebase.
- Replace the current configuration system with typed configuration objects.
- Introduce automated testing.
- Improve package organization and dependency boundaries.
- Implement a strategy interface supporting multiple interchangeable algorithms.
- Expand evaluation beyond historical returns to include risk-adjusted metrics (Sharpe ratio, maximum drawdown, transaction costs, and walk-forward validation).
- Build a richer visualization and reporting pipeline instead of relying primarily on notebooks.

While I wouldn't consider this repository production-ready today, I'm proud of it because it marked the transition from writing isolated scripts to thinking about software architecture.

---

## Future Work

Potential extensions include:

- Additional benchmark strategies
- Strategy comparison framework
- Transaction cost modeling
- Walk-forward validation
- Live paper trading
- Web dashboard for performance visualization

---

## References

Gupta, R., Gupta, S., Singh, J., & Kais, S.
**Entropy-Assisted Quality Pattern Identification in Finance.**
arXiv:2503.06251, 2025.  [oai_citation:2‡2503.06251v1.pdf](sediment://file_00000000b468720c9e0626cb2fa8c2e7)

---

## License

This project is licensed under the MIT License.
