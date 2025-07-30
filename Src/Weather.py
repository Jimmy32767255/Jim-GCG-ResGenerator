import json
import os
from loguru import logger

def generate_gcg_res_weather(output_dir, excel_bin_output_path):
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

    output_lines = []

    for item in weather_excel_config_data:
        weather_area_id = item.get('weatherAreaId')
        weather_name = item.get('profileName')

        if weather_area_id is not None and weather_name:
            output_lines.append(f"{weather_area_id}:{weather_name}")

    output_file_path = os.path.join(output_dir, "Weather.txt")
    try:
        with open(output_file_path, 'w', encoding='latin-1') as f:
            for line in output_lines:
                f.write(line + '\n')
        logger.info(f"成功生成 {output_file_path} 文件")
    except IOError as e:
        logger.error(f"错误：写入文件 {output_file_path} 时发生错误：{e}")