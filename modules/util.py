import os
import json
import traceback
import re
from PIL import Image
import piexif
import piexif.helper
from datetime import datetime
from typing import Dict, Optional, TypedDict, Union, List
from ..my_types import TGenInfo



class util:
    # @staticmethod
    # def initialize_defaults(prompt, extra_pnginfo):
    #     util.write_prompt(prompt, extra_pnginfo)
    #     print("check prompt_decode_err.log")
    #     traceback.print_exc()
    #     return "", [], "unknown", "00", "000000"

    # @staticmethod
    # def write_prompt(prompt, extra_pnginfo):
    #     log_file_name = os.path.join(os.path.dirname(__file__), "prompt_decode_err.log")
    #     with open(log_file_name, "w", encoding="utf-8") as f:
    #         f.write('"prompt:"\n')
    #         json.dump(prompt, f, indent=4, ensure_ascii=False)
    #         if extra_pnginfo is not None:
    #             f.write('\n\n"extra_pnginfo:"\n')
    #             json.dump(extra_pnginfo, f, indent=4, ensure_ascii=False)


    @staticmethod
    def _is_valid_text(text):
        return isinstance(text, str) and text.strip() and text != "undefined"

    # # #############################
    # # Eagle保存用コメントを作成
    # @staticmethod
    # def make_annotation_text(gen_info:TGenInfo) -> str:
    #     positive = gen_info["prompt_text"]["prompt"]
    #     negative = gen_info["prompt_text"]["negative"]
    #     tmp_annotation = ""

    #     if util._is_valid_text(positive):
    #         tmp_annotation += positive
    #     if util._is_valid_text(negative):
    #         tmp_annotation += "\n" if tmp_annotation.strip() else ""
    #         tmp_annotation += "Negative prompt:" + negative
    #     if util._is_valid_text(memo_text):
    #         tmp_annotation += "\n" if tmp_annotation.strip() else ""
    #         tmp_annotation += "Memo:" + memo_text
    #     return tmp_annotation


    # ####################
    # 現在時刻のテキストを取得
    @staticmethod
    def get_datetime_str_msec() -> str:
        """
        Gets the current datetime as a string with millisecond precision.
        This method generates and returns a string representing the current datetime with millisecond precision.
        """
        now = datetime.now()
        date_time_str = now.strftime("%Y%m%d_%H%M%S")
        return f"{date_time_str}_{now.microsecond:06}"


    # #########################
    # webp用にExifデータを作成する
    # ただしa1111のPNGInfoに表示するが、ワークフローは再現しない
    @staticmethod
    def get_exif_from_prompt(img, formated_info:str, extra_pnginfo, prompt):
        metadata = img.getexif()

        if len(metadata) == 0:
            metadata = {"0th": {}, "Exif": {}, "GPS": {}, "Interop": {}, "1st": {}}

        if prompt is not None:
            metadata["0th"][0x0110] = "prompt:{}".format(json.dumps(prompt))
        if extra_pnginfo is not None:
            inital_exif = 0x010f
            for x in extra_pnginfo:
                metadata["0th"][inital_exif] = "{}:{}".format(x, json.dumps(extra_pnginfo[x]))
                inital_exif -= 1

        metadata["Exif"][piexif.ExifIFD.UserComment] = piexif.helper.UserComment.dump(formated_info, "unicode")

        return piexif.dump(metadata)


    @staticmethod
    def get_prompt_tags(prompt_text: str) -> list:
        if (
            not isinstance(prompt_text, str)
            or not prompt_text.strip()
            or prompt_text == "undefined"
        ):
            return []

        cleaned_string = re.sub(r":\d+\.\d+", "", prompt_text)
        items = cleaned_string.split(",")
        return [
            re.sub(r"[\(\)]", "", item).strip()
            for item in items
            if re.sub(r"[\(\)]", "", item).strip()
        ]
