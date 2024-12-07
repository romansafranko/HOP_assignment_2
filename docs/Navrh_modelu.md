# Návrh modelu problému

## Dáta a reprezentácia

- **Predmet**: má nasledujúce atribúty:
  - **Kód predmetu** (napr. "CS497").
  - **Počet cvičení** (napr. 5).
  - **Zoznam kvalifikovaných vyučujúcich** (napr. ["assist.prof. Trevor Edwards", "prof. Jack Thompson", ...]).

- **Vyučujúci**:
  - **Meno a titul (rola)**: napr. "prof. Jack Thompson".
  - **Kapacita vyučovania**: maximálny počet rozvrhových jednotiek (napr. prof. = 5, assoc.prof. = 8, assist.prof. = 11, phd. = 4).
  - **Aktuálne využitie kapacity**: sledované počas priraďovania.

Dáta sú čítané zo vstupného CSV súboru a ukladané do dátových štruktúr, ako je zoznam predmetov a mapovanie vyučujúcich na ich kapacity a aktuálne využitie.

---

## Kandidát riešenia

Kandidát (riešenie) je kompletný zoznam priradení, kde každý predmet obsahuje:
- Obsadeného (alebo obsadených) prednášajúceho(ich).
- Obsadených cvičiacich, pokrývajúcich celý počet cvičení.

```json
{
  "course_code": "CS497",
  "lecture": ["prof. Jack Thompson"] alebo ["prof. Jack Thompson", "prof. John Smith"],
  "exercises": ["assist.prof. Trevor Edwards", "assist.prof. Trevor Edwards", "Veronica Hill", ...]
}
```
---

## Kontrola splnenia podmienok (kriteriálna funkcia)

1. **Prednáška**:
   - Musí byť obsadená jedným alebo dvoma kvalifikovanými vyučujúcimi.
   - Pravidlá:
     - Maximálne dvaja profesori alebo dvaja assoc.prof. môžu byť spolu.
     - Ak sú dvaja, ich zaťaženie sa delí rovnomerne (0,5 na každého).

2. **Cvičenia**:
   - Počet cvičení musí byť úplne pokrytý.

3. **Kapacity vyučujúcich**:
   - Žiadny vyučujúci nesmie prekročiť svoju kapacitu.

4. **Pravidlá prideľovania rolí**:
   - Dodržiavajú sa preferencie doktorandov a ďalšie pravidlá.

---

## Implementácia kontrol

- **Pred priradením prednášajúceho**:
  - Kontroluje sa, či môže vyučujúci prijať ďalšiu rozvrhovú jednotku (alebo polovicu pri zdieľaní).

- **Pri priraďovaní cvičení**:
  - Postupuje sa sekvenčne:
    - Prednosť majú doktorandi, potom asistenti, následne docenti a nakoniec profesori.
  - Kontroluje sa kapacita vyučujúceho pre pridelenie cvičení.

- **Sledovanie zaťaženia (workloads)**:
  - Aktualizácia stavu zaťaženia sa vykonáva priebežne po každom priradení.

- **Nevalidné riešenia**:
  - Ak po prejdení všetkých typov vyučujúcich ostanú neobsadené cvičenia, riešenie je označené ako nevalidné.
  - Predpokladá sa však, že riešenie existuje (podľa zadania).

---
