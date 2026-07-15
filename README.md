<![CDATA[<div align="center">

```
 ╔══════════════════════════════════════════════════════╗
 ║                                                      ║
 ║    ███╗   ███╗██╗   ██╗██╗   ██╗███╗   ██╗           ║
 ║    ████╗ ████║╚██╗ ██╔╝██║   ██║████╗  ██║           ║
 ║    ██╔████╔██║ ╚████╔╝ ██║   ██║██╔██╗ ██║           ║
 ║    ██║╚██╔╝██║  ╚██╔╝  ╚██╗ ██╔╝██║╚██╗██║           ║
 ║    ██║ ╚═╝ ██║   ██║    ╚████╔╝ ██║ ╚████║           ║
 ║    ╚═╝     ╚═╝   ╚═╝     ╚═══╝  ╚═╝  ╚═══╝           ║
 ║                                                      ║
 ║       No-Code Visual Novel Constructor               ║
 ║       for Yandex Games Platform                      ║
 ╚══════════════════════════════════════════════════════╝
```

**No-Code GUI-Конструктор Визуальных Новелл для Яндекс Игр**

![Version](https://img.shields.io/badge/version-1.0.0-blue?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)
![Platform](https://img.shields.io/badge/platform-Yandex%20Games-yellow?style=flat-square)
![Python](https://img.shields.io/badge/python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![PySide6](https://img.shields.io/badge/GUI-PySide6-41CD52?style=flat-square&logo=qt&logoColor=white)
![JS](https://img.shields.io/badge/engine-Vanilla%20JS-F7DF1E?style=flat-square&logo=javascript&logoColor=black)

</div>

---

Визуальный десктопный редактор на **Python (PySide6)**, позволяющий собирать интерактивные новеллы с диалогами, выборами, персонажами и музыкой — **без навыков программирования**.

На выходе генерируется лёгкая сборка игры на чистом **JavaScript (Vanilla JS)**, адаптированная для мобильных телефонов и ПК, готовая к публикации на **Яндекс Игры**.

> *A no-code desktop editor (Python / PySide6) for building interactive visual novels with dialogue, branching choices, character sprites, and audio. Exports a lightweight Vanilla JS game optimized for mobile & desktop, ready to publish on Yandex Games.*

---

## 📑 Содержание / Table of Contents

- [✨ Возможности / Features](#-возможности--features)
- [🚀 Быстрый старт / Quick Start](#-быстрый-старт--quick-start)
- [📁 Структура проекта / Project Structure](#-структура-проекта--project-structure)
- [🎭 Библиотека персонажей / Characters Library](#-библиотека-персонажей--characters-library)
- [🖼️ Библиотека фонов / Backgrounds Library](#️-библиотека-фонов--backgrounds-library)
- [🎵 Аудио: BGM и SFX / Audio](#-аудио-bgm-и-sfx--audio)
- [🎬 Переходы между сценами / Scene Transitions](#-переходы-между-сценами--scene-transitions)
- [✍️ Инлайн-форматирование текста / Inline Formatting](#️-инлайн-форматирование-текста--inline-formatting)
- [💭 Мысли персонажей / Thoughts](#-мысли-персонажей--thoughts)
- [🎨 GUI-профили / GUI Profiles](#-gui-профили--gui-profiles)
- [⌨️ Горячие клавиши / Keyboard Shortcuts](#-горячие-клавиши--keyboard-shortcuts)
- [🖥️ Эффект печатной машинки / Typewriter Effect](#️-эффект-печатной-машинки--typewriter-effect)
- [💰 Монетизация / Monetization](#-монетизация--monetization)
- [📦 Формат экспорта / Export Format](#-формат-экспорта--export-format)
- [🖼️ Скриншоты / Screenshots](#️-скриншоты--screenshots)
- [📄 Лицензия / License](#-лицензия--лицензия)

---

## ✨ Возможности / Features

| Категория | Описание |
|---|---|
| **Сцены и диалоги** | Создание, удаление, переименование сцен. Настройка фона (изображение или цвет). Список реплик со спикером, текстом, спрайтом и позицией. Перетаскивание реплик вверх/вниз. |
| **Ветвление сюжета** | Кнопки выбора с переходом на другие сцены. Автоматический переход (`jump`) по окончании диалога. |
| **Персонажи** | Встроенная библиотека персонажей с именами, цветами и набором спрайтов (эмоциями). |
| **Фоны** | Библиотека фонов — изображения или сплошные цвета, с привязкой к сценам. |
| **Аудио** | Фоновая музыка (BGM) с зацикливанием и командой остановки. Звуковые эффекты (SFX) на каждый шаг реплики. Ползунок громкости в HUD. |
| **Переходы** | `fade`, `slide`, `zoom` — анимированные переходы фона между сценами. |
| **Форматирование** | Инлайн-теги: жирный `/b/`, курсив `/i/`, подчёркивание `/u/`, цвет `/color=.../`, зачёркивание `/s/`. |
| **Мысли** | Специальный режим реплики — курсивный текст в скобках, без имени спикера. |
| **GUI-профили** | Полная кастомизация панелей, шрифтов, цветов, размеров через CSS-переменные. |
| **Печатная машинка** | Посимвольный вывод текста с настраиваемой скоростью. |
| **Монетизация** | Полноэкранная реклама Яндекс с настраиваемым интервалом. In-App покупка для отключения рекламы. Mock SDK для локального тестирования. |
| **Адаптивность** | Автомасштабирование под любой экран (1280×720 base → `transform: scale`). |

---

## 🚀 Быстрый старт / Quick Start

### Предварительные требования / Prerequisites

- **Python 3.10+**
- **PySide6** (`pip install PySide6`)

### Установка и запуск / Installation

```bash
# 1. Клонируйте или скачайте проект
git clone <repository-url>
cd myvn

# 2. Создайте виртуальное окружение
python -m venv .venv

# 3. Активируйте окружение
# Windows:
.venv\Scripts\activate
# macOS/Linux:
# source .venv/bin/activate

# 4. Установите зависимости
pip install PySide6

# 5. Запустите редактор
python editor.py
```

### Ваши первые шаги / First Steps

1. 🎬 Создайте сцену и задайте ей фон
2. 🎭 Добавьте персонажа в библиотеку (имя, цвет, спрайты)
3. 💬 Добавьте реплики с текстом и выбранным персонажем
4. 🔀 Настройте выборы или автопереход на следующую сцену
5. 🎵 Добавьте фоновую музыку и звуковые эффекты
6. 📦 Нажмите **«Экспорт в HTML5»** — получите готовый ZIP

---

## 📁 Структура проекта / Project Structure

```
myvn/
├── editor.py            # 🖥️  Главный GUI-редактор (PySide6)
├── exporter.py          # 📦  Модуль экспорта в HTML5 / ZIP
├── README.md            # 📖  Документация
├── .gitignore
│
├── templates/           # 🎮  Шаблоны движка (копируются при экспорте)
│   ├── index.html       #     Основная HTML-страница
│   ├── style.css        #     Адаптивные стили (glassmorphism)
│   ├── game.js          #     Движок воспроизведения новеллы
│   ├── yandex_sdk.js    #     Обёртка Яндекс SDK + Mock SDK
│   └── story.js         #     Шаблон данных истории (JSON)
│
├── export/              # 📂  Папка с результатом экспорта
│   ├── index.html
│   ├── style.css
│   ├── game.js
│   ├── yandex_sdk.js
│   ├── story.js
│   └── assets/          #     Фоны и спрайты
│
└── игра.json            # 💾  Файл-проект редактора
```

---

## 🎭 Библиотека персонажей / Characters Library

Каждый персонаж имеет:

| Поле | Описание |
|---|---|
| `name` | Отображаемое имя в диалоговом окне |
| `color` | Цвет имени (HEX), например `#ff007f` |
| `sprites` | Словарь спрайтов (эмоций): `{ "Улыбка": "path.png", "Грусть": "path2.png" }` |

Спрайты отображаются в трёх слотах: **left** (25%), **center** (50%), **right** (75%) — или по произвольным координатам `[x%, y%]`.

---

## 🖼️ Библиотека фонов / Backgrounds Library

Фоны задаются для каждой сцены двумя способами:

- **Изображение** — путь к файлу или URL (`assets/bg_forest.jpg`)
- **Сплошной цвет** — HEX, RGB или RGBA (`#2c3e50`, `rgba(0,0,0,0.8)`)

Фоны из библиотеки переиспользуются между сценами по имени.

---

## 🎵 Аудио: BGM и SFX / Audio

| Тип | Описание | Где задаётся |
|---|---|---|
| **BGM** (фоновая музыка) | Зацикливается автоматически. Значение `"stop"` останавливает воспроизведение. | В настройках сцены |
| **SFX** (звуковой эффект) | Воспроизводится одноразово при показе конкретной реплики. | В настройках реплики |

Ползунок громкости 🔊 в HUD позволяет регулировать уровень звука в реальном времени.

---

## 🎬 Переходы между сценами / Scene Transitions

| Переход | CSS-класс | Описание |
|---|---|---|
| `fade` | `transition-fade-out` | Плавное затухание фона |
| `slide` | `transition-slide-out` | Сдвиг фона влево с затуханием |
| `zoom` | `transition-zoom-out` | Увеличение с затуханием |
| `none` | — | Мгновенная смена |

---

## ✍️ Инлайн-форматирование текста / Inline Formatting

Используйте слеш-теги прямо в тексте реплик для стилизации:

| Тег | Синтаксис | Результат | HTML |
|---|---|---|---|
| **Жирный** | `/b/текст/b/` | **текст** | `<b>текст</b>` |
| **Курсив** | `/i/текст/i/` | *текст* | `<i>текст</i>` |
| **Подчёркивание** | `/u/текст/u/` | <u>текст</u> | `<u>текст</u>` |
| **Цвет** | `/color=#ff0000/текст/color/` | <span style="color:#ff0000">текст</span> | `<span style="color:#ff0000">текст</span>` |
| **Зачёркивание** | `/s/текст/s/` | ~~текст~~ | `<s>текст</s>` |

### Пример / Example

```
Привет! Это /b/важное/b/ сообщение с /color=#00ffff/бирюзовым/color/ акцентом.
```

Результат: Привет! Это **важное** сообщение с <span style="color:#00ffff">бирюзовым</span> акцентом.

---

## 💭 Мысли персонажей / Thoughts

Если реплика помечена как «мысль» (`is_thought: true`):

- Имя спикера скрывается
- Текст выводится *курсивом* в скобках: *(Текст мысли…)*
- Идеально для внутреннего монолога главного героя

---

## 🎨 GUI-профили / GUI Profiles

Полная кастомизация интерфейса через CSS-переменные:

| Переменная | Назначение | По умолчанию |
|---|---|---|
| `--panel-bg` | Фон панели диалога | `rgba(18, 18, 24, 0.75)` |
| `--panel-border` | Цвет рамки панели | `rgba(255, 255, 255, 0.1)` |
| `--panel-radius` | Скругление углов | `12px` |
| `--dialogue-height` | Высота панели диалога | `180px` |
| `--text-color` | Цвет текста диалога | `#f3f3f7` |
| `--text-size` | Размер текста диалога | `18px` |
| `--name-color` | Цвет имени спикера | `#ffcc00` |
| `--name-size` | Размер имени спикера | `20px` |
| `--name-bold` | Жирность имени | `bold` |
| `--choice-bg` | Фон кнопок выбора | `rgba(18, 18, 24, 0.9)` |
| `--choice-hover-bg` | Фон кнопки при наведении | `#1e1e24` |
| `--choice-border-color` | Цвет рамки кнопки выбора | `rgba(255, 255, 255, 0.15)` |
| `--choice-text-color` | Цвет текста выбора | `#f3f3f7` |
| `--choice-size` | Размер текста выбора | `16px` |
| `--font-family` | Семейство шрифтов | `system-ui, …` |

---

## ⌨️ Горячие клавиши / Keyboard Shortcuts

| Клавиша | Действие |
|---|---|
| `Space` / `Enter` | Следующая реплика / продвинуть диалог |
| `Escape` | Вернуться в меню |

---

## 🖥️ Эффект печатной машинки / Typewriter Effect

Текст диалога выводится посимвольно с настраиваемой скоростью, создавая эффект «печатной машинки». Нажмите на панель диалога во время анимации, чтобы мгновенно показать весь текст.

---

## 💰 Монетизация / Monetization

### Полноэкранная реклама (Interstitial)

- Автоматический вызов с настраиваемым интервалом (по умолчанию 3 минуты)
- Показывается на переходах между сценами и при выборе
- Игра ставится на паузу, звук приглушается на время показа

### In-App покупки

- Нерасходуемая покупка «Отключение рекламы»
- Кнопка появляется в меню и HUD при указании ID покупки
- Статус проверяется автоматически при запуске через SDK

### Mock SDK (локальное тестирование)

Если Яндекс SDK недоступен (открытие локально), движок автоматически переключается в режим симуляции с интерактивным окном рекламы и диалогом покупки.

---

## 📦 Формат экспорта / Export Format

При нажатии **«Экспорт в HTML5»** создаётся:

| Файл / Папка | Описание |
|---|---|
| `index.html` | Основная страница с SEO-тегами, прелоадером и HUD |
| `style.css` | Адаптивные стили с glassmorphism-эффектами |
| `game.js` | Движок воспроизведения новеллы |
| `yandex_sdk.js` | Обёртка Яндекс SDK с Mock-режимом |
| `story.js` | Сгенерированные данные вашей истории (JSON) |
| `assets/` | Фоны и спрайты с относительными путями |
| `{Имя}_yandex.zip` | Готовый архив для загрузки в консоль Яндекс Игр |

### Настройка в консоли Яндекс Игр

1. Зарегистрируйтесь в [консоли разработчика](https://games.yandex.ru/dev)
2. Загрузите полученный ZIP-архив
3. Создайте нерасходуемую покупку (вкладка **Покупки**) с ID, совпадающим с настройками редактора
4. Отправьте игру на модерацию

---

## 🖼️ Скриншоты / Screenshots

> 📸 *Скриншоты будут добавлены в ближайшее время.*

<!-- Placeholder for screenshots:
![Editor](screenshots/editor.png)
![Game](screenshots/game.png)
![Menu](screenshots/menu.png)
-->

---

## 📄 Лицензия / License

Этот проект распространяется под лицензией **MIT License**.

```
MIT License

Copyright (c) 2026 myvn contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

<div align="center">

**Made with ❤️ for visual novel creators**

*Создано с ❤️ для создателей визуальных новелл*

</div>
]]>
