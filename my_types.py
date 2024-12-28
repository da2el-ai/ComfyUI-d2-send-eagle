from dataclasses import dataclass
from typing import Dict, Optional, TypedDict, Union, List

# SendEagleノードの入力パラメーター
class TNodeParams(TypedDict):
    format: str
    lossless_webp: bool
    save_tags: str
    filename_template: str
    eagle_folder: str
    compression: int
    positive: Optional[str]
    negative: Optional[str]
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

@dataclass
class D2_TD2Pipe:
    ckpt_name: Optional[str] = None
    positive: Optional[str] = None
    negative: Optional[str] = None
    seed: Optional[int] = None
    steps: Optional[int] = None
    cfg: Optional[float] = None
    sampler_name: Optional[str] = None
    scheduler: Optional[str] = None
    denoise: Optional[float] = None
    width: Optional[int] = None
    height: Optional[int] = None
