"""
live_nav_fetch.py
Day 1 - Tasks 2 & 3: Fetch live NAV history from the mfapi.in API
for the 6 selected schemes and save each as a raw CSV in data/raw/.
"""

import time
import requests
import pandas as pd

SCHEMES = {
    "HDFC_Top_100": 125497,
    "SBI_Bluechip": 119551,
    "ICICI_Bluechip": 120503,
    "Nippon_Large_Cap": 118632,
    "Axis_Bluechip": 119092,
    "Kotak_Bluechip": 120841,
}

RAW_DIR = "data/raw"


def fetch_one(name, code):
    url = f"https://api.mfapi.in/mf/{code}"
    print(f"Fetching {name} (code {code}) ...")

    response = requests.get(url, timeout=30)
    response.raise_for_status()
    payload = response.json()

    df = pd.DataFrame(payload["data"])
    df["date"] = pd.to_datetime(df["date"], format="%d-%m-%Y")
    df["nav"] = pd.to_numeric(df["nav"])
    df["amfi_code"] = payload["meta"]["scheme_code"]
    df["scheme_name"] = payload["meta"]["scheme_name"]

    df = df.sort_values("date").reset_index(drop=True)
    return df, payload["meta"]["scheme_name"]


def main():
    for name, code in SCHEMES.items():
        try:
            df, api_name = fetch_one(name, code)
            out_path = f"{RAW_DIR}/nav_{name}_{code}.csv"
            df.to_csv(out_path, index=False)
            print(f"  saved {len(df):>5} rows  ->  {out_path}")
            print(f"  API reports this code as: {api_name}\n")
        except Exception as e:
            print(f"  FAILED for {name} ({code}): {e}\n")
        time.sleep(1)

    print("Done. Check data/raw for the NAV CSV files.")


if __name__ == "__main__":
    main()
