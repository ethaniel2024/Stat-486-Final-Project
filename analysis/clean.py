"""
clean.py — Broadway data cleaning pipeline
STAT 486 Final Project

Reads:  data/raw/Uncleaned_Broadway_Data.csv
Writes: data/processed/Broadway_Data_Clean.csv

Run from the repository root:
    python analysis/clean.py
"""

from pathlib import Path
import re
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = ROOT / "data" / "processed" / "Broadway_Data.csv"
OUT_PATH = ROOT / "data" / "processed" / "Broadway_Data_Clean.csv"

# ---------------------------------------------------------------------------
# 1. Load
# ---------------------------------------------------------------------------
df = pd.read_csv(RAW_PATH)
print(f"Loaded {len(df):,} rows, {df.shape[1]} columns")
print("Original columns:", df.columns.tolist())

# ---------------------------------------------------------------------------
# 2. Rename concatenated columns to their actual intended names
#    The scraper fused adjacent column headers together.
# ---------------------------------------------------------------------------
df = df.rename(columns={
    "This Week GrossPotential Gross": "This Week Gross",
    "Avg TicketTop Ticket":           "Avg Ticket",
    "Seats SoldSeats in Theatre":     "Seats Sold",
    "PerfsPreviews":                   "Perfs",
    "TonyNominatedMusical":            "Tony Nominated Musical",
    "Diff $":                          "Gross Change",
    "Diff % cap":                      "Cap Change Pct",
    "% Cap":                           "Pct Cap",
})

# ---------------------------------------------------------------------------
# 3. Parse "This Week Gross" — values look like "1229667.1" already numeric
#    but strip any stray $ or , just in case.
# ---------------------------------------------------------------------------
def strip_currency(s):
    return re.sub(r"[$,]", "", str(s))

df["This Week Gross"] = pd.to_numeric(
    df["This Week Gross"].astype(str).map(strip_currency), errors="coerce"
)
df["Gross Change"] = pd.to_numeric(
    df["Gross Change"].astype(str).map(strip_currency), errors="coerce"
)

# ---------------------------------------------------------------------------
# 4. Split "Avg Ticket" — values look like "$129.33$249.00" (avg + top
#    ticket concatenated) or just "$129.33". Extract the FIRST dollar amount.
# ---------------------------------------------------------------------------
def extract_first_dollar(s):
    """Return the first $NNN.NN value as a float, or NaN."""
    m = re.search(r"\$?([\d,]+\.\d+)", str(s))
    if m:
        return float(m.group(1).replace(",", ""))
    return np.nan

def extract_second_dollar(s):
    """Return the second $NNN.NN value (Top Ticket) as a float, or NaN."""
    matches = re.findall(r"\$?([\d,]+\.\d+)", str(s))
    if len(matches) >= 2:
        return float(matches[1].replace(",", ""))
    return np.nan

raw_ticket = df["Avg Ticket"].copy()   # save before overwriting
df["Avg Ticket"] = raw_ticket.map(extract_first_dollar)
df["Top Ticket"] = raw_ticket.map(extract_second_dollar)

# ---------------------------------------------------------------------------
# 5. Split "Seats Sold" — values like "9,5081,727" mean 9508 sold / 1727 cap.
#    Pattern: two comma-formatted numbers concatenated.
#    Strategy: strip commas then split on the boundary where a digit group
#    ends and another begins — specifically where we see >=4-digit + >=3-digit.
# ---------------------------------------------------------------------------
def split_seats(raw):
    """Return (seats_sold, seats_capacity) as ints or (NaN, NaN)."""
    s = re.sub(r",", "", str(raw))          # remove all commas → "95081727"
    # Try to split: first number is 4 digits, second is 3–4 digits
    m = re.match(r"^(\d{3,5})(\d{3,4})$", s)
    if m:
        return int(m.group(1)), int(m.group(2))
    # Fallback: single valid integer (no capacity available)
    if re.match(r"^\d+$", s):
        return int(s), np.nan
    return np.nan, np.nan

seats = df["Seats Sold"].apply(split_seats)
df["Seats Sold"]        = seats.apply(lambda x: x[0])
df["Seats In Theatre"]  = seats.apply(lambda x: x[1])

# ---------------------------------------------------------------------------
# 6. Split "Perfs" — values like "60" (perfs only) or "80" (may include
#    previews). The column is already a single integer in most cases.
# ---------------------------------------------------------------------------
df["Perfs"] = pd.to_numeric(df["Perfs"].astype(str), errors="coerce")

# ---------------------------------------------------------------------------
# 7. Parse remaining columns
# ---------------------------------------------------------------------------
df["Week Ending"]  = pd.to_datetime(df["Week Ending"], errors="coerce")
df["Pct Cap"]      = pd.to_numeric(df["Pct Cap"].astype(str), errors="coerce")
df["Cap Change Pct"] = pd.to_numeric(
    df["Cap Change Pct"].astype(str), errors="coerce"
)
df["Tony Nominated Musical"] = df["Tony Nominated Musical"].map(
    {"True": True, "False": False, True: True, False: False}
)

# ---------------------------------------------------------------------------
# 8. Drop rows missing Show, Theater, Week Ending, or This Week Gross
#    (the 24 missing Show/Theater rows are dropped here)
# ---------------------------------------------------------------------------
n_before = len(df)
df = df.dropna(subset=["Show", "Theater", "Week Ending", "This Week Gross"])
n_dropped = n_before - len(df)
print(f"Dropped {n_dropped} rows with missing Show/Theater/Date/Gross")

# ---------------------------------------------------------------------------
# 9. Dedup — keep first occurrence of any (Show, Week Ending) duplicate
# ---------------------------------------------------------------------------
n_before = len(df)
df = df.drop_duplicates(subset=["Show", "Week Ending"], keep="first")
print(f"Removed {n_before - len(df)} duplicate show-week rows")

# ---------------------------------------------------------------------------
# 10. Sort and reset index
# ---------------------------------------------------------------------------
df = df.sort_values(["Show", "Week Ending"]).reset_index(drop=True)

# ---------------------------------------------------------------------------
# 11. Quality-check summary
# ---------------------------------------------------------------------------
print("\n=== Quality Check Summary ===")
print(f"Rows:            {len(df):,}")
print(f"Shows:           {df['Show'].nunique():,}")
print(f"Reporting weeks: {df['Week Ending'].nunique():,}")
print(f"Date range:      {df['Week Ending'].min().date()} – {df['Week Ending'].max().date()}")
print("\nMissingness per column:")
print(df.isnull().sum().to_string())
print("\nNumeric summary:")
print(df[["This Week Gross", "Avg Ticket", "Seats Sold", "Seats In Theatre",
          "Pct Cap", "Perfs"]].describe().round(2).to_string())

# ---------------------------------------------------------------------------
# 12. Save
# ---------------------------------------------------------------------------
OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUT_PATH, index=False)
print(f"\nSaved cleaned data → {OUT_PATH}")

