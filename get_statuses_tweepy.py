import pandas as pd

df = pd.read_csv("df_json.csv", sep=";", encoding="utf-8")

df = df[["id", "extended_entities"]]

df["extended_entities"] = df["extended_entities"].fillna("{}")

print(df.extended_entities.to_dict("records"))

df2 = pd.json_normalize(df["extended_entities"])

print(df2)