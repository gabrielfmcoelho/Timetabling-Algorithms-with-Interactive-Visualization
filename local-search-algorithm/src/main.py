import json
from local_search import local_search

if __name__ == "__main__":
    with open('../data/inputs/input1.json', 'r') as file:
        data = json.load(file)

    classes = data['classes']
    teachers = data['teachers']
    rooms = data['rooms']
    times = data['times']
    subjects = data['subjects']

    best_schedule = local_search(classes, teachers, rooms, times, subjects)

    with open('../data/outputs/timetabling_output.json', 'w') as file:
        json.dump(best_schedule, file, indent=2, ensure_ascii=False)

    print("Timetabling concluído. Resultados salvos em 'data/outputs/timetabling_output.json'.")