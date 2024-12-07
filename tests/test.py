import csv

# Definícia maximálnych kapacít
capacities = {
    "prof.": 5,
    "assoc.prof.": 8,
    "assist.prof.": 11,
    "phd.": 4
}

def validate_workloads(input_file):
    workloads = {}  # Sledovanie aktuálneho zaťaženia jednotlivých vyučujúcich

    with open(input_file, 'r') as file:
        reader = csv.reader(file, delimiter=';')
        for row in reader:
            course_code = row[0]  # Kód predmetu
            lecture = row[1]      # Prednášajúci
            exercises = row[2:]   # Cvičiaci

            # Overenie prednášky
            lecture_instructors = lecture.split('/')
            if len(lecture_instructors) > 2:
                raise ValueError(f"Viac ako dvaja prednášajúci na predmete {course_code}.")
            if len(lecture_instructors) == 2:
                for instructor in lecture_instructors:
                    if not any(role in instructor for role in ["prof.", "assoc.prof."]):
                        raise ValueError(f"Neplatná kombinácia prednášajúcich na predmete {course_code}.")
                    workloads[instructor] = workloads.get(instructor, 0) + 0.5
            elif lecture_instructors[0] != "None":
                workloads[lecture_instructors[0]] = workloads.get(lecture_instructors[0], 0) + 1

            # Overenie cvičení
            for instructor in exercises:
                role = ("prof." if "prof." in instructor and "assoc." not in instructor else
                        "assoc.prof." if "assoc.prof." in instructor else
                        "assist.prof." if "assist.prof." in instructor else
                        "phd.")
                workloads[instructor] = workloads.get(instructor, 0) + 1
                if workloads[instructor] > capacities[role]:
                    raise ValueError(f"Inštruktor {instructor} prekročil maximálnu kapacitu na predmete {course_code}.")

            # Overenie počtu cvičení
            if len(exercises) != len(set(exercises)):
                raise ValueError(f"Cvičenia na predmete {course_code} nie sú rozdelené správne.")

    print("Všetky podmienky sú splnené.")

# Spustenie testu
if __name__ == "__main__":
    import sys
    from pathlib import Path

    # Kontrola argumentu pre vstupný súbor
    if len(sys.argv) < 2:
        print("Usage: python validate_workloads.py <assigned_workloads_file>")
        sys.exit(1)

    # Cesta k vstupnému súboru
    input_path = Path(sys.argv[1])

    # Spustenie validácie
    validate_workloads(input_path)