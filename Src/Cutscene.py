import os
import json
from loguru import logger

def generate_gcg_res_cutscene(output_dir, excel_bin_output_path, text_map_file_path, not_generate_no_json_name_res, not_generate_no_text_map_name_res):
    """
    生成 Cutscene.txt 文件，包含过场动画ID和对应的中文名称。
    如果名称不存在，则使用默认值。
    """
    logger.info("开始生成 Cutscene.txt 文件...")
    
    # 定义输入和输出文件路径
    cutscene_data_path = os.path.join(excel_bin_output_path, "CutsceneExcelConfigData.json")
    output_file_path = os.path.join(output_dir, "Cutscene.txt")

    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

    cutscene_data = {}
    text_map = {}

    try:
        with open(cutscene_data_path, 'r', encoding='latin-1') as f:
            cutscene_data = json.load(f)
        logger.info(f"成功读取过场动画数据文件: {cutscene_data_path}")
    except FileNotFoundError:
        logger.error(f"错误：未找到过场动画数据文件 {cutscene_data_path}")
        return
    except json.JSONDecodeError:
        logger.error(f"错误：过场动画数据文件 {cutscene_data_path} 不是有效的 JSON 格式")
        return
    except Exception as e:
        logger.error(f"读取过场动画数据文件 {cutscene_data_path} 失败: {e}")
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

    try:
        with open(output_file_path, 'w', encoding='latin-1') as f:
            for entry in cutscene_data:
                cutscene_id = entry.get('id')
                cutscene_path = entry.get('path')
                
                if cutscene_id is not None:
                    # 获取过场动画名称，如果不存在则使用默认值
                    # 由于CutsceneExcelConfigData.json中没有titleTextMapHash，我们使用path字段作为名称
                    cutscene_name = cutscene_path
                    if not cutscene_name:
                        if not_generate_no_json_name_res:
                            logger.warning(f"跳过生成无Json名称的过场动画资源: {cutscene_id}")
                            continue
                        cutscene_name = f"[N/A] {cutscene_id}"
                    # 对于过场动画，名称直接从path字段获取，所以不需要从text_map中获取
                    # if not cutscene_name and not_generate_no_text_map_name_res:
                    #     logger.warning(f"跳过生成无正式名称的过场动画资源: {cutscene_id}")
                    #     continue
                    f.write(f"{cutscene_id}:{cutscene_name}\n")
        logger.info(f"成功生成 {output_file_path} 文件")
    except IOError as e:
        logger.error(f"错误：写入文件 {output_file_path} 时发生错误：{e}")