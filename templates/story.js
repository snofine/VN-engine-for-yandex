// story.js - Contains the visual novel script data
window.storyData = {
    "config": {
        "title": "Демо Новелла",
        "start_scene": "scene_1",
        "ads_interval_minutes": 1,
        "inapp_remove_ads_id": "no_ads_30rub",
        "gui_profile": "Дефолтный",
        "characters": {
            "alisa": {
                "name": "Алиса",
                "color": "#ff007f",
                "sprites": {
                    "Улыбка": "https://img.icons8.com/color/344/anime-emoji.png"
                }
            }
        },
        "backgrounds": {
            "Город": "#2c3e50",
            "Лес": "#0b2611"
        }
    },
    "gui": {
        "panel_bg": "rgba(18, 18, 24, 0.75)",
        "panel_border": "rgba(255, 255, 255, 0.1)",
        "panel_radius": 12,
        "dialogue_height": 180,
        "text_color": "#f3f3f7",
        "text_size": 18,
        "name_color": "#ffcc00",
        "name_size": 20,
        "name_bold": true,
        "choice_bg": "rgba(18, 18, 24, 0.9)",
        "choice_hover_bg": "#1e1e24",
        "choice_border_color": "rgba(255, 255, 255, 0.15)",
        "choice_text_color": "#f3f3f7",
        "choice_size": 16,
        "font_family": "system-ui"
    },
    "scenes": {
        "scene_1": {
            "background": "#14141f",
            "dialogues": [
                {
                    "character_id": "",
                    "speaker": "Рассказчик",
                    "text": "Добро пожаловать в демонстрационную новеллу!",
                    "is_thought": false,
                    "text_bold": true,
                    "text_italic": false,
                    "sprite": {"position": "center", "image": ""}
                },
                {
                    "character_id": "alisa",
                    "speaker": "Алиса",
                    "text": "Привет! Я твой первый персонаж. И я могу общаться с тобой.",
                    "is_thought": false,
                    "text_bold": false,
                    "text_italic": false,
                    "sprite": {
                        "position": "center",
                        "image": "https://img.icons8.com/color/344/anime-emoji.png"
                    }
                },
                {
                    "character_id": "",
                    "speaker": "",
                    "text": "Хм... Она выглядит очень дружелюбно.",
                    "is_thought": true,
                    "text_bold": false,
                    "text_italic": true,
                    "sprite": {"position": "center", "image": ""}
                },
                {
                    "character_id": "alisa",
                    "speaker": "Алиса",
                    "text": "Давай проверим выбор сцен. Куда отправимся?",
                    "is_thought": false,
                    "text_bold": false,
                    "text_italic": false,
                    "sprite": {
                        "position": "center",
                        "image": "https://img.icons8.com/color/344/anime-emoji.png"
                    }
                }
            ],
            "choices": [
                {
                    "text": "Пойти в таинственный лес",
                    "next_scene": "scene_forest"
                },
                {
                    "text": "Остаться в городе",
                    "next_scene": "scene_city"
                }
            ]
        },
        "scene_forest": {
            "background": "#0b2611",
            "dialogues": [
                {
                    "character_id": "",
                    "speaker": "Рассказчик",
                    "text": "Лес встретил вас прохладой и загадочным шепотом листьев.",
                    "is_thought": false,
                    "text_bold": false,
                    "text_italic": false,
                    "sprite": {"position": "center", "image": ""}
                },
                {
                    "character_id": "alisa",
                    "speaker": "Алиса",
                    "text": "Ого! Тут темновато. Будь осторожен, реклама показывается раз в минуту на переходах!",
                    "is_thought": false,
                    "text_bold": false,
                    "text_italic": false,
                    "sprite": {
                        "position": "center",
                        "image": "https://img.icons8.com/color/344/anime-emoji.png"
                    }
                }
            ],
            "choices": [
                {
                    "text": "Вернуться в начало",
                    "next_scene": "scene_1"
                }
            ]
        },
        "scene_city": {
            "background": "#2c3e50",
            "dialogues": [
                {
                    "character_id": "",
                    "speaker": "Рассказчик",
                    "text": "Город сиял неоновыми огнями и шумел машинами.",
                    "is_thought": false,
                    "text_bold": false,
                    "text_italic": false,
                    "sprite": {"position": "center", "image": ""}
                },
                {
                    "character_id": "alisa",
                    "speaker": "Алиса",
                    "text": "Городская суета... Тут гораздо безопаснее леса. Вернемся?",
                    "is_thought": false,
                    "text_bold": false,
                    "text_italic": false,
                    "sprite": {
                        "position": "center",
                        "image": "https://img.icons8.com/color/344/anime-emoji.png"
                    }
                }
            ],
            "choices": [
                {
                    "text": "Вернуться в начало",
                    "next_scene": "scene_1"
                }
            ]
        }
    }
};
