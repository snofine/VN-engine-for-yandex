# editor.py - PySide6 GUI Creator/Editor for HTML5 Visual Novels (Yandex Games)
import sys
import os
import json
from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QListWidget, QListWidgetItem, QPushButton, QLabel, QLineEdit, QTextEdit,
    QComboBox, QSpinBox, QCheckBox, QFileDialog, QTabWidget, QGroupBox,
    QFormLayout, QMessageBox, QInputDialog, QToolBar, QStyle, QFrame, QColorDialog
)
from PySide6.QtGui import QIcon, QFont, QColor, QPalette

# Import exporter module
from exporter import export_project

# Modern Dark Theme Stylesheet
DARK_THEME_STYLE = """
QMainWindow {
    background-color: #0f0f14;
}
QWidget {
    color: #e0e0e9;
    font-family: "Segoe UI", system-ui, sans-serif;
    font-size: 13px;
}
QFrame#separator {
    background-color: #232331;
}
QTabWidget::panel {
    border: 1px solid #232331;
    background-color: #151522;
    border-radius: 8px;
}
QTabBar::tab {
    background-color: #101018;
    color: #a0a0b2;
    border: 1px solid #232331;
    border-bottom: none;
    padding: 10px 16px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
}
QTabBar::tab:selected {
    background-color: #151522;
    color: #ffcc00;
    border-bottom: 2px solid #ffcc00;
}
QTabBar::tab:hover {
    color: #ffffff;
}
QGroupBox {
    border: 1px solid #2d2d42;
    border-radius: 8px;
    margin-top: 12px;
    padding-top: 16px;
    font-weight: bold;
    color: #ffcc00;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 10px;
    padding: 0 5px;
}
QLineEdit, QTextEdit, QComboBox, QSpinBox {
    background-color: #1c1c2a;
    border: 1px solid #2d2d42;
    border-radius: 5px;
    padding: 6px 10px;
    color: #f0f0f5;
}
QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QSpinBox:focus {
    border: 1px solid #ffcc00;
}
QLineEdit:disabled, QTextEdit:disabled, QComboBox:disabled, QSpinBox:disabled {
    background-color: #12121b;
    border-color: #1d1d2b;
    color: #808090;
}
QPushButton {
    background-color: #2a2a3e;
    border: 1px solid #3c3c56;
    border-radius: 5px;
    padding: 8px 16px;
    font-weight: bold;
    color: #ffffff;
}
QPushButton:hover {
    background-color: #383854;
    border-color: #53537a;
}
QPushButton:disabled {
    background-color: #181825;
    border-color: #20202e;
    color: #606070;
}
QPushButton:pressed {
    background-color: #1f1f2e;
}
QPushButton#action-btn {
    background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #ffaa00, stop:1 #ffcc00);
    color: #000000;
    border: none;
}
QPushButton#action-btn:hover {
    background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #ffbb33, stop:1 #ffdd33);
}
QPushButton#danger-btn {
    background-color: #4a1c1c;
    border: 1px solid #7a2b2b;
}
QPushButton#danger-btn:hover {
    background-color: #612222;
}
QListWidget {
    background-color: #12121d;
    border: 1px solid #232331;
    border-radius: 6px;
    padding: 5px;
}
QListWidget::item {
    padding: 8px 12px;
    border-radius: 4px;
    margin-bottom: 2px;
}
QListWidget::item:hover {
    background-color: #1e1e2d;
}
QListWidget::item:selected {
    background-color: #2d2d44;
    color: #ffcc00;
    font-weight: bold;
}
QCheckBox {
    spacing: 8px;
}
QCheckBox::indicator {
    width: 18px;
    height: 18px;
}
QScrollBar:vertical {
    border: none;
    background: #101018;
    width: 10px;
    margin: 0px;
}
QScrollBar::handle:vertical:hover {
    background: #ffcc00;
}
"""

GUI_PRESETS = {
    "Дефолтный": {
        "panel_bg": "rgba(18, 18, 24, 0.75)",
        "panel_border": "rgba(255, 255, 255, 0.1)",
        "panel_radius": 12,
        "dialogue_height": 180,
        "text_color": "#f3f3f7",
        "text_size": 18,
        "name_color": "#ffcc00",
        "name_size": 20,
        "name_bold": True,
        "choice_bg": "rgba(18, 18, 24, 0.9)",
        "choice_hover_bg": "#1e1e24",
        "choice_border_color": "rgba(255, 255, 255, 0.15)",
        "choice_text_color": "#f3f3f7",
        "choice_size": 16,
        "font_family": "system-ui"
    },
    "Классический Ren'Py": {
        "panel_bg": "rgba(0, 0, 0, 0.7)",
        "panel_border": "rgba(255, 255, 255, 0.2)",
        "panel_radius": 0,
        "dialogue_height": 160,
        "text_color": "#ffffff",
        "text_size": 18,
        "name_color": "#ff8080",
        "name_size": 22,
        "name_bold": True,
        "choice_bg": "rgba(30, 30, 30, 0.9)",
        "choice_hover_bg": "#ff8080",
        "choice_border_color": "rgba(255, 255, 255, 0.3)",
        "choice_text_color": "#ffffff",
        "choice_size": 16,
        "font_family": "Georgia"
    },
    "Аниме Неон": {
        "panel_bg": "rgba(35, 10, 45, 0.8)",
        "panel_border": "#ff007f",
        "panel_radius": 15,
        "dialogue_height": 190,
        "text_color": "#ffffff",
        "text_size": 18,
        "name_color": "#00ffff",
        "name_size": 22,
        "name_bold": True,
        "choice_bg": "rgba(20, 5, 25, 0.95)",
        "choice_hover_bg": "#ff007f",
        "choice_border_color": "#00ffff",
        "choice_text_color": "#ffffff",
        "choice_size": 16,
        "font_family": "system-ui"
    },
    "Киберпанк": {
        "panel_bg": "rgba(240, 240, 0, 0.15)",
        "panel_border": "#f0f000",
        "panel_radius": 2,
        "dialogue_height": 170,
        "text_color": "#00ffff",
        "text_size": 18,
        "name_color": "#f0f000",
        "name_size": 20,
        "name_bold": True,
        "choice_bg": "rgba(0, 0, 0, 0.9)",
        "choice_hover_bg": "#f0f000",
        "choice_border_color": "#00ffff",
        "choice_text_color": "#00ffff",
        "choice_size": 16,
        "font_family": "Courier New"
    }
}

class VisualNovelEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("myvn - No-Code GUI Конструктор Визуальных Новелл (Яндекс Игры)")
        self.resize(1300, 950)
        self.setStyleSheet(DARK_THEME_STYLE)
        
        # State
        self.project_path = None
        self.project_data = {
            "config": {
                "title": "Новая Новелла",
                "start_scene": "",
                "ads_interval_minutes": 3,
                "inapp_remove_ads_id": "no_ads_30rub",
                "export_dir": "",
                "gui_profile": "Дефолтный",
                "characters": {},
                "backgrounds": {},
                "music": {},
                "sfx": {}
            },
            "gui": dict(GUI_PRESETS["Дефолтный"]),
            "scenes": {}
        }
        
        self.selected_scene_id = None
        self.selected_dialogue_idx = None
        self.selected_choice_idx = None
        
        self.selected_char_id = None
        self.selected_char_sprite_idx = None
        self.selected_bg_lib_name = None
        
        self.selected_music_lib_name = None
        self.selected_sfx_lib_name = None
        
        self.is_updating_ui = False # Guard to prevent update recursion
        
        self.init_ui()
        self.new_project() # Initialize with a clean project
        
    def init_ui(self):
        # 1. Menu bar & ToolBar
        toolbar = QToolBar("Панель инструментов")
        toolbar.setIconSize(QSize(20, 20))
        toolbar.setMovable(False)
        self.addToolBar(toolbar)
        
        new_act = toolbar.addAction("📄 Новый проект")
        new_act.triggered.connect(self.new_project)
        
        open_act = toolbar.addAction("📂 Открыть")
        open_act.triggered.connect(self.open_project)
        
        save_act = toolbar.addAction("💾 Сохранить")
        save_act.triggered.connect(self.save_project)
        
        toolbar.addSeparator()
        
        export_act = QPushButton("⚡ Экспорт в HTML5")
        export_act.setObjectName("action-btn")
        export_act.clicked.connect(self.export_html5)
        toolbar.addWidget(export_act)
        
        # 2. Main Layout Splitter
        main_splitter = QSplitter(Qt.Horizontal)
        self.setCentralWidget(main_splitter)
        
        # Left Panel: Scenes List
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(10, 10, 10, 10)
        
        scene_list_title = QLabel("Список Сцен:")
        scene_list_title.setFont(QFont("Segoe UI", 11, QFont.Bold))
        left_layout.addWidget(scene_list_title)
        
        self.scene_list = QListWidget()
        self.scene_list.currentRowChanged.connect(self.scene_selected)
        left_layout.addWidget(self.scene_list)
        
        scene_btns_layout = QHBoxLayout()
        add_scene_btn = QPushButton("➕ Добавить")
        add_scene_btn.clicked.connect(self.add_scene)
        scene_btns_layout.addWidget(add_scene_btn)
        
        del_scene_btn = QPushButton("❌ Удалить")
        del_scene_btn.setObjectName("danger-btn")
        del_scene_btn.clicked.connect(self.delete_scene)
        scene_btns_layout.addWidget(del_scene_btn)
        left_layout.addLayout(scene_btns_layout)
        
        set_start_btn = QPushButton("⭐ Сделать Стартовой")
        set_start_btn.clicked.connect(self.set_start_scene)
        left_layout.addWidget(set_start_btn)
        
        main_splitter.addWidget(left_panel)
        
        # Right Panel: Tabs
        right_tab_widget = QTabWidget()
        main_splitter.addWidget(right_tab_widget)
        
        # TAB 1: SCENE EDITOR
        scene_editor_tab = QWidget()
        scene_editor_layout = QVBoxLayout(scene_editor_tab)
        
        # Scene properties (Background, Transition, Music)
        scene_props_group = QGroupBox("Свойства сцены (фон, эффекты и BGM)")
        scene_props_layout = QHBoxLayout(scene_props_group)
        
        # 1. Bg selector
        bg_select_layout = QVBoxLayout()
        bg_select_layout.addWidget(QLabel("<b>Задний фон сцены:</b>"))
        self.scene_bg_combo = QComboBox()
        self.scene_bg_combo.currentIndexChanged.connect(self.scene_bg_combo_changed)
        bg_select_layout.addWidget(self.scene_bg_combo)
        
        self.bg_input = QLineEdit()
        self.bg_input.setPlaceholderText("Цвет или файл...")
        self.bg_input.textChanged.connect(self.update_scene_bg)
        bg_select_layout.addWidget(self.bg_input)
        
        self.bg_browse_btn = QPushButton("Выбрать файл")
        self.bg_browse_btn.clicked.connect(self.browse_bg_image)
        bg_select_layout.addWidget(self.bg_browse_btn)
        scene_props_layout.addLayout(bg_select_layout)
        
        # 2. Transition selector
        trans_select_layout = QVBoxLayout()
        trans_select_layout.addWidget(QLabel("<b>Эффект появления:</b>"))
        self.scene_trans_combo = QComboBox()
        self.scene_trans_combo.addItem("Без эффекта", "none")
        self.scene_trans_combo.addItem("Затухание (Fade)", "fade")
        self.scene_trans_combo.addItem("Сдвиг (Slide)", "slide")
        self.scene_trans_combo.addItem("Масштаб (Zoom)", "zoom")
        self.scene_trans_combo.currentIndexChanged.connect(self.update_scene_transition)
        trans_select_layout.addWidget(self.scene_trans_combo)
        trans_select_layout.addStretch()
        scene_props_layout.addLayout(trans_select_layout)
        
        # 3. BGM selector
        bgm_select_layout = QVBoxLayout()
        bgm_select_layout.addWidget(QLabel("<b>Музыка (BGM):</b>"))
        self.scene_bgm_combo = QComboBox()
        self.scene_bgm_combo.currentIndexChanged.connect(self.scene_bgm_combo_changed)
        bgm_select_layout.addWidget(self.scene_bgm_combo)
        
        self.scene_bgm_input = QLineEdit()
        self.scene_bgm_input.setPlaceholderText("Путь к файлу BGM...")
        self.scene_bgm_input.textChanged.connect(self.update_scene_bgm)
        bgm_select_layout.addWidget(self.scene_bgm_input)
        
        self.scene_bgm_browse_btn = QPushButton("Обзор музыки")
        self.scene_bgm_browse_btn.clicked.connect(self.browse_scene_bgm)
        bgm_select_layout.addWidget(self.scene_bgm_browse_btn)
        scene_props_layout.addLayout(bgm_select_layout)
        
        scene_editor_layout.addWidget(scene_props_group)
        
        # Dialogue steps splitter
        scene_splitter = QSplitter(Qt.Vertical)
        scene_editor_layout.addWidget(scene_splitter)
        
        # Top half: Dialogue List
        diag_list_widget = QWidget()
        diag_list_layout = QVBoxLayout(diag_list_widget)
        diag_list_layout.setContentsMargins(0, 5, 0, 5)
        
        diag_title_layout = QHBoxLayout()
        diag_title_layout.addWidget(QLabel("<b>Шаги диалога в сцене:</b>"))
        
        move_up_btn = QPushButton("▲")
        move_up_btn.setToolTip("Переместить шаг вверх")
        move_up_btn.clicked.connect(self.move_dialogue_up)
        diag_title_layout.addWidget(move_up_btn)
        
        move_down_btn = QPushButton("▼")
        move_down_btn.setToolTip("Переместить шаг вниз")
        move_down_btn.clicked.connect(self.move_dialogue_down)
        diag_title_layout.addWidget(move_down_btn)
        diag_list_layout.addLayout(diag_title_layout)
        
        self.dialogue_list = QListWidget()
        self.dialogue_list.currentRowChanged.connect(self.dialogue_selected)
        diag_list_layout.addWidget(self.dialogue_list)
        
        diag_btns_layout = QHBoxLayout()
        add_diag_btn = QPushButton("➕ Добавить реплику")
        add_diag_btn.clicked.connect(self.add_dialogue)
        diag_btns_layout.addWidget(add_diag_btn)
        
        del_diag_btn = QPushButton("❌ Удалить реплику")
        del_diag_btn.setObjectName("danger-btn")
        del_diag_btn.clicked.connect(self.delete_dialogue)
        diag_btns_layout.addWidget(del_diag_btn)
        diag_list_layout.addLayout(diag_btns_layout)
        
        scene_splitter.addWidget(diag_list_widget)
        
        # Bottom half: Dialogue details + Choices Editor
        details_splitter = QSplitter(Qt.Horizontal)
        scene_splitter.addWidget(details_splitter)
        
        # Dialogue detail panel
        diag_detail_panel = QGroupBox("Редактор реплики")
        diag_detail_layout = QFormLayout(diag_detail_panel)
        
        # thoughts / formatting
        format_layout = QHBoxLayout()
        self.diag_is_thought = QCheckBox("💭 Мысли")
        self.diag_is_thought.stateChanged.connect(self.diag_is_thought_changed)
        format_layout.addWidget(self.diag_is_thought)
        
        self.diag_text_bold = QCheckBox("<b>Ж</b>")
        self.diag_text_bold.stateChanged.connect(self.save_current_dialogue_fields)
        format_layout.addWidget(self.diag_text_bold)
        
        self.diag_text_italic = QCheckBox("<i>К</i>")
        self.diag_text_italic.stateChanged.connect(self.save_current_dialogue_fields)
        format_layout.addWidget(self.diag_text_italic)
        diag_detail_layout.addRow("Формат реплики:", format_layout)
        
        # Character picker combo
        self.diag_char_combo = QComboBox()
        self.diag_char_combo.currentIndexChanged.connect(self.diag_char_combo_changed)
        diag_detail_layout.addRow("Персонаж:", self.diag_char_combo)
        
        self.speaker_input = QLineEdit()
        self.speaker_input.setPlaceholderText("Имя говорящего персонажа")
        self.speaker_input.textChanged.connect(self.save_current_dialogue_fields)
        diag_detail_layout.addRow("Имя спикера:", self.speaker_input)
        
        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText("Текст, который отобразится на экране...")
        self.text_input.textChanged.connect(self.save_current_dialogue_fields)
        diag_detail_layout.addRow("Текст реплики:", self.text_input)
        
        # Dialogue Sound Effect (SFX)
        self.diag_sfx_combo = QComboBox()
        self.diag_sfx_combo.currentIndexChanged.connect(self.diag_sfx_combo_changed)
        diag_detail_layout.addRow("Звуковой эффект:", self.diag_sfx_combo)
        
        self.sfx_raw_widget = QWidget()
        sfx_raw_layout = QHBoxLayout(self.sfx_raw_widget)
        sfx_raw_layout.setContentsMargins(0, 0, 0, 0)
        self.diag_sfx_input = QLineEdit()
        self.diag_sfx_input.setPlaceholderText("Файл звука...")
        self.diag_sfx_input.textChanged.connect(self.save_current_dialogue_fields)
        sfx_raw_layout.addWidget(self.diag_sfx_input)
        sfx_browse_btn = QPushButton("Обзор")
        sfx_browse_btn.clicked.connect(self.browse_dialogue_sfx)
        sfx_raw_layout.addWidget(sfx_browse_btn)
        diag_detail_layout.addRow("Файл SFX:", self.sfx_raw_widget)
        
        # Sprite picker combo (Expressions list)
        self.diag_sprite_expr_combo = QComboBox()
        self.diag_sprite_expr_combo.currentIndexChanged.connect(self.diag_sprite_expr_changed)
        diag_detail_layout.addRow("Эмоция спрайта:", self.diag_sprite_expr_combo)
        
        # Raw Sprite path input
        self.sprite_raw_widget = QWidget()
        sprite_raw_layout = QHBoxLayout(self.sprite_raw_widget)
        sprite_raw_layout.setContentsMargins(0, 0, 0, 0)
        self.sprite_input = QLineEdit()
        self.sprite_input.setPlaceholderText("Путь к файлу...")
        self.sprite_input.textChanged.connect(self.save_current_dialogue_fields)
        sprite_raw_layout.addWidget(self.sprite_input)
        sprite_browse = QPushButton("Обзор")
        sprite_browse.clicked.connect(self.browse_sprite_image)
        sprite_raw_layout.addWidget(sprite_browse)
        diag_detail_layout.addRow("Файл спрайта:", self.sprite_raw_widget)
        
        self.sprite_pos_type = QComboBox()
        self.sprite_pos_type.addItems(["Предустановка", "Координаты X, Y (%)"])
        self.sprite_pos_type.currentIndexChanged.connect(self.sprite_pos_type_changed)
        diag_detail_layout.addRow("Тип позиции:", self.sprite_pos_type)

        self.sprite_pos_combo = QComboBox()
        self.sprite_pos_combo.addItems(["center", "left", "right"])
        self.sprite_pos_combo.currentIndexChanged.connect(self.save_current_dialogue_fields)
        diag_detail_layout.addRow("Предустановка:", self.sprite_pos_combo)

        self.sprite_x_coord = QSpinBox()
        self.sprite_x_coord.setRange(0, 100)
        self.sprite_x_coord.setValue(50)
        self.sprite_x_coord.setSuffix(" %")
        self.sprite_x_coord.valueChanged.connect(self.save_current_dialogue_fields)
        diag_detail_layout.addRow("Координата X:", self.sprite_x_coord)
        self.sprite_x_coord.hide()

        self.sprite_y_coord = QSpinBox()
        self.sprite_y_coord.setRange(-100, 100)
        self.sprite_y_coord.setValue(0)
        self.sprite_y_coord.setSuffix(" %")
        self.sprite_y_coord.valueChanged.connect(self.save_current_dialogue_fields)
        diag_detail_layout.addRow("Координата Y:", self.sprite_y_coord)
        self.sprite_y_coord.hide()
        
        details_splitter.addWidget(diag_detail_panel)
        
        # Choices details panel
        choices_panel = QGroupBox("Выборы / Переходы")
        choices_layout = QVBoxLayout(choices_panel)
        choices_layout.addWidget(QLabel("<b>Варианты выбора в конце сцены:</b>"))
        
        self.choices_list = QListWidget()
        self.choices_list.currentRowChanged.connect(self.choice_selected)
        choices_layout.addWidget(self.choices_list)
        
        choices_ctrl_layout = QHBoxLayout()
        add_choice_btn = QPushButton("➕ Выбор")
        add_choice_btn.clicked.connect(self.add_choice)
        choices_ctrl_layout.addWidget(add_choice_btn)
        
        del_choice_btn = QPushButton("❌ Удалить")
        del_choice_btn.setObjectName("danger-btn")
        del_choice_btn.clicked.connect(self.delete_choice)
        choices_ctrl_layout.addWidget(del_choice_btn)
        choices_layout.addLayout(choices_ctrl_layout)
        
        self.choice_text_input = QLineEdit()
        self.choice_text_input.setPlaceholderText("Текст на кнопке выбора")
        self.choice_text_input.textChanged.connect(self.save_choice_fields)
        choices_layout.addWidget(self.choice_text_input)
        
        self.choice_target_combo = QComboBox()
        self.choice_target_combo.currentIndexChanged.connect(self.save_choice_fields)
        choices_layout.addWidget(self.choice_target_combo)
        
        choices_layout.addWidget(QFrame(frameShape=QFrame.HLine))
        choices_layout.addWidget(QLabel("<b>Или автоматический переход:</b>"))
        
        self.next_scene_combo = QComboBox()
        self.next_scene_combo.currentIndexChanged.connect(self.update_scene_jump)
        choices_layout.addWidget(self.next_scene_combo)
        
        details_splitter.addWidget(choices_panel)
        
        right_tab_widget.addTab(scene_editor_tab, "🎬 Редактор Сцен")
        
        # TAB 2: ASSETS LIBRARY
        assets_tab = QWidget()
        assets_layout = QVBoxLayout(assets_tab)
        assets_layout.setContentsMargins(5, 5, 5, 5)
        
        assets_inner_tab = QTabWidget()
        assets_layout.addWidget(assets_inner_tab)
        
        # 2A: Characters Subtab
        char_subtab = QWidget()
        char_subtab_lay = QHBoxLayout(char_subtab)
        
        char_lib_widget = QGroupBox("👥 Библиотека Персонажей")
        char_lib_layout = QVBoxLayout(char_lib_widget)
        self.char_lib_list = QListWidget()
        self.char_lib_list.currentRowChanged.connect(self.character_selected)
        char_lib_layout.addWidget(self.char_lib_list)
        
        char_btns = QHBoxLayout()
        add_char_btn = QPushButton("➕ Персонажа")
        add_char_btn.clicked.connect(self.add_character)
        char_btns.addWidget(add_char_btn)
        del_char_btn = QPushButton("❌ Удалить")
        del_char_btn.setObjectName("danger-btn")
        del_char_btn.clicked.connect(self.delete_character)
        char_btns.addWidget(del_char_btn)
        char_lib_layout.addLayout(char_btns)
        
        char_subtab_lay.addWidget(char_lib_widget)
        
        # Character properties panel
        self.char_props_panel = QGroupBox("Параметры персонажа")
        char_props_layout = QFormLayout(self.char_props_panel)
        
        self.char_name_input = QLineEdit()
        self.char_name_input.textChanged.connect(self.char_field_changed)
        char_props_layout.addRow("Имя:", self.char_name_input)
        
        self.char_color_input = QLineEdit()
        self.char_color_input.textChanged.connect(self.char_field_changed)
        char_color_btn = QPushButton("Цвет")
        char_color_btn.clicked.connect(lambda: self.choose_color(self.char_color_input))
        char_color_lay = QHBoxLayout()
        char_color_lay.addWidget(self.char_color_input)
        char_color_lay.addWidget(char_color_btn)
        char_props_layout.addRow("Цвет имени:", char_color_lay)
        
        # Sprites list for character
        char_props_layout.addRow(QLabel("<b>Эмоции / Спрайты персонажа:</b>"))
        self.char_sprites_list = QListWidget()
        self.char_sprites_list.currentRowChanged.connect(self.char_sprite_selected)
        char_props_layout.addRow(self.char_sprites_list)
        
        sprite_btns = QHBoxLayout()
        add_sprite_btn = QPushButton("➕ Спрайт")
        add_sprite_btn.clicked.connect(self.add_char_sprite)
        sprite_btns.addWidget(add_sprite_btn)
        del_sprite_btn = QPushButton("❌ Спрайт")
        del_sprite_btn.setObjectName("danger-btn")
        del_sprite_btn.clicked.connect(self.delete_char_sprite)
        sprite_btns.addWidget(del_sprite_btn)
        char_props_layout.addRow(sprite_btns)
        
        self.sprite_name_input = QLineEdit()
        self.sprite_name_input.setPlaceholderText("Название (например: Радость)")
        self.sprite_name_input.textChanged.connect(self.char_sprite_field_changed)
        char_props_layout.addRow("Название:", self.sprite_name_input)
        
        self.sprite_path_input = QLineEdit()
        self.sprite_path_input.textChanged.connect(self.char_sprite_field_changed)
        sprite_path_browse = QPushButton("Обзор")
        sprite_path_browse.clicked.connect(self.browse_char_sprite_path)
        sprite_path_lay = QHBoxLayout()
        sprite_path_lay.addWidget(self.sprite_path_input)
        sprite_path_lay.addWidget(sprite_path_browse)
        char_props_layout.addRow("Путь к файлу:", sprite_path_lay)
        
        char_subtab_lay.addWidget(self.char_props_panel)
        self.char_props_panel.hide()
        
        assets_inner_tab.addTab(char_subtab, "👥 Персонажи")
        
        # 2B: Backgrounds Subtab
        bg_subtab = QWidget()
        bg_subtab_lay = QHBoxLayout(bg_subtab)
        
        bg_lib_widget = QGroupBox("🖼 Библиотека Фонов")
        bg_lib_layout = QVBoxLayout(bg_lib_widget)
        self.bg_lib_list = QListWidget()
        self.bg_lib_list.currentRowChanged.connect(self.bg_lib_selected)
        bg_lib_layout.addWidget(self.bg_lib_list)
        
        bg_btns = QHBoxLayout()
        add_bg_btn = QPushButton("➕ Добавить фон")
        add_bg_btn.clicked.connect(self.add_bg_lib)
        bg_btns.addWidget(add_bg_btn)
        del_bg_btn = QPushButton("❌ Удалить фон")
        del_bg_btn.setObjectName("danger-btn")
        del_bg_btn.clicked.connect(self.delete_bg_lib)
        bg_btns.addWidget(del_bg_btn)
        bg_lib_layout.addLayout(bg_btns)
        bg_subtab_lay.addWidget(bg_lib_widget)
        
        self.bg_props_panel = QGroupBox("Параметры фона")
        bg_props_lay = QFormLayout(self.bg_props_panel)
        
        self.bg_name_input = QLineEdit()
        self.bg_name_input.textChanged.connect(self.bg_lib_field_changed)
        bg_props_lay.addRow("Название:", self.bg_name_input)
        
        self.bg_path_input = QLineEdit()
        self.bg_path_input.textChanged.connect(self.bg_lib_field_changed)
        bg_path_browse = QPushButton("Обзор")
        bg_path_browse.clicked.connect(self.browse_bg_lib_path)
        bg_path_lay = QHBoxLayout()
        bg_path_lay.addWidget(self.bg_path_input)
        bg_path_lay.addWidget(bg_path_browse)
        bg_props_lay.addRow("Файл фона:", bg_path_lay)
        bg_subtab_lay.addWidget(self.bg_props_panel)
        self.bg_props_panel.hide()
        
        assets_inner_tab.addTab(bg_subtab, "🖼 Фоны")
        
        # 2C: Audio Subtab (Music & SFX Libraries)
        audio_subtab = QWidget()
        audio_subtab_lay = QHBoxLayout(audio_subtab)
        
        # Split into Left (BGM) and Right (SFX)
        audio_splitter = QSplitter(Qt.Horizontal)
        audio_subtab_lay.addWidget(audio_splitter)
        
        # Left Panel: Music Library
        music_lib_widget = QGroupBox("🎵 Фоновая Музыка (BGM)")
        music_lib_layout = QVBoxLayout(music_lib_widget)
        
        self.music_lib_list = QListWidget()
        self.music_lib_list.currentRowChanged.connect(self.music_lib_selected)
        music_lib_layout.addWidget(self.music_lib_list)
        
        music_btns = QHBoxLayout()
        add_music_btn = QPushButton("➕ Добавить BGM")
        add_music_btn.clicked.connect(self.add_music_lib)
        music_btns.addWidget(add_music_btn)
        del_music_btn = QPushButton("❌ Удалить BGM")
        del_music_btn.setObjectName("danger-btn")
        del_music_btn.clicked.connect(self.delete_music_lib)
        music_btns.addWidget(del_music_btn)
        music_lib_layout.addLayout(music_btns)
        
        self.music_props_widget = QWidget()
        music_props_lay = QFormLayout(self.music_props_widget)
        music_props_lay.setContentsMargins(0, 5, 0, 0)
        self.music_name_input = QLineEdit()
        self.music_name_input.textChanged.connect(self.music_lib_field_changed)
        music_props_lay.addRow("Название BGM:", self.music_name_input)
        self.music_path_input = QLineEdit()
        self.music_path_input.textChanged.connect(self.music_lib_field_changed)
        music_path_browse = QPushButton("Обзор")
        music_path_browse.clicked.connect(self.browse_music_lib_path)
        music_path_lay = QHBoxLayout()
        music_path_lay.addWidget(self.music_path_input)
        music_path_lay.addWidget(music_path_browse)
        music_props_lay.addRow("Файл музыки:", music_path_lay)
        music_lib_layout.addWidget(self.music_props_widget)
        self.music_props_widget.hide()
        
        audio_splitter.addWidget(music_lib_widget)
        
        # Right Panel: SFX Library
        sfx_lib_widget = QGroupBox("🔊 Звуковые Эффекты (SFX)")
        sfx_lib_layout = QVBoxLayout(sfx_lib_widget)
        
        self.sfx_lib_list = QListWidget()
        self.sfx_lib_list.currentRowChanged.connect(self.sfx_lib_selected)
        sfx_lib_layout.addWidget(self.sfx_lib_list)
        
        sfx_btns = QHBoxLayout()
        add_sfx_btn = QPushButton("➕ Добавить SFX")
        add_sfx_btn.clicked.connect(self.add_sfx_lib)
        sfx_btns.addWidget(add_sfx_btn)
        del_sfx_btn = QPushButton("❌ Удалить SFX")
        del_sfx_btn.setObjectName("danger-btn")
        del_sfx_btn.clicked.connect(self.delete_sfx_lib)
        sfx_btns.addWidget(del_sfx_btn)
        sfx_lib_layout.addLayout(sfx_btns)
        
        self.sfx_props_widget = QWidget()
        sfx_props_lay = QFormLayout(self.sfx_props_widget)
        sfx_props_lay.setContentsMargins(0, 5, 0, 0)
        self.sfx_name_input = QLineEdit()
        self.sfx_name_input.textChanged.connect(self.sfx_lib_field_changed)
        sfx_props_lay.addRow("Название SFX:", self.sfx_name_input)
        self.sfx_path_input = QLineEdit()
        self.sfx_path_input.textChanged.connect(self.sfx_lib_field_changed)
        sfx_path_browse = QPushButton("Обзор")
        sfx_path_browse.clicked.connect(self.browse_sfx_lib_path)
        sfx_path_lay = QHBoxLayout()
        sfx_path_lay.addWidget(self.sfx_path_input)
        sfx_path_lay.addWidget(sfx_path_browse)
        sfx_props_lay.addRow("Файл звука:", sfx_path_lay)
        sfx_lib_layout.addWidget(self.sfx_props_widget)
        self.sfx_props_widget.hide()
        
        audio_splitter.addWidget(sfx_lib_widget)
        audio_splitter.setSizes([600, 600])
        
        assets_inner_tab.addTab(audio_subtab, "🎵 Звуки и Музыка")
        
        right_tab_widget.addTab(assets_tab, "📦 Библиотека Ассетов")
        
        # TAB 3: MONETIZATION SETTINGS
        monetization_tab = QWidget()
        monetization_layout = QVBoxLayout(monetization_tab)
        monetization_layout.setContentsMargins(20, 20, 20, 20)
        
        ads_box = QGroupBox("А. Настройка полноэкранной рекламы (Interstitial)")
        ads_form = QFormLayout(ads_box)
        ads_form.setSpacing(15)
        
        self.enable_ads_check = QCheckBox("Включить автоматический показ рекламы")
        self.enable_ads_check.setChecked(True)
        ads_form.addRow(self.enable_ads_check)
        
        self.ads_interval_spin = QSpinBox()
        self.ads_interval_spin.setRange(1, 60)
        self.ads_interval_spin.setValue(3)
        self.ads_interval_spin.setSuffix(" мин.")
        ads_form.addRow("Интервал между рекламой:", self.ads_interval_spin)
        
        monetization_layout.addWidget(ads_box)
        
        iap_box = QGroupBox("Б. Внутриигровые покупки (In-App Purchases)")
        iap_form = QFormLayout(iap_box)
        iap_form.setSpacing(15)
        
        self.enable_iap_check = QCheckBox("Добавить покупку 'Отключение рекламы'")
        self.enable_iap_check.setChecked(True)
        iap_form.addRow(self.enable_iap_check)
        
        self.iap_id_input = QLineEdit("no_ads_30rub")
        self.iap_id_input.setPlaceholderText("Идентификатор покупки в панели Яндекс.Игр")
        iap_form.addRow("ID покупки в Яндексе:", self.iap_id_input)
        
        price_label = QLabel("30 руб. / Ян.Валюта (Справочно)")
        price_label.setStyleSheet("color: #a0a0b2;")
        iap_form.addRow("Стоимость покупки:", price_label)
        
        monetization_layout.addWidget(iap_box)
        monetization_layout.addStretch()
        
        right_tab_widget.addTab(monetization_tab, "💰 Настройки Монетизации")
        
        # TAB 4: GUI CUSTOMIZATION
        gui_tab = QWidget()
        gui_layout = QVBoxLayout(gui_tab)
        gui_layout.setContentsMargins(20, 20, 20, 20)
        
        profile_group = QGroupBox("Профиль интерфейса")
        profile_form = QFormLayout(profile_group)
        self.gui_profile_combo = QComboBox()
        self.gui_profile_combo.addItems(["Дефолтный", "Классический Ren'Py", "Аниме Неон", "Киберпанк", "Пользовательский"])
        self.gui_profile_combo.currentIndexChanged.connect(self.gui_profile_changed)
        profile_form.addRow("Текущий профиль GUI:", self.gui_profile_combo)
        gui_layout.addWidget(profile_group)
        
        self.gui_custom_group = QGroupBox("Параметры кастомизации интерфейса")
        self.gui_custom_layout = QFormLayout(self.gui_custom_group)
        self.gui_custom_layout.setSpacing(10)
        
        self.gui_dialogue_height = QSpinBox()
        self.gui_dialogue_height.setRange(100, 350)
        self.gui_dialogue_height.setValue(180)
        self.gui_dialogue_height.setSuffix(" px")
        self.gui_dialogue_height.valueChanged.connect(self.gui_field_changed)
        self.gui_custom_layout.addRow("Высота панели диалога:", self.gui_dialogue_height)
        
        self.gui_panel_bg = QLineEdit()
        self.gui_panel_bg.textChanged.connect(self.gui_field_changed)
        panel_bg_btn = QPushButton("Цвет")
        panel_bg_btn.clicked.connect(lambda: self.choose_color(self.gui_panel_bg))
        panel_bg_layout = QHBoxLayout()
        panel_bg_layout.addWidget(self.gui_panel_bg)
        panel_bg_layout.addWidget(panel_bg_btn)
        self.gui_custom_layout.addRow("Фон панели (rgba/hex):", panel_bg_layout)
        
        self.gui_panel_border = QLineEdit()
        self.gui_panel_border.textChanged.connect(self.gui_field_changed)
        panel_border_btn = QPushButton("Цвет")
        panel_border_btn.clicked.connect(lambda: self.choose_color(self.gui_panel_border))
        panel_border_layout = QHBoxLayout()
        panel_border_layout.addWidget(self.gui_panel_border)
        panel_border_layout.addWidget(panel_border_btn)
        self.gui_custom_layout.addRow("Рамка панели (rgba/hex):", panel_border_layout)
        
        self.gui_panel_radius = QSpinBox()
        self.gui_panel_radius.setRange(0, 50)
        self.gui_panel_radius.setValue(12)
        self.gui_panel_radius.setSuffix(" px")
        self.gui_panel_radius.valueChanged.connect(self.gui_field_changed)
        self.gui_custom_layout.addRow("Скругление углов панели:", self.gui_panel_radius)
        
        self.gui_text_color = QLineEdit()
        self.gui_text_color.textChanged.connect(self.gui_field_changed)
        text_color_btn = QPushButton("Цвет")
        text_color_btn.clicked.connect(lambda: self.choose_color(self.gui_text_color))
        text_color_layout = QHBoxLayout()
        text_color_layout.addWidget(self.gui_text_color)
        text_color_layout.addWidget(text_color_btn)
        self.gui_custom_layout.addRow("Цвет основного текста:", text_color_layout)
        
        self.gui_text_size = QSpinBox()
        self.gui_text_size.setRange(10, 36)
        self.gui_text_size.setValue(18)
        self.gui_text_size.setSuffix(" px")
        self.gui_text_size.valueChanged.connect(self.gui_field_changed)
        self.gui_custom_layout.addRow("Размер текста реплик:", self.gui_text_size)
        
        self.gui_name_color = QLineEdit()
        self.gui_name_color.textChanged.connect(self.gui_field_changed)
        name_color_btn = QPushButton("Цвет")
        name_color_btn.clicked.connect(lambda: self.choose_color(self.gui_name_color))
        name_color_layout = QHBoxLayout()
        name_color_layout.addWidget(self.gui_name_color)
        name_color_layout.addWidget(name_color_btn)
        self.gui_custom_layout.addRow("Цвет имени персонажа:", name_color_layout)
        
        self.gui_name_size = QSpinBox()
        self.gui_name_size.setRange(10, 36)
        self.gui_name_size.setValue(20)
        self.gui_name_size.setSuffix(" px")
        self.gui_name_size.valueChanged.connect(self.gui_field_changed)
        self.gui_custom_layout.addRow("Размер имени персонажа:", self.gui_name_size)
        
        self.gui_name_bold = QCheckBox("Жирный шрифт для имени")
        self.gui_name_bold.setChecked(True)
        self.gui_name_bold.stateChanged.connect(self.gui_field_changed)
        self.gui_custom_layout.addRow("Стиль имени:", self.gui_name_bold)
        
        self.gui_choice_bg = QLineEdit()
        self.gui_choice_bg.textChanged.connect(self.gui_field_changed)
        choice_bg_btn = QPushButton("Цвет")
        choice_bg_btn.clicked.connect(lambda: self.choose_color(self.gui_choice_bg))
        choice_bg_layout = QHBoxLayout()
        choice_bg_layout.addWidget(self.gui_choice_bg)
        choice_bg_layout.addWidget(choice_bg_btn)
        self.gui_custom_layout.addRow("Фон кнопок выбора:", choice_bg_layout)
        
        self.gui_choice_hover_bg = QLineEdit()
        self.gui_choice_hover_bg.textChanged.connect(self.gui_field_changed)
        choice_hover_bg_btn = QPushButton("Цвет")
        choice_hover_bg_btn.clicked.connect(lambda: self.choose_color(self.gui_choice_hover_bg))
        choice_hover_bg_layout = QHBoxLayout()
        choice_hover_bg_layout.addWidget(self.gui_choice_hover_bg)
        choice_hover_bg_layout.addWidget(choice_hover_bg_btn)
        self.gui_custom_layout.addRow("Фон кнопок при наведении:", choice_hover_bg_layout)
        
        self.gui_choice_border_color = QLineEdit()
        self.gui_choice_border_color.textChanged.connect(self.gui_field_changed)
        choice_border_color_btn = QPushButton("Цвет")
        choice_border_color_btn.clicked.connect(lambda: self.choose_color(self.gui_choice_border_color))
        choice_border_color_layout = QHBoxLayout()
        choice_border_color_layout.addWidget(self.gui_choice_border_color)
        choice_border_color_layout.addWidget(choice_border_color_btn)
        self.gui_custom_layout.addRow("Рамка кнопок выбора:", choice_border_color_layout)
        
        self.gui_choice_text_color = QLineEdit()
        self.gui_choice_text_color.textChanged.connect(self.gui_field_changed)
        choice_text_color_btn = QPushButton("Цвет")
        choice_text_color_btn.clicked.connect(lambda: self.choose_color(self.gui_choice_text_color))
        choice_text_color_layout = QHBoxLayout()
        choice_text_color_layout.addWidget(self.gui_choice_text_color)
        choice_text_color_layout.addWidget(choice_text_color_btn)
        self.gui_custom_layout.addRow("Цвет текста вариантов:", choice_text_color_layout)
        
        self.gui_choice_size = QSpinBox()
        self.gui_choice_size.setRange(10, 36)
        self.gui_choice_size.setValue(16)
        self.gui_choice_size.setSuffix(" px")
        self.gui_choice_size.valueChanged.connect(self.gui_field_changed)
        self.gui_custom_layout.addRow("Размер текста вариантов:", self.gui_choice_size)
        
        self.gui_font_family = QComboBox()
        self.gui_font_family.addItems(["system-ui", "Georgia", "Courier New", "Times New Roman", "Arial"])
        self.gui_font_family.currentIndexChanged.connect(self.gui_field_changed)
        self.gui_custom_layout.addRow("Шрифт всей игры:", self.gui_font_family)
        
        gui_layout.addWidget(self.gui_custom_group)
        gui_layout.addStretch()
        
        right_tab_widget.addTab(gui_tab, "🎨 Настройки GUI")
        
        # TAB 5: PROJECT SETTINGS
        settings_tab = QWidget()
        settings_layout = QVBoxLayout(settings_tab)
        settings_layout.setContentsMargins(20, 20, 20, 20)
        
        proj_box = QGroupBox("Общие настройки проекта")
        proj_form = QFormLayout(proj_box)
        proj_form.setSpacing(15)
        
        self.proj_title_input = QLineEdit("Моя Новелла")
        proj_form.addRow("Название новеллы:", self.proj_title_input)
        
        export_dir_layout = QHBoxLayout()
        self.export_dir_input = QLineEdit()
        self.export_dir_input.setText("F:\\myvn\\export")
        export_dir_layout.addWidget(self.export_dir_input)
        
        export_dir_browse = QPushButton("Обзор...")
        export_dir_browse.clicked.connect(self.browse_export_directory)
        export_dir_layout.addWidget(export_dir_browse)
        proj_form.addRow("Папка экспорта:", export_dir_layout)
        
        settings_layout.addWidget(proj_box)
        settings_layout.addStretch()
        
        right_tab_widget.addTab(settings_tab, "⚙ Настройки Проекта")
        
        # Set splitter sizes
        main_splitter.setSizes([300, 900])
        scene_splitter.setSizes([450, 450])
        details_splitter.setSizes([450, 450])
        
    # Project File Management
    def new_project(self):
        self.project_path = None
        self.project_data = {
            "config": {
                "title": "Моя Новелла",
                "start_scene": "scene_1",
                "ads_interval_minutes": 3,
                "inapp_remove_ads_id": "no_ads_30rub",
                "export_dir": "F:\\myvn\\export",
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
                },
                "music": {},
                "sfx": {}
            },
            "gui": dict(GUI_PRESETS["Дефолтный"]),
            "scenes": {
                "scene_1": {
                    "background": "#14141f",
                    "transition": "fade",
                    "bgm": "",
                    "dialogues": [
                        {
                            "character_id": "alisa",
                            "speaker": "Алиса",
                            "text": "Привет! Это твоя первая сцена с плавным переходом.",
                            "is_thought": False,
                            "text_bold": False,
                            "text_italic": False,
                            "sfx": "",
                            "sprite": {"position": "center", "image": "https://img.icons8.com/color/344/anime-emoji.png"}
                        }
                    ],
                    "choices": [],
                    "next_scene": ""
                }
            }
        }
        self.refresh_all_ui()
        self.scene_list.setCurrentRow(0)
        
    def open_project(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Открыть файл проекта myvn", "F:\\myvn", "Проект myvn (*.json)"
        )
        if not file_path:
            return
            
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            if "config" not in data or "scenes" not in data:
                raise ValueError("Некорректный формат файла проекта.")
            
            # Upgrade keys for old files
            if "characters" not in data["config"]:
                data["config"]["characters"] = {}
            if "backgrounds" not in data["config"]:
                data["config"]["backgrounds"] = {}
            if "music" not in data["config"]:
                data["config"]["music"] = {}
            if "sfx" not in data["config"]:
                data["config"]["sfx"] = {}
                
            self.project_path = file_path
            self.project_data = data
            self.refresh_all_ui()
            
            start_scene = self.project_data["config"].get("start_scene", "")
            if start_scene in self.project_data["scenes"]:
                idx = list(self.project_data["scenes"].keys()).index(start_scene)
                self.scene_list.setCurrentRow(idx)
            elif self.project_data["scenes"]:
                self.scene_list.setCurrentRow(0)
                
            QMessageBox.information(self, "Открыто", "Проект успешно загружен.")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось открыть файл проекта:\n{str(e)}")
            
    def save_project(self):
        if not self.project_path:
            self.save_project_as()
        else:
            self.sync_config_from_ui()
            try:
                with open(self.project_path, "w", encoding="utf-8") as f:
                    json.dump(self.project_data, f, indent=4, ensure_ascii=False)
                self.statusBar().showMessage(f"Проект сохранен в: {self.project_path}", 3000)
            except Exception as e:
                QMessageBox.critical(self, "Ошибка сохранения", f"Не удалось сохранить проект:\n{str(e)}")
                
    def save_project_as(self):
        self.sync_config_from_ui()
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Сохранить проект как", "F:\\myvn", "Проект myvn (*.json)"
        )
        if not file_path:
            return
            
        self.project_path = file_path
        self.save_project()
        
    def sync_config_from_ui(self):
        config = self.project_data["config"]
        config["title"] = self.proj_title_input.text()
        config["export_dir"] = self.export_dir_input.text()
        config["gui_profile"] = self.gui_profile_combo.currentText()
        
        if self.enable_ads_check.isChecked():
            config["ads_interval_minutes"] = self.ads_interval_spin.value()
        else:
            config["ads_interval_minutes"] = 0
            
        if self.enable_iap_check.isChecked():
            config["inapp_remove_ads_id"] = self.iap_id_input.text()
        else:
            config["inapp_remove_ads_id"] = ""
            
        # Sync GUI variables
        if self.gui_profile_combo.currentText() == "Пользовательский":
            gui = self.project_data["gui"]
            gui["dialogue_height"] = self.gui_dialogue_height.value()
            gui["panel_bg"] = self.gui_panel_bg.text()
            gui["panel_border"] = self.gui_panel_border.text()
            gui["panel_radius"] = self.gui_panel_radius.value()
            
            gui["text_color"] = self.gui_text_color.text()
            gui["text_size"] = self.gui_text_size.value()
            
            gui["name_color"] = self.gui_name_color.text()
            gui["name_size"] = self.gui_name_size.value()
            gui["name_bold"] = self.gui_name_bold.isChecked()
            
            gui["choice_bg"] = self.gui_choice_bg.text()
            gui["choice_hover_bg"] = self.gui_choice_hover_bg.text()
            gui["choice_border_color"] = self.gui_choice_border_color.text()
            gui["choice_text_color"] = self.gui_choice_text_color.text()
            gui["choice_size"] = self.gui_choice_size.value()
            gui["font_family"] = self.gui_font_family.currentText()

    # Export Logic
    def export_html5(self):
        self.sync_config_from_ui()
        export_dir = self.export_dir_input.text().strip()
        
        if not export_dir:
            QMessageBox.warning(self, "Внимание", "Пожалуйста, укажите папку экспорта.")
            return
            
        ok, msg = export_project(self.project_data, export_dir)
        if ok:
            QMessageBox.information(self, "Экспорт Завершен", msg)
        else:
            QMessageBox.critical(self, "Ошибка экспорта", msg)

    # UI Refresh helpers
    def refresh_all_ui(self):
        self.is_updating_ui = True
        
        # Config inputs
        config = self.project_data.get("config", {})
        self.proj_title_input.setText(config.get("title", "Моя Новелла"))
        self.export_dir_input.setText(config.get("export_dir", "F:\\myvn\\export"))
        
        ads_interval = config.get("ads_interval_minutes", 3)
        if ads_interval > 0:
            self.enable_ads_check.setChecked(True)
            self.ads_interval_spin.setValue(ads_interval)
        else:
            self.enable_ads_check.setChecked(False)
            self.ads_interval_spin.setValue(3)
            
        iap_id = config.get("inapp_remove_ads_id", "")
        if iap_id:
            self.enable_iap_check.setChecked(True)
            self.iap_id_input.setText(iap_id)
        else:
            self.enable_iap_check.setChecked(False)
            self.iap_id_input.setText("no_ads_30rub")
            
        # Refresh GUI Profile settings
        gui_profile = config.get("gui_profile", "Дефолтный")
        profile_idx = self.gui_profile_combo.findText(gui_profile)
        if profile_idx >= 0:
            self.gui_profile_combo.setCurrentIndex(profile_idx)
            
        gui_data = self.project_data.get("gui", dict(GUI_PRESETS["Дефолтный"]))
        self.load_gui_fields(gui_data)
        
        if gui_profile == "Пользовательский":
            self.set_gui_fields_enabled(True)
        else:
            self.set_gui_fields_enabled(False)
            
        # Refresh Assets Tab lists
        self.refresh_assets_tab_lists()
        
        # Refresh Scene list
        self.refresh_scene_list()
        
        self.is_updating_ui = False
        
    def refresh_scene_list(self):
        self.scene_list.clear()
        start_scene = self.project_data["config"].get("start_scene", "")
        
        for scene_id in self.project_data["scenes"].keys():
            item = QListWidgetItem(scene_id)
            if scene_id == start_scene:
                item.setText(f"⭐ {scene_id} [СТАРТ]")
                item.setForeground(QColor("#ffcc00"))
            self.scene_list.addItem(item)
            
        self.refresh_scene_comboboxes()
        
    def refresh_scene_comboboxes(self):
        # Temp save selections
        curr_choice_target = self.choice_target_combo.currentText()
        curr_next_scene = self.next_scene_combo.currentText()
        
        self.choice_target_combo.clear()
        self.next_scene_combo.clear()
        
        self.choice_target_combo.addItem("[Нет перехода]", "")
        self.next_scene_combo.addItem("[Нет перехода]", "")
        
        for s_id in self.project_data["scenes"].keys():
            self.choice_target_combo.addItem(s_id, s_id)
            self.next_scene_combo.addItem(s_id, s_id)
            
        idx = self.choice_target_combo.findText(curr_choice_target)
        if idx >= 0: self.choice_target_combo.setCurrentIndex(idx)
        
        idx = self.next_scene_combo.findText(curr_next_scene)
        if idx >= 0: self.next_scene_combo.setCurrentIndex(idx)
        
        # Refresh Backgrounds combo from library
        self.refresh_bg_combo_list()
        
        # Refresh BGM combo from library
        self.refresh_bgm_combo_list()
        
        # Refresh Character combos in dialogue panel
        self.refresh_dialogue_char_combos()
        
        # Refresh SFX combo from library
        self.refresh_sfx_combo_list()

    # GUI Profile handlers
    def gui_profile_changed(self, index):
        profile_name = self.gui_profile_combo.currentText()
        
        if profile_name != "Пользовательский":
            preset_data = GUI_PRESETS[profile_name]
            self.is_updating_ui = True
            self.load_gui_fields(preset_data)
            self.is_updating_ui = False
            self.set_gui_fields_enabled(False)
            self.project_data["gui"] = dict(preset_data)
        else:
            self.set_gui_fields_enabled(True)
            
        self.project_data["config"]["gui_profile"] = profile_name

    def gui_field_changed(self):
        if self.is_updating_ui:
            return
        if self.gui_profile_combo.currentText() == "Пользовательский":
            self.sync_config_from_ui()

    def load_gui_fields(self, gui_data):
        self.gui_dialogue_height.setValue(gui_data.get("dialogue_height", 180))
        self.gui_panel_bg.setText(gui_data.get("panel_bg", "rgba(18, 18, 24, 0.75)"))
        self.gui_panel_border.setText(gui_data.get("panel_border", "rgba(255, 255, 255, 0.1)"))
        self.gui_panel_radius.setValue(gui_data.get("panel_radius", 12))
        
        self.gui_text_color.setText(gui_data.get("text_color", "#f3f3f7"))
        self.gui_text_size.setValue(gui_data.get("text_size", 18))
        
        self.gui_name_color.setText(gui_data.get("name_color", "#ffcc00"))
        self.gui_name_size.setValue(gui_data.get("name_size", 20))
        self.gui_name_bold.setChecked(gui_data.get("name_bold", True))
        
        self.gui_choice_bg.setText(gui_data.get("choice_bg", "rgba(18, 18, 24, 0.9)"))
        self.gui_choice_hover_bg.setText(gui_data.get("choice_hover_bg", "#1e1e24"))
        self.gui_choice_border_color.setText(gui_data.get("choice_border_color", "rgba(255, 255, 255, 0.15)"))
        self.gui_choice_text_color.setText(gui_data.get("choice_text_color", "#f3f3f7"))
        self.gui_choice_size.setValue(gui_data.get("choice_size", 16))
        
        font_family = gui_data.get("font_family", "system-ui")
        f_idx = self.gui_font_family.findText(font_family)
        if f_idx >= 0:
            self.gui_font_family.setCurrentIndex(f_idx)

    def set_gui_fields_enabled(self, enabled):
        self.gui_dialogue_height.setEnabled(enabled)
        self.gui_panel_bg.setEnabled(enabled)
        self.gui_panel_border.setEnabled(enabled)
        self.gui_panel_radius.setEnabled(enabled)
        
        self.gui_text_color.setEnabled(enabled)
        self.gui_text_size.setEnabled(enabled)
        
        self.gui_name_color.setEnabled(enabled)
        self.gui_name_size.setEnabled(enabled)
        self.gui_name_bold.setEnabled(enabled)
        
        self.gui_choice_bg.setEnabled(enabled)
        self.gui_choice_hover_bg.setEnabled(enabled)
        self.gui_choice_border_color.setEnabled(enabled)
        self.gui_choice_text_color.setEnabled(enabled)
        self.gui_choice_size.setEnabled(enabled)
        self.gui_font_family.setEnabled(enabled)

    def choose_color(self, line_edit):
        current_color_str = line_edit.text().strip()
        init_color = QColor("#ffcc00")
        if current_color_str.startswith("#"):
            init_color = QColor(current_color_str)
            
        color = QColorDialog.getColor(init_color, self, "Выберите цвет")
        if color.isValid():
            if current_color_str.startswith("rgba") or "," in current_color_str:
                line_edit.setText(f"rgba({color.red()}, {color.green()}, {color.blue()}, 0.8)")
            else:
                line_edit.setText(color.name())

    def sprite_pos_type_changed(self):
        if self.is_updating_ui: return
        is_custom = self.sprite_pos_type.currentText() == "Координаты X, Y (%)"
        self.sprite_pos_combo.setVisible(not is_custom)
        self.sprite_x_coord.setVisible(is_custom)
        self.sprite_y_coord.setVisible(is_custom)
        self.save_current_dialogue_fields()

    # Scenes CRUD
    def add_scene(self):
        scene_name, ok = QInputDialog.getText(self, "Новая сцена", "Введите уникальный ID сцены:")
        if not ok or not scene_name.strip():
            return
            
        scene_id = scene_name.strip().lower().replace(" ", "_")
        if scene_id in self.project_data["scenes"]:
            QMessageBox.warning(self, "Внимание", "Сцена с таким ID уже существует!")
            return
            
        self.project_data["scenes"][scene_id] = {
            "background": "#14141f",
            "transition": "none",
            "bgm": "",
            "dialogues": [],
            "choices": [],
            "next_scene": ""
        }
        
        if not self.project_data["config"].get("start_scene"):
            self.project_data["config"]["start_scene"] = scene_id
            
        self.refresh_scene_list()
        
        idx = list(self.project_data["scenes"].keys()).index(scene_id)
        self.scene_list.setCurrentRow(idx)
        
    def delete_scene(self):
        if not self.selected_scene_id:
            return
            
        confirm = QMessageBox.question(
            self, "Удаление сцены", f"Вы уверены, что хотите удалить сцену '{self.selected_scene_id}'?"
        )
        if confirm != QMessageBox.Yes:
            return
            
        del self.project_data["scenes"][self.selected_scene_id]
        
        if self.project_data["config"].get("start_scene") == self.selected_scene_id:
            self.project_data["config"]["start_scene"] = ""
            
        self.selected_scene_id = None
        self.selected_dialogue_idx = None
        self.selected_choice_idx = None
        
        self.refresh_scene_list()
        
        if self.project_data["scenes"]:
            self.scene_list.setCurrentRow(0)
        else:
            self.clear_scene_ui()
            
    def set_start_scene(self):
        if not self.selected_scene_id:
            return
        self.project_data["config"]["start_scene"] = self.selected_scene_id
        self.refresh_scene_list()
        
    def scene_selected(self, index):
        if index < 0 or self.is_updating_ui:
            return
            
        self.selected_scene_id = list(self.project_data["scenes"].keys())[index]
        self.refresh_selected_scene_ui()
        
    def clear_scene_ui(self):
        self.bg_input.clear()
        self.scene_bgm_input.clear()
        self.dialogue_list.clear()
        self.clear_dialogue_fields()
        self.choices_list.clear()
        self.choice_text_input.clear()
        self.choice_target_combo.setCurrentIndex(0)
        self.next_scene_combo.setCurrentIndex(0)
        
    def refresh_selected_scene_ui(self):
        if not self.selected_scene_id:
            return
            
        self.is_updating_ui = True
        scene = self.project_data["scenes"][self.selected_scene_id]
        
        # Match scene background combo selection
        scene_bg = scene.get("background", "")
        self.bg_input.setText(scene_bg)
        
        # Populate backgrounds combobox
        self.refresh_bg_combo_list()
        
        # Try to find if this path matches a library background
        found_bg = False
        bg_lib = self.project_data["config"].get("backgrounds", {})
        for name, path in bg_lib.items():
            if path == scene_bg:
                bg_idx = self.scene_bg_combo.findText(name)
                if bg_idx >= 0:
                    self.scene_bg_combo.setCurrentIndex(bg_idx)
                    self.bg_input.hide()
                    self.bg_browse_btn.hide()
                    found_bg = True
                    break
        if not found_bg:
            self.scene_bg_combo.setCurrentIndex(0) # [Вручную / Цвет]
            self.bg_input.show()
            self.bg_browse_btn.show()
            
        # Match transition combo selection
        trans = scene.get("transition", "none")
        idx_trans = self.scene_trans_combo.findData(trans)
        if idx_trans >= 0:
            self.scene_trans_combo.setCurrentIndex(idx_trans)
        else:
            self.scene_trans_combo.setCurrentIndex(0)
            
        # Match BGM combo selection
        scene_bgm = scene.get("bgm", "")
        self.scene_bgm_input.setText(scene_bgm)
        self.refresh_bgm_combo_list()
        
        found_bgm = False
        if scene_bgm == "stop":
            self.scene_bgm_combo.setCurrentIndex(1) # [Остановить музыку]
            self.scene_bgm_input.hide()
            self.scene_bgm_browse_btn.hide()
            found_bgm = True
        elif scene_bgm == "":
            self.scene_bgm_combo.setCurrentIndex(0) # [Без изменений]
            self.scene_bgm_input.hide()
            self.scene_bgm_browse_btn.hide()
            found_bgm = True
        else:
            music_lib = self.project_data["config"].get("music", {})
            for name, path in music_lib.items():
                if path == scene_bgm:
                    idx = self.scene_bgm_combo.findText(name)
                    if idx >= 0:
                        self.scene_bgm_combo.setCurrentIndex(idx)
                        self.scene_bgm_input.hide()
                        self.scene_bgm_browse_btn.hide()
                        found_bgm = True
                        break
        if not found_bgm:
            self.scene_bgm_combo.setCurrentIndex(2) # [Вручную / Путь]
            self.scene_bgm_input.show()
            self.scene_bgm_browse_btn.show()
        
        # Populate Dialogues list
        self.dialogue_list.clear()
        for idx, diag in enumerate(scene.get("dialogues", [])):
            text_preview = diag.get("text", "")[:30] + "..." if len(diag.get("text", "")) > 30 else diag.get("text", "")
            speaker = diag.get("speaker", "Без имени")
            if diag.get("is_thought"):
                self.dialogue_list.addItem(f"{idx+1}. 💭 ({text_preview})")
            else:
                self.dialogue_list.addItem(f"{idx+1}. [{speaker}] {text_preview}")
            
        # Populate Choices list
        self.choices_list.clear()
        for idx, choice in enumerate(scene.get("choices", [])):
            self.choices_list.addItem(f"Выбор: {choice.get('text')} -> {choice.get('next_scene')}")
            
        next_scene = scene.get("next_scene", "")
        if next_scene:
            idx = self.next_scene_combo.findData(next_scene)
            if idx >= 0: self.next_scene_combo.setCurrentIndex(idx)
        else:
            self.next_scene_combo.setCurrentIndex(0)
            
        self.clear_dialogue_fields()
        self.choice_text_input.clear()
        self.choice_target_combo.setCurrentIndex(0)
        
        self.selected_dialogue_idx = None
        self.selected_choice_idx = None
        self.is_updating_ui = False
        
    def update_scene_bg(self, text):
        if self.is_updating_ui or not self.selected_scene_id: return
        self.project_data["scenes"][self.selected_scene_id]["background"] = text

    def update_scene_transition(self, index):
        if self.is_updating_ui or not self.selected_scene_id: return
        trans = self.scene_trans_combo.currentData()
        self.project_data["scenes"][self.selected_scene_id]["transition"] = trans

    def update_scene_bgm(self, text):
        if self.is_updating_ui or not self.selected_scene_id: return
        self.project_data["scenes"][self.selected_scene_id]["bgm"] = text

    def browse_bg_image(self):
        if not self.selected_scene_id: return
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Выбрать фоновое изображение", "", "Изображения (*.png *.jpg *.jpeg *.webp)"
        )
        if file_path:
            self.bg_input.setText(file_path)

    def browse_scene_bgm(self):
        if not self.selected_scene_id: return
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Выбрать BGM аудиофайл", "", "Музыка (*.mp3 *.ogg *.wav)"
        )
        if file_path:
            self.scene_bgm_input.setText(file_path)
            
    def scene_bg_combo_changed(self, index):
        if self.is_updating_ui or not self.selected_scene_id: return
        
        bg_name = self.scene_bg_combo.currentText()
        if bg_name == "[Вручную / Цвет]":
            self.bg_input.show()
            self.bg_browse_btn.show()
        else:
            self.bg_input.hide()
            self.bg_browse_btn.hide()
            
            # Load library path
            bg_lib = self.project_data["config"].get("backgrounds", {})
            bg_path = bg_lib.get(bg_name, "")
            self.bg_input.setText(bg_path)
            self.update_scene_bg(bg_path)

    def scene_bgm_combo_changed(self, index):
        if self.is_updating_ui or not self.selected_scene_id: return
        
        bgm_name = self.scene_bgm_combo.currentText()
        if bgm_name == "[Без изменений]":
            self.scene_bgm_input.hide()
            self.scene_bgm_browse_btn.hide()
            self.scene_bgm_input.setText("")
            self.update_scene_bgm("")
        elif bgm_name == "[Остановить музыку]":
            self.scene_bgm_input.hide()
            self.scene_bgm_browse_btn.hide()
            self.scene_bgm_input.setText("stop")
            self.update_scene_bgm("stop")
        elif bgm_name == "[Вручную / Путь к файлу]":
            self.scene_bgm_input.show()
            self.scene_bgm_browse_btn.show()
        else:
            self.scene_bgm_input.hide()
            self.scene_bgm_browse_btn.hide()
            
            music_lib = self.project_data["config"].get("music", {})
            m_path = music_lib.get(bgm_name, "")
            self.scene_bgm_input.setText(m_path)
            self.update_scene_bgm(m_path)

    # Dialogue steps CRUD & Edit
    def add_dialogue(self):
        if not self.selected_scene_id: return
        scene = self.project_data["scenes"][self.selected_scene_id]
        
        new_step = {
            "character_id": "",
            "speaker": "Рассказчик",
            "text": "Новая реплика диалога...",
            "is_thought": False,
            "text_bold": False,
            "text_italic": False,
            "sfx": "",
            "sprite": {"position": "center", "image": ""}
        }
        scene["dialogues"].append(new_step)
        
        self.refresh_selected_scene_ui()
        self.dialogue_list.setCurrentRow(len(scene["dialogues"]) - 1)
        
    def delete_dialogue(self):
        if not self.selected_scene_id or self.selected_dialogue_idx is None: return
        scene = self.project_data["scenes"][self.selected_scene_id]
        
        del scene["dialogues"][self.selected_dialogue_idx]
        self.selected_dialogue_idx = None
        self.refresh_selected_scene_ui()
        
    def dialogue_selected(self, index):
        if index < 0 or self.is_updating_ui: return
        self.selected_dialogue_idx = index
        
        self.is_updating_ui = True
        step = self.project_data["scenes"][self.selected_scene_id]["dialogues"][index]
        
        # Load formatting
        self.diag_is_thought.setChecked(step.get("is_thought", False))
        self.diag_text_bold.setChecked(step.get("text_bold", False))
        self.diag_text_italic.setChecked(step.get("text_italic", False))
        
        # Populate character combos
        self.refresh_dialogue_char_combos()
        
        char_id = step.get("character_id", "")
        if char_id:
            c_idx = self.diag_char_combo.findData(char_id)
            if c_idx >= 0:
                self.diag_char_combo.setCurrentIndex(c_idx)
        else:
            self.diag_char_combo.setCurrentIndex(0) # [Без персонажа / Рассказчик]
            
        self.speaker_input.setText(step.get("speaker", ""))
        self.text_input.setPlainText(step.get("text", ""))
        
        # SFX setup
        sfx_path = step.get("sfx", "")
        self.diag_sfx_input.setText(sfx_path)
        self.refresh_sfx_combo_list()
        
        found_sfx = False
        if not sfx_path:
            self.diag_sfx_combo.setCurrentIndex(0) # [Без звука]
            self.sfx_raw_widget.hide()
            found_sfx = True
        else:
            sfx_lib = self.project_data["config"].get("sfx", {})
            for name, path in sfx_lib.items():
                if path == sfx_path:
                    sfx_idx = self.diag_sfx_combo.findText(name)
                    if sfx_idx >= 0:
                        self.diag_sfx_combo.setCurrentIndex(sfx_idx)
                        self.sfx_raw_widget.hide()
                        found_sfx = True
                        break
        if not found_sfx:
            self.diag_sfx_combo.setCurrentIndex(1) # [Вручную / Путь к файлу]
            self.sfx_raw_widget.show()
        
        # Populate sprites expressions combos
        self.refresh_dialogue_sprite_expr_combo()
        
        sprite = step.get("sprite", {})
        if sprite:
            img_path = sprite.get("image", "")
            self.sprite_input.setText(img_path)
            
            # Try to match to character sprite expression
            matched_expr = False
            if char_id and char_id in self.project_data["config"]["characters"]:
                char_info = self.project_data["config"]["characters"][char_id]
                sprites_map = char_info.get("sprites", {})
                for expr, expr_path in sprites_map.items():
                    if expr_path == img_path:
                        expr_idx = self.diag_sprite_expr_combo.findText(expr)
                        if expr_idx >= 0:
                            self.diag_sprite_expr_combo.setCurrentIndex(expr_idx)
                            self.sprite_raw_widget.hide()
                            matched_expr = True
                            break
            if not matched_expr:
                self.diag_sprite_expr_combo.setCurrentIndex(0) # [Вручную / Путь]
                self.sprite_raw_widget.show()
                
            pos = sprite.get("position", "center")
            if isinstance(pos, list):
                self.sprite_pos_type.setCurrentIndex(1) # Координаты X, Y (%)
                x = int(pos[0]) if len(pos) > 0 else 50
                y = int(pos[1]) if len(pos) > 1 else 0
                self.sprite_x_coord.setValue(x)
                self.sprite_y_coord.setValue(y)
                self.sprite_pos_combo.hide()
                self.sprite_x_coord.show()
                self.sprite_y_coord.show()
            elif isinstance(pos, (int, float)) or (isinstance(pos, str) and pos.strip().isdigit()):
                self.sprite_pos_type.setCurrentIndex(1)
                self.sprite_x_coord.setValue(int(pos))
                self.sprite_y_coord.setValue(0)
                self.sprite_pos_combo.hide()
                self.sprite_x_coord.show()
                self.sprite_y_coord.show()
            else:
                self.sprite_pos_type.setCurrentIndex(0) # Предустановка
                pos_idx = self.sprite_pos_combo.findText(str(pos).lower())
                if pos_idx >= 0: self.sprite_pos_combo.setCurrentIndex(pos_idx)
                self.sprite_pos_combo.show()
                self.sprite_x_coord.hide()
                self.sprite_y_coord.hide()
        else:
            self.sprite_input.clear()
            self.sprite_pos_type.setCurrentIndex(0)
            self.sprite_pos_combo.setCurrentIndex(0)
            self.sprite_pos_combo.show()
            self.sprite_x_coord.hide()
            self.sprite_y_coord.hide()
            self.diag_sprite_expr_combo.setCurrentIndex(0)
            self.sprite_raw_widget.show()
            
        self.toggle_thought_ui_state()
        self.is_updating_ui = False
        
    def clear_dialogue_fields(self):
        self.speaker_input.clear()
        self.text_input.clear()
        self.sprite_input.clear()
        self.diag_sfx_input.clear()
        self.sprite_pos_type.setCurrentIndex(0)
        self.sprite_pos_combo.setCurrentIndex(0)
        self.sprite_pos_combo.show()
        self.sprite_x_coord.hide()
        self.sprite_y_coord.hide()
        self.diag_is_thought.setChecked(False)
        self.diag_text_bold.setChecked(False)
        self.diag_text_italic.setChecked(False)
        self.diag_char_combo.setCurrentIndex(0)
        self.diag_sprite_expr_combo.setCurrentIndex(0)
        self.sprite_raw_widget.show()
        self.diag_sfx_combo.setCurrentIndex(0)
        self.sfx_raw_widget.hide()
        
    def save_current_dialogue_fields(self):
        if self.is_updating_ui or not self.selected_scene_id or self.selected_dialogue_idx is None:
            return
            
        scene = self.project_data["scenes"][self.selected_scene_id]
        step = scene["dialogues"][self.selected_dialogue_idx]
        
        step["is_thought"] = self.diag_is_thought.isChecked()
        step["text_bold"] = self.diag_text_bold.isChecked()
        step["text_italic"] = self.diag_text_italic.isChecked()
        step["sfx"] = self.diag_sfx_input.text().strip()
        
        # Save character details
        if step["is_thought"]:
            step["character_id"] = ""
            step["speaker"] = ""
        else:
            step["character_id"] = self.diag_char_combo.currentData() or ""
            step["speaker"] = self.speaker_input.text()
            
        step["text"] = self.text_input.toPlainText()
        
        # Save sprite details
        sprite_img = self.sprite_input.text()
        
        if self.sprite_pos_type.currentText() == "Координаты X, Y (%)":
            sprite_pos = [self.sprite_x_coord.value(), self.sprite_y_coord.value()]
        else:
            sprite_pos = self.sprite_pos_combo.currentText()
            
        step["sprite"] = {
            "position": sprite_pos,
            "image": sprite_img
        }
        
        # Update list item text
        self.is_updating_ui = True
        text_preview = step["text"][:30] + "..." if len(step["text"]) > 30 else step["text"]
        list_item = self.dialogue_list.item(self.selected_dialogue_idx)
        if list_item:
            if step["is_thought"]:
                list_item.setText(f"{self.selected_dialogue_idx+1}. 💭 ({text_preview})")
            else:
                list_item.setText(f"{self.selected_dialogue_idx+1}. [{step['speaker']}] {text_preview}")
        self.is_updating_ui = False

    def diag_is_thought_changed(self, state):
        self.toggle_thought_ui_state()
        self.save_current_dialogue_fields()
        
    def toggle_thought_ui_state(self):
        is_thought = self.diag_is_thought.isChecked()
        self.diag_char_combo.setDisabled(is_thought)
        self.speaker_input.setDisabled(is_thought)
        if is_thought:
            self.speaker_input.clear()

    def diag_char_combo_changed(self, index):
        if self.is_updating_ui: return
        
        char_id = self.diag_char_combo.currentData()
        if char_id:
            # Set default name
            char_info = self.project_data["config"]["characters"].get(char_id, {})
            self.speaker_input.setText(char_info.get("name", ""))
        else:
            self.speaker_input.clear()
            
        # Refresh sprite expressions
        self.refresh_dialogue_sprite_expr_combo()
        self.save_current_dialogue_fields()
        
    def diag_sprite_expr_changed(self, index):
        if self.is_updating_ui: return
        
        expr_name = self.diag_sprite_expr_combo.currentText()
        if expr_name == "[Вручную / Путь к файлу]":
            self.sprite_raw_widget.show()
        else:
            self.sprite_raw_widget.hide()
            # Find and set character sprite path
            char_id = self.diag_char_combo.currentData()
            if char_id:
                char_info = self.project_data["config"]["characters"].get(char_id, {})
                img_path = char_info.get("sprites", {}).get(expr_name, "")
                self.sprite_input.setText(img_path)
                
        self.save_current_dialogue_fields()

    def diag_sfx_combo_changed(self, index):
        if self.is_updating_ui: return
        
        sfx_name = self.diag_sfx_combo.currentText()
        if sfx_name == "[Без звука]":
            self.sfx_raw_widget.hide()
            self.diag_sfx_input.setText("")
        elif sfx_name == "[Вручную / Путь к файлу]":
            self.sfx_raw_widget.show()
        else:
            self.sfx_raw_widget.hide()
            sfx_lib = self.project_data["config"].get("sfx", {})
            self.diag_sfx_input.setText(sfx_lib.get(sfx_name, ""))
            
        self.save_current_dialogue_fields()

    def refresh_dialogue_char_combos(self):
        # Temp save selection
        curr = self.diag_char_combo.currentData()
        
        self.is_updating_ui = True
        self.diag_char_combo.clear()
        self.diag_char_combo.addItem("[Без персонажа / Рассказчик]", "")
        
        chars = self.project_data["config"].get("characters", {})
        for c_id, c_info in chars.items():
            self.diag_char_combo.addItem(c_info.get("name", c_id), c_id)
            
        idx = self.diag_char_combo.findData(curr)
        if idx >= 0:
            self.diag_char_combo.setCurrentIndex(idx)
        self.is_updating_ui = False

    def refresh_dialogue_sprite_expr_combo(self):
        curr_expr = self.diag_sprite_expr_combo.currentText()
        
        self.is_updating_ui = True
        self.diag_sprite_expr_combo.clear()
        self.diag_sprite_expr_combo.addItem("[Вручную / Путь к файлу]")
        
        char_id = self.diag_char_combo.currentData()
        if char_id:
            char_info = self.project_data["config"]["characters"].get(char_id, {})
            sprites_map = char_info.get("sprites", {})
            for expr in sprites_map.keys():
                self.diag_sprite_expr_combo.addItem(expr)
                
        idx = self.diag_sprite_expr_combo.findText(curr_expr)
        if idx >= 0:
            self.diag_sprite_expr_combo.setCurrentIndex(idx)
        self.is_updating_ui = False

    def browse_sprite_image(self):
        if self.selected_dialogue_idx is None: return
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Выбрать спрайт персонажа", "", "Спрайты (*.png *.webp)"
        )
        if file_path:
            self.sprite_input.setText(file_path)

    def browse_dialogue_sfx(self):
        if self.selected_dialogue_idx is None: return
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Выбрать SFX звуковой эффект", "", "Звуки (*.mp3 *.ogg *.wav)"
        )
        if file_path:
            self.diag_sfx_input.setText(file_path)
            
    def move_dialogue_up(self):
        if not self.selected_scene_id or self.selected_dialogue_idx is None or self.selected_dialogue_idx == 0:
            return
        idx = self.selected_dialogue_idx
        scene = self.project_data["scenes"][self.selected_scene_id]
        
        scene["dialogues"][idx], scene["dialogues"][idx-1] = scene["dialogues"][idx-1], scene["dialogues"][idx]
        self.refresh_selected_scene_ui()
        self.dialogue_list.setCurrentRow(idx-1)
        
    def move_dialogue_down(self):
        if not self.selected_scene_id or self.selected_dialogue_idx is None:
            return
        scene = self.project_data["scenes"][self.selected_scene_id]
        idx = self.selected_dialogue_idx
        if idx >= len(scene["dialogues"]) - 1:
            return
            
        scene["dialogues"][idx], scene["dialogues"][idx+1] = scene["dialogues"][idx+1], scene["dialogues"][idx]
        self.refresh_selected_scene_ui()
        self.dialogue_list.setCurrentRow(idx+1)

    # Choices CRUD & Edit
    def add_choice(self):
        if not self.selected_scene_id: return
        scene = self.project_data["scenes"][self.selected_scene_id]
        
        new_choice = {
            "text": "Новый вариант выбора",
            "next_scene": ""
        }
        scene["choices"].append(new_choice)
        self.refresh_selected_scene_ui()
        self.choices_list.setCurrentRow(len(scene["choices"]) - 1)
        
    def delete_choice(self):
        if not self.selected_scene_id or self.selected_choice_idx is None: return
        scene = self.project_data["scenes"][self.selected_scene_id]
        
        del scene["choices"][self.selected_choice_idx]
        self.selected_choice_idx = None
        self.refresh_selected_scene_ui()
        
    def choice_selected(self, index):
        if index < 0 or self.is_updating_ui: return
        self.selected_choice_idx = index
        
        self.is_updating_ui = True
        choice = self.project_data["scenes"][self.selected_scene_id]["choices"][index]
        self.choice_text_input.setText(choice.get("text", ""))
        
        target = choice.get("next_scene", "")
        idx = self.choice_target_combo.findData(target)
        if idx >= 0: self.choice_target_combo.setCurrentIndex(idx)
        
        self.is_updating_ui = False
        
    def save_choice_fields(self):
        if self.is_updating_ui or not self.selected_scene_id or self.selected_choice_idx is None:
            return
            
        scene = self.project_data["scenes"][self.selected_scene_id]
        choice = scene["choices"][self.selected_choice_idx]
        
        choice["text"] = self.choice_text_input.text()
        choice["next_scene"] = self.choice_target_combo.currentData()
        
        self.is_updating_ui = True
        list_item = self.choices_list.item(self.selected_choice_idx)
        if list_item:
            list_item.setText(f"Выбор: {choice['text']} -> {choice['next_scene']}")
        self.is_updating_ui = False
        
    def update_scene_jump(self, index):
        if self.is_updating_ui or not self.selected_scene_id: return
        self.project_data["scenes"][self.selected_scene_id]["next_scene"] = self.next_scene_combo.currentData()

    def browse_export_directory(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Выбрать папку экспорта", self.export_dir_input.text())
        if dir_path:
            self.export_dir_input.setText(os.path.abspath(dir_path))

    # ASSETS LIBRARY OPERATIONS
    def refresh_assets_tab_lists(self):
        self.is_updating_ui = True
        
        # 1. Populate character list
        self.char_lib_list.clear()
        chars = self.project_data["config"].get("characters", {})
        for char_id, char_info in chars.items():
            self.char_lib_list.addItem(QListWidgetItem(f"{char_info.get('name', char_id)} ({char_id})"))
            
        # 2. Populate backgrounds list
        self.bg_lib_list.clear()
        bgs = self.project_data["config"].get("backgrounds", {})
        for bg_name in bgs.keys():
            self.bg_lib_list.addItem(QListWidgetItem(bg_name))
            
        # 3. Populate Music list
        self.music_lib_list.clear()
        music = self.project_data["config"].get("music", {})
        for music_name in music.keys():
            self.music_lib_list.addItem(QListWidgetItem(music_name))
            
        # 4. Populate SFX list
        self.sfx_lib_list.clear()
        sfx = self.project_data["config"].get("sfx", {})
        for sfx_name in sfx.keys():
            self.sfx_lib_list.addItem(QListWidgetItem(sfx_name))
            
        # Hide properties subpanels
        self.char_props_panel.hide()
        self.bg_props_panel.hide()
        self.music_props_widget.hide()
        self.sfx_props_widget.hide()
        
        self.selected_char_id = None
        self.selected_bg_lib_name = None
        self.selected_music_lib_name = None
        self.selected_sfx_lib_name = None
        
        self.is_updating_ui = False
        
    def refresh_bg_combo_list(self):
        curr_selection = self.scene_bg_combo.currentText()
        
        self.is_updating_ui = True
        self.scene_bg_combo.clear()
        self.scene_bg_combo.addItem("[Вручную / Цвет]")
        
        bgs = self.project_data["config"].get("backgrounds", {})
        for name in bgs.keys():
            self.scene_bg_combo.addItem(name)
            
        idx = self.scene_bg_combo.findText(curr_selection)
        if idx >= 0:
            self.scene_bg_combo.setCurrentIndex(idx)
        self.is_updating_ui = False

    def refresh_bgm_combo_list(self):
        curr_selection = self.scene_bgm_combo.currentText()
        
        self.is_updating_ui = True
        self.scene_bgm_combo.clear()
        self.scene_bgm_combo.addItem("[Без изменений]")
        self.scene_bgm_combo.addItem("[Остановить музыку]")
        self.scene_bgm_combo.addItem("[Вручную / Путь к файлу]")
        
        music = self.project_data["config"].get("music", {})
        for name in music.keys():
            self.scene_bgm_combo.addItem(name)
            
        idx = self.scene_bgm_combo.findText(curr_selection)
        if idx >= 0:
            self.scene_bgm_combo.setCurrentIndex(idx)
        self.is_updating_ui = False

    def refresh_sfx_combo_list(self):
        curr_selection = self.diag_sfx_combo.currentText()
        
        self.is_updating_ui = True
        self.diag_sfx_combo.clear()
        self.diag_sfx_combo.addItem("[Без звука]")
        self.diag_sfx_combo.addItem("[Вручную / Путь к файлу]")
        
        sfx = self.project_data["config"].get("sfx", {})
        for name in sfx.keys():
            self.diag_sfx_combo.addItem(name)
            
        idx = self.diag_sfx_combo.findText(curr_selection)
        if idx >= 0:
            self.diag_sfx_combo.setCurrentIndex(idx)
        self.is_updating_ui = False

    # Character actions
    def add_character(self):
        name, ok = QInputDialog.getText(self, "Добавить персонажа", "Укажите ID (латиницей, например: anton):")
        if not ok or not name.strip(): return
        
        char_id = name.strip().lower().replace(" ", "_")
        if char_id in self.project_data["config"]["characters"]:
            QMessageBox.warning(self, "Ошибка", "Персонаж с таким ID уже существует.")
            return
            
        display_name, ok2 = QInputDialog.getText(self, "Имя персонажа", "Отображаемое имя:")
        if not ok2 or not display_name.strip(): return
        
        self.project_data["config"]["characters"][char_id] = {
            "name": display_name.strip(),
            "color": "#ffffff",
            "sprites": {}
        }
        
        self.refresh_assets_tab_lists()
        row = list(self.project_data["config"]["characters"].keys()).index(char_id)
        self.char_lib_list.setCurrentRow(row)
        self.refresh_scene_comboboxes()
        
    def delete_character(self):
        if not self.selected_char_id: return
        confirm = QMessageBox.question(self, "Удаление", f"Удалить персонажа '{self.selected_char_id}'?")
        if confirm == QMessageBox.Yes:
            del self.project_data["config"]["characters"][self.selected_char_id]
            self.selected_char_id = None
            self.refresh_assets_tab_lists()
            self.refresh_scene_comboboxes()
            
    def character_selected(self, index):
        if index < 0 or self.is_updating_ui: return
        
        self.selected_char_id = list(self.project_data["config"]["characters"].keys())[index]
        self.is_updating_ui = True
        
        char_info = self.project_data["config"]["characters"][self.selected_char_id]
        self.char_name_input.setText(char_info.get("name", ""))
        self.char_color_input.setText(char_info.get("color", "#ffffff"))
        
        # Populate character sprites list
        self.char_sprites_list.clear()
        for expr in char_info.get("sprites", {}).keys():
            self.char_sprites_list.addItem(expr)
            
        self.sprite_name_input.clear()
        self.sprite_path_input.clear()
        self.selected_char_sprite_idx = None
        
        self.char_props_panel.show()
        self.is_updating_ui = False
        
    def char_field_changed(self):
        if self.is_updating_ui or not self.selected_char_id: return
        char_info = self.project_data["config"]["characters"][self.selected_char_id]
        
        char_info["name"] = self.char_name_input.text()
        char_info["color"] = self.char_color_input.text()
        
        # Update display item in list
        self.is_updating_ui = True
        curr_row = self.char_lib_list.currentRow()
        list_item = self.char_lib_list.item(curr_row)
        if list_item:
            list_item.setText(f"{char_info['name']} ({self.selected_char_id})")
        self.is_updating_ui = False
        self.refresh_scene_comboboxes()
        
    # Character Sprites actions
    def add_char_sprite(self):
        if not self.selected_char_id: return
        name, ok = QInputDialog.getText(self, "Добавить эмоцию", "Назовите эмоцию (например: Злость):")
        if not ok or not name.strip(): return
        
        expr_name = name.strip()
        char_info = self.project_data["config"]["characters"][self.selected_char_id]
        if expr_name in char_info.get("sprites", {}):
            QMessageBox.warning(self, "Ошибка", "Такая эмоция уже создана.")
            return
            
        char_info["sprites"][expr_name] = ""
        
        self.is_updating_ui = True
        self.char_sprites_list.addItem(expr_name)
        self.is_updating_ui = False
        
        row = self.char_sprites_list.count() - 1
        self.char_sprites_list.setCurrentRow(row)
        self.refresh_scene_comboboxes()
        
    def delete_char_sprite(self):
        if not self.selected_char_id or self.selected_char_sprite_idx is None: return
        char_info = self.project_data["config"]["characters"][self.selected_char_id]
        expr_name = self.char_sprites_list.item(self.selected_char_sprite_idx).text()
        
        confirm = QMessageBox.question(self, "Удаление", f"Удалить спрайт '{expr_name}'?")
        if confirm == QMessageBox.Yes:
            del char_info["sprites"][expr_name]
            self.selected_char_sprite_idx = None
            
            self.is_updating_ui = True
            self.char_sprites_list.clear()
            for expr in char_info.get("sprites", {}).keys():
                self.char_sprites_list.addItem(expr)
            self.sprite_name_input.clear()
            self.sprite_path_input.clear()
            self.is_updating_ui = False
            self.refresh_scene_comboboxes()
            
    def char_sprite_selected(self, index):
        if index < 0 or self.is_updating_ui: return
        self.selected_char_sprite_idx = index
        
        self.is_updating_ui = True
        expr_name = self.char_sprites_list.item(index).text()
        char_info = self.project_data["config"]["characters"][self.selected_char_id]
        img_path = char_info["sprites"].get(expr_name, "")
        
        self.sprite_name_input.setText(expr_name)
        self.sprite_path_input.setText(img_path)
        self.is_updating_ui = False
        
    def char_sprite_field_changed(self):
        if self.is_updating_ui or not self.selected_char_id or self.selected_char_sprite_idx is None: return
        
        char_info = self.project_data["config"]["characters"][self.selected_char_id]
        old_name = self.char_sprites_list.item(self.selected_char_sprite_idx).text()
        new_name = self.sprite_name_input.text().strip()
        img_path = self.sprite_path_input.text().strip()
        
        if not new_name: return
        
        if old_name != new_name:
            if new_name in char_info["sprites"]:
                QMessageBox.warning(self, "Ошибка", "Название эмоции должно быть уникальным.")
                return
            del char_info["sprites"][old_name]
            
        char_info["sprites"][new_name] = img_path
        
        self.is_updating_ui = True
        self.char_sprites_list.item(self.selected_char_sprite_idx).setText(new_name)
        self.is_updating_ui = False
        self.refresh_scene_comboboxes()
        
    def browse_char_sprite_path(self):
        if self.selected_char_sprite_idx is None: return
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Выбрать спрайт эмоции", "", "Изображения (*.png *.webp)"
        )
        if file_path:
            self.sprite_path_input.setText(file_path)

    # Background Library actions
    def add_bg_lib(self):
        name, ok = QInputDialog.getText(self, "Добавить фон в библиотеку", "Название фона (например: Кабинет):")
        if not ok or not name.strip(): return
        
        bg_name = name.strip()
        bg_lib = self.project_data["config"].get("backgrounds", {})
        if bg_name in bg_lib:
            QMessageBox.warning(self, "Ошибка", "Фон с таким именем уже существует.")
            return
            
        bg_lib[bg_name] = ""
        self.refresh_assets_tab_lists()
        
        row = list(bg_lib.keys()).index(bg_name)
        self.bg_lib_list.setCurrentRow(row)
        self.refresh_bg_combo_list()
        
    def delete_bg_lib(self):
        if not self.selected_bg_lib_name: return
        confirm = QMessageBox.question(self, "Удаление", f"Удалить фон '{self.selected_bg_lib_name}'?")
        if confirm == QMessageBox.Yes:
            bg_lib = self.project_data["config"].get("backgrounds", {})
            del bg_lib[self.selected_bg_lib_name]
            self.selected_bg_lib_name = None
            self.refresh_assets_tab_lists()
            self.refresh_bg_combo_list()
            
    def bg_lib_selected(self, index):
        if index < 0 or self.is_updating_ui: return
        self.selected_bg_lib_name = list(self.project_data["config"]["backgrounds"].keys())[index]
        
        self.is_updating_ui = True
        bg_lib = self.project_data["config"].get("backgrounds", {})
        self.bg_name_input.setText(self.selected_bg_lib_name)
        self.bg_path_input.setText(bg_lib.get(self.selected_bg_lib_name, ""))
        self.bg_props_panel.show()
        self.is_updating_ui = False
        
    def bg_lib_field_changed(self):
        if self.is_updating_ui or not self.selected_bg_lib_name: return
        bg_lib = self.project_data["config"].get("backgrounds", {})
        
        old_name = self.selected_bg_lib_name
        new_name = self.bg_name_input.text().strip()
        bg_path = self.bg_path_input.text().strip()
        
        if not new_name: return
        
        if old_name != new_name:
            if new_name in bg_lib:
                QMessageBox.warning(self, "Ошибка", "Фон с таким именем уже существует.")
                return
            del bg_lib[old_name]
            self.selected_bg_lib_name = new_name
            
        bg_lib[new_name] = bg_path
        
        self.is_updating_ui = True
        curr_row = self.bg_lib_list.currentRow()
        list_item = self.bg_lib_list.item(curr_row)
        if list_item:
            list_item.setText(new_name)
        self.is_updating_ui = False
        self.refresh_bg_combo_list()
        
    def browse_bg_lib_path(self):
        if not self.selected_bg_lib_name: return
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Выбрать файл фона", "", "Изображения (*.png *.jpg *.jpeg *.webp)"
        )
        if file_path:
            self.bg_path_input.setText(file_path)

    # Music Library actions
    def add_music_lib(self):
        name, ok = QInputDialog.getText(self, "Добавить BGM", "Название композиции (например: Главная Тема):")
        if not ok or not name.strip(): return
        
        music_name = name.strip()
        music_lib = self.project_data["config"].get("music", {})
        if music_name in music_lib:
            QMessageBox.warning(self, "Ошибка", "Аудио с таким названием уже есть.")
            return
            
        music_lib[music_name] = ""
        self.refresh_assets_tab_lists()
        
        row = list(music_lib.keys()).index(music_name)
        self.music_lib_list.setCurrentRow(row)
        self.refresh_bgm_combo_list()
        
    def delete_music_lib(self):
        if not self.selected_music_lib_name: return
        confirm = QMessageBox.question(self, "Удаление", f"Удалить композицию '{self.selected_music_lib_name}'?")
        if confirm == QMessageBox.Yes:
            music_lib = self.project_data["config"].get("music", {})
            del music_lib[self.selected_music_lib_name]
            self.selected_music_lib_name = None
            self.refresh_assets_tab_lists()
            self.refresh_bgm_combo_list()
            
    def music_lib_selected(self, index):
        if index < 0 or self.is_updating_ui: return
        self.selected_music_lib_name = list(self.project_data["config"]["music"].keys())[index]
        
        self.is_updating_ui = True
        music_lib = self.project_data["config"].get("music", {})
        self.music_name_input.setText(self.selected_music_lib_name)
        self.music_path_input.setText(music_lib.get(self.selected_music_lib_name, ""))
        self.music_props_widget.show()
        self.is_updating_ui = False
        
    def music_lib_field_changed(self):
        if self.is_updating_ui or not self.selected_music_lib_name: return
        music_lib = self.project_data["config"].get("music", {})
        
        old_name = self.selected_music_lib_name
        new_name = self.music_name_input.text().strip()
        m_path = self.music_path_input.text().strip()
        
        if not new_name: return
        
        if old_name != new_name:
            if new_name in music_lib:
                QMessageBox.warning(self, "Ошибка", "Название BGM должно быть уникальным.")
                return
            del music_lib[old_name]
            self.selected_music_lib_name = new_name
            
        music_lib[new_name] = m_path
        
        self.is_updating_ui = True
        curr_row = self.music_lib_list.currentRow()
        list_item = self.music_lib_list.item(curr_row)
        if list_item:
            list_item.setText(new_name)
        self.is_updating_ui = False
        self.refresh_bgm_combo_list()
        
    def browse_music_lib_path(self):
        if not self.selected_music_lib_name: return
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Выбрать файл фоновой музыки", "", "Аудио (*.mp3 *.ogg *.wav)"
        )
        if file_path:
            self.music_path_input.setText(file_path)

    # SFX Library actions
    def add_sfx_lib(self):
        name, ok = QInputDialog.getText(self, "Добавить SFX", "Название эффекта (например: Стук в дверь):")
        if not ok or not name.strip(): return
        
        sfx_name = name.strip()
        sfx_lib = self.project_data["config"].get("sfx", {})
        if sfx_name in sfx_lib:
            QMessageBox.warning(self, "Ошибка", "SFX с таким названием уже есть.")
            return
            
        sfx_lib[sfx_name] = ""
        self.refresh_assets_tab_lists()
        
        row = list(sfx_lib.keys()).index(sfx_name)
        self.sfx_lib_list.setCurrentRow(row)
        self.refresh_sfx_combo_list()
        
    def delete_sfx_lib(self):
        if not self.selected_sfx_lib_name: return
        confirm = QMessageBox.question(self, "Удаление", f"Удалить эффект '{self.selected_sfx_lib_name}'?")
        if confirm == QMessageBox.Yes:
            sfx_lib = self.project_data["config"].get("sfx", {})
            del sfx_lib[self.selected_sfx_lib_name]
            self.selected_sfx_lib_name = None
            self.refresh_assets_tab_lists()
            self.refresh_sfx_combo_list()
            
    def sfx_lib_selected(self, index):
        if index < 0 or self.is_updating_ui: return
        self.selected_sfx_lib_name = list(self.project_data["config"]["sfx"].keys())[index]
        
        self.is_updating_ui = True
        sfx_lib = self.project_data["config"].get("sfx", {})
        self.sfx_name_input.setText(self.selected_sfx_lib_name)
        self.sfx_path_input.setText(sfx_lib.get(self.selected_sfx_lib_name, ""))
        self.sfx_props_widget.show()
        self.is_updating_ui = False
        
    def sfx_lib_field_changed(self):
        if self.is_updating_ui or not self.selected_sfx_lib_name: return
        sfx_lib = self.project_data["config"].get("sfx", {})
        
        old_name = self.selected_sfx_lib_name
        new_name = self.sfx_name_input.text().strip()
        s_path = self.sfx_path_input.text().strip()
        
        if not new_name: return
        
        if old_name != new_name:
            if new_name in sfx_lib:
                QMessageBox.warning(self, "Ошибка", "Название SFX должно быть уникальным.")
                return
            del sfx_lib[old_name]
            self.selected_sfx_lib_name = new_name
            
        sfx_lib[new_name] = s_path
        
        self.is_updating_ui = True
        curr_row = self.sfx_lib_list.currentRow()
        list_item = self.sfx_lib_list.item(curr_row)
        if list_item:
            list_item.setText(new_name)
        self.is_updating_ui = False
        self.refresh_sfx_combo_list()
        
    def browse_sfx_lib_path(self):
        if not self.selected_sfx_lib_name: return
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Выбрать файл звукового эффекта", "", "Аудио (*.mp3 *.ogg *.wav)"
        )
        if file_path:
            self.sfx_path_input.setText(file_path)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor("#0f0f14"))
    palette.setColor(QPalette.WindowText, QColor("#e0e0e9"))
    palette.setColor(QPalette.Base, QColor("#12121d"))
    palette.setColor(QPalette.AlternateBase, QColor("#151522"))
    palette.setColor(QPalette.ToolTipBase, QColor("#1a1a24"))
    palette.setColor(QPalette.ToolTipText, QColor("#e0e0e9"))
    palette.setColor(QPalette.Text, QColor("#f0f0f5"))
    palette.setColor(QPalette.Button, QColor("#2a2a3e"))
    palette.setColor(QPalette.ButtonText, QColor("#ffffff"))
    palette.setColor(QPalette.BrightText, QColor("#ffcc00"))
    palette.setColor(QPalette.Highlight, QColor("#2d2d44"))
    palette.setColor(QPalette.HighlightedText, QColor("#ffcc00"))
    app.setPalette(palette)
    
    editor = VisualNovelEditor()
    editor.show()
    sys.exit(app.exec())
