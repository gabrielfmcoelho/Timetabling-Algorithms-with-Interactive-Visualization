from typing import List, Dict

def evaluate_solution(schedule: List[Dict]) -> int:
    conflicts = 0
    used_times = {}
    used_rooms = {}
    used_teachers = {}

    for class_info in schedule:
        for day_schedule in class_info['schedule']:
            for period in day_schedule['periods']:
                day = day_schedule['day']
                time = period.get('time')
                teacher = period.get('teacher')
                room = period.get('room')

                time_key = (day, time)
                room_key = (day, time, room)
                teacher_key = (day, time, teacher)

                # Conflito de horários
                if time_key in used_times:
                    conflicts += 1
                used_times[time_key] = True

                # Conflito de salas
                if room_key in used_rooms:
                    conflicts += 1
                used_rooms[room_key] = True

                # Conflito de professores
                if teacher_key in used_teachers:
                    conflicts += 1
                used_teachers[teacher_key] = True

    return conflicts