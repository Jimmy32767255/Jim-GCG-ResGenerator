import os
from loguru import logger

def generate_gcg_res_banners(output_dir, banners_file):
    """
    生成 Banners.json 文件，复制指定文件的内容。
    """
    logger.info("开始生成 Banners.json 文件...")
    output_file = os.path.join(output_dir, "Banners.json")
    
    try:
        # 确保输出目录存在
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(banners_file, 'r', encoding='latin-1') as infile:
            content = infile.read()
        logger.info(f"成功读取源文件: {banners_file}")
        
        with open(output_file, 'w', encoding='latin-1') as outfile:
            outfile.write(content)
        logger.info(f"成功生成 {output_file} 文件")
    except FileNotFoundError:
        logger.error(f"错误：未找到源文件 {banners_file}")
    except Exception as e:
        logger.error(f"错误：生成 Banners.json 失败: {e}")