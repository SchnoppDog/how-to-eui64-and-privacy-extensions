# Privacy-Extensions

## Disclaimer

I am not an expert in python or in IPv6. The informations presented here are based on my knowledge about networking and python. Don't take these informations as bullet proof facts and inform yourself plenty about this topic. Ressources I used can be found on the bottom of this document.

## What Are IPv6 Privacy Extensions?

IPv6 privacy exetensions extends the [rfc-4941](https://tools.ietf.org/html/rfc4941) for stateless address autoconfiguration (SLAAC). Its the descendant of eui-64. It's main object is to anonymize the interface identifier. Why thats only half of the story I will tell you later.

### Why Privacy Extensions?

If you read the readme for the eui-64 method before then you should know that you can derive the mac-address from the interface identifier without much effort. With this you can be tracked quite easily, websites could read from the mac-address its manufacturer or someone could copy the mac-address and do something nasty with it. These are things we really don't want to happen. For that we use privacy extensions to anonymize our interface identifier. Hence, it is harder to track you down or do something else.

### How Are Privacy Extensions Created?

Now we come to the most interesting part. I'd like to show you three different approaches on how to create an interface identifier using privacy extensions:

  1. The 'rfc'-way (RFC 3041)
  2. Method described by 'elektronik-kompendium'
  3. System boot time (not included in the python-script)

**Keep in mind that there are more approaches on how to create privacy extensions**. Now come to think of it why do different approaches exist? To be honest I don't know. In my oppinion the IETF rfc only 'suggests' how privacy extensions are created. In the end it's up to the manufacturer on how to implement it in their software.

### Privacy Extensions Method 1: Do It Like The IETF RFC Suggests

The IETFs rfc 3041 creates privacy extensions by putting a so called `history value` and the eui-64 based mac-address of the host together and hash it with the md5-hashalgorithm. Now you might be asking what this `history value` might be. This history value describes a value, which is present at boot time of the host. There are two values that can be used:

  1. A random generated value
  2. Whenever a new interface identifier is generated, a value generated by the computation is saved as the `history value` for the next iteration of the algorithm

Let's say we don't have a computated value so we generate our own random value. The steps on how to create privacy extensions are fairly simple:

  1. Generate a cryptographical strong random value:

```txt
d1ccbd1825293666aa4297922ee9ab2c205a6a676f007c97db269d6fb7b9a38d
```

  2. Append the eui-64 based mac-address at the end of the random value:

```txt
d1ccbd1825293666aa4297922ee9ab2c205a6a676f007c97db269d6fb7b9a38d00:1A:3F:FF:FE:F1:4C:C6
```

  3. Create a md5-hash in hexadecimal format with the new random value as input:

```txt
de4d64ef06f2869cd3197096c86b7625
```

  4. Take the leftmost 64 bits:

```txt
de4d64ef06f2869c
```

  5. Set bit 6 to `0`:

```txt
de
d ==> 1101
e ==> 1110
==> 1101 1110
          ^
==> 1101 1010
1101 ==> d
1010 ==> a

==> da4d64ef06f2869c
```

  6. Create an IPv6 interface identifier:

```txt
da4d:64ef:06f2:869c
```

  7. Take the rightmost 64 bits and save it as `history value`

```txt
d3197096c86b7625 ==> history value. Used for the next computation of an interface identifier instead of a random value.
```

That sums up how the rfc 3041 suggests to generate privacy extensions for IPv6-addresses.

### Privacy Extensions Method 2: Do It Like Elektronik-Kompendium Suggests

Other than the IETFs rfc for privacy extensions, the german website `elektronik-kompendium` doesn't use a history value or a random number to generate privacy extensions. Instead they use the current ntp-timestamp and the mac-address of the host and hash it with a the sha1-hashalgorithm thus creating a 64 bits long hash to use as privacy extensions. It would look something like this:

  1. Get the current ntp-timestamp: `05:19:57`
  2. Append the mac-address: `05:19:5700:1A:3F:F1:4C:C6`
  3. Hash it with sha1: `9987e92f9fa0c71ad6f3f22ee4be7afd7cea66b7`
  4. Take the leftmost 64 bits: `9987e92f9fa0c71a`
  5. Create the IPv6 interface identifier: `9987:e92f:9fa0:c71a`

### Privacy Extensions Method 3: Use The System Startup Time

Another approach a former teacher of mine suggested, uses the systems startup time accurate to the nanosecond. Together with the hosts mac-address and a hashalgorithm like sha1 or any other creating the IPv6 privacy extensions. To be honest it's quite impossible to turn on two or more systems at the exact same time. There will always be a short delay between each start even if they are timed really good. That's why it should be impossible to generate same hashes. This means that no address-collition would appear in the global address scope. However, this is only theoretical and won't be implemented in future.

### The Problem With Privacy Extension: Datasecurity

What if I told you that you could be tracked even with privacy extensions enabled? This would be confusing wouldn't it? While it's true that the main objective of privacy extensions is to anonymize your interface identifier, your IPv6 ISP-prefix isn't. That means you still can be tracked with your isp-prefix. It's not accurate because your interface identifier is anonymized, but it can be a range of a few kilometers. Some ISPs are already taking countermeasurements against it by exchanging the ISP-prefix for each private customer in a certain period of time.

### Why Using A Constant Interface Identifier When Privacy Extensions Exists?

With privacy extensions enabled your interface identifier is anonymized and changes in a certain period of time. This promotes the usage of privacy extennsions. But there are times when privacy extensions are a big problem. If you want to make a service public like a webserver or something else, chances are that you won't be happy with privacy extensions enbaled. Such public services do need a static public ip-address. With privacy extensions enabled your public ip-address would change quite often. That means you need to disable privacy extensions in order to make your service publicly available.  

## Sources

[https://tools.ietf.org/html/rfc4941](https://tools.ietf.org/html/rfc4941)

[https://tools.ietf.org/html/rfc2373](https://tools.ietf.org/html/rfc2373)

[https://tools.ietf.org/html/rfc3041#section-3.2](https://tools.ietf.org/html/rfc3041#section-3.2)

[https://www.elektronik-kompendium.de/sites/net/1601271.htm](https://www.elektronik-kompendium.de/sites/net/1601271.htm) ***german only***