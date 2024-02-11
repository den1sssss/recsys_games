from typing import Any, Text

from actions.predict import Predict
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

predict = Predict()


class ActionClosestTo(Action):
    def name(self) -> Text:
        return "action_get_closest_to"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict[Text, Any]) -> list[dict[Text, Any]]:
        target_name = str(tracker.get_slot("target_name"))
        count = 5

        try:
            count = int(count)
        except ValueError:
            dispatcher.utter_message("Неправильный формат:(")

        found_name = "Call of Duty"
        try:
            found_name = predict.find_name(target_name)
        except Exception:
            dispatcher.utter_message("Такую игру я не знаю")
            return []

        predictions = list(predict.recommend(found_name, count=count))

        message = f"Я знаю игру {found_name}, вам обязательно понравятся такие игры как:\n\n"
        for prediction in predictions:
            message += f"{prediction.v}\n"
        dispatcher.utter_message(message)

        return []


class ActionBestFromPublisher(Action):
    def name(self) -> Text:
        return "action_get_best_from_publisher"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict[Text, Any]) -> list[dict[Text, Any]]:
        target_name = str(tracker.get_slot("target_name"))
        field_name = "Publisher"
        count = 5

        predictions = "\n".join(predict.best_from(count=count, field=field_name, name=target_name))
        dispatcher.utter_message(f"Самые лучшие игры по данным параметрам: \n\n{predictions}")

        return []


class ActionBestFromDeveloper(Action):
    def name(self) -> Text:
        return "action_get_best_from_developer"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict[Text, Any]) -> list[dict[Text, Any]]:
        target_name = str(tracker.get_slot("target_name"))
        field_name = "Developer"
        count = 5

        predictions = "\n".join(predict.best_from(count=count, field=field_name, name=target_name))
        dispatcher.utter_message(f"Самые лучшие игры по данным параметрам: \n\n{predictions}")

        return []
