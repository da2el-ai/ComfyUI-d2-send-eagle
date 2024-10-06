# D2 Send Eagle

[English][<a href="README_ja.md">日本語</a>][<a href="README_zh.md">繁体中文</a>]

This is a custom node for ComfyUI that sends generated images to the image management software [Eagle](https://en.eagle.cool/).

It's an extension of an existing custom node [ComfyUI-send-eagle-slim](https://github.com/shingo1228/ComfyUI-send-eagle-slim), modified to my preferences. Thanks to Shingo.T for creating the original excellent custom node.

<img src="img/image.png">


## Sample Workflow

<img src="img/sample_workflow.png">


---

## 主な機能Main Features

- Send images received via `image` to Eagle
- Record text received via `positive` and `negative` as memos in Eagle
- Option to choose between png and webp formats


### Differences between png and webp formats

- png format
  - **Can save** ComfyUI workflow
  - **Cannot be displayed** in StableDiffusion webui A1111's PNGInfo
- webp format
  - **Cannot save** ComfyUI workflow
  - **Can be displayed** in StableDiffusion webui A1111's PNGInfo

---

## Installation

### Using ComfyUI Manager

1. Open ComfyUI Manager
2. Click on `Custom Nodes Manager`
3. Search for `D2 Send Eagle`
4. Click `Install`
5. Restart ComfyUI

### Using Command Prompt

1. Open Command Prompt
2. Navigate to `{ComfyUI installation folder}/custom_nodes`
3. Run `git clone https://github.com/da2el-ai/ComfyUI-d2-send-eagle`

---

## Inputs / Options

- `images`
  - Images to be saved
- `positive`
  - Positive prompt
- `negative`
  - Negative prompt
- `format`
  - Choose between webp / png for saving format
- `lossless_webp`
  - Choose between lossless or lossy. Effective when `webp` is selected.
- `compression`
  - Specify compression rate. Effective when `lossy` is selected for webp.
- `save_tags`
  - Choose whether to save as Eagle tags
  - `None`: Don't save
  - `Prompt + Checkpoint`: Save prompts and model name
  - `Prompt`: Save prompts
  - `Checkpoint`: Save model name
- `filename_template`
  - Specify filename format
  - Default is `{model}-{width}-{height}-{seed}`
  - Available parameters: `width`, `height`, `model_name`, `steps`, `seed`
- `eagle_folder`
  - Specify Eagle folder name or folder ID. If the folder doesn't exist, it will be created.

---

## Other Features

### Local Image Saving

In addition to sending to Eagle, images are also saved locally in the following folder.
This folder name cannot be changed.

`./ComfyUI/output/YYYY-MM-DD/YYYYMMDD_HHMMss_SSSSSS-{FinalImage_width}-{FinalImage_height}.webp`

### Supported KSamplers

The following KSampler types are supported.
You can add more by editing `config.yaml`.

- KSampler
- KSamplerAdvanced
- KSampler With Refiner (Fooocus)
- BNK_TiledKSampler
- KSampler (Efficient)
- GenerateNAID

---

## Change Log

- 2024/10/04
  - Added a toggle button to hide image previews
    - This was added because when the preview was enlarged, the `memo_text` also became larger and obstructive
  - Added IMAGE to output
    - This is just a pass-through. It's not necessary, but we added it anyway
- 2024/09/29
  - Added support for NovelAI generation node GenerateNAID
  - Made it possible to specify settings in `config.yaml`
  - Added recording of prompt information in Exif for webp format
- 2024/08/19
  - Fixed issue where model name couldn't be retrieved when using Unet Loader
- 2024/08/04
  - Initial release
