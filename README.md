# Regime-switching correlations for minimum-variance portfolios

This project studies whether letting the correlations between assets change with market conditions
improves a minimum-variance portfolio. It was the empirical part of my academic paper in
econometrics.

## The idea, in plain terms

When markets are calm, assets move fairly independently, so spreading money across them reduces risk.
During a crisis they tend to fall together, and diversification breaks down exactly when it is needed
most. A portfolio built on a single fixed correlation matrix cannot anticipate this.

The model used here estimates correlations that move over time, and it allows those correlations to
behave differently depending on the market state. A hidden state, calm or crisis, is inferred from
the S&P 500, and the correlation dynamics adapt to it. In the literature this belongs to the family
of Markov-switching Dynamic Conditional Correlation models.

The objective is a Global Minimum Variance portfolio, meaning the set of weights that minimises the
portfolio variance at each date.

## What is actually implemented

For the multivariate part I did not call a ready-made package. The likelihood function, the
recursive update of the correlation matrix, and the maximum-likelihood estimation are written from
scratch, both for the standard time-varying-correlation model and for the version whose parameters
switch with the market state. This was the point of the thesis, so it made sense to build the
estimator rather than treat it as a black box.

## How the analysis is organised

The notebook follows four steps.

1. Data checks. Standard tests confirm that the return series are stationary, show volatility
   clustering, and have fatter tails than a normal distribution. This is what justifies using a
   volatility model rather than a simple linear regression.
2. Market state. A two-state model estimated on the S&P 500 separates calm periods from crisis
   periods. Two statistical tests then confirm that volatility and correlations really do differ
   between the two states, which is the assumption the rest of the work relies on.
3. Individual volatilities. For each asset the best volatility specification is selected among
   several standard ones, allowing for asymmetry (bad news raising volatility more than good news)
   and for fat tails.
4. Backtest. The model is estimated on 2005 to 2014 and evaluated on data it has never seen, from
   2015 to 2026. At each date it produces a covariance matrix, the portfolio weights follow from it,
   and the result is compared against a rolling-window covariance and against an equally weighted
   portfolio.

## What the results say

Every variance-minimising portfolio beats the naive equally weighted allocation, which confirms the
basic value of the approach.

The regime-switching model does not win in every period. Over long calm stretches a simple rolling
covariance is more stable and slightly better, because the richer model adds estimation noise. During
genuine crises, the 2020 COVID crash and the 2022 energy shock, the regime-switching model reacts to
the break and delivers the lowest realised risk. Added complexity pays off only when the market
regime justifies it.

## Files

`ms_dcc_gmv_portfolio.ipynb` contains the full analysis, from the data checks to the backtest and the
crisis stress tests, with all the figures.
`fetch_data.py` rebuilds the price data from public exchange-traded funds so the notebook can be run
end to end.
`requirements.txt` lists the packages.

## How to run

```bash
pip install -r requirements.txt
python fetch_data.py
jupyter notebook ms_dcc_gmv_portfolio.ipynb
```

The notebook keeps its outputs, so all the figures already show up when the file is opened on GitHub.

## Data

Nine asset classes are proxied by public exchange-traded funds (broad equities, long-term Treasury
bonds, gold, and six sector funds covering technology, energy, consumer staples, financials,
healthcare, and utilities). No proprietary data is used.

## Tools

Python, with statsmodels and arch for the time-series models, scipy for the optimisation, and pandas
and numpy for the data handling.
