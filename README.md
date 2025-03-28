# コエモジ∞ - 音声・動画文字起こしアプリケーション

OpenAI Whisperモデルを使用して、音声ファイルや動画ファイルから自動的に文字起こしを行うデスクトップアプリケーションです。

## ディレクトリ構造と主要ファイル

```
コエモジ∞
│
├── main.py                     # アプリケーションのエントリーポイント
│
├── transcriber.py              # 文字起こし処理を行うコアモジュール
├── transcriber.spec            # PyInstallerのビルド仕様ファイル
│
├── requirements.txt            # 必要なPythonパッケージリスト
│
├── run_app.bat                 # Windows用の起動バッチファイル
├── run_hidden.vbs              # バックグラウンド実行用スクリプト
│
├── create_icon.py              # アイコン生成ユーティリティ
├── create_shortcut.py          # ショートカット作成ユーティリティ
│
├── ui/                         # ユーザーインタフェース関連モジュール
│   ├── __init__.py             # パッケージ初期化ファイル
│   ├── main_window.py          # メインウィンドウの実装
│   ├── settings_window.py      # 設定ウィンドウの実装
│   └── result_window.py        # 結果表示ウィンドウの実装
│
├── utils/                      # ユーティリティ関連モジュール
│   ├── __init__.py             # パッケージ初期化ファイル
│   └── config_manager.py       # 設定管理モジュール
│
├── resources/                  # リソースファイル
│   ├── koemoji-infinity-logo.png           # ロゴ画像
│   ├── koemoji-infinity-logo-48x48 px.png  # 48x48ピクセルのロゴ画像
│   ├── koemoji-infinity-logo-touka.png     # 透過ロゴ画像
│   ├── play.png                # 再生アイコン
│   ├── stop.png                # 停止アイコン
│   ├── plus.png                # 追加アイコン
│   ├── settings.png            # 設定アイコン
│   └── cancel.png              # キャンセルアイコン
│
└── archive/                    # アーカイブディレクトリ（開発リファレンス用）
```

## 各ファイルの役割

### メイン実行ファイル
- **main.py**: アプリケーションの起動ポイント。設定の読み込みとメインウィンドウの初期化を行う。

### コア機能
- **transcriber.py**: OpenAI Whisperを使用して音声・動画ファイルの文字起こしを行う中核モジュール。
- **transcriber.spec**: PyInstallerでのアプリケーションビルド設定ファイル。

### UI (ユーザーインタフェース)
- **ui/main_window.py**: メインウィンドウのUI実装。ファイル選択、処理開始などの機能を提供。
- **ui/settings_window.py**: 設定画面のUI実装。文字起こしに関する各種設定の変更機能を提供。
- **ui/result_window.py**: 文字起こし結果を表示するウィンドウの実装。

### ユーティリティ
- **utils/config_manager.py**: アプリケーション設定の読み込み・保存を管理するモジュール。
- **create_icon.py**: アプリケーションアイコンを生成するユーティリティ。
- **create_shortcut.py**: デスクトップショートカットを作成するユーティリティ。

### 実行ヘルパー
- **run_app.bat**: Windowsでアプリケーションを起動するためのバッチファイル。
- **run_hidden.vbs**: アプリケーションをバックグラウンドで実行するためのスクリプト。

### リソース
- **resources/**: アイコン、ロゴなどの画像リソースを格納するディレクトリ。

### 依存関係
- **requirements.txt**: 必要なPythonパッケージとそのバージョンを指定するファイル。

## 機能概要

1. **ファイル選択**: 複数の音声・動画ファイルをUIから選択可能
2. **バッチ処理**: 複数ファイルの連続処理をサポート
3. **設定カスタマイズ**: Whisperモデルのサイズや言語設定などをカスタマイズ可能
4. **テキスト出力**: 文字起こし結果をテキストファイルとして保存
5. **タイムスタンプ機能**: 音声の区切りごとにタイムスタンプを付与
6. **モダンUI**: 使いやすいマテリアルデザインテイストのインターフェイス

## 技術スタック

- **Python**: ベースとなるプログラミング言語
- **Tkinter**: GUIフレームワーク
- **OpenAI Whisper**: 音声認識・文字起こしエンジン
- **PIL/Pillow**: 画像処理ライブラリ
- **FFmpeg**: 動画・音声ファイル処理ライブラリ

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