import json
from src.local_search import local_search
from src.MetricsEvaluator import metrics_evaluator

if __name__ == "__main__":
    metrics_evaluator.start_timer()

    with open('../data/inputs/input1.json', 'r') as file:
        data = json.load(file)

    classes = data['classes']
    teachers = data['teachers']
    rooms = data['rooms']
    times = data['times']
    subjects = data['subjects']
    days = data['days'] 

    best_schedule, metrics_evaluator = local_search(classes, teachers, rooms, times, subjects, days)

    print(metrics_evaluator)

    with open('../data/outputs/timetabling_output.json', 'w') as file:
        json.dump(best_schedule, file, indent=2, ensure_ascii=False)

    print("Timetabling concluído. Resultados salvos em 'data/outputs/timetabling_output.json'.")