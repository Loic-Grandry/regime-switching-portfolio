"""Reconstruit data_etf_20years.csv (prix de cloture ajustes) a partir de proxies ETF publics.
Colonnes attendues par le notebook : date + price_{equity,bond,gold,tech,energy,staples,finance,health,utils}.
Usage : python fetch_data.py
"""
import yfinance as yf

TICKERS = {
    "price_equity":  "SPY",   # S&P 500 (marche / variable d'etat)
    "price_bond":    "TLT",   # obligations longues US
    "price_gold":    "GLD",   # or
    "price_tech":    "XLK",   # technologie
    "price_energy":  "XLE",   # energie
    "price_staples": "XLP",   # consommation de base
    "price_finance": "XLF",   # finance
    "price_health":  "XLV",   # sante
    "price_utils":   "XLU",   # utilities
}

def main(start="2005-01-01", end=None, out="data_etf_20years.csv"):
    px = yf.download(list(TICKERS.values()), start=start, end=end, auto_adjust=True)["Close"]
    px = px.rename(columns={v: k for k, v in TICKERS.items()})[list(TICKERS.keys())].dropna()
    px.index.name = "date"
    px.to_csv(out)
    print(f"ecrit {out} : {len(px)} lignes, {px.index.min().date()} -> {px.index.max().date()}")

if __name__ == "__main__":
    main()
