# Privacy-Extensions

## Disclaimer

Ich bin kein Experte, was Python-Programmierung oder die Themen rund um IPv6 angeht. Alle hier aufgeführten Informationen basieren auf meinem Wissen über die Netzwerktechnik, als auch Python. Bitte nimm in Kenntnis, dass die aufgeführten Informationen keine Garantie für die absolute Richtigkeit der Methode übernehmen. Daher ist es ratsam sich auch andere Quellen anzuschauen, um sich mehr über das Thema zu informieren. Quellen, welche ich für meine Recherche benutzt habe, findest du am Ende des Dokuments.

## Was sind IPv6 Privacy Extensions?

IPv6 Privacy Extensions erweitert den [rfc-4941](https://tools.ietf.org/html/rfc4941)-Standard für Stateless Address Autoconfiguration (SLAAC). Dabei handelt es sich um den Nachfolger des veralteten EUI-64 Verfahrens. Die Hauptaufgabe von Privacy Extensions ist es den Interface Identifier einer IPv6-Adresse zu anonymisieren. Warum das jedoch nur die halbe Wahrheit ist, werde ich nachfolgend in diesem Dokument erläutern.

### Warum Privacy Extensions?

Wenn du mein Readme zum EUI-64-Verfahren gelesen hast, solltest du bereits wissen, dass man ohne große Anstrengungen die MAC-Adresse ganz einfach aus dem Interface Identifier ableiten kann. Mit dieser ist es möglich getrackt zu werden, manche Webseiten könnten mehr Informationen über dein Betriebssystem wie Hersteller etc. erfahren oder eine böswillige Person könnte damit Unfug treiben. Wir möchten nicht, dass das unbedingt passiert oder? Deswegen verwenden wir Privacy Extensions, um unseren Interface Identifier zu anonymisieren. Dadurch wird es schwerer jemanden zu tracken oder sonstige Schandtaten mit zu treiben.

### Wie werden Privacy Extension erstellt?

Kommen wir zum eigentlich interessanten Teil. Ich möchte dir drei Möglichkeiten präsentieren wie man den Interface Identifier von IPv6 mit Privacy Extensions erstellt:

  1. Wie es 'RFC-3041' vorschlägt
  2. Eine Methode, die das 'Elektrik-Kompendium' vorschlägt
  3. Zeit des ersten Systemstarts (nicht als Skript enthalten!)

**Achte darauf, dass es deutlich mehr Möglichkeiten gibt, Privacy Extensions zu erstellen**. Nun könnte man sich fragen, weshalb es so viele verschiedene Möglichkeiten existieren wie man die Privacy Extensions erstellt. Um ehrlich zu sein, kann ich das nicht beantworten. Meiner Meinung nach gibt die IETF RFC nur eine Möglichkeit von vielen vor wie man Privacy Extensions erstellen kann. Letztendlich ist es dem Hersteller selbst überlassen wie er diese in seiner Software implementiert.

### Privacy Extensions Möglichkeit 1: Wie es die IETF RFC vorschlägt

Die IETF RFC 3041 beschreibt das Erzeugen der Privacy Extensions so, dass ein sogenannter `History Value` und die EUI-64 basierte Mac-Adresse zusammengefügt werden und anschließend ein MD5-Hash aus dem Ergebnis erzeugt wird. Nun fragst du dich vielleicht, was dieser `History Value` eigentlich ist. Der `History Value` beschreibt einen Wert, welcher beim Bootvorgang des jeweiligen Hosts bereitgestellt wird. Dabei gibt es zwei Werte, welche bereitgestellt werden können:

  1. Eine zufällig generierte Zahl
  2. Immer dann, wenn ein neuer Interface Identifier erstellt wird, wird ein bestimmter errechneter Wert als `History Value` abgespeichert. Dieser wird, anstatt einer zufälligen Zahl, für die nächste Erstellung von Privacy Extensions benutzt.

Gehen wir in dieser Möglichkeit einfach davon aus, dass wir keinen History Value besitzen. Deswegen erstellen wir einen zufälligen Wert. Die Schritte wie die Privacy Extensions erstellt werden, sind ziemlich einfach zu verstehen:

  1. Erstelle einen kryptografisch starken, zufälligen Wert:

```txt
d1ccbd1825293666aa4297922ee9ab2c205a6a676f007c97db269d6fb7b9a38d
```

  2. Hänge die EUI-64 basierte MAC-Adresse an den zufällig generierten Wert:

```txt
d1ccbd1825293666aa4297922ee9ab2c205a6a676f007c97db269d6fb7b9a38d00:1A:3F:FF:FE:F1:4C:C6
```

  3. Erstelle einen MD5-Hash im hexadezimalen Format mit dem vorherig erstellen Wert als Eingabe:

```txt
de4d64ef06f2869cd3197096c86b7625
```

  4. Benutz die, von links aus gesehenen ersten 64 Bits:

```txt
de4d64ef06f2869c
```

  5. Setze das sechste Bit auf `0`:

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

  6. Erstelle den IPv6 Interface Identifer:

```txt
da4d:64ef:06f2:869c
```

  7. Benutz die, von rechts aus gesehenen 64 Bits des erstellten MD5-Hashes als `History Value`

```txt
d3197096c86b7625 ==> History Value. Wird für die Erstellung der nächsten Privacy Extensions benutzt, anstatt einen zufälligen Wert zu berechnen.
```

Diese Vorgehensweise fasst zusammen wie Privacy Extensions für IPv6-Adressen laut IETF RFC 3041 erstellt werden.

### Privacy Extensions Möglichkeit 2: Wie es das Elektronik-Kompendium vorschlägt

Anders als die Möglichkeit des RFCs der IETF benutzt die deutsche Webseite `Elektronik-Kompendium` weder einen History Value noch einen zufällig generierten String für die Erstellung der IPv6 Privacy Extensions. Stattdessen beschreiben sie die Erstellung der Privacy Extensions so, dass sie den jetzigen NTP-Zeitstempel sowie die MAC-Adresse zusammenfügen und diese mit dem Hashalgorithmus SHA1 hashen. Als Ergebnis erhält man einen 64 Bit langen SHA1-Hash für die Verwendung als Privacy Extensions. Die Vorangehensweise kann zum Beispiel folgendermaßen aussehen:

  1. Die aktuelle Zeit erfassen: `05:19:57`
  2. Die MAC-Adresse hinzufügen: `05:19:5700:1A:3F:F1:4C:C6`
  3. Mit SHA1 als Hashalgorithmus hashen: `9987e92f9fa0c71ad6f3f22ee4be7afd7cea66b7`
  4. Die ersten 64 Bits von links benutzen: `9987e92f9fa0c71a`
  5. Den Interface Identifier daraus bilden: `9987:e92f:9fa0:c71a`

### Privacy Extensions Möglichkeit 3: Die erste Systemstartzeit nutzen

Eine andere Möglichkeit kommt von einen meiner damaligen Lehrer, welcher der Meinung ist, dass es besser wäre die Systemstartzeit des jeweiligen Computers zu benutzen. Zusammen mit dieser bis auf Nanosekunden berechnete Startzeit und der MAC-Adresse soll ein 64 Bit langer Hash mit einem der gängigen Hashalgorithmen erstellt werden. Denn wenn man darüber nachdenkt ist es ziemlich unwahrscheinlich, dass verschiedene Computer zur gleichen Zeit gestartet werden können. Ganz gleich wie gut das Starten der Computer abgestimmt wäre, es würde so gut wie immer eine kleine Zeitverzögerung von System zu System geben. Daher sollte es ziemlich unmöglich sein eine Adressen-Kolission im globalen IPv6-Einsatzbereich hervorzurufen. Jedoch ist dies nur eine theoretische Ansicht und wird meiner Meinung nach sehr wahrscheinlich nirgends implementiert.

### Das Problem mit den Privacy Extensions: Datensicherheit

Was wäre, wenn ich dir sagen würde, dass du selbst mit aktivierten Privacy Extensions zurückverfolgt werden könntest? Das wäre mit Sicherheit verwirrend order? Immerhin sind die Privacy Extensions dafür da, deinen Interface Identifier zu anonymisieren. Zwar ist das für den Interface Identifier richtig, nicht jedoch für den ISP-Präfix. Das bedeutet, dass du wie bei IPv4 in einem Umkreis von ein Paar Kilometern zurückverfolgt werden kannst. Manche Internet Service Provider entwickeln bereits Gegenmaßnahmen, welche zum Beispiel innerhalb einer bestimmten Zeit den ISP-Präfix hin und wieder mal durch einen neuen auswechseln.

### Warum einen statischen Interface Identifier benutzen, wenn es doch Privacy Extensions gibt?

Mit aktivierten Privacy Extensions ist dein Interface Identifier anonymisiert und wird in bestimmten Zeitperioden durch einen Neuen gewechselt. Das fördert den Einsatz von Privacy Extensions. Doch es gibt auch Anwendungsbereiche, in welchen aktivierte Privacy Extensions stören können. Möchtest du zum Beispiel einen Service wie einen Webserver der Öffentlichkeit bereitstellen, dann wirst du mit aktivierten Privacy Extensions nicht glücklich. Mit aktivierten Privacy Extensions kann man deine Adresse als "dynamisch" anerkennen. Das bedeutet, dass diese immer in einer gewissen Zeitspanne wechselt, was für dauerhaft erreichbare, öffentliche Dienste nicht der Fall sein sollte. Deshalb werden für solche Dienste die Privacy Extensions in der Regel ausgeschaltet.

## Quellen

[https://tools.ietf.org/html/rfc4941](https://tools.ietf.org/html/rfc4941)

[https://tools.ietf.org/html/rfc2373](https://tools.ietf.org/html/rfc2373)

[https://tools.ietf.org/html/rfc3041#section-3.2](https://tools.ietf.org/html/rfc3041#section-3.2)

[https://www.elektronik-kompendium.de/sites/net/1601271.htm](https://www.elektronik-kompendium.de/sites/net/1601271.htm)