# import pickle  # noqa: S403
# from dataclasses import dataclass
# from difflib import get_close_matches
# from pathlib import Path

# from loguru import logger

# import pandas as pd


# @dataclass
# class PredictValue:
#     v: str
#     conf: float


# @dataclass
# class Predict:
#     def __post_init__(self) -> None:
#         data = Path("data")

#         # with open(data / "combined_model.pkl", "rb") as f:
#         #     self.combined_model = pickle.load(f)  # noqa: S301

#         # self.df_processed = pd.read_csv(data / "df_processed.csv")
#         # self._names: list[str] = list(self.df_processed["Title"].unique())

#     def recommend_with_find(self, target_name: str, count: int = 10) -> list[PredictValue]:
#         name = self.find_name(target_name)
#         return self.recommend(target_name=name, count=count)

#     def recommend(self, target_name: str, count: int = 10) -> list[PredictValue]:
#         idx = self.df_processed[self.df_processed["Title"] == target_name].index[0]
#         score_series = pd.Series(self.combined_model[idx]).sort_values(ascending=False)

#         top = count + 1
#         top_indexes = list(score_series.iloc[1:top].index)

#         list_ = []
#         for i in top_indexes:
#             list_.append(PredictValue(v=self.df_processed["Title"].iloc[i], conf=score_series[i]))

#         logger.debug(
#             "recommendation done: target_name: {}, count: {}\nresult: {}",
#             target_name,
#             count,
#             list_,
#         )
#         return list_

#     def find_names(self, name: str, count: int) -> list[str]:
#         names = get_close_matches(name, self._names, n=count * 3)
#         names = (  # noqa: ECE001
#             self.df_processed[self.df_processed["Title"].isin(names)]
#             .sort_values(by="Score", ascending=False)["Title"]
#             .values.tolist()
#         )

#         concrete = self.df_processed[self.df_processed["Title"] == name]
#         if len(concrete) != 0:
#             found_name = concrete.iloc[0]["Title"]
#             names.remove(found_name)
#             names.insert(0, found_name)

#         return names[:count]

#     def find_name(self, name: str) -> str:
#         found_names = self.find_names(name, count=1)
#         if len(found_names) == 0:
#             raise KeyError(f"Name not found: {name}")
#         return found_names[0]

#     def best_from(self, count: int, field: str, name: str) -> list[str]:
#         best = list(  # noqa: ECE001
#             self.df_processed[self.df_processed[field] == name].sort_values(by="Score", ascending=False).Title[:count]
#         )

#         logger.debug("found best from: field: {}, name: {}, best: {}", field, name, best)
#         return best
