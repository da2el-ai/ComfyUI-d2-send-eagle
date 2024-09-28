import json
import re
import yaml
import os
import shutil
from pathlib import Path
from ..my_types import TGenInfo, TConfig


DEBUG = False
BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_FILE = BASE_DIR / 'config.yaml'
CONFIG_ORG = BASE_DIR / 'config.org.yaml'


def dprint(str, dict=[]):
    if DEBUG:
        print(f"debug:{str}")
        if dict:
            print(json.dumps(dict, indent=2))


class ParamsExtractor:
    def __init__(self, params, ):
        """constructor

        Args:
            prompt (_type_): ComfyUI hidden object "prompt".
        """
        self._prompt = params["prompt"]

        if DEBUG:
            self._show_data()

        self._load_config()
        self.gen_info:TGenInfo = self._gather_info(params["positive"], params["negative"])


    # ##################
    # プロンプトからEagleタグを取得
    def get_prompt_tags(self):
        cleaned_string = re.sub(r":\d+\.\d+", "", self.gen_info["positive"])
        items = cleaned_string.split(",")

        return [
            re.sub(r"[\(\)]", "", item).strip()
            for item in items
            if re.sub(r"[\(\)]", "", item).strip()
        ]


    # ##################
    # 設定ファイルを読み込む
    def _load_config(self):
        # ユーザー設定がなければオリジナル設定をコピーする
        if not os.path.exists(CONFIG_FILE):
            shutil.copy2(CONFIG_ORG, CONFIG_FILE)

        with open(CONFIG_FILE, "r", encoding="utf-8") as file:
            self.config:TConfig = yaml.safe_load(file)


    # ##################
    # 受け取ったパラメターを表示
    def _show_data(self):
        dprint("prompt(hidden object)", self._prompt)


    # ##################
    # 必要なパラメーターをまとめる
    def _gather_info(self, positive, negative) -> TGenInfo:

        gen_info:TGenInfo = {
            "steps": 0,
            "sampler_name": "",
            "scheduler": "",
            "cfg": 0,
            "seed": 0,
            "model_name": "",
            "width": 0,
            "height": 0,
            "positive": positive,
            "negative": negative,
        }

        ksamplers = self._get_ksamplers()

        if not ksamplers:
            return gen_info

        # 最初のKsamplerのみ対象とする
        key, ksampler = ksamplers[0]

        gen_info["model_name"] = self._extract_model_name(ksampler)
        width, height = self._extract_image_size(ksampler)
        gen_info["width"] = width
        gen_info["height"] = height
        gen_info["steps"] = ksampler["inputs"]["steps"]
        gen_info["sampler_name"] = self._extract_sampler_name(ksampler)
        gen_info["scheduler"] = ksampler["inputs"]["scheduler"]
        gen_info["cfg"] = ksampler["inputs"]["cfg"]
        gen_info["seed"] = ksampler["inputs"].get(
            "seed", ksampler["inputs"].get("noise_seed", None)
        )
        
        return gen_info


    def _get_ksamplers(self):
        ksamplers = [
            (k, v)
            for k, v in self._prompt.items()
            if v["class_type"] in self.config["ksamplers"]
        ]
        return sorted(ksamplers, key=lambda x: int(x[0]))


    # ######################
    # モデル名を取得
    def _extract_model_name(self, node):
        try:
            model_input = node.get("inputs", {}).get("model")
            if model_input and isinstance(model_input, list) and model_input:
                ckpt_name = self._get_ckpt_name(model_input[0])
                if ckpt_name:
                    return ckpt_name.replace("/", "_").replace("\\", "_")
        except Exception:
            pass
        return ""

    # モデル名読み込んだノードIDからモデル名を取得
    def _get_ckpt_name(self, node_number):
        """Recursively search for the 'ckpt_name' key starting from the specified node."""
        node = self._prompt[node_number]
        if "ckpt_name" in node["inputs"]:
            return node["inputs"]["ckpt_name"]
        if "model" in node["inputs"]:
            return self._get_ckpt_name(node["inputs"]["model"][0])
        if "unet_name" in node["inputs"]:
            return node["inputs"]["unet_name"]
        return None


    # ######################
    # サンプラー名を取得
    def _extract_sampler_name(self, node):
        sampler = node["inputs"].get("sampler") or node["inputs"].get("sampler_name")
        return sampler if sampler is not None else ""

    # ######################
    # 画像サイズを取得
    def _extract_image_size(self, node):
        # サイズ情報を持ってるならそのまま返す
        if "width" in node["inputs"]:
            return node["inputs"]["width"], node["inputs"]["height"]

        width, height = self._get_image_size_from_latent_image(node["inputs"]["latent_image"][0])
        return width, height

    def _get_image_size_from_latent_image(self, node_number):
        target_node = self._prompt[node_number]

        if "width" in target_node["inputs"]:
            return target_node["inputs"]["width"], target_node["inputs"]["height"]

        if "clip_width" in target_node.get("outputs", {}):
            return target_node["outputs"]["clip_width"], target_node["outputs"]["clip_height"]

        elif target_node["class_type"] == "SDXL Empty Latent Image":
            resolusion_str = target_node["inputs"]["resolution"]
            pattern = r"(\d+) x (\d+)"
            match = re.search(pattern, resolusion_str)
            return int(match.group(1)), int(match.group(2))

        else:
            return 0, 0

    # ######################
    # PngInfoやEagleメモ用のテキストに整形
    def format_info(self, memo:str):
        formatted_str = self.config["output_format"].format(**self.gen_info, memo=memo)
        return formatted_str

    # def extract_and_format(self):
    #     """Extract and format the required information from the loaded JSON data."""
    #     info = self._gather_info()
    #     if not info:
    #         return "No suitable data found."
    #     return self.format_info(info)

    # def formatted_annotation(self):
    #     annotation = ""
    #     if len(self.info["prompt"]) > 0:
    #         annotation += self.info["prompt"]

    #     if len(self.info["negative"]) > 0:
    #         if len(annotation) > 0:
    #             annotation += "\n"
    #         annotation += "Negative prompt: "
    #         annotation += self.info["negative"]

    #     if len(annotation) > 0:
    #         annotation += "\n"
    #     annotation += self.extract_and_format()

    #     return annotation

