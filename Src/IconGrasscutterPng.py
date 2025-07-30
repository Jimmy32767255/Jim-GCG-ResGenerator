import os
from loguru import logger

def copy_icon_grasscutter_png(output_dir, source_file):
    """
    复制 IconGrasscutter.png 文件。
    """
    logger.info("开始复制 IconGrasscutter.png 文件...")
    output_file = os.path.join(output_dir, "IconGrasscutter.png")

    try:
        # 确保输出目录存在
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(source_file, 'rb') as infile:
            content = infile.read()
        logger.info(f"成功读取源文件: {source_file}")
        
        with open(output_file, 'wb') as outfile:
            outfile.write(content)
        logger.info(f"成功复制 {output_file} 文件")
    except FileNotFoundError:
        logger.error(f"错误：未找到源文件 {source_file}")
    except Exception as e:
        logger.error(f"错误：复制 IconGrasscutter.png 失败: {e}")