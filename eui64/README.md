# EUI-64 Method

## Disclaimer

I am not an expert in python or in IPv6. The informations presented here are based on my knowledge about networking and python. Don't take these informations as bullet proof facts and inform yourself plenty about this topic. Ressources I used can be found at the bottom of this document.

Also please keep in mind that I will not cover much history about IPv6 or the eui-64 method.

## What Is EUI-64?

EUI-64 is a method to generate a valid 64 bit interface identifier for the respective host-system. EUI-64 has been the first version for creating interface identifiers. Today eui-64 is only used for link-local addresses (local-scope, not routeable) since this method has a big security flaw. This security flaw includes that you can calculate the mac-address of the connecting device from the IPv6s interface identifier, as we will see later. With this flaw you have been able to track the geo-location of devices in i.e. your enterprise WiFi-network. This is quite unpleasent since workers don't want to be tracked permantly. This is one security flaw with eui64 and there are many more.

## Create EUI-64-Address: The Simple Way

If you want a simple explanation on how an interface identifier is created with the eui-64 method here you go:

  1. Split the mac-address in half.
  2. Add `ff:fe` into the middle.
  3. Invert the seventh bit to either 1 (if seventh bit is 0) or 0 (if seventh bit is 1, see notes)
  4. Create the IPv6-Address.

## Create EUI-64-Address: Detailed

If the step above is too inaccurate to understand I will explain it here in more detail. 

### 1. Split The MAC-Address In Half

Let's assume we have the following 48 bits mac-address: `00:1A:3F:F1:4C:C6`. Since the mac-address is written in hexadecimal numbers each block owns 8 bits (1 hex-digit = 4 bits) or 1 byte. A mac-address possess 6 hex-blocks with two hex-digits which in summary are 48 bits. Now the first step is to divide these 48 bits into two 24 bits-blocks like this:

```txt
00:1A:3F | F1:4C:C6
==> 1. 00:1A:3F
==> 2. F1:4C.C6
```

### 2. Add 'FF:FE'

Now that we have the two 24 bits-blocks we need to insert `FF:FE` into the middle of the address. So the address will look like this:

```txt
00:1A:3F + FF:FE + F1:4C:6C ==> 00:1A:3F:FF:FE:F1:4C:6C
```

### 3. Invert The Seventh Bit

Now that we inserted `FF:FE` into the middle of our mac-address we need to invert the seventh bit on the beginning of the mac-address. **Remember**: each block of a mac-address has 8 bits. With that in mind we need the first two hex-digits of the mac-address which are `00`. For simple understanding we convert the hex-digits into binary:

```txt
1. First 0 to binary: 0000
2. Second 0 to binary: 0000
==> 0000 0000 ==> 00000000
```

Now we look at the seventh bit. If it's a `0` we need to set it to `1`. If the seventh bit is a `1` we need to set it to `0` (see notes). In our case everything is `0` so we can assume our seventh bit will also be `0`. In that case we need to invert it like this:

```txt
0000 0000
       ^ 
==> 0000 0010 ==> 00000010
```

Now we need to convert the binary digits into hex again to get our mac-address back:

```txt
0000 ==> 0
0010 ==> 2
==> 02
==> 02:1A:3F:FF:FE:F1:4C:6C
```

### 4. Create The IPv6-Address

Our last step is fairly simple: create an IPv6-address with the available blocks. We know that a IPv6-address is in total 128 bits (or 16 bytes). Since we need to create our interface identifier we only need to set the last 64 bits. An IPv6-address is divided into 8 16 bits blocks. In our case we only need to create half of the blocks. With that in mind we can put together our interface identifier like this:

```txt
02:1A:3F:FF:FE:F1:4C:6C ==> 021A:3FFF:FEF1:4C6C
```

Voilà you just created your eui-64-based interface identifier.

## Back To The Security-Flaw

Now let's get back to the security flaw I mentioned earlier in this document. If you payed attention you now can easily calculate the mac-address from the eui-64 interface identifier. You only need to reverse the steps we just did. Simple right? That's why a new standard had to be developed. This standard is now specified under 'IPv6 Privacy Extensions'. But even **with** privacy extensions enabled you might run into errors. If you want to know more just have a look in the readme-file for IPv6 privacy extensions.

## Notes

As mentioned in the text to create the eui-64 interface identifier you need to invert the seventh bit in the last step. Now there are some approaches I like to discuss. As mentioned in the rfc-4291 for the eui-64 method the numbers `1` and `0` have different meanings. For `1` it's said that this address is specified as global/universal-scope whereas `0` represents the local-scope of an address.

I know wikipedia isn't a reliable source to refer to for information, but in its entry for the eui-64 method nothing special is noted about the numbers `1` and `0` when flipping the seventh bit.

As for the german website 'elektronik-kompendium' it roughly mentions that the number `0` stays for a mac-address assigned by the IEEE. For the number `1` it is said that it's something like a non-real 'fantasy'-like address. But in the following sentence they tell that a made-up (fantasy) mac-address has a `0` as seventh bit. This is a contradiction in terms of their previous mentioning on the fantasy-like mac-address. Either they misspelled their sentences or they don't know the actual meaning for these numbers.

I personally think it's best to stick to the method of inverting the bit, whether it's from a `1` to a `0` or vice versa. But you should keep in mind what the rfc mentions about the eui-64 method.

## Sources

[https://tools.ietf.org/html/rfc4291](https://tools.ietf.org/html/rfc4291)

[https://de.wikipedia.org/wiki/EUI-64](https://de.wikipedia.org/wiki/EUI-64)

[https://www.elektronik-kompendium.de/sites/net/1902131.htm](https://www.elektronik-kompendium.de/sites/net/1902131.htm) ***german only***