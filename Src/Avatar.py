import json
import os
from loguru import logger

def generate_gcg_res_avatar(output_dir, excel_bin_output_path, text_map_file_path):
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
        logger.info(f"成功读取文本映射文件: {os.path.join(text_map_file_path, 'TextMapCHS.json')}")
    except FileNotFoundError:
        logger.error(f"错误：未找到文本映射文件 {os.path.join(text_map_file_path, 'TextMapCHS.json')}")
        return
    except json.JSONDecodeError:
        logger.error(f"错误：文本映射文件 {os.path.join(text_map_file_path, 'TextMapCHS.json')} 不是有效的 JSON 格式")
        return
    except Exception as e:
        logger.error(f"读取文本映射文件 {os.path.join(text_map_file_path, 'TextMapCHS.json')} 失败: {e}")
        return

    output_lines = []
    for item in avatar_excel_config_data:
        avatar_id = item.get('id')
        name_text_map_hash = item.get('nameTextMapHash')

        # 获取角色名称，如果不存在则使用默认值
        name = text_map.get(str(name_text_map_hash))
        if not name:
            name = f"[N/A] {name_text_map_hash}"
        
        output_lines.append(f"{avatar_id}:{name}")

    try:
        output_file_path = os.path.join(output_dir, "Avatar.txt")
        with open(output_file_path, 'w', encoding='latin-1') as f:
            for line in output_lines:
                f.write(line + '\n')
        logger.info(f"成功生成 {output_file_path} 文件，共 {len(output_lines)} 行")
    except IOError as e:
        logger.error(f"错误：写入文件 {output_file_path} 时发生错误：{e}")