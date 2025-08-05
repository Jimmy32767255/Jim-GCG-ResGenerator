import json
import os
from loguru import logger

import json
def generate_gcg_res_gadget(output_dir, excel_bin_output_path, text_map_file_path, not_generate_no_json_name_res, not_generate_no_text_map_name_res, added_mode=False):
    """
    生成 Gadget.txt 文件，包含实体ID和对应的中文名称。
    如果名称不存在，则使用默认值。
    """
    logger.info("开始生成 Gadget.txt 文件...")

    # 定义输入和输出文件路径
    gadget_data_file_path = os.path.join(excel_bin_output_path, "GadgetExcelConfigData.json")
    output_file_path = os.path.join(output_dir, "Gadget.txt")

    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

    gadget_excel_config_data = {}
    text_map = {}

    try:
        with open(gadget_data_file_path, 'r', encoding='latin-1') as f:
            gadget_excel_config_data = json.load(f)
        logger.info(f"成功读取实体数据文件: {gadget_data_file_path}")
    except FileNotFoundError:
        logger.error(f"错误：未找到实体数据文件 {gadget_data_file_path}")
        return
    except json.JSONDecodeError:
        logger.error(f"错误：实体数据文件 {gadget_data_file_path} 不是有效的 JSON 格式")
        return
    except Exception as e:
        logger.error(f"读取实体数据文件 {gadget_data_file_path} 失败: {e}")
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
    existing_items = set()

    # 如果是补充模式，尝试读取现有文件内容
    if added_mode and os.path.exists(output_file_path):
        try:
            with open(output_file_path, 'r', encoding='latin-1') as f:
                for line in f:
                    parts = line.strip().split(':', 1)
                    if len(parts) == 2:
                        existing_items.add(parts[0])
            logger.info(f"在补充模式下，已读取 {len(existing_items)} 个现有实体。")
        except Exception as e:
            logger.warning(f"补充模式下读取现有文件失败，将完全重新生成: {e}")
            existing_items.clear() # 清空，强制完全重新生成

    for item in gadget_excel_config_data:
        item_id = str(item.get('id'))

        # 如果是补充模式且该项已存在，则跳过
        if added_mode and item_id in existing_items:
            continue
        json_name = item.get('jsonName')
        interact_name_text_map_hash = item.get('interactNameTextMapHash')

        name = None
        # 尝试从 TextMap 中查找对应 ID 的名称
        if interact_name_text_map_hash is not None:
            name = text_map.get(str(interact_name_text_map_hash))

        # 如果没有找到，则使用 GECD 中的 jsonName
        if not name and json_name:
            name = json_name
            
        # 检查是否跳过无Json名称资源
        if not_generate_no_json_name_res and not json_name:
            logger.warning(f"跳过实体ID: {item_id}，因为它没有 Json 名称。")
            continue
            
        # 检查是否跳过无正式名称资源
        if not_generate_no_text_map_name_res and not name:
            logger.warning(f"跳过实体ID: {item_id}，因为它没有正式名称。")
            continue
            
        # 如果仍然没有名称，则使用默认值
        if not name:
            name = f"[N/A] {interact_name_text_map_hash}"

        output_lines.append(f"{item_id}:{name}")

    try:
        # 根据 added_mode 决定写入模式
        write_mode = 'a' if added_mode else 'w'
        with open(output_file_path, write_mode, encoding='latin-1') as f:
            for line in output_lines:
                f.write(line + '\n')
        logger.info(f"成功生成 {output_file_path} 文件")
    except IOError as e:
        logger.error(f"错误：写入文件 {output_file_path} 时发生错误：{e}")