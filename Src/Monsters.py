import os
import json
from loguru import logger

def generate_gcg_res_monsters(output_dir, excel_bin_output_path, text_map_file_path, not_generate_no_json_name_res, not_generate_no_text_map_name_res):
    """
    生成 GCG 怪物资源文件 Monsters.txt，包含怪物ID和对应的中文名称。
    如果名称不存在，则使用默认值。
    """
    logger.info("开始生成 GCG 怪物资源文件 Monsters.txt...")

    # 定义输入和输出文件路径
    monster_data_file_path = os.path.join(excel_bin_output_path, "MonsterExcelConfigData.json")
    output_file_path = os.path.join(output_dir, "Monsters.txt")

    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

    monster_data = {}
    text_map = {}

    try:
        with open(monster_data_file_path, 'r', encoding='latin-1') as f:
            monster_data = json.load(f)
        logger.info(f"成功读取怪物数据文件: {monster_data_file_path}")
    except FileNotFoundError:
        logger.error(f"错误：未找到怪物数据文件 {monster_data_file_path}")
        return
    except json.JSONDecodeError:
        logger.error(f"错误：怪物数据文件 {monster_data_file_path} 不是有效的 JSON 格式")
        return
    except Exception as e:
        logger.error(f"读取怪物数据文件 {monster_data_file_path} 失败: {e}")
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

    output_lines = []

    for item in monster_data:
        monster_id = item.get('id')
        name_text_map_hash = item.get('nameTextMapHash')

        # 根据 not_generate_no_json_name_res 跳过没有 Json 名称的资源
        if not_generate_no_json_name_res and not name_text_map_hash:
            logger.warning(f"跳过怪物ID: {monster_id}，因为它没有 Json 名称。")
            continue

        name = text_map.get(str(name_text_map_hash))

        # 根据 not_generate_no_text_map_name_res 跳过没有正式名称的资源
        if not_generate_no_text_map_name_res and not name:
            logger.warning(f"跳过怪物ID: {monster_id}，因为它没有正式名称。")
            continue

        if not name:
            name = f"[N/A] {name_text_map_hash}"

        if name:
            output_lines.append(f"{monster_id}:{name}")

    try:
        with open(output_file_path, 'w', encoding='latin-1') as f:
            for line in output_lines:
                f.write(line + '\n')
        logger.info(f"成功生成 {output_file_path} 文件")
    except IOError as e:
        logger.error(f"错误：写入文件 {output_file_path} 时发生错误：{e}")