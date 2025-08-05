import json
import os
from loguru import logger

def generate_gcg_res_avatar(output_dir, excel_bin_output_path, text_map_file_path, not_generate_no_json_name_res, not_generate_no_text_map_name_res, added_mode):
    """
    生成 Avatar.txt 文件，包含角色ID和对应的中文名称。
    如果名称不存在，则使用默认值。
    """
    logger.info("开始生成 Avatar.txt 文件...")

    # 定义输入和输出文件路径
    avatar_data = {}
    text_map = {}

    try:
        with open(os.path.join(excel_bin_output_path, "AvatarExcelConfigData.json"), 'r', encoding='latin-1') as f:
            avatar_excel_config_data = json.load(f)
        logger.info(f"成功读取角色数据文件: {os.path.join(excel_bin_output_path, 'AvatarExcelConfigData.json')}")
    except FileNotFoundError:
        logger.error(f"错误：未找到角色数据文件 {os.path.join(excel_bin_output_path, 'AvatarExcelConfigData.json')}")
        return
    except json.JSONDecodeError:
        logger.error(f"错误：角色数据文件 {os.path.join(excel_bin_output_path, 'AvatarExcelConfigData.json')} 不是有效的 JSON 格式")
        return
    except Exception as e:
        logger.error(f"读取角色数据文件 {os.path.join(excel_bin_output_path, 'AvatarExcelConfigData.json')} 失败: {e}")
        return

    try:
        with open(os.path.join(text_map_file_path), 'r', encoding='latin-1') as f:
            text_map = json.load(f)
        logger.info(f"成功读取文本映射文件: {os.path.join(text_map_file_path, 'TextMap.json')}")
    except FileNotFoundError:
        logger.error(f"错误：未找到文本映射文件 {os.path.join(text_map_file_path, 'TextMap.json')}")
        return
    except json.JSONDecodeError:
        logger.error(f"错误：文本映射文件 {os.path.join(text_map_file_path, 'TextMap.json')} 不是有效的 JSON 格式")
        return
    except Exception as e:
        logger.error(f"读取文本映射文件 {os.path.join(text_map_file_path, 'TextMap.json')} 失败: {e}")
        return

    all_items = {}

    output_file_path = os.path.join(output_dir, "Avatar.txt")

    if added_mode and os.path.exists(output_file_path):
        try:
            with open(output_file_path, 'r', encoding='latin-1') as f:
                for line in f:
                    parts = line.strip().split(':', 1)
                    if len(parts) == 2:
                        all_items[parts[0]] = parts[1]
            logger.info(f"在补充模式下，已读取 {len(all_items)} 个现有角色。")
        except Exception as e:
            logger.warning(f"补充模式下读取现有文件失败，将完全重新生成: {e}")
            all_items.clear() # 清空，强制完全重新生成

    for item in avatar_excel_config_data:
        avatar_id = str(item.get('id'))
        name_text_map_hash = item.get('nameTextMapHash')

        # 获取角色名称，如果不存在则使用默认值
        name = text_map.get(str(name_text_map_hash))
        if not name:
            if not_generate_no_text_map_name_res:
                logger.warning(f"跳过生成无正式名称的角色资源: {avatar_id}")
                continue
            name = f"[N/A] {name_text_map_hash}"
        
        all_items[avatar_id] = name

    # 将所有条目按 ID 排序
    sorted_items = sorted(all_items.items(), key=lambda x: int(x[0]))

    try:
        with open(output_file_path, 'w', encoding='latin-1') as f:
            for avatar_id, name in sorted_items:
                f.write(f"{avatar_id}:{name}\n")
        logger.info(f"成功生成 {output_file_path} 文件，共 {len(sorted_items)} 行")
    except IOError as e:
        logger.error(f"错误：写入文件 {output_file_path} 时发生错误：{e}")