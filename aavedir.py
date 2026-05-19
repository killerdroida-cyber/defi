import requests
from tabulate import tabulate

URL = "https://api.v3.aave.com/graphql"

CHAINS = {
    "Arbitrum": 42161,
    "Base": 8453,
    "Avalanche": 43114,
    "Polygon": 137,
    "BNB": 56,
    "Linea": 59144
}

all_markets = []

for chain_name, chain_id in CHAINS.items():

    print(f"Consultando {chain_name}...")

    query = f"""
    query {{
      markets(
        request: {{
          chainIds: [{chain_id}]
        }}
      ) {{

        reserves {{

          underlyingToken {{
            symbol
          }}

          supplyInfo {{
            apy {{
              value
            }}
          }}

          borrowInfo {{
            apy {{
              value
            }}
          }}

        }}
      }}
    }}
    """

    response = requests.post(
        URL,
        json={"query": query},
        headers={
            "User-Agent": "Mozilla/5.0"
        }
    )

    data = response.json()

    try:

        markets = data["data"]["markets"]

        for market in markets:

            for reserve in market["reserves"]:

                symbol = reserve[
                    "underlyingToken"
                ]["symbol"]

                supply_apy_raw = reserve[
                    "supplyInfo"
                ]["apy"]["value"]

                supply_apy = (
                    float(supply_apy_raw) * 100
                )

                borrow_info = reserve.get(
                    "borrowInfo"
                )

                borrow_apy = 0

                if borrow_info:

                    borrow_apy_raw = borrow_info[
                        "apy"
                    ]["value"]

                    borrow_apy = (
                        float(borrow_apy_raw) * 100
                    )

                all_markets.append({
                    "chain": chain_name,
                    "symbol": symbol,
                    "supply_apy": round(supply_apy, 2),
                    "borrow_apy": round(borrow_apy, 2)
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
print("=" * 80)
print("AAVE REAL-TIME RATES")
print("=" * 80)

print(
    tabulate(
        all_markets[:100],
        headers="keys",
        tablefmt="pretty"
    )
)

print("\nTotal markets:", len(all_markets))
