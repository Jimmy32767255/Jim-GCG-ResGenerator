import json
import os
from loguru import logger

import json

def generate_gcg_res_artifact_main_attribution(output_dir, excel_bin_output_path, text_map_file_path, not_generate_no_json_name_res, not_generate_no_text_map_name_res, added_mode):
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
    existing_ids = set()

    if added_mode and os.path.exists(output_file_path):
        try:
            with open(output_file_path, 'r', encoding='latin-1') as f:
                for line in f:
                    parts = line.strip().split(':', 1)
                    if len(parts) > 0:
                        existing_ids.add(parts[0])
            logger.info(f"在补充模式下，已读取 {output_file_path} 中现有的圣遗物主属性ID。")
        except IOError as e:
            logger.error(f"错误：读取现有文件 {output_file_path} 失败: {e}")
            added_mode = False # 如果读取失败，则退回到完全生成模式
    for item in reliquary_main_prop_data:
        artifact_main_attribution_id = item.get('id')
        prop_type = item.get('propType')

        # 检查是否跳过无Json名称资源 (这里propType是直接从json获取，所以直接检查其是否存在)
        if not_generate_no_json_name_res and not prop_type:
            logger.warning(f"跳过圣遗物主属性ID: {artifact_main_attribution_id}，因为它没有 Json 名称。")
            continue

        # propType 字段通常是字符串，直接作为名称
        name = prop_type

        # 检查是否跳过无正式名称资源 (这里name就是propType，所以检查name即可)
        if not_generate_no_text_map_name_res and not name:
            logger.warning(f"跳过圣遗物主属性ID: {artifact_main_attribution_id}，因为它没有正式名称。")
            continue

        if not name:
            name = f"[N/A] {prop_type}"
        
        if added_mode and str(artifact_main_attribution_id) in existing_ids:
            logger.info(f"在补充模式下，跳过已存在的圣遗物主属性ID: {artifact_main_attribution_id}")
            continue
        output_lines.append(f"{artifact_main_attribution_id}:{name}")

    try:
        mode = 'a' if added_mode else 'w'
        with open(output_file_path, mode, encoding='latin-1') as f:
            for line in output_lines:
                f.write(line + '\n')
        logger.info(f"成功{'追加' if added_mode else '生成'} {output_file_path} 文件，共 {len(output_lines)} 行")
    except IOError as e:
        logger.error(f"错误：写入文件 {output_file_path} 时发生错误：{e}")