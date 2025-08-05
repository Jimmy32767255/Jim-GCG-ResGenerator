import json
import os
from loguru import logger

import json

def generate_gcg_res_weapon(output_dir, excel_bin_output_path, text_map_file_path, not_generate_no_json_name_res, not_generate_no_text_map_name_res, added_mode):
    """
    生成 Weapon.txt 文件，包含武器ID和对应的中文名称。
    如果名称不存在，则使用默认值。
    """
    logger.info("开始生成 Weapon.txt 文件...")

    # 定义输入和输出文件路径
    weapon_data_file_path = os.path.join(excel_bin_output_path, "WeaponExcelConfigData.json")
    output_file_path = os.path.join(output_dir, "Weapon.txt")

    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

    weapon_excel_config_data = {}
    text_map = {}

    try:
        with open(weapon_data_file_path, 'r', encoding='latin-1') as f:
            weapon_excel_config_data = json.load(f)
        logger.info(f"成功读取武器数据文件: {weapon_data_file_path}")
    except FileNotFoundError:
        logger.error(f"错误：未找到武器数据文件 {weapon_data_file_path}")
        return
    except json.JSONDecodeError:
        logger.error(f"错误：武器数据文件 {weapon_data_file_path} 不是有效的 JSON 格式")
        return
    except Exception as e:
        logger.error(f"读取武器数据文件 {weapon_data_file_path} 失败: {e}")
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

    existing_weapon_ids = set()
    if added_mode and os.path.exists(output_file_path):
        try:
            with open(output_file_path, 'r', encoding='latin-1') as f:
                for line in f:
                    if ':' in line:
                        existing_weapon_ids.add(line.split(':')[0].strip())
            logger.info(f"在补充模式下读取现有 Weapon.txt 文件，已存在 {len(existing_weapon_ids)} 个武器ID。")
        except Exception as e:
            logger.warning(f"读取现有 Weapon.txt 文件失败，将重新生成所有内容: {e}")
            existing_weapon_ids.clear()

    output_lines = []
    for item in weapon_excel_config_data:
        weapon_id = str(item.get('id'))
        if added_mode and weapon_id in existing_weapon_ids:
            logger.debug(f"在补充模式下跳过已存在的武器ID: {weapon_id}")
            continue
        weapon_id = item.get('id')
        name_text_map_hash = item.get('nameTextMapHash')

        # 检查是否跳过无Json名称资源
        if not_generate_no_json_name_res and not name_text_map_hash:
            logger.warning(f"跳过武器ID: {weapon_id}，因为它没有 Json 名称。")
            continue

        name = text_map.get(str(name_text_map_hash))

        # 检查是否跳过无正式名称资源
        if not_generate_no_text_map_name_res and not name:
            logger.warning(f"跳过武器ID: {weapon_id}，因为它没有正式名称。")
            continue

        if not name:
            name = f"[N/A] {name_text_map_hash}"
        
        output_lines.append(f"{weapon_id}:{name}")

    try:
        # 根据 added_mode 决定写入模式
        write_mode = 'a' if added_mode else 'w'
        with open(output_file_path, write_mode, encoding='latin-1') as f:
            for line in output_lines:
                f.write(line + '\n')
        logger.info(f"成功生成 {output_file_path} 文件，共 {len(output_lines)} 行")
    except IOError as e:
        logger.error(f"错误：写入文件 {output_file_path} 时发生错误：{e}")