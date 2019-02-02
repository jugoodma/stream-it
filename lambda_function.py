from botocore.vendored import requests
"""
thanks to https://github.com/dawoudt/JustWatchAPI
"""
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

def build_response_object(output_speech, reprompt, should_end_session):
  """
  available keys:
  outputSpeech, card, reprompt, shouldEndSession, directives

  we are only using:
  outputSpeech, reprompt, shouldEndSession
  """
  return {
    "outputSpeech": {
      "type": "SSML",
      "ssml": "<speak>" + output_speech + "</speak>"
    },
    "reprompt": {
      "type": "SSML",
      "ssml": "<speak>" + reprompt + "</speak>"
    } if reprompt else None,
    "shouldEndSession": should_end_session
  }

def where_stream(intent):
  """
  main api code
  """
  speech = "I'm sorry, I couldn't find that one."
  try:
    # get requested film
    film = intent['slots']['film']['value']
    # search for the query
    r = requests.Session()
    query = {"query": film, "page_size": 1}
    res = r.post(api, json=query, headers=head)
    lst = [providers[str(x['provider_id'])]
            for x in res.json()['items'][0]['offers']
            if (x['monetization_type'] == 'flatrate') and (x['presentation_type'] == 'hd')]
    if lst and len(lst) > 0:
      if len(lst) == 1:
        lst = lst[0]
      else:
        lst = ", ".join(lst[:-1]) + ", and " + lst[-1]
      speech = "You can stream {} on ".format(film) + lst
    else:
      speech = "It looks like {} isn't available to stream anywhere.".format(film)
  except (AttributeError, ValueError, KeyError, IndexError): pass
  return speech

def lambda_handler(event, context):
  """
  main lambda handler

  the idea is to make this lambda function _smaller_
  with less overhead caused by the ask core
  """
  # you'll need to handle applicationId in AWS Lambda console
  # but here's the sample code for it
  '''
  if (event['session']['application']['applicationId'] != 'YOUR ALEXA SKILL APP ID'):
    raise ValueError("Invalid Application ID")
  '''
  try:
    # handle intents
    if event['request']['type'] == 'LaunchRequest':
      speech = "Welcome! What film are you searching for?"
      reprompt = speech
      end = False
    elif event['request']['intent']['name'] == 'StreamIntent':
      speech = where_stream(event['request']['intent'])
      reprompt = ""
      end = True
    else:
      speech = "Sorry, there was some problem. Please try again!"
      reprompt = ""
      end = False
  except Exception as e:
    # some error happened
    speech = "Sorry, there was some problem."
    reprompt = ""
    end = True

  return {
    "version": "1.0",
    "response": build_response_object(speech, reprompt, end)
  }
