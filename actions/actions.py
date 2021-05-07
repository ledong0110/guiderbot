# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []


from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from MainBackend import FindPath
from pyvi import ViUtils


class ActionFindPath(Action):

	def name(self) -> Text:
		return "action_find_path"

	def run(self, dispatcher: CollectingDispatcher,
			tracker: Tracker,
			domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		start = str(tracker.get_slot("departure"))
		start = start.upper()
		SlotSet("departure", "none")
		end = str(tracker.get_slot("location"))
		end = end.upper()
		dispatcher.utter_message(text=start)
		dispatcher.utter_message(text=end)
		if start == "NONE":
			location = end.replace(" ", "+")
			dispatcher.utter_message(text="Đây là kết quả mình tìm được trên google map\nhttps://www.google.com/maps/dir/?api=1&destination={}".format(location))	
			return []
		if start == "NONE" & end == "NONE":
			dispatcher.utter_message(text="Không tìm thấy địa điểm bạn nhập")
			return []
		dispatcher.utter_message(text="Đợi minh tí nha...")
		start = str(ViUtils.remove_accents(start)).replace("b'","").replace("'", '')
		end = str(ViUtils.remove_accents(end)).replace("b'","").replace("'", '')
		u = FindPath(start, end)

		if u == -1:
			dispatcher.utter_message(text="Không tìm thấy địa điểm bạn nhập")
			return [SlotSet("departure", "none")]
		dispatcher.utter_message(text="Đây là bản đồ đường đến của bạn")
		dispatcher.utter_message(attachment="https://d038e9f6b7e7.ngrok.io/ToDrawMap/Path.jpg")
		dispatcher.utter_message(text="Đây là kết quả mình tìm được trên google map\nhttps://www.google.com/maps/dir/?api=1&destination={}".format(end.replace(" ", "+")))

		return [SlotSet("departure", "none"), SlotSet("location", "none")]
