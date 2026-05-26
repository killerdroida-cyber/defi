import requests
import csv
from tabulate import tabulate

# ==========================================
# KAMINO MULTI MARKET SCANNER
# TERMUX VERSION
# ==========================================

MARKETS = {
    "MAIN": "7u3HeHxYDLhnCoErrtycNokbQYbWGzLs6JSDqGAv5PfF",
    "PRIME": "CqAoLuqWtavaVE8deBjMKe8ZfSt9ghR6Vb8nfsyabyHA",
    "MAPLE": "6WEGfej9B9wjxRs6t4BYpb9iCXd8CpTpJ8fVSNzHCC5y",
    "ONRE": "47tfyEG9SsdEnUm9cw5kY9BXngQGqu3LBoop9j5uTAv8",
    "JLP": "DxXdAyU3kCjnyggvHmY5nAwg5cRbbmdyX3npfDMjjMek",
    "SOLSTICE": "9Y7uwXgQ68mGqRtZfuFaP4hc4fxeJ7cE9zTtqTxVhfGU",
    "JITO": "H6rHXmXoCQvq8Ue81MqNh7ow5ysPa1dSozwW3PU1dDH6",
    "HUMA": "52FSGeeokLpgvgAMdqxyt5Hoc2TbUYj5b8yxrEdZ37Vf"
}

headers = {
    "User-Agent": "Mozilla/5.0"
}

all_data = []

for market_name, market_id in MARKETS.items():

    url = (
        f"https://api.kamino.finance/"
        f"kamino-market/{market_id}/reserves/metrics"
    )

    try:

        response = requests.get(
            url,
            headers=headers,
            timeout=20
        )

        data = response.json()

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

                available_liquidity = (
                    total_supply_usd
                    - total_borrow_usd
                )

                spread = (
                    supply_apy
                    - borrow_apy
                )

                all_data.append({

                    "market": market_name,

                    "symbol": symbol,

                    "supply_apy": round(
                        supply_apy, 2
                    ),

                    "borrow_apy": round(
                        borrow_apy, 2
                    ),

                    "spread": round(
                        spread, 2
                    ),

                    "utilization": round(
                        utilization, 2
                    ),

                    "supply_usd": round(
                        total_supply_usd, 2
                    ),

                    "borrow_usd": round(
                        total_borrow_usd, 2
                    ),

                    "available_usd": round(
                        available_liquidity, 2
                    )

                })

            except Exception as e:

                print(
                    f"Error reserve "
                    f"{market_name}: {e}"
                )

    except Exception as e:

        print(
            f"Error market "
            f"{market_name}: {e}"
        )

# ==========================================
# SORT
# ==========================================

all_data = sorted(
    all_data,
    key=lambda x: x["supply_apy"],
    reverse=True
)

# ==========================================
# PRINT TABLE
# ==========================================

print("\n")
print("=" * 140)
print("KAMINO ALL MARKETS")
print("=" * 140)

print(
    tabulate(
        all_data,
        headers="keys",
        tablefmt="pretty"
    )
)

print("\nTotal markets:", len(all_data))

# ==========================================
# EXPORT CSV
# ==========================================

csv_file = "kamino_all_markets.csv"

keys = all_data[0].keys()

with open(
    csv_file,
    "w",
    newline="",
    encoding="utf-8"
) as output_file:

    dict_writer = csv.DictWriter(
        output_file,
        fieldnames=keys
    )

    dict_writer.writeheader()

    dict_writer.writerows(all_data)

print(f"\nCSV exportado: {csv_file}")