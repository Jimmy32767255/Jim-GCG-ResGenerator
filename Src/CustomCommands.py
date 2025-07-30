import os
from loguru import logger

def generate_gcg_res_custom_commands(output_dir, gcg_res_origin_path, lang):
    """
    生成 CustomCommands.txt 文件，包含自定义命令的描述和命令本身。
    """
    logger.info("开始生成 CustomCommands.txt 文件...")
    
    # 定义输入和输出文件路径
    source_file_path = os.path.join(gcg_res_origin_path, lang, 'CustomCommands.txt')
    output_file_path = os.path.join(output_dir, 'CustomCommands.txt')

    commands = {}
    try:
        with open(source_file_path, 'r', encoding='latin-1') as f:
            lines = f.readlines()
            for i in range(0, len(lines), 2):
                if i + 1 < len(lines):
                    description = lines[i].strip()
                    command = lines[i+1].strip()
                    if description and command:
                        commands[description] = command
        logger.info(f"成功读取源文件: {source_file_path}")
    except FileNotFoundError:
        logger.warning(f"警告：未找到源文件 {source_file_path}，尝试从 en-us 目录加载。")
        source_file_path_en_us = os.path.join(gcg_res_origin_path, 'en-us', 'CustomCommands.txt')
        try:
            with open(source_file_path_en_us, 'r', encoding='latin-1') as f:
                lines = f.readlines()
                for i in range(0, len(lines), 2):
                    if i + 1 < len(lines):
                        description = lines[i].strip()
                        command = lines[i+1].strip()
                        if description and command:
                            commands[description] = command
            logger.info(f"成功从 en-us 目录读取源文件: {source_file_path_en_us}")
        except FileNotFoundError:
            logger.error(f"错误：未找到 en-us 源文件 {source_file_path_en_us}。")
            return
        except Exception as e:
            logger.error(f"读取 en-us 源文件 {source_file_path_en_us} 失败: {e}。")
            return
    except Exception as e:
        logger.error(f"读取源文件 {source_file_path} 失败: {e}")
        return

    try:
        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
        with open(output_file_path, 'w', encoding='latin-1') as f:
            for description, command in commands.items():
                f.write(f"{description}\n{command}\n")
        logger.info(f"成功生成 {output_file_path} 文件")
    except IOError as e:
        logger.error(f"错误：写入文件 {output_file_path} 时发生错误：{e}")