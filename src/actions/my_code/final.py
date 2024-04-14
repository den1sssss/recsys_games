import pickle  # noqa: S403
from dataclasses import dataclass
from difflib import get_close_matches
from pathlib import Path
from enum import Enum

from loguru import logger

import pandas as pd


@dataclass
class PredictValue:
    """Класс для хранения предсказанных значений и их уверенности."""
    v: str  # Предсказанное значение
    conf: float  # Уверенность в предсказании

class Models(Enum):
    COMBINED = "cos_sim.pkl"
    COS_SIM = "cos_sim.pkl"
    COSINE_SIM = "cosine_sim.pkl"

@dataclass
class Predict:
    """Главный класс рекомендательной системы."""
    def __post_init__(self) -> None:
        """Метод инициализации объекта Predict."""
        self.data = Path("data")  # Путь к папке с данными

        # Загрузка комбинированной модели из файла
        with open(self.data / Models.COS_SIM.value, "rb") as f:
            self.model = pickle.load(f)

        # Загрузка обработанных данных из файла CSV
        self.df_processed = pd.read_csv(self.data / "df_processed.csv")

        # Список уникальных названий элементов
        self._names: list[str] = list(self.df_processed["Title"].unique())

    def change_model(self, model: Models):
        with open(self.data / model.value, "rb") as f:
            self.model = pickle.load(f)

    def recommend_with_find(self, target_name: str, count: int = 10) -> list[PredictValue]:
        """Метод для рекомендации с использованием поиска."""
        name = self.find_name(target_name)  # Нахождение наиболее подходящего имени
        return self.recommend(target_name=name, count=count)

    def recommend(self, target_name: str, count: int = 10) -> list[PredictValue]:
        """Метод для рекомендации."""
        idx = self.df_processed[self.df_processed["Title"] == target_name].index[0]  # Индекс целевого элемента
        score_series = pd.Series(self.model[idx]).sort_values(ascending=False)  # Серия оценок

        top = count + 1  # Количество рекомендаций плюс один для исключения самого элемента
        top_indexes = list(score_series.iloc[1:top].index)  # Индексы топ-N рекомендаций

        recommendations = []  # Список для хранения предсказанных значений
        for i in top_indexes:
            recommendations.append(PredictValue(v=self.df_processed["Title"].iloc[i], conf=score_series[i]))

        logger.debug(
            "recommendation done: target_name: {}, count: {}\nresult: {}",
            target_name,
            count,
            recommendations,
        )
        return recommendations

    def find_names(self, name: str, count: int) -> list[str]:
        """Метод для поиска похожих названий."""
        # Поиск похожих названий
        names = get_close_matches(name, self._names, n=count * 3)
        # Фильтрация похожих названий из обработанных данных и сортировка по оценке
        names = (
            self.df_processed[self.df_processed["Title"].isin(names)]
            .sort_values(by="Score", ascending=False)["Title"]
            .values.tolist()
        )

        # Помещение конкретного названия в начало списка, если оно было найдено
        concrete = self.df_processed[self.df_processed["Title"] == name]
        if len(concrete) != 0:
            found_name = concrete.iloc[0]["Title"]
            names.remove(found_name)
            names.insert(0, found_name)

        return names[:count]

    def find_name(self, name: str) -> str:
        """Метод для нахождения наиболее подходящего имени."""
        found_names = self.find_names(name, count=1)
        if len(found_names) == 0:
            raise KeyError(f"Name not found: {name}")
        return found_names[0]
    
    def best_from(self, count: int, field: str, name: str) -> list[str]:
        """Метод для нахождения лучших элементов из определенного поля."""
        # Выборка лучших элементов из определенного поля
        best = list(
            self.df_processed[self.df_processed[field] == name]
            .sort_values(by="Score", ascending=False).Title[:count]
        )

        # Логирование выполненного поиска лучших элементов
        logger.debug("found best from: field: {}, name: {}, best: {}", field, name, best)
        return best