# Technická dokumentácia a návod na spustenie riešenia

## Popis riešenia

Hlavnou úlohou skriptu **main.py** je priradiť vyučujúcych (profesorov, docentov, odborných asistentov a doktorandov) k rozvrhovým jednotkám (prednáškam a cvičeniam) tak, aby boli dodržané nasledovné podmienky:
1. Prednášky majú prideleného jedného alebo dvoch vyučujúcich podľa priorít a voľnej kapacity.
2. Maximálna kapacita prednášajúcich je:
    - Profesor (prof.) môže odučiť max. 5 jednotiek (pričom 2 profesori na jednej prednáške sa rátajú ako 0,5 jednotky na každého).
    - Docent (assoc.prof.) max. 8 jednotiek.
    - Odborný asistent (assist.prof.) max. 11 jednotiek.
    - Doktorand (phd.) max. 4 jednotky cvičení.
3. Prednášky majú prioritu v prideľovaní k profesorom, ak nie sú k dispozícii, prideľujú sa docentom, odborným asistentom a ak nie je iná možnosť, aj doktorandom.
4. Cvičenia sú prideľované po splnení prednáškových požiadaviek od najnižších pozícií (doktorandi), následne odborní asistenti, docenti a v prípade nutnosti aj profesori, tak, aby nikto neprekročil maximálnu kapacitu.
5. Výstupom je súbor .csv, v ktorom je ku každému predmetu priradený prednášajúci (alebo dvaja), a za nimi zoznam vyučujúcich cvičení.

Súčasťou riešenia je aj validačný skript **test.py**, ktorý skontroluje, či žiadny vyučujúci neprekročil maximálne kapacity a či sú rozdelenia prednášok a cvičení v súlade so zadanými pravidlami.

---

## Štruktúra projektu

```bash
HOP_ASSIGNMENT_2/
├── docs/
│   ├── Analyza_problemu.md
│   └── Navrh_modelu.md
├── output/
│   └── README.md
├── sample/
│   └── test_file.csv
├── src/
│   └── main.py
├── tests/
│   └── test.py
└── README.md 
```

- docs/: Obsahuje dokumentáciu k analýze a návrhu riešenia.
- output/: Adresár, kam sa ukladajú vygenerované výstupné súbory.
- sample/: Obsahuje ukážkový vstupný súbor test_file.csv.
- src/: Zdrojový kód riešenia (main.py).
- tests/: Obsahuje testovací skript test.py na validáciu výsledného priradenia.
- README.md: Hlavný dokument s návodom na použitie a technickou dokumentáciou.

---

## Návod na nastavenie prostredia

### Požiadavky:
- Python 3.8+ (Odporúčaný)
- Žiadne špeciálne knižnice navyše nie sú potrebné (kód používa len štandardnú knižnicu Pythonu)

### Inštalácia a spustenie
**Klonovanie repozitára:**

```bash
git clone https://your_repo_url/HOP_ASSIGNMENT_2.git
cd HOP_ASSIGNMENT_2
```

**Vytvorenie virtuálneho prostredia (odporúčané):**

```bash
python -m venv venv
source venv/bin/activate   # Na Linux / MacOS
# alebo
venv\Scripts\activate      # Na Windows
```

**Inštalácia závislostí:**
V tomto projekte nie sú požadované externé balíčky. Ak by ste v budúcnosti nejaké potrebovali, stačí ich inštalovať príkazom:

```bash
pip install -r requirements.txt
```
(Súbor requirements.txt momentálne nie je prítomný, keďže nie je potrebný.)

---

## Návod na prácu s riešením
### Spustenie hlavného programu
Pripravte si vstupný .csv súbor s predmetmi a dostupnými vyučujúcimi. Formát jedného riadku je:

```bash
kod_predmetu;počet_cvičení;zoznam_vyučujúcich
```
Napríklad:

```bash
CS497;5;assist.prof. Trevor Edwards,prof. Jack Thompson,assoc.prof. Theo Gardner, Veronica Hill
```

Tento súbor uložte napr. do adresára sample/ pod menom file_name.csv.

Spustite skript main.py s argumentom na vstupný súbor:

```bash
python src/main.py sample/test_file.csv
```
Skript vygeneruje výstupný súbor do adresára output/, napr.:

```bash
output/file_name_assigned_workloads.csv
```

Vo výstupnom súbore .csv nájdete kód predmetu a priradených vyučujúcich podľa formátu:

```bash
kod_predmetu;prednasajuci,cviciaci1,cviciaci2,...
```

Napríklad:

```bash
CS121;assoc.prof. Max Parker,Jennifer Gardner,Jennifer Gardner
```

### Validácia výsledku
Pre overenie, či výstup spĺňa všetky kapacitné a rolové obmedzenia, spustite testovací skript:

```bash
python tests/test.py output/test_file_assigned_workloads.csv
```

Ak sú všetky pravidlá dodržané, uvidíte hlášku:

```bash
Všetky podmienky sú splnené.
```

Ak dôjde k nedodržaniu pravidiel, skript vyhodí príslušné chybové hlásenie.

---

## Popis implementácie (`main.py`)

### 1. Funkcia `assign_workloads`
1. Vstupy a výstupy

**Vstup:** Súbor (input_file) so záznamami o predmetoch, počte cvičení a vyučujúcich.

**Výstup:** Súbor (output_file) s priradenými úväzkami (kto prednáša a kto vedie cvičenia).

2. Definovanie maximálnych kapacít

```bash
capacities = {
    "prof.": 5,
    "assoc.prof.": 8,
    "assist.prof.": 11,
    "phd.": 4
}
```

Každá rola má maximálny počet úväzkov (počet rozvrhových jednotiek), ktoré môže zvládnuť:

- Profesor (`prof.`): max. 5.
- Docent (`assoc.prof.`): max. 8.
- Odborný asistent (`assist.prof.`): max. 11.
- Doktorand (`phd.`): max. 4.

3. Premenné na sledovanie stavu

```bash
workloads = {}  # Sledovanie aktuálneho zaťaženia jednotlivých vyučujúcich
results = []    # Uloženie výsledkov na export
```
**workloads:** Ukladá zaťaženie jednotlivých vyučujúcich.

**results:** Obsahuje záznamy vo formáte výstupného súboru.


### 2. Načítanie a spracovanie vstupného súboru

```bash
with open(input_file, 'r') as file:
    lines = file.readlines()
```

- Načítajú sa všetky riadky zo súboru (každý riadok obsahuje predmet, počet cvičení a zoznam vyučujúcich).

**Spracovanie každého riadku**

```bash
course_code, num_exercises, instructors_raw = line.strip().split(';')
num_exercises = int(num_exercises)
instructors = [instr.strip() for instr in instructors_raw.split(',')]
```

- Rozdelenie riadka na:
    - Kód predmetu (`course_code`).
    - Počet cvičení (`num_exercises`).
    - Zoznam vyučujúcich (`instructors`).

### 3. Klasifikácia vyučujúcich podľa rolí

```bash
professors = [i for i in instructors if "prof." in i and "assoc." not in i]
assoc_professors = [i for i in instructors if "assoc.prof." in i]
assist_professors = [i for i in instructors if "assist.prof." in i]
phd_students = [i for i in instructors if not any(role in i for role in ["prof.", "assoc.prof.", "assist.prof."])]
```

- Vyučujúci sú rozdelení podľa ich rolí:
    - `professors`: Profesori.
    - `assoc_professors`: Docenti.
    - `assist_professors`: Odborní asistenti.
    - `phd_students`: Doktorandi.

### 4. Priradenie prednášok

```bash
if len(professors) >= 2 and all(workloads.get(p, 0) + 0.5 <= capacities["prof."] for p in professors[:2]):
    lecture = professors[:2]
elif professors and workloads.get(professors[0], 0) + 1 <= capacities["prof."]:
    lecture = [professors[0]]
elif assoc_professors and workloads.get(assoc_professors[0], 0) + 1 <= capacities["assoc.prof."]:
    lecture = [assoc_professors[0]]
elif assist_professors and workloads.get(assist_professors[0], 0) + 1 <= capacities["assist.prof."]:
    lecture = [assist_professors[0]]
elif phd_students:
    lecture = [phd_students[0]]
```

- Prednášky sa priraďujú v poradí podľa rolí:
    1. Dvaja profesori (ak majú dostatok kapacity na 0.5 úväzku každý).
    2. Jeden profesor.
    3. Jeden docent.
    4. Jeden odborný asistent.
    5. Jeden doktorand (ako posledná možnosť).

### 5. Priradenie cvičení

```bash
for group, role in zip([phd_students, assist_professors, assoc_professors, professors],
                       ["phd.", "assist.prof.", "assoc.prof.", "prof."]):
    for instructor in group:
        if num_exercises <= 0:
            break
        available_capacity = int(capacities[role] - workloads.get(instructor, 0))
        to_assign = min(available_capacity, num_exercises)
        if to_assign > 0:
            exercise_assignments.extend([instructor] * to_assign)
            workloads[instructor] = workloads.get(instructor, 0) + to_assign
            num_exercises -= to_assign
```

- Cvičenia sa priraďujú v poradí: doktorandi, odborní asistenti, docenti, profesori.
- Kontroluje sa dostupná kapacita každého vyučujúceho.
- Počet cvičení je znížený po každom priradení.

### 6. Uloženie výsledkov

```bash
lecture_assignment = '/'.join(lecture) if lecture else "None"
assignments = [lecture_assignment] + exercise_assignments
results.append(f"{course_code};{','.join(assignments)}")
```

- Prednášajúci sa uloží vo formáte: "prof1/prof2".
- Cvičenia sú uložené ako zoznam mien vyučujúcich.

### 7. Zápis do výstupného súboru

```bash
with open(output_file, 'w') as file:
    file.write('\n'.join(results))
```

- Všetky výsledky sa zapíšu do súboru v štruktúrovanom formáte.
### 8. Hlavná časť programu

```bash
if __name__ == "__main__":
    ...
```

- Načítajú sa argumenty z príkazového riadku.
- Vytvorí sa výstupný adresár, ak neexistuje.
- Spustí sa funkcia assign_workloads.

## Popis testovacieho skriptu (`test.py`)

Skript **test.py** načíta vygenerovaný .csv výstup a overí:
- Či nie sú prekročené kapacity vyučujúcich.
- Či je platná kombinácia prednášajúcich (max dvaja prednášajúci, a ak dvaja, tak obaja musia byť aspoň docenti).
- Či sa nedeje duplicitné priradenie cvičení jednému vyučujúcemu nad rámec kapacity.
Ak niektorá z kontrol zlyhá, skript vyhodí **ValueError** s vysvetľujúcim hlásením.