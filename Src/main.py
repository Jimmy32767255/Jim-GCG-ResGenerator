import os
import sys
import argparse
import shutil
from tqdm import tqdm
from loguru import logger

# 配置Loguru日志
logger.remove()  # 移除默认的控制台输出
logger.add(sys.stderr, level="ERROR")  # 控制台只显示ERROR及以上等级的日志
logger.add("log.txt", level="DEBUG")  # 记录DEBUG级别日志到log.txt

def normalize_path(path):
    """统一路径格式，处理Windows路径问题"""
    return os.path.normpath(path.strip())

# 导入各个生成脚本
from Gadget import generate_gcg_res_gadget
from Achievement import generate_gcg_res_achievement
from Activity import generate_gcg_res_activity
from Artifact import generate_gcg_res_artifact
from Item import generate_gcg_res_item
from Monsters import generate_gcg_res_monsters
from Quest import generate_gcg_res_quest
from Weapon import generate_gcg_res_weapon
from ArtifactCat import generate_gcg_res_artifact_cat
from ArtifactMainAttribution import generate_gcg_res_artifact_main_attribution
from ArtifactSubAttribution import generate_gcg_res_artifact_sub_attribution
from Avatar import generate_gcg_res_avatar
from CustomCommands import generate_gcg_res_custom_commands
from Cutscene import generate_gcg_res_cutscene
from Dungeon import generate_gcg_res_dungeon
from GachaBannerPrefab import generate_gcg_res_gacha_banner_prefab
from GachaBannerTitle import generate_gcg_res_gacha_banner_title
from PlayerProperty import generate_gcg_res_player_property
from Scene import generate_gcg_res_scene
from ShopType import generate_gcg_res_shop_type
from IconGrasscutterIco import copy_icon_grasscutter_ico
from IconGrasscutterPng import copy_icon_grasscutter_png
from ImgSupportPng import copy_img_support_png
from NewtonsoftJsonDll import copy_newtonsoft_json_dll
from Banners import generate_gcg_res_banners
from MyTools import generate_gcg_res_mytools
from Permissions import generate_gcg_res_permissions
from SceneTag import generate_gcg_res_scene_tag
from WeaponColor import generate_gcg_res_weapon_color
from Weather import generate_gcg_res_weather

def generate_resources_core(output_dir, grasscutter_res_origin_path, gcg_res_origin_path,
                            enable_fallback_language=False,
                            generate_all=True,
                            not_generate_no_json_name_res=False,
                            not_generate_no_text_map_name_res=False,
                            added_mode=False):
    logger.info("开始生成所有GCG资源文件...")

    if added_mode:
        logger.info(f"启用补充模式，正在复制 {gcg_res_origin_path} 到 {output_dir}...")
        try:
            # 复制 GCG-Res-Origin 到 GCG-Res-Output
            if os.path.exists(output_dir):
                shutil.rmtree(output_dir)
            shutil.copytree(gcg_res_origin_path, output_dir)
            logger.info("复制完成。")
        except Exception as e:
            logger.error(f"复制文件时出错: {e}")
            return

    # 处理生成选项的互斥性
    selected_options = sum([generate_all, not_generate_no_json_name_res, not_generate_no_text_map_name_res])
    if selected_options > 1:
        logger.error("错误：'生成所有资源'、'不生成无Json名称资源' 和 '不生成无正式名称资源' 只能选择其中一个。")
        return
    
    # 如果选择了“生成所有资源”，则强制其他两个为False
    if generate_all:
        not_generate_no_json_name_res = False
        not_generate_no_text_map_name_res = False

    excel_bin_output_path = os.path.join(grasscutter_res_origin_path, "ExcelBinOutput")
    text_map_root_path = os.path.join(grasscutter_res_origin_path, "TextMap")

    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    # 定义语言代码到文件夹名称的映射
    lang_map = {
        "CHS": "zh-cn",
        "CHT": "zh-tw",
        "DE": "de-de",
        "EN": "en-us",
        "ES": "es-es",
        "FR": "fr-fr",
        "ID": "id-id",
        "IT": "it-it",
        "JP": "ja-jp",
        "KR": "ko-kr",
        "PT": "pt-pt",
        "RU": "ru-ru",
        "TH": "th-th",
        "TR": "tr-tr",
        "VI": "vi-vn",
    }

    # 获取所有需要处理的JSON文件
    try:
        json_files = [f for f in os.listdir(text_map_root_path) if f.startswith("TextMap") and f.endswith(".json")]
        if not json_files:
            logger.error(f"在 {text_map_root_path} 中未找到任何TextMap JSON文件")
            return
    except Exception as e:
        logger.error(f"无法读取TextMap目录: {e}")
        return

    # 使用tqdm显示总进度
    with tqdm(total=len(json_files), desc="总进度", unit="语言") as total_pbar:
        # 遍历TextMap目录下的所有JSON文件
        for filename in json_files:
            try:
                if filename.startswith("TextMap") and filename.endswith(".json"):
                    lang_code = filename[len("TextMap"): -len(".json")]
                    if lang_code.endswith("_0") or lang_code.endswith("_1"):
                        lang_code = lang_code[:-2]  # 移除_0或_1

                    output_sub_dir_name = lang_map.get(lang_code, lang_code.lower())

                    # 如果未启用回退语言，则检查GCG-Res-Origin目录下是否存在对应语言的文件夹
                    if not enable_fallback_language:
                        lang_dir_path = os.path.join(gcg_res_origin_path, output_sub_dir_name)
                        if not os.path.exists(lang_dir_path):
                            logger.warning(f"跳过语言版本 {lang_code}，因为在 {gcg_res_origin_path} 中未找到对应的语言文件夹 {output_sub_dir_name} 且未启用回退语言")
                            total_pbar.update(1)
                            continue

                    current_output_dir = os.path.join(output_dir, output_sub_dir_name)
                    os.makedirs(current_output_dir, exist_ok=True)
                    current_text_map_path = os.path.join(text_map_root_path, filename)

                    logger.info(f"\n===== 正在处理语言: {lang_code} =====")
                    logger.info(f"输出目录: {current_output_dir}")
                    logger.info(f"TextMap路径: {current_text_map_path}")

                    # 定义所有生成函数及其参数
                    generation_tasks = [
                        # 添加生成任务
                        (generate_gcg_res_gadget, (current_output_dir, excel_bin_output_path, current_text_map_path, not_generate_no_json_name_res, not_generate_no_text_map_name_res, added_mode)),
                        (generate_gcg_res_achievement, (current_output_dir, excel_bin_output_path, current_text_map_path, not_generate_no_json_name_res, not_generate_no_text_map_name_res, added_mode)),
                        (generate_gcg_res_activity, (current_output_dir, excel_bin_output_path, current_text_map_path, not_generate_no_json_name_res, not_generate_no_text_map_name_res, added_mode)),
                        (generate_gcg_res_artifact, (current_output_dir, excel_bin_output_path, current_text_map_path, not_generate_no_json_name_res, not_generate_no_text_map_name_res, added_mode)),
                        (generate_gcg_res_item, (current_output_dir, excel_bin_output_path, current_text_map_path, not_generate_no_json_name_res, not_generate_no_text_map_name_res, added_mode)),
                        (generate_gcg_res_monsters, (current_output_dir, excel_bin_output_path, current_text_map_path, not_generate_no_json_name_res, not_generate_no_text_map_name_res, added_mode)),
                        (generate_gcg_res_quest, (current_output_dir, excel_bin_output_path, current_text_map_path, not_generate_no_json_name_res, not_generate_no_text_map_name_res, added_mode)),
                        (generate_gcg_res_weapon, (current_output_dir, excel_bin_output_path, current_text_map_path, not_generate_no_json_name_res, not_generate_no_text_map_name_res, added_mode)),
                        (generate_gcg_res_artifact_cat, (current_output_dir, excel_bin_output_path, current_text_map_path, not_generate_no_json_name_res, not_generate_no_text_map_name_res, added_mode)),
                        (generate_gcg_res_artifact_main_attribution, (current_output_dir, excel_bin_output_path, current_text_map_path, not_generate_no_json_name_res, not_generate_no_text_map_name_res, added_mode)),
                        (generate_gcg_res_artifact_sub_attribution, (current_output_dir, excel_bin_output_path, current_text_map_path, not_generate_no_json_name_res, not_generate_no_text_map_name_res, added_mode)),
                        (generate_gcg_res_avatar, (current_output_dir, excel_bin_output_path, current_text_map_path, not_generate_no_json_name_res, not_generate_no_text_map_name_res, added_mode)),
                        (generate_gcg_res_custom_commands, (current_output_dir, gcg_res_origin_path, output_sub_dir_name)),
                        (generate_gcg_res_cutscene, (current_output_dir, excel_bin_output_path, current_text_map_path, not_generate_no_json_name_res, not_generate_no_text_map_name_res, added_mode)),
                        (generate_gcg_res_dungeon, (current_output_dir, excel_bin_output_path, current_text_map_path, not_generate_no_json_name_res, not_generate_no_text_map_name_res, added_mode)),
                        (generate_gcg_res_gacha_banner_prefab, (current_output_dir, os.path.join(gcg_res_origin_path, "GachaBannerPrefab.txt"))),
                        (generate_gcg_res_gacha_banner_title, (current_output_dir, os.path.join(gcg_res_origin_path, "GachaBannerTitle.txt"))),
                        (generate_gcg_res_player_property, (current_output_dir, os.path.join(gcg_res_origin_path, "PlayerProperty.txt"))),
                        (generate_gcg_res_scene, (current_output_dir, excel_bin_output_path, current_text_map_path, not_generate_no_json_name_res, not_generate_no_text_map_name_res, added_mode)),
                        (generate_gcg_res_shop_type, (current_output_dir, excel_bin_output_path, current_text_map_path, not_generate_no_json_name_res, not_generate_no_text_map_name_res, added_mode)),
                    ]

                    if generation_tasks:
                        with tqdm(total=len(generation_tasks), desc=f"语言 {lang_code}", unit="文件", leave=False) as lang_pbar:
                            for func, args in generation_tasks:
                                try:
                                    logger.info(f"正在执行: {func.__name__}")
                                    func(*args)
                                except Exception as e:
                                    logger.error(f"生成 {func.__name__} 时出错: {e}")
                                lang_pbar.update(1)
                    else:
                        logger.info(f"语言 {lang_code}：没有选择任何生成任务，跳过。")
                    total_pbar.update(1)
            except Exception as e:
                logger.error(f"处理文件 {filename} 时出错: {e}")
                total_pbar.update(1)

    # 调用复制脚本复制其他文件
    logger.info("\n===== 开始复制全局资源文件 =====")
    try:
        copy_icon_grasscutter_ico(output_dir, os.path.join(gcg_res_origin_path, "IconGrasscutter.ico"))
        copy_icon_grasscutter_png(output_dir, os.path.join(gcg_res_origin_path, "IconGrasscutter.png"))
        copy_img_support_png(output_dir, os.path.join(gcg_res_origin_path, "ImgSupport.png"))
        copy_newtonsoft_json_dll(output_dir, os.path.join(gcg_res_origin_path, "Newtonsoft.Json.dll"))
        generate_gcg_res_banners(output_dir, os.path.join(gcg_res_origin_path, "Banners.json"))
        generate_gcg_res_mytools(output_dir, os.path.join(gcg_res_origin_path, "MyTools.java"))
        generate_gcg_res_permissions(output_dir, os.path.join(gcg_res_origin_path, "Permissions.txt"))
        generate_gcg_res_scene_tag(output_dir, os.path.join(gcg_res_origin_path, "SceneTag.txt"))
        generate_gcg_res_weapon_color(output_dir, os.path.join(gcg_res_origin_path, "WeaponColor.txt"))

    except Exception as e:
        logger.error(f"复制全局资源文件时出错: {e}")

    logger.info("\n所有GCG资源文件生成和复制完成。")

def main():
    output_dir = normalize_path(args.gcg_res_output) if args.gcg_res_output else normalize_path(input("请输入GCG-Res-Output目录的路径: "))
    if not output_dir:
        logger.error("未输入GCG-Res-Output目录，程序退出")
        return

    gcg_res_origin_path = normalize_path(args.gcg_res_origin) if args.gcg_res_origin else normalize_path(input("请输入GCG-Res-Origin目录的路径: "))
    if not gcg_res_origin_path:
        logger.error("未输入GCG-Res-Origin目录，程序退出")
        return

    grasscutter_res_origin_path = normalize_path(args.grasscutter_res_origin) if args.grasscutter_res_origin else normalize_path(input("请输入Grasscutter-Res-Origin目录的路径: "))
    if not grasscutter_res_origin_path:
        logger.error("未输入Grasscutter-Res-Origin目录，程序退出")
        return

    generate_resources_core(output_dir,
                            grasscutter_res_origin_path,
                            gcg_res_origin_path,
                            args.enable_fallback_language,
                            args.generate_all,
                            args.not_generate_no_json_name_res,
                            args.not_generate_no_text_map_name_res,
                            args.added_mode)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GCG资源生成器")
    parser.add_argument('-C', '--cli', action='store_true', help='以命令行模式运行')
    parser.add_argument('-B', '--enable-fallback-language', action='store_true', help='启用回退语言')
    parser.add_argument('-A', '--generate-all', action='store_true', help='生成所有资源')
    parser.add_argument('-J', '--not-generate-no-json-name-res', action='store_true', help='不生成无Json名称资源')
    parser.add_argument('-M', '--not-generate-no-text-map-name-res', action='store_true', help='不生成无正式名称资源')
    parser.add_argument("-S", "--added-mode", action="store_true", help="启用补充模式，先复制再生成缺失资源")
    parser.add_argument("-O", "--gcg-res-output", type=str, help="GCG-Res-Output目录的路径")
    parser.add_argument("-G", "--gcg-res-origin", type=str, help="GCG-Res-Origin目录的路径")
    parser.add_argument("-R", "--grasscutter-res-origin", type=str, help="Grasscutter-Res-Origin目录的路径")
    args = parser.parse_args()

    if args.cli:
        main()
    else:
        from gui import GCGResGeneratorGUI
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        window = GCGResGeneratorGUI()
        window.show()
        sys.exit(app.exec_())