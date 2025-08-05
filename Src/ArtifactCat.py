import os
import json
from loguru import logger

def generate_gcg_res_artifact_cat(output_dir, excel_bin_output_path, text_map_file_path, not_generate_no_json_name_res, not_generate_no_text_map_name_res, added_mode):
    """
    生成 ArtifactCat.txt 文件，包含圣遗物套装ID和对应的中文名称。
    如果名称不存在，则使用默认值。
    """
    logger.info("开始生成 ArtifactCat.txt 文件...")

    # 定义输入和输出文件路径
    artifact_cat_data_path = os.path.join(excel_bin_output_path, "ReliquarySetExcelConfigData.json")
    output_file_path = os.path.join(output_dir, "ArtifactCat.txt")

    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

    artifact_cat_excel_config_data = {}
    text_map = {}

    try:
        with open(artifact_cat_data_path, 'r', encoding='latin-1') as f:
            artifact_cat_excel_config_data = json.load(f)
        logger.info(f"成功读取圣遗物套装数据文件: {artifact_cat_data_path}")
    except FileNotFoundError:
        logger.error(f"错误：未找到圣遗物套装数据文件 {artifact_cat_data_path}")
        return
    except json.JSONDecodeError:
        logger.error(f"错误：圣遗物套装数据文件 {artifact_cat_data_path} 不是有效的 JSON 格式")
        return
    except Exception as e:
        logger.error(f"读取圣遗物套装数据文件 {artifact_cat_data_path} 失败: {e}")
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
            logger.info(f"在补充模式下，已读取 {len(all_items)} 个现有圣遗物套装。")
        except Exception as e:
            logger.warning(f"补充模式下读取现有文件失败，将完全重新生成: {e}")
            all_items.clear() # 清空，强制完全重新生成

    for item in artifact_cat_excel_config_data:
        artifact_cat_id = str(item.get('setId'))
        name_text_map_hash = item.get('equipAffixId')

        # 检查是否跳过无Json名称资源
        if not_generate_no_json_name_res and not name_text_map_hash:
            logger.warning(f"跳过圣遗物套装ID: {artifact_cat_id}，因为缺少Json名称且 '不生成无Json名称资源' 已启用")
            continue

        # 获取圣遗物套装名称，如果不存在则使用默认值
        name = text_map.get(str(name_text_map_hash))

        # 检查是否跳过无正式名称资源
        if not_generate_no_text_map_name_res and not name:
            logger.warning(f"跳过圣遗物套装ID: {artifact_cat_id}，因为它没有正式名称。")
            continue

        if not name:
            name = f"[N/A] {name_text_map_hash}"
        
        all_items[artifact_cat_id] = name

    # 将所有条目按 ID 排序
    sorted_items = sorted(all_items.items(), key=lambda x: int(x[0]))

    try:
        with open(output_file_path, 'w', encoding='latin-1') as f:
            for artifact_cat_id, name in sorted_items:
                f.write(f"{artifact_cat_id}:{name}\n")
        logger.info(f"成功生成 {output_file_path} 文件，共 {len(sorted_items)} 行")
    except IOError as e:
        logger.error(f"错误：写入文件 {output_file_path} 时发生错误：{e}")