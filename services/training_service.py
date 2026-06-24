# services/training_service.py
import copy
from data.training_data import SPLIT_TEMPLATES, GOAL_MODIFIERS

def get_program(goal, place, split, week=None):
    split_data = SPLIT_TEMPLATES.get(split, {}).get(place)
    if not split_data:
        return {"error": "Программа не найдена"}
    modifier = GOAL_MODIFIERS.get(goal, GOAL_MODIFIERS["поддержка формы"])

    base_days = copy.deepcopy(split_data)

    for day in base_days:
        for i, ex in enumerate(day["exercises"]):
            ex["sets"] = max(2, ex["sets"] + modifier["sets_add"])
            low, high = ex["reps_range"]
            new_low = max(4, low + modifier["reps_shift"])
            new_high = max(6, high + modifier["reps_shift"])
            if "unit" in ex and ex["unit"] == "сек":
                ex["reps"] = f"{new_low}-{new_high} {ex['unit']}"
            else:
                ex["reps"] = f"{new_low}-{new_high}"
            del ex["reps_range"]
            if i == len(day["exercises"]) - 1 and modifier["cardio"]:
                ex["notes"] = modifier["cardio"]
            else:
                ex["notes"] = ex.get("notes", "")

    weeks = []
    for w in range(1, 5):
        week_days = copy.deepcopy(base_days)
        if w >= 3:
            for day in week_days:
                for ex in day["exercises"]:
                    ex["sets"] = min(5, ex["sets"] + 1)
        weeks.append({
            "week_number": w,
            "days": week_days
        })

    if week:
        return {"weeks": [weeks[week-1]]}
    return {"weeks": weeks}