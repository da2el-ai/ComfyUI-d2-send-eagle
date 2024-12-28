# D2 Send Eagle

[English][<a href="README_ja.md">日本語</a>][<a href="README_zh.md">繁体中文</a>]


A custom node for sending images generated in ComfyUI to the image management software [Eagle](https://en.eagle.cool/).

Please also try [D2 Nodes ComfyUI](https://github.com/da2el-ai/d2-nodes-ComfyUI/), which contains a collection of useful custom nodes.


<img src="img/image.png">


## Sample Workflows

### Basic Configuration Workflow

<a href="workflow/workflow_basic.png" target="_blkank">
  <img src="workflow/workflow_basic.png">
</a>

### Workflow Using D2 Nodes ComfyUI

<a href="workflow/workflow_d2-node.png" target="_blkank">
  <img src="workflow/workflow_d2-node.png">
</a>

- Gets checkpoint name from `D2 Checkpoint Loader` and removes the ".safetensors" extension using `D2 Filename Template`
- Retrieves generation parameters from `d2_pipe`


---

## Main Features

- Sends images received through `image` to Eagle
- Records text received through `positive` and `negative` as Eagle memos
- Supports both png and webp formats

### Generation Parameters Recorded as Image and Eagle Comments

- Parameters such as positive, negative, CFG, steps are retrieved from the KSampler connected to D2 Send Eagle
- May not be retrievable depending on the workflow
- Parameters can also be specified through d2_pipe


#### Supported KSamplers

The following KSampler types are supported.
You can add more by editing `config.yaml`.

- KSampler
- KSamplerAdvanced
- KSampler With Refiner (Fooocus)
- BNK_TiledKSampler
- KSampler (Efficient)
- GenerateNAID


### Differences Between png and webp Formats

- png format
  - **Can save** ComfyUI workflows
  - **Cannot display** in StableDiffusion webui A1111's PNGInfo
- webp format
  - **Cannot save** ComfyUI workflows
  - **Can display** in StableDiffusion webui A1111's PNGInfo

---

## Installation

### Using ComfyUI Manager

1. Open ComfyUI Manager
2. Click `Custom Nodes Manager`
3. Search for `D2 Send Eagle`
4. Click `Install`
5. Restart ComfyUI

### Using Command Prompt

1. Open Command Prompt
1. Navigate to `{ComfyUI installation folder}/custom_nodes`
2. `git clone https://github.com/da2el-ai/ComfyUI-d2-send-eagle`

---

## Inputs / Options

- `images`
  - Images to save
- `d2_pipe`
  - Collection of generation parameters
- `positive`
  - Positive prompt
- `negative`
  - Negative prompt
- `format`
  - Choose from webp / png / jpeg formats
- `lossless_webp`
  - Choose between lossless and lossy. Active when `webp` is selected.
- `compression`
  - Specify compression rate. Active when selecting `lossy` for webp or when using `jpeg`.
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
  - Specify Eagle folder name or folder ID. Creates new folder if it doesn't exist

---

## Other Features

### Local Image Saving

In addition to sending to Eagle, images are also saved locally in the following folder.
This folder name cannot be changed.

`./ComfyUI/output/YYYY-MM-DD/YYYYMMDD_HHMMss_SSSSSS-{FinalImage_width}-{FinalImage_height}.webp`


---

## Change Log

- 2024/12/28
  - Added support for d2_pipe in d2-node-comfyui
- 2024/11/13
  - Added JPEG format support
- 2024/10/04
  - Added toggle button to hide image preview
    - Because enlarging preview also enlarged `memo_text` which was inconvenient
  - Added IMAGE to output
    - Just a passthrough. Not necessary but added anyway
- 2024/09/29
  - Added support for NovelAI generation node GenerateNAID
  - Made settings configurable through `config.yaml`
  - Added Exif prompt information recording for webp format
- 2024/08/19
  - Fixed issue with model name not being retrieved when using Unet Loader
- 2024/08/04
  - Initial release

---

## Acknowledgements

D2 Send Eagle is an extension of an existing custom node [ComfyUI-send-eagle-slim](https://github.com/shingo1228/ComfyUI-send-eagle-slim), modified to my preferences. Thanks to Shingo.T for creating such an excellent custom node.
