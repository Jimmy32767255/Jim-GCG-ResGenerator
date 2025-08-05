import os
import json
from loguru import logger

def generate_gcg_res_shop_type(output_dir, excel_bin_output_path, text_map_path, not_generate_no_json_name_res, not_generate_no_text_map_name_res, added_mode):
    """
    生成 ShopType.txt 文件，从 ShopExcelConfigData.json 中读取数据。
    """
    logger.info("开始生成 ShopType.txt 文件...")
    output_file = os.path.join(output_dir, "ShopType.txt")
    shop_excel_file = os.path.join(excel_bin_output_path, "ShopExcelConfigData.json")

    shop_data = {}
    if added_mode and os.path.exists(output_file):
        with open(output_file, 'r', encoding='latin-1') as f:
            for line in f:
                line = line.strip()
                if line and ':' in line:
                    try:
                        shop_id, shop_name = line.split(':', 1)
                        shop_data[int(shop_id)] = shop_name
                    except ValueError:
                        logger.warning(f"跳过 ShopType.txt 中格式错误的行: {line}")

    try:
        with open(shop_excel_file, 'r', encoding='latin-1') as f:
            shops = json.load(f)

        for shop in shops:
            shop_id = shop.get("shopId")
            shop_type = shop.get("shopType")

            if shop_id is None:
                continue

            if not_generate_no_json_name_res and not shop_type:
                logger.info(f"跳过 Shop ID: {shop_id}，因为没有 shopType 字段且设置了不生成无JSON名称资源。")
                continue

            if not_generate_no_text_map_name_res:
                # ShopType.json 中没有需要文本映射的字段，此参数在此处不生效，但为了保持一致性保留
                pass

            name = shop_type if shop_type else f"[N/A] 商店ID {shop_id}"
            shop_data[shop_id] = name

        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w', encoding='latin-1') as f:
            for shop_id in sorted(shop_data.keys()):
                f.write(f"{shop_id}:{shop_data[shop_id]}\n")
        logger.info(f"成功生成 {output_file} 文件")

    except FileNotFoundError:
        logger.error(f"错误：未找到文件 {shop_excel_file}")
    except Exception as e:
        logger.error(f"错误：生成 ShopType.txt 失败: {e}")