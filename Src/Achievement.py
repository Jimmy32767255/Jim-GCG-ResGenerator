import json
import os
from loguru import logger

import json
def generate_gcg_res_achievement(output_dir, excel_bin_output_path, text_map_file_path, not_generate_no_json_name_res, not_generate_no_text_map_name_res, added_mode=False):
    """
    生成 Achievement.txt 文件，包含成就ID和对应的中文名称。
    如果名称不存在，则使用默认值。
    """
    logger.info("开始生成 Achievement.txt 文件...")

    # 定义输入和输出文件路径
    achievement_data_path = os.path.join(excel_bin_output_path, "AchievementExcelConfigData.json")
    output_file_path = os.path.join(output_dir, "Achievement.txt")

    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

    achievement_excel_config_data = []
    text_map = {}

    # 读取 AchievementExcelConfigData.json
    try:
        with open(achievement_data_path, 'r', encoding='latin-1') as f:
            achievement_excel_config_data = json.load(f)
        logger.info(f"成功读取成就数据文件: {achievement_data_path}")
    except FileNotFoundError:
        logger.error(f"错误：未找到成就数据文件 {achievement_data_path}")
        return
    except json.JSONDecodeError:
        logger.error(f"错误：成就数据文件 {achievement_data_path} 不是有效的 JSON 格式")
        return
    except Exception as e:
        logger.error(f"读取成就数据文件 {achievement_data_path} 失败: {e}")
        return

    # 读取文本映射文件
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

    output_lines = []
    existing_items = set()

    # 如果是补充模式，尝试读取现有文件内容
    if added_mode and os.path.exists(output_file_path):
        try:
            with open(output_file_path, 'r', encoding='latin-1') as f:
                for line in f:
                    parts = line.strip().split(':', 1)
                    if len(parts) == 2:
                        existing_items.add(parts[0])
            logger.info(f"在补充模式下，已读取 {len(existing_items)} 个现有成就。")
        except Exception as e:
            logger.warning(f"补充模式下读取现有文件失败，将完全重新生成: {e}")
            existing_items.clear() # 清空，强制完全重新生成

    for item in achievement_excel_config_data:
        item_id = str(item.get('id'))

        # 如果是补充模式且该项已存在，则跳过
        if added_mode and item_id in existing_items:
            continue
        title_text_map_hash = item.get('titleTextMapHash')

        # 尝试从 TextMap 中查找对应 ID 的名称
        name = None
        if title_text_map_hash is not None:
            name = text_map.get(str(title_text_map_hash))

        # 如果没有找到，则根据参数决定是否跳过
        if not name:
            if not_generate_no_text_map_name_res:
                logger.warning(f"警告：成就 ID {item_id} 没有找到对应的文本映射名称，已跳过。")
                continue
            else:
                name = f"[N/A] {title_text_map_hash}"

        output_lines.append(f"{item_id}:{name}")

    # 写入 Achievement.txt
    try:
        if added_mode:
            with open(output_file_path, 'a', encoding='latin-1') as f:
                for line in output_lines:
                    f.write(line + '\n')
            logger.info(f"成功向 {output_file_path} 追加 {len(output_lines)} 行新成就数据")
        else:
            with open(output_file_path, 'w', encoding='latin-1') as f:
                for line in output_lines:
                    f.write(line + '\n')
            logger.info(f"成功生成 {output_file_path}，共 {len(output_lines)} 行")
    except IOError as e:
        logger.error(f"错误：写入文件 {output_file_path} 失败: {e}")