# data/training_data.py

SPLIT_TEMPLATES = {
    "фулбоди": {
        "зал": [
            {
                "day_name": "Фулбоди 1",
                "exercises": [
                    {"exercise": "Приседания со штангой", "sets": 3, "reps_range": (8, 12)},
                    {"exercise": "Жим штанги лёжа", "sets": 3, "reps_range": (8, 12)},
                    {"exercise": "Тяга штанги в наклоне", "sets": 3, "reps_range": (8, 12)},
                    {"exercise": "Жим гантелей сидя", "sets": 3, "reps_range": (10, 15)},
                    {"exercise": "Подъём штанги на бицепс", "sets": 3, "reps_range": (10, 15)},
                    {"exercise": "Скручивания", "sets": 3, "reps_range": (15, 20)}
                ]
            },
            {
                "day_name": "Фулбоди 2",
                "exercises": [
                    {"exercise": "Мёртвая тяга", "sets": 3, "reps_range": (8, 12)},
                    {"exercise": "Жим гантелей на наклонной", "sets": 3, "reps_range": (10, 12)},
                    {"exercise": "Тяга вертикального блока", "sets": 3, "reps_range": (10, 15)},
                    {"exercise": "Выпады с гантелями", "sets": 3, "reps_range": (10, 12)},
                    {"exercise": "Разгибания рук на блоке", "sets": 3, "reps_range": (12, 15)},
                    {"exercise": "Планка", "sets": 3, "reps_range": (30, 60), "unit": "сек"}
                ]
            }
        ],
        "дома": [
            {
                "day_name": "Фулбоди 1 (дома)",
                "exercises": [
                    {"exercise": "Приседания", "sets": 3, "reps_range": (15, 20)},
                    {"exercise": "Отжимания", "sets": 3, "reps_range": (10, 15)},
                    {"exercise": "Обратные отжимания от стула", "sets": 3, "reps_range": (12, 15)},
                    {"exercise": "Выпады", "sets": 3, "reps_range": (12, 15)},
                    {"exercise": "Берпи", "sets": 3, "reps_range": (8, 10)},
                    {"exercise": "Скручивания", "sets": 3, "reps_range": (20, 25)}
                ]
            },
            {
                "day_name": "Фулбоди 2 (дома)",
                "exercises": [
                    {"exercise": "Ягодичный мостик", "sets": 3, "reps_range": (15, 20)},
                    {"exercise": "Алмазные отжимания", "sets": 3, "reps_range": (8, 12)},
                    {"exercise": "Тяга рюкзака в наклоне", "sets": 3, "reps_range": (12, 15)},
                    {"exercise": "Болгарские выпады", "sets": 3, "reps_range": (10, 12)},
                    {"exercise": "Супермен", "sets": 3, "reps_range": (12, 15)},
                    {"exercise": "Планка боковая", "sets": 3, "reps_range": (20, 40), "unit": "сек"}
                ]
            }
        ]
    },
    "верх/низ": {
        "зал": [
            {
                "day_name": "Верх (зал)",
                "exercises": [
                    {"exercise": "Жим штанги лёжа", "sets": 4, "reps_range": (8, 10)},
                    {"exercise": "Тяга штанги в наклоне", "sets": 4, "reps_range": (8, 10)},
                    {"exercise": "Армейский жим стоя", "sets": 3, "reps_range": (10, 12)},
                    {"exercise": "Подтягивания (или тяга блока)", "sets": 3, "reps_range": (8, 10)},
                    {"exercise": "Подъём штанги на бицепс", "sets": 3, "reps_range": (10, 12)},
                    {"exercise": "Французский жим", "sets": 3, "reps_range": (10, 12)}
                ]
            },
            {
                "day_name": "Низ (зал)",
                "exercises": [
                    {"exercise": "Приседания со штангой", "sets": 4, "reps_range": (8, 10)},
                    {"exercise": "Румынская тяга", "sets": 4, "reps_range": (8, 10)},
                    {"exercise": "Жим ногами", "sets": 3, "reps_range": (10, 12)},
                    {"exercise": "Сгибания ног в тренажёре", "sets": 3, "reps_range": (12, 15)},
                    {"exercise": "Подъёмы на носки стоя", "sets": 4, "reps_range": (15, 20)}
                ]
            }
        ],
        "дома": [
            {
                "day_name": "Верх (дома)",
                "exercises": [
                    {"exercise": "Отжимания широким хватом", "sets": 4, "reps_range": (12, 15)},
                    {"exercise": "Тяга рюкзака в наклоне", "sets": 4, "reps_range": (12, 15)},
                    {"exercise": "Жим гантелей стоя", "sets": 3, "reps_range": (10, 12)},
                    {"exercise": "Подтягивания (или резина)", "sets": 3, "reps_range": (6, 10)},
                    {"exercise": "Отжимания на брусьях (стулья)", "sets": 3, "reps_range": (10, 12)}
                ]
            },
            {
                "day_name": "Низ (дома)",
                "exercises": [
                    {"exercise": "Приседания с рюкзаком", "sets": 4, "reps_range": (12, 15)},
                    {"exercise": "Ягодичный мостик с весом", "sets": 4, "reps_range": (12, 15)},
                    {"exercise": "Выпады вперёд", "sets": 3, "reps_range": (10, 12)},
                    {"exercise": "Мёртвая тяга с рюкзаком", "sets": 3, "reps_range": (12, 15)},
                    {"exercise": "Подъёмы на носки", "sets": 4, "reps_range": (20, 25)}
                ]
            }
        ]
    },
    "трёхдневный сплит": {
        "зал": [
            {
                "day_name": "День 1: Грудь + трицепс",
                "exercises": [
                    {"exercise": "Жим штанги лёжа", "sets": 4, "reps_range": (8, 10)},
                    {"exercise": "Жим гантелей на наклонной", "sets": 3, "reps_range": (10, 12)},
                    {"exercise": "Разведения гантелей", "sets": 3, "reps_range": (12, 15)},
                    {"exercise": "Французский жим", "sets": 3, "reps_range": (10, 12)},
                    {"exercise": "Разгибания рук на блоке", "sets": 3, "reps_range": (12, 15)}
                ]
            },
            {
                "day_name": "День 2: Спина + бицепс",
                "exercises": [
                    {"exercise": "Становая тяга", "sets": 4, "reps_range": (6, 8)},
                    {"exercise": "Тяга штанги в наклоне", "sets": 4, "reps_range": (8, 10)},
                    {"exercise": "Тяга верхнего блока", "sets": 3, "reps_range": (10, 12)},
                    {"exercise": "Подъём штанги на бицепс", "sets": 3, "reps_range": (10, 12)},
                    {"exercise": "Молотки с гантелями", "sets": 3, "reps_range": (12, 15)}
                ]
            },
            {
                "day_name": "День 3: Ноги + плечи",
                "exercises": [
                    {"exercise": "Приседания со штангой", "sets": 4, "reps_range": (8, 10)},
                    {"exercise": "Жим ногами", "sets": 3, "reps_range": (10, 12)},
                    {"exercise": "Армейский жим стоя", "sets": 4, "reps_range": (8, 10)},
                    {"exercise": "Махи гантелями в стороны", "sets": 3, "reps_range": (12, 15)},
                    {"exercise": "Подъёмы на носки", "sets": 4, "reps_range": (15, 20)}
                ]
            }
        ],
        "дома": [
            {
                "day_name": "День 1: Грудь + трицепс (дома)",
                "exercises": [
                    {"exercise": "Отжимания широким хватом", "sets": 4, "reps_range": (12, 15)},
                    {"exercise": "Алмазные отжимания", "sets": 3, "reps_range": (8, 12)},
                    {"exercise": "Обратные отжимания от стула", "sets": 3, "reps_range": (12, 15)},
                    {"exercise": "Французский жим с бутылками", "sets": 3, "reps_range": (12, 15)}
                ]
            },
            {
                "day_name": "День 2: Спина + бицепс (дома)",
                "exercises": [
                    {"exercise": "Тяга рюкзака в наклоне", "sets": 4, "reps_range": (12, 15)},
                    {"exercise": "Подтягивания (или тяга резины)", "sets": 3, "reps_range": (6, 10)},
                    {"exercise": "Подъём рюкзака на бицепс", "sets": 3, "reps_range": (12, 15)},
                    {"exercise": "Концентрированные сгибания", "sets": 3, "reps_range": (12, 15)}
                ]
            },
            {
                "day_name": "День 3: Ноги + плечи (дома)",
                "exercises": [
                    {"exercise": "Приседания с рюкзаком", "sets": 4, "reps_range": (12, 15)},
                    {"exercise": "Выпады назад", "sets": 3, "reps_range": (10, 12)},
                    {"exercise": "Жим гантелей стоя", "sets": 4, "reps_range": (10, 12)},
                    {"exercise": "Махи гантелями в стороны", "sets": 3, "reps_range": (12, 15)},
                    {"exercise": "Подъёмы на носки", "sets": 4, "reps_range": (20, 25)}
                ]
            }
        ]
    }
}

GOAL_MODIFIERS = {
    "похудение": {"sets_add": 0, "reps_shift": +3, "cardio": "20-30 мин интервального кардио после тренировки"},
    "набор массы": {"sets_add": 1, "reps_shift": -2, "cardio": "минимум кардио, только разминка"},
    "рельеф": {"sets_add": 0, "reps_shift": +4, "cardio": "20 мин низкоинтенсивного кардио"},
    "поддержка формы": {"sets_add": 0, "reps_shift": 0, "cardio": "по желанию 15-20 мин"}
}