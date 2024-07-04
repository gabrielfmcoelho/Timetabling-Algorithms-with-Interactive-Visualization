from typing import List, Dict

def evaluate_solution(schedule: List[Dict]) -> int:
    conflicts = 0
    used_times = {}
    used_rooms = {}

    for class_info in schedule:
        for day_schedule in class_info['schedule']:
            for period in day_schedule['periods']:
                time_key = (day_schedule['day'], period.get('time'))
                room_key = (day_schedule['day'], period.get('time'), period.get('room'))

                # Conflito de horários
                if time_key in used_times:
                    conflicts += 1
                used_times[time_key] = True

                # Conflito de salas
                if room_key in used_rooms:
                    conflicts += 1
                used_rooms[room_key] = True
                
    return conflicts