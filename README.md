# コエモジ∞ - 音声・動画文字起こしアプリケーション

OpenAI Whisperを使用して動画や音声ファイルから音声を抽出し、自動的に文字起こしを行うデスクトップアプリケーションです。

## 機能

- 動画ファイル（MP4, AVI, MOV, MKV, WMV, FLV, WebM）からの文字起こし
- 音声ファイル（MP3, WAV, OGG, FLAC）からの文字起こし
- OpenAIのWhisperモデルを使用した高精度な音声認識
- 複数のWhisperモデルサイズを選択可能（tiny, base, small, medium, large）
- 日本語を含む多言語対応
- 文字起こし結果のタイムスタンプ付きテキスト出力
- GPU高速化（CUDAまたはROCm対応GPUがある場合）
- 游ゴシックフォントを使用した見やすいユーザーインターフェース

## インストール方法

### 必要条件

- Python 3.8以上
- FFmpeg

### インストール手順

1. リポジトリをクローン：
   ```
   git clone https://github.com/yourusername/audio-video-transcriber.git
   cd audio-video-transcriber
   ```

2. 依存パッケージのインストール：
   ```
   pip install -r requirements.txt
   ```

3. FFmpegのインストール：
   - Windows: [FFmpegのダウンロードページ](https://ffmpeg.org/download.html)からダウンロードしてインストール
   - macOS: `brew install ffmpeg`
   - Linux: `sudo apt install ffmpeg`

## 使用方法

アプリケーションを起動：
```
python main.py
```

1. 「ファイル追加」ボタンをクリックして動画または音声ファイルを追加
2. 必要に応じて設定を調整
3. 「文字起こし開始」ボタンをクリックして処理を開始
4. 処理完了後、結果を確認して保存

## プロジェクト構成

```
.
├── main.py           # アプリケーションのエントリーポイント
├── transcriber.py    # 文字起こし処理のメインロジック
├── config.json       # アプリケーション設定ファイル
├── requirements.txt  # 依存パッケージリスト
├── ui/               # ユーザーインターフェース関連ファイル
│   ├── main_window.py     # メインウィンドウの実装
│   ├── settings_window.py # 設定ウィンドウの実装
│   └── result_window.py   # 結果表示ウィンドウの実装
├── utils/            # ユーティリティ関数と補助クラス
│   └── config_manager.py  # 設定管理クラス
└── resources/        # リソースファイル（ロゴ、アイコンなど）
    ├── koemoji-infinity-logo.png      # ロゴ画像
    ├── koemoji-infinity-icon.png      # アイコン画像
    └── その他のUIアイコン
```

## ライセンス

MITライセンス 