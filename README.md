# stream-it
Alexa skill that tells you where you can stream movies/shows

[See it here!](https://www.amazon.com/jugoodma-Stream-It/dp/B07NC6H4CZ)

The skill uses `lambda_function.py` deployed on AWS Lambda to interface with the [JustWatch](https://www.justwatch.com) API (unofficial)

NOTE: I wrote this skill during the infancy of Alexa skill development.
As such, the `model.json` here is likely outdated with current development practices/idioms.
One such example, I wrote this skill before [name-free interactions](https://developer.amazon.com/en-US/docs/alexa/custom-skills/understand-name-free-interaction-for-custom-skills.html) were a thing.

NOTE: It looks like Alexa has the idea of this skill built-in now, rendering my skill useless.
I also thought that JustWatch had, since the publishing of my skill, made their own skill, but I can only find [this skill](https://www.amazon.com/VWAP-Just-Watch/dp/B088FJ7W1M) now.
Their GitHub repo is [here](https://github.com/vinaywadhwa/just-watch-voice) if you're interested.

NOTE: I did email the creators of JustWatch asking if I could use their API for this skill, and they told me yes :)

Hopefully anyone else that wants to interface with the JustWatch API can find this code useful!

Ideally this skill would be more than just English, but that's a problem for another day

```
python3 -i lambda_function.py
>>> where_stream({'slots':{'film':{'value':'interstellar'}}})
['FXNow', 'DIRECTV', 'Spectrum On Demand', 'Paramount+ Amazon Channel']
'You can stream interstellar on FXNow, DIRECTV, Spectrum On Demand, and Paramount+ Amazon Channel'
```
