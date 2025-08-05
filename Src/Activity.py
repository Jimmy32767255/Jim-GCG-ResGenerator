import os
import json
from loguru import logger

import os
def generate_gcg_res_activity(output_dir, excel_bin_output_path, text_map_file_path, not_generate_no_json_name_res, not_generate_no_text_map_name_res, added_mode=False):
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
    existing_items = set()

    # 如果是补充模式，尝试读取现有文件内容
    if added_mode and os.path.exists(output_file_path):
        try:
            with open(output_file_path, 'r', encoding='latin-1') as f:
                for line in f:
                    parts = line.strip().split(':', 1)
                    if len(parts) == 2:
                        existing_items.add(parts[0])
            logger.info(f"在补充模式下，已读取 {len(existing_items)} 个现有活动。")
        except Exception as e:
            logger.warning(f"补充模式下读取现有文件失败，将完全重新生成: {e}")
            existing_items.clear() # 清空，强制完全重新生成

    for item in activity_data:
        activity_id = str(item.get('ActivityId'))

        # 如果是补充模式且该项已存在，则跳过
        if added_mode and activity_id in existing_items:
            continue
        title_text_map_hash = item.get('NameTextMapHash')

        # 根据 not_generate_no_json_name_res 跳过没有 Json 名称的资源
        if not_generate_no_json_name_res and not title_text_map_hash:
            logger.warning(f"跳过活动ID: {activity_id}，因为它没有 Json 名称。")
            continue

        # 获取活动名称，如果不存在则使用默认值
        name = text_map.get(str(title_text_map_hash))

        # 根据 not_generate_no_text_map_name_res 跳过没有正式名称的资源
        if not_generate_no_text_map_name_res and not name:
            logger.warning(f"跳过活动ID: {activity_id}，因为它没有正式名称。")
            continue

        if not name:
            name = f"[N/A] {title_text_map_hash}"

        output_lines.append(f"{activity_id}:{name}")

    # 写入到 Activity.txt
    try:
        if added_mode:
            with open(output_file_path, 'a', encoding='latin-1') as f:
                for line in output_lines:
                    f.write(line + '\n')
            logger.info(f"成功向 {output_file_path} 追加 {len(output_lines)} 行新活动数据")
        else:
            with open(output_file_path, 'w', encoding='latin-1') as f:
                for line in output_lines:
                    f.write(line + '\n')
            logger.info(f"成功生成 {output_file_path}，共 {len(output_lines)} 行")
    except IOError as e:
        logger.error(f"错误：写入文件 {output_file_path} 失败：{e}")