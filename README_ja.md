# D2 Send Eagle

[<a href="README.md">English</a>][日本語][<a href="README_zh.md">繁体中文</a>]

ComfyUIで生成した画像を画像管理ソフト [Eagle](https://en.eagle.cool/) に送るカスタムノードです。

便利なカスタムノードをまとめた [D2 Nodes ComfyUI](https://github.com/da2el-ai/d2-nodes-ComfyUI/)も是非お試しください。


<img src="img/image.png">


## サンプルワークフロー

### 基本的な構成のワークフロー

<a href="workflow/workflow_basic.png" target="_blkank">
  <img src="workflow/workflow_basic.png">
</a>

### D2 Nodes ComfyUI を使ったワークフロー

<a href="workflow/workflow_d2-node.png" target="_blkank">
  <img src="workflow/workflow_d2-node.png">
</a>

- チェックポイント名を `D2 Checkpoint Loader` から取得し、`D2 Filename Template` を使って拡張子「.safetensors」を削除している
- `d2_pipe` から生成パラメータ—を取得している


---

## 主な機能

- `image` で受け取った画像を Eagle に送信する
- `positive`、`negative` で受け取ったテキストを Eagle のメモとして記録する
- png形式、webp形式が選択可能

### 画像、Eagleのコメントとして記録する生成パラメーター

- positive、negtive、CFG、steps などのパラメーターは D2 Send Eagle に接続している KSampler から取得しています
- ワークフローによっては取得できないことがあります
- d2_pipe からパラメータを指定することもできます


#### 対応 KSampler

下記の KSampler系に対応しています。
`config.yaml` を編集すると自分で増やすことができます。

- KSampler
- KSamplerAdvanced
- KSampler With Refiner (Fooocus)
- BNK_TiledKSampler
- KSampler (Efficient)
- GenerateNAID


### png形式と webp形式の違い

- png形式
  - ComfyUIワークフローを**保存できる**
  - StableDiffusion webui A1111 の PNGInfoには**表示できない**
- webp形式
  - ComfyUIワークフローを**保存できない**
  - StableDiffusion webui A1111 の PNGInfoには**表示できる**

---

## インストール

### ComfyUI Manager を使う場合

1. ComfyUI Manager を開く
2. `Custom Nodes Manager` をクリック
3. `D2 Send Eagle` を検索
4. `Install` をクリック
5. ComfyUI を再起動

### コマンドプロンプトを使う場合

1. コマンドプロンプトを開く
1. `{ComfyUIインストールフォルダ}/custom_nodes` に移動
2. `git clone https://github.com/da2el-ai/ComfyUI-d2-send-eagle`

---

## 入力 / オプション

- `images`
  - 保存する画像
- `d2_pipe`
  - 生成パラメータをまとめたもの
- `positive`
  - ポジティブプロンプト
- `negative`
  - ネガティブプロンプト
- `format`
  - 保存形式を webp / png / jpeg から選択
- `lossless_webp`
  - 可逆（lossless）か不可逆（lossy）から選択。`webp` を選択した時に有効。
- `compression`
  - 圧縮率を指定。webp で `lossy` を選択するか、または `jpeg` を選択したときに有効。
- `save_tags`
  - Eagle のタグとして保存するか選択
  - `None`: 保存しない
  - `Prompt + Checkpoint`: プロンプトとモデル名を保存
  - `Prompt`: プロンプトを保存
  - `Checkpoint`: モデル名を保存
- `filename_template`
  - ファイル名の書式を指定
  - 初期設定では `{model}-{width}-{height}-{seed}`
  - 使用可能なパラメーター: `width`、`height`、`model_name`、`steps`、`seed`
- `eagle_folder`
  - Eagleのフォルダ名、またはフォルダIDを指定。フォルダが存在しなければ新規作成する

---

## その他の機能

### ローカルにも画像を保存

Eagleに送信する他に、ローカル環境の下記フォルダにも画像を保存します。
このフォルダ名は変更できません。

`./ComfyUI/output/YYYY-MM-DD/YYYYMMDD_HHMMss_SSSSSS-{FinalImage_width}-{FinalImage_height}.webp`


---

## 変更履歴

- 2024/12/28
  - d2-node-comfyui の d2_pipe に対応
- 2024/11/13
  - JPEG方式に対応
- 2024/10/04
  - イメージプレビューを非表示にするトグルボタンを追加
    - プレビューを大きくすると `memo_text` も一緒に大きくなって邪魔だったので
  - output に IMAGE を追加
    - ただのパススルーです。必要ではないけど追加しました
- 2024/09/29
  - NovelAI生成ノード GenerateNAID に対応
  - 設定項目を `config.yaml` で指定できるようにした
  - webp形式の時にプロンプト情報を Exif に記録するようにした
- 2024/08/19
  - Unet Loaderを使った時にモデル名を取得できないのを修正
- 2024/08/04
  - とりあえず公開

---

## 謝辞

D2 Send Eagle は [ComfyUI-send-eagle-slim](https://github.com/shingo1228/ComfyUI-send-eagle-slim) という既存のカスタムノードを自分の好みに拡張したものです。素晴らしいカスタムノードを制作してくださった Shingo.T 様に感謝です。

