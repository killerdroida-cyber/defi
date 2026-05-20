import requests
from tabulate import tabulate

# ==========================================
# KAMINO MAIN MARKET DIRECT
# ==========================================

MARKET = "7u3HeHxYDLhnCoErrtycNokbQYbWGzLs6JSDqGAv5PfF"

URL = f"https://api.kamino.finance/kamino-market/{MARKET}/reserves/metrics"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(
    URL,
    headers=headers
)

data = response.json()

all_markets = []

for reserve in data:

    try:

        symbol = reserve.get(
            "liquidityToken",
            "UNKNOWN"
        )

        supply_apy = float(
            reserve.get("supplyApy", 0)
        ) * 100

        borrow_apy = float(
            reserve.get("borrowApy", 0)
        ) * 100

        total_supply_usd = float(
            reserve.get("totalSupplyUsd", 0)
        )

        total_borrow_usd = float(
            reserve.get("totalBorrowUsd", 0)
        )

        utilization = 0

        if total_supply_usd > 0:

            utilization = (
                total_borrow_usd
                / total_supply_usd
            ) * 100

        all_markets.append({
            "symbol": symbol,
            "supply_apy": round(supply_apy, 2),
            "borrow_apy": round(borrow_apy, 2),
            "utilization": round(utilization, 2),
            "supply_usd": round(total_supply_usd, 2),
            "borrow_usd": round(total_borrow_usd, 2)
        })

    except Exception as e:
        print("Error:", e)

# Ordenar manualmente sin pandas
all_markets = sorted(
    all_markets,
    key=lambda x: x["supply_apy"],
    reverse=True
)

print("\n")
print("=" * 70)
print("KAMINO MAIN MARKET DIRECT")
print("=" * 70)

print(
    tabulate(
        all_markets,
        headers="keys",
        tablefmt="pretty"
    )
)

print("\nTotal markets:", len(all_markets))