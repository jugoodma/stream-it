from botocore.vendored import requests
"""
thanks to https://github.com/dawoudt/JustWatchAPI
https://github.com/lufinkey/node-justwatch-api/blob/master/index.js
"""
api = "https://api.justwatch.com/content/titles/en_US/popular" # used to not requre '/content' -- in future versions, may require 'apis' instead of 'api'
head = {'User-Agent': 'StreamIt Amazon Alexa Skill'}
"""
code to get providers:
requests.Session().get("https://apis.justwatch.com/content/providers/locale/en_US").json()
we only want ones with 'flatrate' in monetization_types[]
map 'id' to 'clear_name'
"""
providers = {
  "8": "Netflix",
  "9": "Amazon Prime Video",
  "11": "Mubi",
  "14": "realeyz",
  "15": "Hulu",
  "25": "Fandor",
  "27": "HBO Now",
  "31": "HBO Go",
  "34": "Epix",
  "37": "Showtime",
  "43": "Starz",
  "78": "CBS",
  "79": "NBC",
  "83": "The CW",
  "87": "Acorn TV",
  "99": "Shudder",
  "100": "GuideDoc",
  "139": "Max Go",
  "143": "Sundance Now",
  "151": "BritBox",
  "155": "History",
  "156": "A&E",
  "157": "Lifetime",
  "175": "Netflix Kids",
  "185": "Screambox",
  "188": "YouTube Premium",
  "190": "Curiosity Stream",
  "191": "Kanopy",
  "194": "Starz Play Amazon Channel",
  "196": "AcornTV Amazon Channel",
  "197": "BritBox Amazon Channel",
  "198": "CBS All Access Amazon Channel",
  "199": "Fandor Amazon Channel",
  "200": "HBO Now Amazon Channel",
  "201": "Mubi Amazon Channel",
  "202": "Screambox Amazon Channel",
  "203": "Showtime Amazon Channel",
  "204": "Shudder Amazon Channel",
  "205": "Sundance Now Amazon Channel",
  "209": "PBS",
  "212": "Hoopla",
  "218": "Eros Now",
  "226": "DC Universe",
  "243": "Comedy Central",
  "247": "Pantaya",
  "248": "Boomerang",
  "249": "UP Faith and Family",
  "251": "Urban Movie Channel",
  "254": "Dove Channel",
  "255": "Yupp TV",
  "257": "fuboTV",
  "258": "Criterion Channel",
  "259": "Magnolia Selects",
  "260": "WWE Network",
  "261": "Nickhits Amazon Channel",
  "262": "Noggin Amazon Channel",
  "264": "MyOutdoorTV",
  "265": "Tribeca Shortlist",
  "267": "Hopster TV",
  "268": "History Vault",
  "269": "Funimation Now",
  "276": "Smithsonian Channel",
  "278": "Pure Flix",
  "281": "Hallmark Movies",
  "282": "Sports Illustrated",
  "283": "Crunchyroll",
  "284": "Lifetime Movie Club",
  "288": "Boomerang Amazon Channel",
  "289": "Cinemax Amazon Channel",
  "290": "Hallmark Movies Now Amazon Channel",
  "291": "MZ Choice Amazon Channel",
  "292": "Pantaya Amazon Channel",
  "293": "PBS Kids Amazon Channel",
  "294": "PBS Masterpiece Amazon Channel",
  "295": "Viewster Amazon Channel",
  "299": "Sling TV",
  "300": "Pluto TV",
  "317": "Cartoon Network",
  "318": "Adult Swim",
  "322": "USA Network",
  "328": "Fox",
  "331": "FlixFling",
  "337": "Disney Plus",
  "343": "Bet+ Amazon Channel",
  "344": "Rakuten Viki",
  "350": "Apple TV Plus",
  "355": "Darkmatter TV",
  "358": "DIRECTV",
  "361": "TCM",
  "363": "TNT",
  "365": "Bravo TV"
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
