import os
from loguru import logger

def generate_gcg_res_player_property(output_dir, player_property_file):
    """
    生成 PlayerProperty.txt 文件，复制指定文件的内容。
    """
    logger.info("开始生成 PlayerProperty.txt 文件...")
    output_file = os.path.join(output_dir, "PlayerProperty.txt")

    try:
        # 确保输出目录存在
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(player_property_file, 'r', encoding='latin-1') as infile:
            content = infile.read()
        logger.info(f"成功读取源文件: {player_property_file}")
        
        with open(output_file, 'w', encoding='latin-1') as outfile:
            outfile.write(content)
        logger.info(f"成功生成 {output_file} 文件")
    except FileNotFoundError:
        logger.warning(f"警告：未找到源文件 {player_property_file}，尝试从 en-us 目录加载。")
        # 直接在GCG-Res-Origin目录下查找en-us文件夹
        gcg_res_origin_dir = os.path.dirname(player_property_file)
        en_us_dir = os.path.join(gcg_res_origin_dir, 'en-us')
        player_property_file_en_us = os.path.join(en_us_dir, os.path.basename(player_property_file))
        
        try:
            with open(player_property_file_en_us, 'r', encoding='latin-1') as infile:
                content = infile.read()
            logger.info(f"成功从 en-us 目录读取源文件: {player_property_file_en_us}")
            with open(output_file, 'w', encoding='latin-1') as outfile:
                outfile.write(content)
            logger.info(f"成功生成 {output_file} 文件")
        except FileNotFoundError:
            logger.error(f"错误：未找到 en-us 源文件 {player_property_file_en_us}")
        except Exception as e:
            logger.error(f"错误：从 en-us 生成 PlayerProperty.txt 失败: {e}")
    except Exception as e:
        logger.error(f"错误：生成 PlayerProperty.txt 失败: {e}")