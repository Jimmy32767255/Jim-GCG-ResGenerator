import json
import os
from loguru import logger

def generate_gcg_res_gadget(output_dir, excel_bin_output_path, text_map_file_path):
    """
    生成 Gadget.txt 文件，包含小工具ID和对应的中文名称。
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
        logger.info(f"成功读取小工具数据文件: {gadget_data_file_path}")
    except FileNotFoundError:
        logger.error(f"错误：未找到小工具数据文件 {gadget_data_file_path}")
        return
    except json.JSONDecodeError:
        logger.error(f"错误：小工具数据文件 {gadget_data_file_path} 不是有效的 JSON 格式")
        return
    except Exception as e:
        logger.error(f"读取小工具数据文件 {gadget_data_file_path} 失败: {e}")
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

    for item in gadget_excel_config_data:
        item_id = item.get('id')
        json_name = item.get('jsonName')
        interact_name_text_map_hash = item.get('interactNameTextMapHash')

        name = None
        # 尝试从 TextMapCHS 中查找对应 ID 的名称
        if interact_name_text_map_hash is not None:
            name = text_map.get(str(interact_name_text_map_hash))

        # 如果没有找到，则使用 GECD 中的 jsonName
        if not name:
            if json_name:
                name = json_name
            else:
                # 如果仍然没有，则使用 "[N/A] " + interactNameTextMapHash
                name = f"[N/A] {interact_name_text_map_hash}"
        
        # 如果 name 是空字符串，也将其替换为默认值
        if not name:
            name = f"[N/A] {interact_name_text_map_hash}"

        output_lines.append(f"{item_id}:{name}")

    try:
        with open(output_file_path, 'w', encoding='latin-1') as f:
            for line in output_lines:
                f.write(line + '\n')
        logger.info(f"成功生成 {output_file_path} 文件")
    except IOError as e:
        logger.error(f"错误：写入文件 {output_file_path} 时发生错误：{e}")