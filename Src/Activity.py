import os
import json
from loguru import logger

def generate_gcg_res_activity(output_dir, excel_bin_output_path, text_map_file_path):
    """
    生成 Activity.txt 文件，包含活动ID和对应的中文名称。
    如果名称不存在，则使用默认值。
    """
    logger.info("开始生成 Activity.txt 文件...")

    # 定义输入和输出文件路径
    activity_data_path = os.path.join(excel_bin_output_path, "ActivityExcelConfigData.json")
    output_file_path = os.path.join(output_dir, "Activity.txt")

    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

    activity_data = {}
    text_map = {}

    # 读取 ActivityExcelConfigData.json
    try:
        with open(activity_data_path, 'r', encoding='latin-1') as f:
            activity_data = json.load(f)
        logger.info(f"成功读取活动数据文件: {activity_data_path}")
    except FileNotFoundError:
        logger.error(f"错误：未找到活动数据文件 {activity_data_path}")
        return
    except json.JSONDecodeError:
        logger.error(f"错误：活动数据文件 {activity_data_path} 不是有效的 JSON 格式")
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

    output_lines = []
    for item in activity_data:
        activity_id = item.get('ActivityId')
        title_text_map_hash = item.get('NameTextMapHash')

        # 获取活动名称，如果不存在则使用默认值
        name = text_map.get(str(title_text_map_hash))
        if not name:
            name = f"[N/A] {title_text_map_hash}"

        output_lines.append(f"{activity_id}:{name}")

    # 写入到 Activity.txt
    try:
        with open(output_file_path, 'w', encoding='latin-1') as f:
            for line in output_lines:
                f.write(line + '\n')
        logger.info(f"成功生成 {output_file_path}，共 {len(output_lines)} 行")
    except IOError as e:
        logger.error(f"错误：写入文件 {output_file_path} 失败：{e}")