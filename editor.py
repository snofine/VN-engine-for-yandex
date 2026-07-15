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
QScrollBar::handle:vertical {
    background: #2d2d42;
    min-height: 20px;
    border-radius: 5px;
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
        self.resize(1200, 850)
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
                "gui_profile": "Дефолтный"
            },
            "gui": dict(GUI_PRESETS["Дефолтный"]),
            "scenes": {}
        }
        
        self.selected_scene_id = None
        self.selected_dialogue_idx = None
        self.selected_choice_idx = None
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
        
        # Scene buttons layout
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
        
        # Right Panel: Tabs for Editor and settings
        right_tab_widget = QTabWidget()
        main_splitter.addWidget(right_tab_widget)
        
        # TAB 1: SCENE EDITOR
        scene_editor_tab = QWidget()
        scene_editor_layout = QVBoxLayout(scene_editor_tab)
        
        # Scene properties (Background)
        bg_group = QGroupBox("Задний фон сцены")
        bg_layout = QHBoxLayout(bg_group)
        self.bg_input = QLineEdit()
        self.bg_input.setPlaceholderText("Путь к файлу картинки или HEX-код цвета (#14141f)")
        self.bg_input.textChanged.connect(self.update_scene_bg)
        bg_layout.addWidget(self.bg_input)
        
        bg_browse_btn = QPushButton("Выбрать файл")
        bg_browse_btn.clicked.connect(self.browse_bg_image)
        bg_layout.addWidget(bg_browse_btn)
        scene_editor_layout.addWidget(bg_group)
        
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
        
        self.speaker_input = QLineEdit()
        self.speaker_input.setPlaceholderText("Имя говорящего персонажа")
        self.speaker_input.textChanged.connect(self.save_current_dialogue_fields)
        diag_detail_layout.addRow("Имя:", self.speaker_input)
        
        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText("Текст, который отобразится на экране новеллы...")
        self.text_input.textChanged.connect(self.save_current_dialogue_fields)
        diag_detail_layout.addRow("Текст реплики:", self.text_input)
        
        # Sprite settings
        sprite_layout = QHBoxLayout()
        self.sprite_input = QLineEdit()
        self.sprite_input.setPlaceholderText("Файл спрайта (.png)")
        self.sprite_input.textChanged.connect(self.save_current_dialogue_fields)
        sprite_layout.addWidget(self.sprite_input)
        
        sprite_browse = QPushButton("Обзор")
        sprite_browse.clicked.connect(self.browse_sprite_image)
        sprite_layout.addWidget(sprite_browse)
        diag_detail_layout.addRow("Спрайт перс.:", sprite_layout)
        
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
        
        # Active Choice Editor
        self.choice_text_input = QLineEdit()
        self.choice_text_input.setPlaceholderText("Текст на кнопке выбора")
        self.choice_text_input.textChanged.connect(self.save_choice_fields)
        choices_layout.addWidget(self.choice_text_input)
        
        self.choice_target_combo = QComboBox()
        self.choice_target_combo.currentIndexChanged.connect(self.save_choice_fields)
        choices_layout.addWidget(self.choice_target_combo)
        
        # Jump target if no choices
        choices_layout.addWidget(QFrame(frameShape=QFrame.HLine))
        choices_layout.addWidget(QLabel("<b>Или автоматический переход:</b>"))
        
        self.next_scene_combo = QComboBox()
        self.next_scene_combo.currentIndexChanged.connect(self.update_scene_jump)
        choices_layout.addWidget(self.next_scene_combo)
        
        details_splitter.addWidget(choices_panel)
        
        right_tab_widget.addTab(scene_editor_tab, "🎬 Редактор Сцен")
        
        # TAB 2: MONETIZATION SETTINGS
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
        
        # TAB 3: GUI CUSTOMIZATION (NEW)
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
        
        # Custom elements group
        self.gui_custom_group = QGroupBox("Параметры кастомизации интерфейса")
        self.gui_custom_layout = QFormLayout(self.gui_custom_group)
        self.gui_custom_layout.setSpacing(10)
        
        # Panel Height
        self.gui_dialogue_height = QSpinBox()
        self.gui_dialogue_height.setRange(100, 350)
        self.gui_dialogue_height.setValue(180)
        self.gui_dialogue_height.setSuffix(" px")
        self.gui_dialogue_height.valueChanged.connect(self.gui_field_changed)
        self.gui_custom_layout.addRow("Высота панели диалога:", self.gui_dialogue_height)
        
        # Dialogue Panel BG Color
        self.gui_panel_bg = QLineEdit()
        self.gui_panel_bg.textChanged.connect(self.gui_field_changed)
        panel_bg_btn = QPushButton("Цвет")
        panel_bg_btn.clicked.connect(lambda: self.choose_color(self.gui_panel_bg))
        panel_bg_layout = QHBoxLayout()
        panel_bg_layout.addWidget(self.gui_panel_bg)
        panel_bg_layout.addWidget(panel_bg_btn)
        self.gui_custom_layout.addRow("Фон панели (rgba/hex):", panel_bg_layout)
        
        # Dialogue Panel Border Color
        self.gui_panel_border = QLineEdit()
        self.gui_panel_border.textChanged.connect(self.gui_field_changed)
        panel_border_btn = QPushButton("Цвет")
        panel_border_btn.clicked.connect(lambda: self.choose_color(self.gui_panel_border))
        panel_border_layout = QHBoxLayout()
        panel_border_layout.addWidget(self.gui_panel_border)
        panel_border_layout.addWidget(panel_border_btn)
        self.gui_custom_layout.addRow("Рамка панели (rgba/hex):", panel_border_layout)
        
        # Dialogue Panel Border Radius
        self.gui_panel_radius = QSpinBox()
        self.gui_panel_radius.setRange(0, 50)
        self.gui_panel_radius.setValue(12)
        self.gui_panel_radius.setSuffix(" px")
        self.gui_panel_radius.valueChanged.connect(self.gui_field_changed)
        self.gui_custom_layout.addRow("Скругление углов панели:", self.gui_panel_radius)
        
        # Text settings
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
        
        # Speaker Name settings
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
        
        # Choice Buttons settings
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
        
        # TAB 4: PROJECT SETTINGS
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
        scene_splitter.setSizes([400, 400])
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
                "gui_profile": "Дефолтный"
            },
            "gui": dict(GUI_PRESETS["Дефолтный"]),
            "scenes": {
                "scene_1": {
                    "background": "#14141f",
                    "dialogues": [
                        {
                            "speaker": "Алиса",
                            "text": "Привет! Это твоя первая сцена.",
                            "sprite": {"position": "center", "image": ""}
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
            
            # Simple validation
            if "config" not in data or "scenes" not in data:
                raise ValueError("Некорректный формат файла проекта.")
                
            self.project_path = file_path
            self.project_data = data
            self.refresh_all_ui()
            
            # Select start scene or first scene
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
            
        # Run export
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

    # GUI Profile handlers
    def gui_profile_changed(self, index):
        profile_name = self.gui_profile_combo.currentText()
        
        if profile_name != "Пользовательский":
            preset_data = GUI_PRESETS[profile_name]
            self.is_updating_ui = True
            self.load_gui_fields(preset_data)
            self.is_updating_ui = False
            self.set_gui_fields_enabled(False)
            # Override project gui dictionary with preset clone
            self.project_data["gui"] = dict(preset_data)
        else:
            self.set_gui_fields_enabled(True)
            
        self.project_data["config"]["gui_profile"] = profile_name

    def gui_field_changed(self):
        if self.is_updating_ui:
            return
        # If user edits fields in custom mode, we sync it
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
        # Parse rgb/rgba or hex for QColorDialog initializer if possible
        init_color = QColor("#ffcc00")
        if current_color_str.startswith("#"):
            init_color = QColor(current_color_str)
            
        color = QColorDialog.getColor(init_color, self, "Выберите цвет")
        if color.isValid():
            # If current string was rgba, output as rgba, otherwise hex
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
        
        self.bg_input.setText(scene.get("background", ""))
        
        self.dialogue_list.clear()
        for idx, diag in enumerate(scene.get("dialogues", [])):
            text_preview = diag.get("text", "")[:30] + "..." if len(diag.get("text", "")) > 30 else diag.get("text", "")
            speaker = diag.get("speaker", "Без имени")
            self.dialogue_list.addItem(f"{idx+1}. [{speaker}] {text_preview}")
            
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

    def browse_bg_image(self):
        if not self.selected_scene_id: return
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Выбрать фоновое изображение", "", "Изображения (*.png *.jpg *.jpeg *.webp)"
        )
        if file_path:
            self.bg_input.setText(file_path)

    # Dialogue steps CRUD & Edit
    def add_dialogue(self):
        if not self.selected_scene_id: return
        scene = self.project_data["scenes"][self.selected_scene_id]
        
        new_step = {
            "speaker": "Алиса" if len(scene["dialogues"]) > 0 else "Рассказчик",
            "text": "Новая реплика диалога...",
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
        
        self.speaker_input.setText(step.get("speaker", ""))
        self.text_input.setPlainText(step.get("text", ""))
        
        sprite = step.get("sprite", {})
        if sprite:
            self.sprite_input.setText(sprite.get("image", ""))
            pos = sprite.get("position", "center")
            
            # Check if position is an array/list of X, Y
            if isinstance(pos, list):
                self.sprite_pos_type.setCurrentIndex(1) # Координаты X, Y (%)
                x = int(pos[0]) if len(pos) > 0 else 50
                y = int(pos[1]) if len(pos) > 1 else 0
                self.sprite_x_coord.setValue(x)
                self.sprite_y_coord.setValue(y)
                self.sprite_pos_combo.hide()
                self.sprite_x_coord.show()
                self.sprite_y_coord.show()
            # Check if position is a single numeric value (X only)
            elif isinstance(pos, (int, float)) or (isinstance(pos, str) and pos.strip().isdigit()):
                self.sprite_pos_type.setCurrentIndex(1) # Координаты X, Y (%)
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
            
        self.is_updating_ui = False
        
    def clear_dialogue_fields(self):
        self.speaker_input.clear()
        self.text_input.clear()
        self.sprite_input.clear()
        self.sprite_pos_type.setCurrentIndex(0)
        self.sprite_pos_combo.setCurrentIndex(0)
        self.sprite_pos_combo.show()
        self.sprite_x_coord.hide()
        self.sprite_y_coord.hide()
        
    def save_current_dialogue_fields(self):
        if self.is_updating_ui or not self.selected_scene_id or self.selected_dialogue_idx is None:
            return
            
        scene = self.project_data["scenes"][self.selected_scene_id]
        step = scene["dialogues"][self.selected_dialogue_idx]
        
        step["speaker"] = self.speaker_input.text()
        step["text"] = self.text_input.toPlainText()
        
        sprite_img = self.sprite_input.text()
        
        if self.sprite_pos_type.currentText() == "Координаты X, Y (%)":
            sprite_pos = [self.sprite_x_coord.value(), self.sprite_y_coord.value()]
        else:
            sprite_pos = self.sprite_pos_combo.currentText()
            
        step["sprite"] = {
            "position": sprite_pos,
            "image": sprite_img
        }
        
        self.is_updating_ui = True
        text_preview = step["text"][:30] + "..." if len(step["text"]) > 30 else step["text"]
        list_item = self.dialogue_list.item(self.selected_dialogue_idx)
        if list_item:
            list_item.setText(f"{self.selected_dialogue_idx+1}. [{step['speaker']}] {text_preview}")
        self.is_updating_ui = False

    def browse_sprite_image(self):
        if self.selected_dialogue_idx is None: return
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Выбрать спрайт персонажа", "", "Спрайты (*.png *.webp)"
        )
        if file_path:
            self.sprite_input.setText(file_path)
            
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
