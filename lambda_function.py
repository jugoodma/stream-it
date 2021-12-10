# from botocore.vendored import requests
import requests
import json
"""
thanks to https://github.com/dawoudt/JustWatchAPI
https://github.com/lufinkey/node-justwatch-api/blob/master/index.js
"""
api = "https://api.justwatch.com/content/titles/en_US/popular" # used to not requre '/content' -- in future versions, may require 'apis' instead of 'api'
head = {'User-Agent': 'StreamIt Amazon Alexa Skill'}

def get_providers(sesh):
  # ideally we'd cache this data, but that's a problem for some other day
  try:
    # get it dynamically
    data = sesh.get("https://apis.justwatch.com/content/providers/locale/en_US").json()
    out = {}
    for ele in data:
      if "flatrate" in ele["monetization_types"]:
        out[ele["id"]] = ele["clear_name"]
    return out
  except Exception as e:
    print(e)
    return {
  8: "Netflix",
  9: "Amazon Prime Video",
  11: "Mubi",
  12: "Crackle",
  14: "realeyz",
  15: "Hulu",
  25: "Fandor",
  27: "HBO Now",
  34: "Epix",
  37: "Showtime",
  43: "Starz",
  79: "NBC",
  80: "AMC",
  87: "Acorn TV",
  99: "Shudder",
  100: "GuideDoc",
  123: "FXNow",
  139: "Max Go",
  143: "Sundance Now",
  148: "ABC",
  151: "BritBox",
  155: "History",
  156: "A&E",
  157: "Lifetime",
  175: "Netflix Kids",
  185: "Screambox",
  188: "YouTube Premium",
  190: "Curiosity Stream",
  191: "Kanopy",
  192: "YouTube",
  194: "Starz Play Amazon Channel",
  196: "AcornTV Amazon Channel",
  197: "BritBox Amazon Channel",
  199: "Fandor Amazon Channel",
  200: "HBO Now Amazon Channel",
  201: "Mubi Amazon Channel",
  202: "Screambox Amazon Channel",
  203: "Showtime Amazon Channel",
  204: "Shudder Amazon Channel",
  205: "Sundance Now Amazon Channel",
  209: "PBS",
  211: "Freeform",
  212: "Hoopla",
  215: "Syfy",
  218: "Eros Now",
  243: "Comedy Central",
  247: "Pantaya",
  248: "Boomerang",
  251: "Urban Movie Channel",
  255: "Yupp TV",
  257: "fuboTV",
  258: "Criterion Channel",
  259: "Magnolia Selects",
  260: "WWE Network",
  261: "Nickhits Amazon Channel",
  262: "Noggin Amazon Channel",
  263: "DreamWorksTV Amazon Channel",
  264: "MyOutdoorTV",
  267: "Hopster TV",
  268: "History Vault",
  269: "Funimation Now",
  276: "Smithsonian Channel",
  278: "Pure Flix",
  281: "Hallmark Movies",
  284: "Lifetime Movie Club",
  288: "Boomerang Amazon Channel",
  289: "Cinemax Amazon Channel",
  290: "Hallmark Movies Now Amazon Channel",
  291: "MZ Choice Amazon Channel",
  292: "Pantaya Amazon Channel",
  293: "PBS Kids Amazon Channel",
  294: "PBS Masterpiece Amazon Channel",
  295: "Viewster Amazon Channel",
  299: "Sling TV",
  309: "Sun Nxt",
  317: "Cartoon Network",
  318: "Adult Swim",
  322: "USA Network",
  328: "Fox",
  331: "FlixFling",
  337: "Disney Plus",
  343: "Bet+ Amazon Channel",
  344: "Rakuten Viki",
  350: "Apple TV Plus",
  358: "DIRECTV",
  361: "TCM",
  363: "TNT",
  365: "Bravo TV",
  366: "Food Network",
  368: "IndieFlix",
  384: "HBO Max",
  387: "Peacock Premium",
  397: "BBC America",
  398: "AHCTV",
  399: "Animal Planet",
  400: "Cooking Channel",
  402: "Destination America",
  403: "Discovery",
  404: "Discovery Life",
  405: "DIY Network",
  406: "HGTV",
  408: "Investigation Discovery",
  410: "Motor Trend",
  411: "Science Channel",
  412: "TLC",
  413: "Travel Channel",
  418: "Paramount Network",
  419: "TV Land",
  420: "Logo TV",
  422: "VH1",
  427: "Mhz Choice",
  430: "HiDive",
  432: "Flix Premiere",
  433: "OVID",
  438: "Chai Flicks",
  444: "Dekkoo",
  445: "Classix",
  446: "Retrocrush",
  453: "MTV",
  454: "Topic",
  455: "Night Flight Plus",
  464: "Kocowa",
  470: "The Film Detective",
  473: "Revry",
  475: "DOCSVILLE",
  485: "Rooster Teeth",
  486: "Spectrum On Demand",
  487: "OXYGEN",
  503: "Hi-YAH",
  504: "VRV",
  506: "TBS",
  507: "tru TV",
  508: "DisneyNOW",
  509: "WeTV",
  514: "AsianCrush",
  520: "Discovery Plus",
  528: "AMC Plus",
  529: "ARROW",
  531: "Paramount Plus",
  546: "WOW Presents Plus",
  551: "Magellan TV",
  554: "BroadwayHD",
  555: "The Oprah Winfrey Network",
  567: "True Story",
  568: "Martha Stewart TV",
  569: "DocAlliance Films",
  571: "British Path\u00e9 TV",
  579: "Film Movement Plus",
  581: "iQIYI",
  582: "Paramount+ Amazon Channel",
  583: "EPIX Amazon Channel",
  584: "Discovery+ Amazon Channel",
  585: "Metrograph",
  617: "Curia",
  632: "Showtime Roku Premium Channel",
  633: "Paramount+ Roku Premium Channel",
  634: "Starz Roku Premium Channel",
  635: "AMC+ Roku Premium Channel",
  636: "Epix Roku Premium Channel"
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
    providers = get_providers(r)
    query = {"query": film, "page_size": 1}
    res = r.post(api, json=query, headers=head)
    lst = [providers[x['provider_id']]
            for x in res.json()['items'][0]['offers']
            if (x['monetization_type'] == 'flatrate') and (x['presentation_type'] == 'hd')]
    print(lst)
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
