import json
import os
from loguru import logger

def generate_gcg_res_artifact_sub_attribution(output_dir, excel_bin_output_path, text_map_file_path, not_generate_no_json_name_res, not_generate_no_text_map_name_res, added_mode):
    """
    生成 ArtifactSubAttribution.txt 文件，包含圣遗物副属性ID和对应的中文名称。
    如果名称不存在，则使用默认值。
    """
    logger.info("开始生成 ArtifactSubAttribution.txt 文件...")

    # 定义输入和输出文件路径
    artifact_sub_attribution_data_path = os.path.join(excel_bin_output_path, "ReliquaryAffixExcelConfigData.json")
    output_file_path = os.path.join(output_dir, "ArtifactSubAttribution.txt")

    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

    artifact_sub_attribution_excel_config_data = {}
    text_map = {}

    try:
        with open(artifact_sub_attribution_data_path, 'r', encoding='latin-1') as f:
            artifact_sub_attribution_excel_config_data = json.load(f)
        logger.info(f"成功读取圣遗物副属性数据文件: {artifact_sub_attribution_data_path}")
    except FileNotFoundError:
        logger.error(f"错误：未找到圣遗物副属性数据文件 {artifact_sub_attribution_data_path}")
        return
    except json.JSONDecodeError:
        logger.error(f"错误：圣遗物副属性数据文件 {artifact_sub_attribution_data_path} 不是有效的 JSON 格式")
        return
    except Exception as e:
        logger.error(f"读取圣遗物副属性数据文件 {artifact_sub_attribution_data_path} 失败: {e}")
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

    all_items = {}

    if added_mode and os.path.exists(output_file_path):
        try:
            with open(output_file_path, 'r', encoding='latin-1') as f:
                for line in f:
                    parts = line.strip().split(':', 1)
                    if len(parts) == 2:
                        all_items[parts[0]] = parts[1]
            logger.info(f"在补充模式下，已读取 {len(all_items)} 个现有圣遗物副属性。")
        except Exception as e:
            logger.warning(f"补充模式下读取现有文件失败，将完全重新生成: {e}")
            all_items.clear() # 清空，强制完全重新生成

    for item in artifact_sub_attribution_excel_config_data:
        artifact_sub_attribution_id = str(item.get('id'))
        prop_type = item.get('propType')

        # propType 字段通常是字符串，直接作为名称
        name = prop_type

        if not name:
            if not_generate_no_json_name_res:
                logger.warning(f"跳过生成无Json名称的圣遗物副属性资源: {artifact_sub_attribution_id}")
                continue
            name = f"[N/A] {prop_type}"
        
        # 对于圣遗物副属性，propType就是其名称，所以不需要从text_map中获取
        # if not name and not_generate_no_text_map_name_res:
        #     logger.warning(f"跳过生成无正式名称的圣遗物副属性资源: {artifact_sub_attribution_id}")
        #     continue
        
        all_items[artifact_sub_attribution_id] = name

    # 将所有条目按 ID 排序
    sorted_items = sorted(all_items.items(), key=lambda x: int(x[0]))

    try:
        with open(output_file_path, 'w', encoding='latin-1') as f:
            for artifact_sub_attribution_id, name in sorted_items:
                f.write(f"{artifact_sub_attribution_id}:{name}\n")
        logger.info(f"成功生成 {output_file_path} 文件，共 {len(sorted_items)} 行")
    except IOError as e:
        logger.error(f"错误：写入文件 {output_file_path} 时发生错误：{e}")