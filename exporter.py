# exporter.py - Visual Novel Exporter Module for HTML5/Yandex Games
import os
import json
import shutil

TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")

def export_project(project_data, export_dir):
    """
    Exports a visual novel project to HTML5 (Yandex Games format).
    :param project_data: dict containing 'config', 'gui', and 'scenes'
    :param export_dir: absolute path to export directory
    :return: (bool, str) status and message
    """
    try:
        # Create export directory if it doesn't exist
        os.makedirs(export_dir, exist_ok=True)
        assets_dest_dir = os.path.join(export_dir, "assets")
        os.makedirs(assets_dest_dir, exist_ok=True)

        exported_data = json.loads(json.dumps(project_data)) # deep copy
        assets_to_copy = [] # list of (source_path, dest_filename)

        def process_asset_path(url_or_path):
            if not url_or_path:
                return url_or_path
            # If it's a web URL or color, leave it as is
            if url_or_path.startswith("http://") or url_or_path.startswith("https://") or url_or_path.startswith("data:"):
                return url_or_path
            # Check if it looks like a hex color
            if url_or_path.startswith("#") or url_or_path.startswith("rgba") or url_or_path.startswith("rgb"):
                return url_or_path
            # If it's a file path, we copy it to assets/ and use relative path
            if os.path.exists(url_or_path):
                filename = os.path.basename(url_or_path)
                dest_path = os.path.join(assets_dest_dir, filename)
                assets_to_copy.append((url_or_path, dest_path))
                return f"assets/{filename}"
            return url_or_path

        # 1. Process backgrounds library assets
        config = exported_data.get("config", {})
        bg_lib = config.get("backgrounds", {})
        for bg_name, bg_path in list(bg_lib.items()):
            bg_lib[bg_name] = process_asset_path(bg_path)

        # 2. Process character library assets
        char_lib = config.get("characters", {})
        for char_id, char_info in char_lib.items():
            sprites_map = char_info.get("sprites", {})
            for expr_name, img_path in list(sprites_map.items()):
                sprites_map[expr_name] = process_asset_path(img_path)

        # 2.5 Process audio library assets (music & sfx)
        music_lib = config.get("music", {})
        for music_name, m_path in list(music_lib.items()):
            music_lib[music_name] = process_asset_path(m_path)
            
        sfx_lib = config.get("sfx", {})
        for sfx_name, s_path in list(sfx_lib.items()):
            sfx_lib[sfx_name] = process_asset_path(s_path)

        # 3. Update scene backgrounds, bgm, and dialogue sprites/sfx paths
        for scene_id, scene in exported_data.get("scenes", {}).items():
            if "background" in scene:
                scene["background"] = process_asset_path(scene["background"])
            
            if "bgm" in scene and scene["bgm"] and scene["bgm"] != "stop":
                scene["bgm"] = process_asset_path(scene["bgm"])
            
            for dialogue in scene.get("dialogues", []):
                if "sprite" in dialogue and dialogue["sprite"]:
                    if "image" in dialogue["sprite"]:
                        dialogue["sprite"]["image"] = process_asset_path(dialogue["sprite"]["image"])
                        
                if "sfx" in dialogue and dialogue["sfx"]:
                    dialogue["sfx"] = process_asset_path(dialogue["sfx"])
        
        # Write story.js
        story_content = f"// Automatically generated visual novel story script\nwindow.storyData = {json.dumps(exported_data, indent=4, ensure_ascii=False)};\n"
        story_js_path = os.path.join(export_dir, "story.js")
        with open(story_js_path, "w", encoding="utf-8") as f:
            f.write(story_content)

        # 4. Copy template files (style.css, yandex_sdk.js, game.js)
        files_to_copy = ["style.css", "yandex_sdk.js", "game.js"]
        for fname in files_to_copy:
            src = os.path.join(TEMPLATES_DIR, fname)
            dst = os.path.join(export_dir, fname)
            if os.path.exists(src):
                shutil.copy2(src, dst)
            else:
                return False, f"Шаблонный файл {fname} не найден в {TEMPLATES_DIR}"

        # Handle index.html and update the title
        index_src = os.path.join(TEMPLATES_DIR, "index.html")
        index_dst = os.path.join(export_dir, "index.html")
        if os.path.exists(index_src):
            with open(index_src, "r", encoding="utf-8") as f:
                html_content = f.read()
            
            title = config.get("title", "Моя Новелла")
            html_content = html_content.replace("<title>Visual Novel</title>", f"<title>{title}</title>")
            
            with open(index_dst, "w", encoding="utf-8") as f:
                f.write(html_content)
        else:
            return False, "Шаблон index.html не найден."

        # 5. Copy asset files
        copied_files = set()
        for src, dst in assets_to_copy:
            if src in copied_files:
                continue
            try:
                shutil.copy2(src, dst)
                copied_files.add(src)
            except Exception as e:
                print(f"Ошибка при копировании ассета {src} -> {dst}: {e}")

        # 6. Create a ZIP archive
        zip_output_name = export_dir + "_yandex"
        shutil.make_archive(zip_output_name, 'zip', export_dir)

        return True, f"Проект успешно экспортирован!\nПапка: {export_dir}\nZIP-архив для Яндекс Игр: {zip_output_name}.zip"
    
    except Exception as e:
        import traceback
        return False, f"Ошибка при экспорте проекта: {str(e)}\n{traceback.format_exc()}"
