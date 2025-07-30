import json
import os
from loguru import logger

def generate_gcg_res_artifact_main_attribution(output_dir, excel_bin_output_path, text_map_file_path):
    """
    生成 ArtifactMainAttribution.txt 文件，包含圣遗物主属性ID和对应的中文名称。
    如果名称不存在，则使用默认值。
    """
    logger.info("开始生成 ArtifactMainAttribution.txt 文件...")

    # 定义输入和输出文件路径
    reliquary_main_prop_data_path = os.path.join(excel_bin_output_path, "ReliquaryMainPropExcelConfigData.json")
    output_file_path = os.path.join(output_dir, "ArtifactMainAttribution.txt")

    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

    reliquary_main_prop_data = {}
    text_map = {}

    try:
        with open(reliquary_main_prop_data_path, 'r', encoding='latin-1') as f:
            reliquary_main_prop_data = json.load(f)
        logger.info(f"成功读取圣遗物主属性数据文件: {reliquary_main_prop_data_path}")
    except FileNotFoundError:
        logger.error(f"错误：未找到圣遗物主属性数据文件 {reliquary_main_prop_data_path}")
        return
    except json.JSONDecodeError:
        logger.error(f"错误：圣遗物主属性数据文件 {reliquary_main_prop_data_path} 不是有效的 JSON 格式")
        return
    except Exception as e:
        logger.error(f"读取圣遗物主属性数据文件 {reliquary_main_prop_data_path} 失败: {e}")
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
    for item in reliquary_main_prop_data:
        artifact_main_attribution_id = item.get('id')
        prop_type = item.get('propType')

        # propType 字段通常是字符串，直接作为名称
        name = prop_type

        if not name:
            name = f"[N/A] {prop_type}"
        
        output_lines.append(f"{artifact_main_attribution_id}:{name}")

    try:
        with open(output_file_path, 'w', encoding='latin-1') as f:
            for line in output_lines:
                f.write(line + '\n')
        logger.info(f"成功生成 {output_file_path} 文件，共 {len(output_lines)} 行")
    except IOError as e:
        logger.error(f"错误：写入文件 {output_file_path} 时发生错误：{e}")