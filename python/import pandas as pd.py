import pandas as pd
from urllib.request import urlopen
from io import BytesIO

# Put this script in the same folder as pokemon.csv.
input_file = "pokemon.csv"
output_file = "pokemon_with_base_hp.csv"

# Official PokéAPI dataset: stat_id 1 is HP.
stats_url = (
    "https://raw.githubusercontent.com/PokeAPI/pokeapi/master/"
    "data/v2/csv/pokemon_stats.csv"
)

pokemon = pd.read_csv(input_file)

with urlopen(stats_url, timeout=30) as response:
    stats = pd.read_csv(BytesIO(response.read()))

hp = stats.loc[stats["stat_id"] == 1, ["pokemon_id", "base_stat"]]
hp = hp.rename(columns={"pokemon_id": "id", "base_stat": "base_hp"})

# Match each row by its Pokémon/form ID.
result = pokemon.merge(hp, on="id", how="left", validate="one_to_one")

# Place base_hp immediately after the Pokémon name column.
cols = result.columns.tolist()
cols.remove("base_hp")
name_col = "identifier" if "identifier" in cols else "pokemon_name"
cols.insert(cols.index(name_col) + 1, "base_hp")
result = result[cols]

result.to_csv(output_file, index=False)

missing = result["base_hp"].isna().sum()
print(f"Saved {output_file} with {len(result)} rows.")
print(f"Rows without an HP stat: {missing}")
