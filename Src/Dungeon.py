import os
import json
from loguru import logger

def generate_gcg_res_dungeon(output_dir, excel_bin_output_path, text_map_file_path, not_generate_no_json_name_res, not_generate_no_text_map_name_res, added_mode):
    """
    生成 Dungeon.txt 文件，包含地牢ID和对应的中文名称。
    如果名称不存在，则使用默认值。
    """
    logger.info("开始生成 Dungeon.txt 文件...")

    # 定义输入和输出文件路径
    dungeon_data_file_path = os.path.join(excel_bin_output_path, "DungeonExcelConfigData.json")
    output_file_path = os.path.join(output_dir, "Dungeon.txt")

    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

    dungeon_data = {}
    text_map = {}

    try:
        with open(dungeon_data_file_path, 'r', encoding='latin-1') as f:
            dungeon_data = json.load(f)
        logger.info(f"成功读取地牢数据文件: {dungeon_data_file_path}")
    except FileNotFoundError:
        logger.error(f"错误：未找到地牢数据文件 {dungeon_data_file_path}")
        return
    except json.JSONDecodeError:
        logger.error(f"错误：地牢数据文件 {dungeon_data_file_path} 不是有效的 JSON 格式")
        return
    except Exception as e:
        logger.error(f"读取地牢数据文件 {dungeon_data_file_path} 失败: {e}")
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

    dungeon_entries = []
    existing_ids = set()

    if added_mode and os.path.exists(output_file_path):
        try:
            with open(output_file_path, 'r', encoding='latin-1') as f:
                for line in f:
                    parts = line.strip().split(':', 1)
                    if len(parts) > 0:
                        existing_ids.add(parts[0])
            logger.info(f"在补充模式下，已读取 {output_file_path} 中现有的地牢ID。")
        except IOError as e:
            logger.error(f"错误：读取现有文件 {output_file_path} 失败: {e}")
            added_mode = False # 如果读取失败，则退回到完全生成模式
    for entry in dungeon_data:
        dungeon_id = entry.get("id")
        name_text_map_hash = entry.get("nameTextMapHash")

        # 检查是否跳过无Json名称资源
        if not_generate_no_json_name_res and not name_text_map_hash:
            logger.warning(f"跳过地牢ID: {dungeon_id}，因为它没有 Json 名称。")
            continue

        # 获取地牢名称，如果不存在则使用默认值
        dungeon_name = text_map.get(str(name_text_map_hash))

        # 检查是否跳过无正式名称资源
        if not_generate_no_text_map_name_res and not dungeon_name:
            logger.warning(f"跳过地牢ID: {dungeon_id}，因为它没有正式名称。")
            continue

        if not dungeon_name:
            dungeon_name = f"[N/A] {name_text_map_hash}"
        if added_mode and str(dungeon_id) in existing_ids:
            logger.info(f"在补充模式下，跳过已存在的地牢ID: {dungeon_id}")
            continue
        dungeon_entries.append(f"{dungeon_id}:{dungeon_name}")

    try:
        mode = 'a' if added_mode else 'w'
        with open(output_file_path, mode, encoding='latin-1') as f:
            for line in dungeon_entries:
                f.write(line + '\n')
        logger.info(f"成功{'追加' if added_mode else '生成'} {output_file_path} 文件")
    except IOError as e:
        logger.error(f"错误：写入文件 {output_file_path} 时发生错误：{e}")