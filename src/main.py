# Hlavná funkcia na priraďovanie úväzkov
def assign_workloads(input_file, output_file):
    # Definovanie maximálnych kapacít pre jednotlivé role
    capacities = {
        "prof.": 5,          # Profesori môžu učiť maximálne 5 rozvrhových jednotiek
        "assoc.prof.": 8,    # Docenti môžu učiť maximálne 8 rozvrhových jednotiek
        "assist.prof.": 11,  # Odborní asistenti môžu učiť maximálne 11 rozvrhových jednotiek
        "phd.": 4            # Doktorandi môžu učiť maximálne 4 cvičenia
    }

    workloads = {}  # Sledovanie aktuálneho zaťaženia jednotlivých vyučujúcich
    results = []    # Zoznam výsledkov na výstup

    # Načítanie vstupného súboru
    with open(input_file, 'r') as file:
        lines = file.readlines()

    # Spracovanie každého riadku zo vstupu
    for line in lines:
        # Parsovanie dát z riadku
        course_code, num_exercises, instructors_raw = line.strip().split(';')
        num_exercises = int(num_exercises)
        instructors = [instr.strip() for instr in instructors_raw.split(',')]

        # Rozdelenie vyučujúcich podľa ich roly
        professors = [i for i in instructors if "prof." in i and "assoc." not in i]
        assoc_professors = [i for i in instructors if "assoc.prof." in i]
        assist_professors = [i for i in instructors if "assist.prof." in i]
        phd_students = [i for i in instructors if
                        not any(role in i for role in ["prof.", "assoc.prof.", "assist.prof."])]

        lecture = None  # Premenná pre prednášku

        # Výber vyučujúcich pre prednášku
        if len(professors) >= 2 and all(workloads.get(p, 0) + 0.5 <= capacities["prof."] for p in professors[:2]):
            lecture = professors[:2]  # Dvaja profesori na prednášku
        elif professors and workloads.get(professors[0], 0) + 1 <= capacities["prof."]:
            lecture = [professors[0]]  # Jeden profesor na prednášku
        elif assoc_professors and workloads.get(assoc_professors[0], 0) + 1 <= capacities["assoc.prof."]:
            lecture = [assoc_professors[0]]  # Jeden docent na prednášku
        elif assist_professors and workloads.get(assist_professors[0], 0) + 1 <= capacities["assist.prof."]:
            lecture = [assist_professors[0]]  # Jeden odborný asistent na prednášku
        elif phd_students:
            lecture = [phd_students[0]]  # Jeden doktorand na prednášku (ak je to nutné)

        # Aktualizácia zaťaženia vyučujúcich na prednáške
        if lecture:
            for lecturer in lecture:
                workloads[lecturer] = workloads.get(lecturer, 0) + (0.5 if len(lecture) > 1 else 1)

        exercise_assignments = []  # Priradenie cvičení
        # Priraďovanie cvičení vyučujúcim
        for group, role in zip([phd_students, assist_professors, assoc_professors, professors],
                               ["phd.", "assist.prof.", "assoc.prof.", "prof."]):
            for instructor in group:
                if num_exercises <= 0:  # Ak sú všetky cvičenia pokryté, ukonči cyklus
                    break
                available_capacity = int(capacities[role] - workloads.get(instructor, 0))
                to_assign = min(available_capacity, num_exercises)  # Koľko cvičení môže vyučujúci pokryť
                if to_assign > 0:
                    exercise_assignments.extend([instructor] * to_assign)  # Priraď toľko cvičení, koľko môže
                    workloads[instructor] = workloads.get(instructor, 0) + to_assign  # Aktualizuj zaťaženie
                    num_exercises -= to_assign  # Zníž počet zostávajúcich cvičení

        # Zostavenie priradení pre aktuálny predmet
        lecture_assignment = '/'.join(lecture) if lecture else "None"
        assignments = [lecture_assignment] + exercise_assignments
        results.append(f"{course_code};{','.join(assignments)}")

    # Zápis výsledkov do výstupného súboru
    with open(output_file, 'w') as file:
        file.write('\n'.join(results))


# Spustenie programu z príkazového riadku
if __name__ == "__main__":
    import sys
    from pathlib import Path

    # Kontrola, či bol poskytnutý vstupný súbor
    if len(sys.argv) < 2:
        print("Usage: python main.py <input_file>")
        sys.exit(1)

    # Získanie cesty k vstupnému súboru
    input_path = Path(sys.argv[1])

    hop_directory = input_path.parents[1]
    output_directory = hop_directory / "output"
    output_directory.mkdir(exist_ok=True)  # Vytvor výstupný adresár, ak neexistuje

    # Definovanie výstupného súboru
    output_path = output_directory / f"{input_path.stem}_assigned_workloads.csv"

    # Volanie funkcie na priradenie úväzkov
    assign_workloads(input_path, output_path)
