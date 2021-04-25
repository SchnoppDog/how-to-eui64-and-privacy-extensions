# EUI-64 Methode

## Disclaimer

Ich bin kein Experte, was Python-Programmierung oder die Themen rund um IPv6 angeht. Alle hier aufgeführten Informationen basieren auf mein Wissen über die Netzwerktechnik, als auch Python. Bitte nehmen Sie in Kenntnis, dass die aufgeführten Informationen keine Garantie für die absolute Richtigkeit der Methode übernehmen. Daher ist es ratsam sich auch andere Quellen anzuschauen, um sich mehr über das Thema zu informieren. Quellen, welche ich für meine Recherche benutzt habe, finden Sie am Ende des Dokuments.

## Was ist EUI-64?

EUI-64 ist eine Methode, um einen 64-Bit Interface Identifier für eine IPv6-Adresse eines Host-System zu erstellen. Das EUI-64-Verfahren war die erste Herangehensweise zur Erstellung eines Interface Identifiers. Heutzutage wird EUI-64, wenn überhaupt, ausschließlich für die Erstellung von Link-Local-Adressen benutzt, da diese eine große Sicherheitsschwachstelle besitzen. Diese Schwachstelle beschreibt, dass es möglich ist die MAC-Adresse eines Clients aus dem EUI-64 erstellten Interface Identifier herzuleiten. Wie das funktioniert werden Sie später erfahren. Mit dieser Schwachstelle war es möglich technische Geräte und somit auch Personen zu Orten und ihre Bewegmuster aufzuzeichnen. Verständlicherweise ist das unangenehm, da z.B. Mitarbeiter von Unternehmen nicht dauerhaft verfolgt werden möchten. Das ist jedoch nur eine Schwachstelle von vielen weiteren.

## Erstellung der EUI-64-Adresse: Die einfache Art

Im Nachfolgenden wird eine simple Erklärung für die Erstellung des EUI-64 Interface Identifiers aufgezeigt:

  1. Teile die MAC-Adresse in der Hälfte auf.
  2. Füge `ff:fe` in die Mitte ein.
  3. Setze das siebte Bit auf eine `1`, wenn es eine `0` ist. Setze es auf eine `0`, wenn es eine `1` ist.
  4. Füge alle Blöcke zu einer IPv6-Adresse zusammen.

## Erstellung der EUI-64-Adresse: Die detaillierte Art

Im Nachfolgenden wird eine detaillierte Erklärung zum Vorgehen aufgezeigt, wenn die oben genannte Erklärung für Sie zu allgemein gehalten ist.

### 1. Aufteilen der MAC-Adresse

Gehen wir davon aus, wir besitzen die folgende 48-Bit MAC-Adresse: `00:1A:3F:F1:4C:C6`. Da die MAC-Adresse in der hexadezimalen Schreibweise geschrieben wird, besitzt jeder Block 8 Bits (1 Hex-Zahl = 4 Bits, 1 Block = 2 Hex-Zahlen) oder umgerechnet 1 Byte. Eine MAC-Adresse besitzt 6 hexadezimale Blöcke, welche in Summe 48 Bits ergeben. Für den ersten Schritt muss die 48-Bit lange MAC-Adresse in zwei 24-Bit Teile aufgeteilt werden:

```txt
00:1A:3F | F1:4C:C6
==> 1. 00:1A:3F
==> 2. F1:4C.C6
```

### 2. Füge `FF:FE` hinzu

Da wir nun die MAC-Adresse in zwei 24-Bit Teile aufgeteilt habe, fügen wir `FF:FE` in der Mitte der Adresse ein:

```txt
00:1A:3F + FF:FE + F1:4C:6C ==> 00:1A:3F:FF:FE:F1:4C:6C
```

### 3. Umkehren des siebten Bits

Da wir nun die erste Hälfte vom EUI-64-Verfahren hinter uns haben, indem wir erfolgreich `FF:FE` zur MAC-Adresse hinzugefügt haben, kommen wir zur zweiten Hälfte.

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