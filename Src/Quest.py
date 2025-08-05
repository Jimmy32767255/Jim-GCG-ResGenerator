import os
import json
from loguru import logger

def generate_gcg_res_quest(output_dir, excel_bin_output_path, text_map_file_path, not_generate_no_json_name_res, not_generate_no_text_map_name_res, added_mode=False):
    """
    生成 Quest.txt 文件，包含任务ID和对应的中文名称。
    如果名称不存在，则使用默认值。
    """
    logger.info("开始生成 Quest.txt 文件...")

    # 定义输入和输出文件路径
    quest_data_file_path = os.path.join(excel_bin_output_path, "QuestExcelConfigData.json")
    output_file_path = os.path.join(output_dir, "Quest.txt")

    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

    quest_excel_config_data = {}
    text_map = {}

    try:
        with open(quest_data_file_path, 'r', encoding='latin-1') as f:
            quest_excel_config_data = json.load(f)
        logger.info(f"成功读取任务数据文件: {quest_data_file_path}")
    except FileNotFoundError:
        logger.error(f"错误：未找到任务数据文件 {quest_data_file_path}")
        return
    except json.JSONDecodeError:
        logger.error(f"错误：任务数据文件 {quest_data_file_path} 不是有效的 JSON 格式")
        return
    except Exception as e:
        logger.error(f"读取任务数据文件 {quest_data_file_path} 失败: {e}")
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

    existing_quest_ids = set()

    if added_mode and os.path.exists(output_file_path):
        logger.info(f"补充模式已启用，正在读取现有文件 {output_file_path}...")
        try:
            with open(output_file_path, 'r', encoding='latin-1') as f:
                for line in f:
                    parts = line.strip().split(':')
                    if len(parts) > 0:
                        existing_quest_ids.add(parts[0])
            logger.info(f"已读取 {len(existing_quest_ids)} 个现有任务ID。")
        except Exception as e:
            logger.error(f"读取现有文件 {output_file_path} 失败: {e}")
            # 即使读取失败，也继续生成，但不进行增量跳过

    output_lines = []

    for item in quest_excel_config_data:
        quest_id = str(item.get("subId"))

        if added_mode and quest_id in existing_quest_ids:
            logger.debug(f"补充模式：跳过已存在的任务ID {quest_id}")
            continue

        title_text_map_hash = item.get("descTextMapHash")

        # 根据 not_generate_no_json_name_res 跳过没有 Json 名称的资源
        if not_generate_no_json_name_res and not title_text_map_hash:
            logger.warning(f"跳过任务ID: {quest_id}，因为它没有 Json 名称。")
            continue

        # 获取任务名称，如果不存在则使用默认值
        title = text_map.get(str(title_text_map_hash))

        # 根据 not_generate_no_text_map_name_res 跳过没有正式名称的资源
        if not_generate_no_text_map_name_res and not title:
            logger.warning(f"跳过任务ID: {quest_id}，因为它没有正式名称。")
            continue

        if not title:
            title = f"[N/A] {title_text_map_hash}"

        output_lines.append(f"{quest_id}:{title}")

    try:
        # 根据 added_mode 决定写入模式
        write_mode = 'a' if added_mode else 'w'
        with open(output_file_path, write_mode, encoding='latin-1') as f:
            for line in output_lines:
                f.write(line + '\n')




        logger.info(f"成功生成 {output_file_path} 文件")
    except IOError as e:
        logger.error(f"错误：写入文件 {output_file_path} 时发生错误：{e}")