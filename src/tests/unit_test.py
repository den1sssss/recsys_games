import pytest
from actions.predict import Predict


@pytest.fixture(scope="class")
def predict() -> Predict:
    return Predict()


class TestPredict:
    def test_find_name_ok(self, predict: Predict):
        assert "Call of Duty: Modern Warfare" == predict.find_name("Call of Duty: Modern Warfare")

    def test_find_names_ok(self, predict: Predict):
        print(predict.find_names("Need for speed", count=5))

        assert {
            "Need for Speed",
            "Need for Speed Heat",
            "Need for Speed Most Wanted",
            "Need for Speed Unbound",
            "Need for Speed Payback",
        } == set(predict.find_names("Need for speed", count=5))

    def test_recomend_ok(self, predict: Predict):
        predict.recommend("Need for Speed", count=5)
        predict.recommend("Call of Duty: Modern Warfare", count=5)

    def test_recomend_with_find_ok(self, predict: Predict):
        # predict.recommend_with_find("Need for Speed", count=5)
        predict.recommend_with_find("starfield", count=5)

    def test_best_from_publisher_ok(self, predict: Predict):
        assert {"Dota 2", "Counter-Strike: Global Offensive"} == set(
            predict.best_from(count=2, field="Publisher", name="Valve")
        )

    def test_best_from_developer_ok(self, predict: Predict):
        assert {"Apex Legends", "Titanfall 2"} == set(
            predict.best_from(count=2, field="Developer", name="Respawn Entertainment")
        )
