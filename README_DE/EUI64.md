# EUI-64 Methode

## Disclaimer

Ich bin kein Experte, was Python-Programmierung oder die Themen rund um IPv6 angeht. Alle hier aufgeführten Informationen basieren auf meinem Wissen über die Netzwerktechnik, als auch Python. Bitte nimm in Kenntnis, dass die aufgeführten Informationen keine Garantie für die absolute Richtigkeit der Methode übernehmen. Daher ist es ratsam sich auch andere Quellen anzuschauen, um sich mehr über das Thema zu informieren. Quellen, welche ich für meine Recherche benutzt habe, findest du am Ende des Dokuments.

## Was ist EUI-64?

EUI-64 ist eine Methode, um einen 64-Bit Interface Identifier für eine IPv6-Adresse eines Host-System zu erstellen. Das EUI-64-Verfahren war die erste Herangehensweise zur Erstellung eines Interface Identifiers. Heutzutage wird EUI-64, wenn überhaupt, ausschließlich für die Erstellung von Link-Local-Adressen benutzt, da diese eine große Sicherheitsschwachstelle besitzen. Diese Schwachstelle beschreibt, dass es möglich ist die MAC-Adresse eines Clients aus dem EUI-64 erstellten Interface Identifier herzuleiten. Wie das funktioniert wirst du später erfahren. Mit dieser Schwachstelle war es möglich technische Geräte und somit auch Personen zu Orten und ihre Bewegungsmuster aufzuzeichnen. Verständlicherweise ist das unangenehm, da z.B. Mitarbeiter von Unternehmen nicht dauerhaft verfolgt werden möchten. Das ist jedoch nur eine Schwachstelle von vielen weiteren.

## Erstellung der EUI-64-Adresse: Die einfache Art

Im Nachfolgenden wird eine simple Erklärung für die Erstellung des EUI-64 Interface Identifiers aufgezeigt:

  1. Teile die MAC-Adresse in der Hälfte auf.
  2. Füge `ff:fe` in die Mitte ein.
  3. Setze das siebte Bit auf eine `1`, wenn es eine `0` ist. Setze es auf eine `0`, wenn es eine `1` ist (siehe Notizen)
  4. Füge alle Blöcke zu einer IPv6-Adresse zusammen.

## Erstellung der EUI-64-Adresse: Die detaillierte Art

Im Nachfolgenden wird eine detaillierte Erklärung zum Vorgehen aufgezeigt, wenn die oben genannte Erklärung für dich zu allgemein gehalten ist.

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

Da wir nun die erste Hälfte vom EUI-64-Verfahren hinter uns haben, indem wir erfolgreich `FF:FE` zur MAC-Adresse hinzugefügt haben, kommen wir zur zweiten Hälfte. **Wie wir wissen** besteht ein MAC-Adressenblock aus 8 Bits. Um das Umkehren des siebten Bits anzuwenden, benötigen wir den ersten MAC-Adressblock, welcher in diesem Fall `00` ist. Dabei ist das Vorgehen wie folgt:

```txt
1. Erste '0' in binär: 0000
2. Zweite '0' in binär: 0000

==> 0000 0000 ==> 00000000
```

Nun schauen wir uns das siebte Bit an. Wenn dieses eine `0` aufweist, kehren wir dieses um, und machen daraus eine `1`. Ist das siebte Bit eine `1` machen wir daraus eine `0` (siehe Notizen). In unserem Fall kehren wir das siebte Bit folgendermaßen um:

```txt
0000 0000
       ^ 
==> 0000 0010 ==> 00000010
```

Nun konvertieren wir die binäre Darstellung wieder in Hexadezimal um, um unsere EUI-64 MAC-Adresse herauszubekommen:

```txt
0000 ==> 0
0010 ==> 2
==> 02
==> 02:1A:3F:FF:FE:F1:4C:6C
```

### 4. Erstellen der IPv6-Adresse / des Interface Identifiers

Unser letzter Schritt ist einfach: wir erstellen eine IPv6-Adresse bzw. den Interface Identifier mit den, in der EUI-64-Adresse enthaltenden hexadezimalen Blöcken. Wir wir bereits wissen ist eine IPv6-Adresse 128 Bits oder 16 Bytes lang. Da wir jedoch nur unseren Interface Identifier setzen wollen, benötigen wir nur die Hälfte der Bits, daher also 64 Bits. Nun können wir unseren Interface Identifier folgendermaßen zusammenstellen:

```txt
02:1A:3F:FF:FE:F1:4C:6C ==> 021A:3FFF:FEF1:4C6C
```

Voilà so haben wir unseren EUI-64 basierten Interface Identifier erfolgreich erzeugt!

## Zurück zur Sicherheitsschwachstelle

Kehren wir nun einmal zu meiner im Text erwähnten Sicherheitsschwachstelle zurück. Wenn du stark aufgepasst hast, dann solltest du nun wissen wie die MAC-Adresse aus der EUI-64-Adresse errechnet werden kann. Dafür musst du nur die angewandten Schritte in umgekehrter Reiehenfolge durchlaufen. Einfach nicht wahr? Das ist mitunter ein Grund, weshalb ein neuer Standard entwickelt werden musste. Dieser Standard ist bekannt und spezifiziert unter dem Namen **IPv6 Privacy Extensions**. Aber selbst **mit** aktivierten Privacy Extensions gibt es Komplikationen. Wenn du mehr über das Thema `Privacy Extensions` wissen möchtest, dann schau dir die README-Datei für die IPv6 Privacy Extensions an.

## Notizen

Wie bereits im Text besprochen muss das siebte Bit der MAC-Adresse umgekehrt werden, um die EUI-64-Adresse zu erstellen. Nun möchte ich jedoch ein paar Anmerkungen dazu machen. Wie in RFC-4291 angesprochen, existieren anscheinend für die jewiligen umgekehrten Bits `1` oder `0` verschiedene Eigenschaften. Dabei wird beschrieben, dass eine `1` auf eine globale / universale Verwendung (globaler Bereich) hinweist. Eine `0` soll dabei den lokalen Bereich kennzeichnen.

Auch wenn Wikipedia generell keine vertrauenswürdige Quelle ist, ist dennoch anzumerken, dass es keinen Eintrag darüber gibt, welche Bedeutung das siebte Bit tatsächlich besitzt.

Die Webseite `Elektronik-Kompendium` merkt hingegen an, dass es sich bei einer `1` des siebten Bits um eine erdachte Adresse (Fantasieadresse) handeln würde. Eine `0` soll darauf hinweisen, dass die MAC-Adresse von der IEEE abstammt. Der nachfolgende Satz steht jedoch im Gegensatz zu dem vorherigen. Hier wird nämlich beschrieben, dass bei einer ausgedachten Adresse das Bit auf `0` gesetzt wird. Entweder ist das ein Schreibrfehler oder die Webseite vermittelt diese Informationen falsch.

Ich persönlich würde sagen, dass es in Ordnung ist weiterhin die bekannte Vorgehensweise zu benutzen (aus 1 zu 0 und aus 0 zu 1). Jedoch solltest du die Anmerkung der RFC im Hinterkopf behalten.

## Quellen

[https://tools.ietf.org/html/rfc4291](https://tools.ietf.org/html/rfc4291)

[https://de.wikipedia.org/wiki/EUI-64](https://de.wikipedia.org/wiki/EUI-64)

[https://www.elektronik-kompendium.de/sites/net/1902131.htm](https://www.elektronik-kompendium.de/sites/net/1902131.htm)
