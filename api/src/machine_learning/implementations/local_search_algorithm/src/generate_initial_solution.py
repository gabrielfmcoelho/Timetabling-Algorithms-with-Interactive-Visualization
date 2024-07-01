from typing import List, Dict
import random

def generate_initial_solution(
    classes: List[Dict], 
    teachers: List[Dict], 
    rooms: List[Dict], 
    times: List[Dict],
    subjects: List[Dict]
) -> List[Dict]:
    
    schedule = []
    for class_info in classes:
        class_schedule = []

        for day in ['Segunda-Feira', 'Terça-Feira', 'Quarta-Feira', 'Quinta-Feira', 'Sexta-Feira']:
            periods = []
            for time in times:
                random_teacher = random.choice(teachers)
                random_room = random.choice(rooms)
                subject = random.choice(random_teacher['subjects'])
                teacher_name = random_teacher['name']
                room_name = random_room['name']
                period = {
                    "day": day,
                    "time": f"{time['start']} - {time['end']}",
                    "subject": next((sub['name'] for sub in subjects if sub['id'] == subject), None),
                    "teacher": teacher_name,
                    "room": room_name
                }
                periods.append(period)
            class_schedule.append({"day": day, "periods": periods})
        schedule.append({"id": class_info['id'], "name": class_info['name'], "schedule": class_schedule})

    return schedule