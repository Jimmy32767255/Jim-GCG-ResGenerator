import json
import os
from loguru import logger

import json

def generate_gcg_res_weather(output_dir, excel_bin_output_path, not_generate_no_json_name_res, not_generate_no_text_map_name_res, added_mode):
    """
    生成 Weather.txt 文件，包含天气区域ID和对应的名称。
    """
    logger.info("开始生成 Weather.txt 文件...")

    # 定义输入和输出文件路径
    weather_data_file_path = os.path.join(excel_bin_output_path, "WeatherExcelConfigData.json")

    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    weather_excel_config_data = {}

    try:
        with open(weather_data_file_path, 'r', encoding='latin-1') as f:
            weather_excel_config_data = json.load(f)
        logger.info(f"成功读取天气数据文件: {weather_data_file_path}")
    except FileNotFoundError:
        logger.error(f"错误：未找到天气数据文件 {weather_data_file_path}")
        return
    except json.JSONDecodeError:
        logger.error(f"错误：天气数据文件 {weather_data_file_path} 不是有效的 JSON 格式")
        return
    except Exception as e:
        logger.error(f"读取天气数据文件 {weather_data_file_path} 失败: {e}")
        return

    output_file_path = os.path.join(output_dir, "Weather.txt")

    all_items = {}
    if added_mode and os.path.exists(output_file_path):
        try:
            with open(output_file_path, 'r', encoding='latin-1') as f:
                for line in f:
                    parts = line.strip().split(':', 1)
                    if len(parts) == 2:
                        all_items[parts[0]] = parts[1]
            logger.info(f"在补充模式下读取现有 Weather.txt 文件，已存在 {len(all_items)} 个天气区域ID。")
        except Exception as e:
            logger.warning(f"读取现有 Weather.txt 文件失败，将重新生成所有内容: {e}")
            all_items.clear()

    for item in weather_excel_config_data:
        weather_area_id = str(item.get('weatherAreaId'))
        weather_name = item.get('profileName')

        # 检查是否跳过无Json名称资源
        if not_generate_no_json_name_res and not weather_name:
            logger.warning(f"跳过天气区域ID: {weather_area_id}，因为它没有 Json 名称。")
            continue
            
        # 检查是否跳过无正式名称资源
        if not_generate_no_text_map_name_res and not weather_name:
            logger.warning(f"跳过天气区域ID: {weather_area_id}，因为它没有正式名称。")
            continue
            
        if weather_area_id is not None:
            if weather_name:
                all_items[weather_area_id] = weather_name
            elif not not_generate_no_json_name_res and not not_generate_no_text_map_name_res:
                all_items[weather_area_id] = "[N/A]"

    # 将所有条目按 ID 排序
    sorted_items = sorted(all_items.items(), key=lambda x: int(x[0]))

    output_file_path = os.path.join(output_dir, "Weather.txt")
    try:
        with open(output_file_path, 'w', encoding='latin-1') as f:
            for weather_area_id, weather_name in sorted_items:
                f.write(f"{weather_area_id}:{weather_name}\n")
        logger.info(f"成功生成 {output_file_path} 文件，共 {len(sorted_items)} 行")
    except IOError as e:
        logger.error(f"错误：写入文件 {output_file_path} 时发生错误：{e}")