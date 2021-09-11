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

Gehen wir in dieser Möglichkeit einfach davon aus, dass wir keinen History Value besitzen. Deswegen erstellen wir einen zufälligen Wert. Die Schritte wie die Privacy Extensions erstellt werden, ist ziemlich einfach zu verstehen:

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

Diese Vorgehensweise fasst zusammen wie Privacy Extensions für IPv6-Adressen laut IETF RC 3041 erstellt werden.