from typing import Dict, Optional, TypedDict, Union, List

# SendEagleノードの入力パラメーター
class TNodeParams(TypedDict):
    format: str
    lossless_webp: bool
    save_tags: str
    filename_template: str
    eagle_folder: str
    compression: int
    positive: str
    negative: str
    memo_text: str
    prompt: Optional[Dict]
    extra_pnginfo: Optional[Dict]


# 生成情報をまとめた辞書
class TGenInfo(TypedDict):
    steps: int
    sampler_name: str
    scheduler: str
    cfg: float
    seed: int
    model_name: str
    width: int
    height: int
    positive: str
    negative: str

class TConfig(TypedDict):
    ksamplers: list
    output_format: str
