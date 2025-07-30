import json
import os
from loguru import logger

def generate_gcg_res_artifact(output_dir, excel_bin_output_path, text_map_file_path):
    """
    生成 Artifact.txt 文件，包含圣遗物ID和对应的中文名称。
    如果名称不存在，则使用默认值。
    """
    logger.info("开始生成 Artifact.txt 文件...")

    # 定义输入和输出文件路径
    artifact_data_path = os.path.join(excel_bin_output_path, "ReliquaryExcelConfigData.json")
    output_file_path = os.path.join(output_dir, "Artifact.txt")

    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

    artifact_data = {}
    text_map = {}

    # 读取 JSON 文件
    try:
        with open(artifact_data_path, 'r', encoding='latin-1') as f:
            artifact_data = json.load(f)
        logger.info(f"成功读取圣遗物数据文件: {artifact_data_path}")
    except FileNotFoundError:
        logger.error(f"错误：未找到圣遗物数据文件 {artifact_data_path}")
        return
    except json.JSONDecodeError:
        logger.error(f"错误：圣遗物数据文件 {artifact_data_path} 不是有效的 JSON 格式")
        return
    except Exception as e:
        logger.error(f"读取圣遗物数据文件 {artifact_data_path} 失败: {e}")
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

    for item in artifact_data:
        item_id = item.get('id')
        name_text_map_hash = item.get('nameTextMapHash')

        # 获取圣遗物名称，如果不存在则使用默认值
        name = text_map.get(str(name_text_map_hash))
        if not name:
            name = f"[N/A] {name_text_map_hash}"

        if name:
            output_lines.append(f"{item_id}:{name}")

    # 写入到 Artifact.txt
    try:
        with open(output_file_path, 'w', encoding='latin-1') as f:
            for line in output_lines:
                f.write(line + '\n')
        logger.info(f"成功生成 {output_file_path}")
    except IOError as e:
        logger.error(f"错误：写入文件 {output_file_path} 失败: {e}")