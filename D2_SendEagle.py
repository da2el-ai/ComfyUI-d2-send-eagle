import os
import numpy as np
import json

from PIL import Image
from PIL.PngImagePlugin import PngInfo
from datetime import datetime

import folder_paths

from .modules.util import util
from .modules.eagle_api import EagleAPI
from .modules.prompt_info_extractor import PromptInfoExtractor

FORCE_WRITE_PROMPT = False


class D2_SendEagle:
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.type = "output"
        self.output_folder = ""
        self.subfolder_name = ""
        self.eagle_api = None


    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),
                "format": (["webp", "png"],),
                # webpの時に可逆（lossless）不可逆（lossy）どちらにするか
                "lossless_webp": (
                    "BOOLEAN",
                    {"default": True, "label_on": "lossless", "label_off": "lossy"},
                ),
                # lossy の時の圧縮率
                "compression": (
                    "INT",
                    {"default": 80, "min": 1, "max": 100, "step": 1},
                ),
                # プロンプトをEagleタグに保存するか
                "save_tags": (
                    "BOOLEAN",
                    {"default": False, "label_on": "save", "label_off": "none"},
                ),
                # 保存するファイル名
                "filename_template": (
                    "STRING",
                    {"multiline": False, "default":"{model}-{width}-{height}-{seed}"},
                ),
                # Eagleフォルダ
                "eagle_folder": (
                    "STRING",
                    {"default": ""}
                ),

                # ポジティブプロンプト
                "positive": (
                    "STRING",
                    {"forceInput": True, "multiline": True},
                ),
                # ネガティブプロンプト
                "negative": (
                    "STRING",
                    {"forceInput": True, "multiline": True},
                ),
                # その他メモ
                "memo_text": (
                    "STRING",
                    {"multiline": True},
                ),
            },
            "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"},
        }

    RETURN_TYPES = ()
    FUNCTION = "add_item"
    OUTPUT_NODE = True
    CATEGORY = "D2"

    # ######################
    # ノード実行でEagleに画像を送る
    def add_item(
        self,
        images,
        format="webp",
        lossless_webp=False,
        save_tags=True,
        filename_template = "{model}-{width}-{height}-{seed}",
        eagle_folder = "",
        compression=80,
        positive=None,
        negative=None,
        memo_text=None,
        prompt=None,
        extra_pnginfo=None,
    ):
        self.output_folder, self.subfolder_name = self.get_output_folder()
        self.eagle_api = EagleAPI()

        results = list()
        params = {
            "format": format,
            "lossless_webp": lossless_webp,
            "save_tags": save_tags,
            "filename_template": filename_template,
            "compression": compression,
            "positive": positive,
            "negative": negative,
            "memo_text": memo_text,
            "prompt": prompt,
            "extra_pnginfo": extra_pnginfo,
        }

        for image in images:
          results.append(self.create_image_object(image, params))

        return {"ui": {"images": results}}


    # ######################
    # イメージオブジェクトを作成
    def create_image_object(self, image, params) -> dict:
        normalized_pixels = 255.0 * image.cpu().numpy()
        img = Image.fromarray(np.clip(normalized_pixels, 0, 255).astype(np.uint8))

        # 画像をローカルに保存
        file_name, file_full_path = self.save_image(img, params)

        # Send image to Eagle
        item = {"path": file_full_path, "name": file_name}
        item["annotation"] = util.make_annotation_text(
            params["positive"], params["negative"], params["memo_text"]
        )

        if(params["save_tags"]):
            item["tags"] = util.get_prompt_tags(params["positive"])

        _ret = self.eagle_api.add_item_from_path(data=item)

        return {
            "filename": file_name, "subfolder": self.subfolder_name, "type": self.type
        }

    # ######################
    # 画像をローカルに保存
    def save_image(self, img, params):
        file_name = ""
        file_full_path = ""
        filename_params = self.get_filename_params(img, params)

        if format == "webp":
            # Save webp image file
            file_name = self.get_filename(params["filename_template"], 'webp', filename_params)
            file_full_path = os.path.join(self.output_folder, file_name)

            exif_data = util.get_exif_from_prompt(
                img.getexif(), params["prompt"], params["extra_pnginfo"]
            )

            img.save(
                file_full_path,
                quality = params["compression"],
                exif = exif_data,
                lossless = params["lossless_webp"],
            )

        else:
            # Save png image file
            file_name = self.get_filename(params["filename_template"], 'png', filename_params)
            file_full_path = os.path.join(self.output_folder, file_name)

            metadata = PngInfo()

            if params["prompt"] is not None:
                metadata.add_text("prompt", json.dumps(params["prompt"]))
            if params["extra_pnginfo"] is not None:
                for x in params["extra_pnginfo"]:
                    metadata.add_text(x, json.dumps(params["extra_pnginfo"][x]))

            img.save(file_full_path, pnginfo=metadata, compress_level=4)

        return file_name, file_full_path

    # ######################
    # 画像保存パスを取得
    def get_output_folder(self):
        subfolder_name = datetime.now().strftime("%Y-%m-%d")

        # 画像保存用フォルダが無ければ作成
        output_folder = os.path.join(self.output_dir, subfolder_name)

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        return output_folder, subfolder_name


    # ######################
    # ファイルネーム用パラメーターを取得
    def get_filename_params(self, img, params) -> dict:
        width, height = img.size
        gen_data = PromptInfoExtractor(params["prompt"])

        model = ""
        steps = ""
        seed = ""

        if gen_data and hasattr(gen_data, 'info') and gen_data.info:
            model = os.path.splitext(gen_data.info.get("model_name", ""))[0]
            steps = gen_data.info.get("steps", "")
            seed = gen_data.info.get("seed", "")

        return {
            "width": width,
            "height": height,
            "model": model,
            "steps": steps,
            "seed": seed,
        }


    # ######################
    # ファイルネームを取得
    def get_filename(self, template:str, ext:str, filename_params) -> str:
        base = template.format(
          width = filename_params["width"],
          height = filename_params["height"],
          model = filename_params["model"],
          steps = filename_params["steps"],
          seed = filename_params["seed"],
        )

        return f"{util.get_datetime_str_msec()}-{base}.{ext}"


