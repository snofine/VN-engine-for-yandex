# exporter.py - Visual Novel Exporter Module for HTML5/Yandex Games
import os
import json
import shutil

TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")

def export_project(project_data, export_dir):
    """
    Exports a visual novel project to HTML5 (Yandex Games format).
    :param project_data: dict containing 'config' and 'scenes'
    :param export_dir: absolute path to export directory
    :return: (bool, str) status and message
    """
    try:
        # Create export directory if it doesn't exist
        os.makedirs(export_dir, exist_ok=True)
        assets_dest_dir = os.path.join(export_dir, "assets")
        os.makedirs(assets_dest_dir, exist_ok=True)

        # 1. Generate story.js
        # We will extract local asset paths and map them to relative paths in the assets/ folder.
        # We modify the project_data inline (a copy of it) so the exported game uses relative paths.
        exported_data = json.loads(json.dumps(project_data)) # deep copy
        
        # Track which local assets need to be copied
        assets_to_copy = [] # list of (source_path, dest_filename)

        def process_asset_path(url_or_path):
            if not url_or_path:
                return url_or_path
            # If it's a web URL, leave it as is
            if url_or_path.startswith("http://") or url_or_path.startswith("https://") or url_or_path.startswith("data:"):
                return url_or_path
            # If it's a file path, we copy it to assets/ and use relative path
            if os.path.exists(url_or_path):
                filename = os.path.basename(url_or_path)
                # Ensure unique filename if needed (simplistic approach: just use basename)
                dest_path = os.path.join(assets_dest_dir, filename)
                assets_to_copy.append((url_or_path, dest_path))
                return f"assets/{filename}"
            return url_or_path

        # Update scene background paths
        for scene_id, scene in exported_data.get("scenes", {}).items():
            if "background" in scene:
                scene["background"] = process_asset_path(scene["background"])
            
            # Update dialogue sprite paths
            for dialogue in scene.get("dialogues", []):
                if "sprite" in dialogue and dialogue["sprite"]:
                    if "image" in dialogue["sprite"]:
                        dialogue["sprite"]["image"] = process_asset_path(dialogue["sprite"]["image"])
        
        # Write story.js
        story_content = f"// Automatically generated visual novel story script\nwindow.storyData = {json.dumps(exported_data, indent=4, ensure_ascii=False)};\n"
        story_js_path = os.path.join(export_dir, "story.js")
        with open(story_js_path, "w", encoding="utf-8") as f:
            f.write(story_content)

        # 2. Copy template files (index.html, style.css, yandex_sdk.js, game.js)
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
            
            # Replace title
            title = exported_data.get("config", {}).get("title", "Моя Новелла")
            html_content = html_content.replace("<title>Visual Novel</title>", f"<title>{title}</title>")
            
            with open(index_dst, "w", encoding="utf-8") as f:
                f.write(html_content)
        else:
            return False, "Шаблон index.html не найден."

        # 3. Copy asset files
        copied_files = set()
        for src, dst in assets_to_copy:
            if src in copied_files:
                continue
            try:
                shutil.copy2(src, dst)
                copied_files.add(src)
            except Exception as e:
                print(f"Ошибка при копировании ассета {src} -> {dst}: {e}")

        # 4. Create a ZIP archive (optional, let's create a ZIP file alongside the folder!)
        # This is extremely convenient for the user to upload directly to Yandex Games.
        zip_output_name = export_dir + "_yandex"
        shutil.make_archive(zip_output_name, 'zip', export_dir)

        return True, f"Проект успешно экспортирован!\nПапка: {export_dir}\nZIP-архив для Яндекс Игр: {zip_output_name}.zip"
    
    except Exception as e:
        import traceback
        return False, f"Ошибка при экспорте проекта: {str(e)}\n{traceback.format_exc()}"
