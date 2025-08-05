import json
import os
from loguru import logger

def generate_gcg_res_scene(output_dir, excel_bin_output_path, text_map_file_path, not_generate_no_json_name_res, not_generate_no_text_map_name_res, added_mode=False):
    """
    生成 Scene.txt 文件，包含场景ID和对应的中文名称。
    如果名称不存在，则使用默认值。
    """
    logger.info("开始生成 Scene.txt 文件...")

    # 定义输入和输出文件路径
    scene_data_file_path = os.path.join(excel_bin_output_path, "SceneExcelConfigData.json")
    output_file_path = os.path.join(output_dir, "Scene.txt")

    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

    scene_excel_config_data = []
    text_map = {}

    try:
        with open(scene_data_file_path, 'r', encoding='latin-1') as f:
            scene_excel_config_data = json.load(f)
        logger.info(f"成功读取场景数据文件: {scene_data_file_path}")
    except FileNotFoundError:
        logger.error(f"错误：未找到场景数据文件 {scene_data_file_path}")
        return
    except json.JSONDecodeError:
        logger.error(f"错误：场景数据文件 {scene_data_file_path} 不是有效的 JSON 格式")
        return
    except Exception as e:
        logger.error(f"读取场景数据文件 {scene_data_file_path} 失败: {e}")
        return

    try:
        with open(text_map_file_path, 'r', encoding='latin-1') as f:
            text_map = json.load(f)
        logger.info(f"成功读取文本映射文件: {text_map_file_path}")
    except FileNotFoundError:
        logger.error(f"错误：未找到文本映射文件 {text_map_file_path}")
        return
    except json.JSONDecodeError:
        logger.error(f"错误：文本映射文件 {text_map_file_path} 不是有效的 JSON 格式")
        return
    except Exception as e:
        logger.error(f"读取文本映射文件 {text_map_file_path} 失败: {e}")
        return

    all_items = {}

    # 如果是补充模式，尝试读取现有文件内容
    if added_mode and os.path.exists(output_file_path):
        try:
            with open(output_file_path, 'r', encoding='latin-1') as f:
                for line in f:
                    parts = line.strip().split(':', 1)
                    if len(parts) == 2:
                        all_items[parts[0]] = parts[1]
            logger.info(f"在补充模式下，已读取 {len(all_items)} 个现有场景。")
        except Exception as e:
            logger.warning(f"补充模式下读取现有文件失败，将完全重新生成: {e}")
            all_items.clear() # 清空，强制完全重新生成

    for item in scene_excel_config_data:
        scene_id = str(item.get('id'))
        script_data = item.get('scriptData')
        comment = item.get('comment')

        name = None
        # 优先使用 comment 作为名称
        if comment:
            name = comment
        # 其次使用 scriptData
        elif script_data:
            name = script_data
            
        # 检查是否跳过无名称资源
        if not_generate_no_json_name_res and not script_data:
            logger.warning(f"跳过场景ID: {scene_id}，因为它没有 scriptData。")
            continue
            
        # 检查是否跳过无正式名称资源
        if not_generate_no_text_map_name_res and not name:
            logger.warning(f"跳过场景ID: {scene_id}，因为它没有名称。")
            continue
            
        # 如果仍然没有名称，则使用默认值
        if not name:
            name = f"[N/A] {scene_id}"

        all_items[scene_id] = name

    # 将所有条目按 ID 排序
    sorted_items = sorted(all_items.items(), key=lambda x: int(x[0]))

    try:
        with open(output_file_path, 'w', encoding='latin-1') as f:
            for scene_id, name in sorted_items:
                f.write(f"{scene_id}:{name}\n")
        logger.info(f"成功生成 {output_file_path} 文件，共 {len(sorted_items)} 行")
    except IOError as e:
        logger.error(f"错误：写入文件 {output_file_path} 时发生错误：{e}")