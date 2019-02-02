import requests

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.dispatch_components import \
    AbstractRequestHandler, \
    AbstractExceptionHandler, \
    AbstractRequestInterceptor
from ask_sdk_core.utils import \
    is_request_type, \
		is_intent_name

"""
thanks to https://github.com/dawoudt/JustWatchAPI
"""

# Skill Builder object
sb = SkillBuilder()
api = "https://api.justwatch.com/titles/en_US/popular"
head = {'User-Agent': 'StreamIt Amazon Alexa Skill'}

"""
code to get providers:
requests.Session().get("https://apis.justwatch.com/content/providers/locale/en_US").json()
we only want ones with 'flatrate' in monetization_types[]
map 'id' to 'clear_name'
"""
providers = {
  "2": "Apple iTunes",
  "3": "Google Play Movies",
  "7": "Vudu",
  "8": "Netflix",
  "9": "Amazon Prime Video",
  "10": "Amazon Video",
  "11": "Mubi",
  "12": "Crackle",
  "14": "realeyz",
  "15": "Hulu",
  "18": "PlayStation",
  "25": "Fandor",
  "27": "HBO Now",
  "31": "HBO Go",
  "34": "Epix",
  "37": "Showtime",
  "43": "Starz",
  "60": "Fandango",
  "68": "Microsoft Store",
  "73": "Tubi TV",
  "78": "CBS",
  "79": "NBC",
  "80": "AMC",
  "83": "The CW",
  "87": "Acorn TV",
  "92": "Yahoo View",
  "99": "Shudder",
  "100": "GuideDoc",
  "105": "FandangoNOW",
  "123": "FXNow",
  "139": "Max Go",
  "143": "Sundance Now",
  "148": "ABC",
  "151": "BritBox",
  "155": "History",
  "156": "A&E",
  "157": "Lifetime",
  "162": "AMC Theatres",
  "175": "Netflix Kids",
  "177": "Pantaflix",
  "185": "Screambox",
  "188": "YouTube Premium",
  "190": "Curiosity Stream",
  "191": "Kanopy",
  "192": "YouTube",
  "206": "CW Seed",
  "207": "The Roku Channel",
  "209": "PBS",
  "211": "Freeform",
  "212": "Hoopla",
  "215": "Syfy",
  "226": "DC Universe"
}


# Request Handler classes
class LaunchRequestHandler(AbstractRequestHandler):
		"""Handler for launch."""
		def can_handle(self, handler_input):
				# type: (HandlerInput) -> bool
				return is_request_type("LaunchRequest")(handler_input)

		def handle(self, handler_input):
				# type: (HandlerInput) -> Response
				speech = "Welcome. What film are you searching for?"
				handler_input.response_builder.speak(speech).ask(speech)
				return handler_input.response_builder.response


class StreamIntentHandler(AbstractRequestHandler):
    """Handler for stream asker."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("StreamIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        err = "I'm sorry, I couldn't find that one."

        try:
            req = handler_input.request_envelope.request
            film = req.intent.slots["film"].value
        except (AttributeError, ValueError, KeyError, IndexError):
            film = None

        if film:
            # search for the query
            r = requests.Session()
            query = {"query": film, "page_size": 1}
            res = r.post(api, json=query, headers=head)

            if res.status_code == 200:
                try:
                    lst = [providers[str(x['provider_id'])]
                           for x in res.json()['items'][0]['offers']
                           if (x['monetization_type'] == 'flatrate') and (x['presentation_type'] == 'hd')]
                except Exception:
                    lst = None

                if lst:
                    l = len(lst)
                    if l == 0:
                        lst = err
                    elif l == 1:
                        lst = lst[0]
                    else:
                        lst = ", ".join(lst[:-1]) + ", and " + lst[-1]
                    speech = "You can stream {} on ".format(film) + lst
                else:
                    speech = "It looks like {} isn't available to stream anywhere.".format(film)
            else:
                speech = err
        else:
            speech = err

        handler_input.response_builder.speak(speech) \
            .set_should_end_session(True)
        return handler_input.response_builder.response


# Exception Handler classes
class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Catch All Exception handler."""
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        print(exception)
        speech = "Sorry, there was some problem. Please try again!!"
        handler_input.response_builder.speak(speech).ask(speech)

        return handler_input.response_builder.response

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(StreamIntentHandler())

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
