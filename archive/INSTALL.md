# インストールと実行方法

## 必要条件

- Python 3.8以上
- FFmpeg

## インストール手順

### 1. リポジトリのクローン

```bash
git clone https://github.com/yourusername/video-transcriber.git
cd video-transcriber
```

### 2. 仮想環境の作成（推奨）

#### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS/Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. 依存パッケージのインストール

```bash
pip install -r requirements.txt
```

### 4. FFmpegのインストール

#### Windows
1. [FFmpegのダウンロードページ](https://ffmpeg.org/download.html)からWindows用のビルドをダウンロード
2. ダウンロードしたアーカイブを展開
3. 展開したフォルダ内の`bin`ディレクトリをシステムのPATH環境変数に追加

#### macOS (Homebrew)
```bash
brew install ffmpeg
```

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install ffmpeg
```

## アプリケーションの実行

```bash
python main.py
```

## トラブルシューティング

### FFmpegが見つからない場合

エラーメッセージ: `FFmpeg executable not found`

解決策:
1. FFmpegが正しくインストールされていることを確認
2. FFmpegの実行ファイルがシステムのPATH環境変数に含まれていることを確認

### Whisperモデルのダウンロードに失敗する場合

エラーメッセージ: `Failed to download Whisper model`

解決策:
1. インターネット接続を確認
2. ファイアウォールやプロキシの設定を確認
3. 手動でモデルをダウンロードして配置:
   - [Whisperのリポジトリ](https://github.com/openai/whisper)からモデルをダウンロード
   - ダウンロードしたモデルを`~/.cache/whisper`ディレクトリに配置

### メモリ不足エラーが発生する場合

エラーメッセージ: `CUDA out of memory` または `RuntimeError: DefaultCPUAllocator: not enough memory`

解決策:
1. より小さいWhisperモデル（tiny, base, small）を選択
2. 長い動画の場合は、短いセグメントに分割して処理 