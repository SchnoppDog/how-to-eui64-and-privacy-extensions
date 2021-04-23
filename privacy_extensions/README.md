# EUI-64 Method

## Disclaimer

I am not an expert in python or in IPv6. The informations presented here are based on my knowledge about networking and python. Don't take these informations as bullet proof facts and inform yourself plenty about this topic. Ressource I used can be found on the bottom of this document.

## What Are IPv6 Privacy Extentions?

IPv6 privacy exetentions extends the [rfc-4941](https://tools.ietf.org/html/rfc4941) for stateless address autoconfiguration (SLAAC). It's the descendant of eui-64. It's main object is to anonymize the interface identifier. Why that's only half of the story I will tell you later.

### Why Privacy Extentions?

If you read the readme for the eui-64 method before then you should know that you can derive the mac-address from the interface identifier without much effort. With this you can be tracked quite easily, websites could read from the mac-address its manufacturer or someone could copy the mac-address and do something nasty with it. These are things we really don't want to happen. For that we use privacy extentions to anonymize our interface identifier. Hence, it is harder to track you down or do something else.

### How Are Privacy Extentions Created?

Now we come to the most interesting part. I'd like to show you three different approaches on how to create an interface identifier using privacy extentions:

  1. The 'rfc'-way (RFC 3041)
  2. Method described by 'elektronik-kompendium'
  3. System boot time

## Sources

[https://tools.ietf.org/html/rfc4941](https://tools.ietf.org/html/rfc4941)

[https://tools.ietf.org/html/rfc2373](https://tools.ietf.org/html/rfc2373)

[https://tools.ietf.org/html/rfc3041#section-3.2](https://tools.ietf.org/html/rfc3041#section-3.2)

[https://www.elektronik-kompendium.de/sites/net/1601271.htm](https://www.elektronik-kompendium.de/sites/net/1601271.htm) ***german only***