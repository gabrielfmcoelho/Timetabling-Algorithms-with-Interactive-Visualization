from typing import List, Dict
import random

def generate_initial_solution(
    classes: List[Dict], 
    teachers: List[Dict], 
    rooms: List[Dict], 
    times: List[Dict],
    subjects: List[Dict],
    days: List[Dict]
) -> List[Dict]:

    schedule = []
    for class_info in classes:
        class_schedule = []

        for day in days:
            day_name = day['name']
            day_schedule = {'day': day_name, 'periods': []}

            for time in times:
                time_info = f"{time['start']} - {time['end']}"
                available_rooms = [room for room in rooms if day['id'] in room['days'] and time['id'] in room['times']]
                random_room = random.choice(available_rooms) if available_rooms else None

                if random_room:
                    room_name = random_room['name']
                else:
                    room_name = "No room available"

                random_teacher = random.choice(teachers)
                subject = random.choice(random_teacher['subjects'])
                teacher_name = random_teacher['name']

                period = {
                    "day": day_name,
                    "time": time_info,
                    "subject": next((sub['name'] for sub in subjects if sub['id'] == subject), None),
                    "teacher": teacher_name,
                    "room": room_name
                }
                day_schedule['periods'].append(period)

            class_schedule.append(day_schedule)

        schedule.append({"id": class_info['id'], "name": class_info['name'], "schedule": class_schedule})

    return schedule