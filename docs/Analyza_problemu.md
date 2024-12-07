# Analýza problému

## Popis problému

Máte k dispozícii zoznam predmetov. Každý predmet má:
- Jeden prednáškový blok (jednu rozvrhovú jednotku pre prednášku).
- Určitý počet cvičení, ktoré treba obsadiť (napr. 5 cvičení).
- Zoznam kandidátov na výučbu (profesori, docenti, odborní asistenti, doktorandi), ktorí sú kvalifikovaní na daný predmet.

Cieľom je priradiť vyučujúcich k prednáške a následne aj k jednotlivým cvičeniam tak, aby:
1. Boli splnené kapacitné obmedzenia na počet rozvrhových jednotiek pre každého vyučujúceho.
2. Boli splnené pravidlá o obsadzovaní prednášky (napr. ak sú dvaja profesori alebo dvaja docenti na jednom predmete, prednáška sa medzi nich delí a zaťaženie v rámci úväzku sa počíta ako 0,5 pre každého).
3. Doktorandi sa primárne prideľujú na predmety, kde sú uvedení (prednostne na také, kde ich "školiteľ" preferuje), ale môžu byť použití aj inde, ak je to nutné.
4. Dodržiava sa pravidlo, že traja profesori alebo traja docenti nemôžu byť naraz na jednom predmete. (Maximálne dvaja profesori alebo dvaja docenti.)

---

## Typ problému

Ide o deliaci a priraďovací problém (assignment problem) s dodatočnými obmedzeniami na kapacity a špecifickými pravidlami pre zdieľanie prednášky. Môžeme ho chápať ako variant viac-kriteriálneho priradenia úloh ľuďom:
- Každý predmet predstavuje „úlohu“, ktorá sa delí na "prednášku" (1 slot) a "cvičenia" (viacero slotov).
- Každý vyučujúci má obmedzenú kapacitu (horný limit) na počet rozvrhových jednotiek.
- Prednášky a cvičenia nemožno priradiť ľubovoľnému vyučujúcemu, iba z podmnožiny kvalifikovaných.
- Preferencie a pravidlá ohľadom rolí (prof., assoc.prof., assist.prof., phd.) určujú prioritu a spôsob obsadenia prednášok a cvičení.

---

## Zložky problému a podmienky

### Kandidáti (vyučujúci)
- Kategorizovaní podľa roly: profesor, docent, odborný asistent, doktorand.

### Kapacity
- Maximálne počty hodín/rozvrhových jednotiek, ktoré môže každý vyučujúci učiť, sú pre každú rolu iné.

### Pravidlá pre prednášku
- Ak sú na predmete dvaja profesori alebo dvaja docenti, zdieľajú jednu prednášku za polovicu záťaže pre každého.
- Ak je prednášajúci len jeden (prof., assoc.prof., assist.prof. alebo phd.), berie si celú záťaž (1).
- Traja profesori alebo traja docenti nemôžu byť spolu na jednom predmete.

### Pravidlá pre cvičenia
- Po obsadení prednášky je potrebné pokryť zvyšný počet cvičení.
- Uprednostňujú sa doktorandi (najmä pri predmetoch, kde sú explicitne uvedení), potom asistenti, potom docenti a nakoniec profesori.

---

## Definícia kritérií a kvality riešenia

Základná implementácia sa zameriava na nájdenie platného riešenia (feasibility) namiesto optimalizácie. Kvalita riešenia by sa však mohla definovať nasledovne:
- Minimalizovať celkové preťaženie alebo nárast kapacity u vyšších pedagogických hodností.
- Minimalizovať počet doktorandov, ktorí učia predmety, kde nie sú preferovaní.
- Minimalizovať použitie profesorov na cvičenia.

V aktuálnej forme sa kód snaží iba uspokojiť dané obmedzenia a neoptimalizuje globálne riešenie.
