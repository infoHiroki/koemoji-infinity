# コエモジ∞ セットアップガイド

このガイドでは、新しいPCに「コエモジ∞」アプリケーションをセットアップする手順を説明します。

## 目次

1. [システム要件](#システム要件)
2. [インストール手順](#インストール手順)
3. [初回起動と設定](#初回起動と設定)
4. [トラブルシューティング](#トラブルシューティング)

## システム要件

### 最小要件
- **OS**: Windows 10/11、macOS 10.15以上、Ubuntu 20.04以上
- **CPU**: Intel Core i5、AMD Ryzen 5、または同等以上
- **メモリ**: 8GB RAM以上
- **ストレージ**: 2GB以上の空き容量
- **インターネット接続**: 初回起動時にWhisperモデルをダウンロードするために必要

### 推奨環境
- **OS**: Windows 11、macOS 12以上、Ubuntu 22.04
- **CPU**: Intel Core i7/i9、AMD Ryzen 7/9、または同等以上
- **メモリ**: 16GB RAM以上
- **GPU**: NVIDIA GeForce RTX、AMD Radeon RX（CUDA/ROCmサポート）
- **ストレージ**: SSD 5GB以上の空き容量
- **インターネット接続**: 高速接続

## インストール手順

### 1. 実行ファイルのダウンロード

最新バージョンのコエモジ∞を以下のいずれかの方法でダウンロードします：

- [リリースページ](https://github.com/yourusername/koemoji-infinity/releases)から最新版のインストーラーをダウンロード
- 以下のリンクから直接ダウンロード：
  - [Windows版](https://github.com/yourusername/koemoji-infinity/releases/latest/download/koemoji-infinity-setup-win.exe)
  - [macOS版](https://github.com/yourusername/koemoji-infinity/releases/latest/download/koemoji-infinity-macos.dmg)
  - [Linux版](https://github.com/yourusername/koemoji-infinity/releases/latest/download/koemoji-infinity-linux.AppImage)

### 2. FFmpegのインストール

コエモジ∞は音声・動画処理にFFmpegを使用します。以下の手順でインストールしてください：

#### Windows
1. [FFmpegのダウンロードページ](https://ffmpeg.org/download.html)から「Windows Builds」をクリック
2. 「essentials build」をダウンロード
3. ダウンロードしたZIPファイルを解凍
4. 解凍したフォルダ内の「bin」ディレクトリにあるファイルを、システムの「PATH」に追加
   - 「コントロールパネル」→「システム」→「システムの詳細設定」→「環境変数」
   - 「Path」を選択し、「編集」をクリック
   - 「新規」をクリックして、FFmpegのbinフォルダのパスを追加（例：`C:\ffmpeg\bin`）
   - 「OK」をクリックして閉じる

#### macOS
1. [Homebrew](https://brew.sh/)がインストールされていることを確認
2. ターミナルを開いて以下のコマンドを実行：
   ```
   brew install ffmpeg
   ```

#### Linux (Ubuntu/Debian)
1. ターミナルを開いて以下のコマンドを実行：
   ```
   sudo apt update
   sudo apt install ffmpeg
   ```

### 3. アプリケーションのインストール

#### Windows
1. ダウンロードしたインストーラー（`.exe`ファイル）をダブルクリック
2. 画面の指示に従ってインストールを完了
3. デスクトップに作成されたショートカットから起動できます

#### macOS
1. ダウンロードした`.dmg`ファイルをダブルクリック
2. アプリケーションをApplicationsフォルダにドラッグ＆ドロップ
3. LaunchpadまたはApplicationsフォルダから起動できます

#### Linux
1. ダウンロードした`.AppImage`ファイルに実行権限を付与：
   ```
   chmod +x koemoji-infinity-linux.AppImage
   ```
2. ファイルをダブルクリックまたは以下のコマンドで実行：
   ```
   ./koemoji-infinity-linux.AppImage
   ```

## 初回起動と設定

### 1. 初回起動

初回起動時、以下の処理が自動的に行われます：

- 必要なフォルダの作成
- デフォルト設定の生成
- Whisperモデルのダウンロード（インターネット接続が必要）

> **注意**: 初回起動時はWhisperモデルのダウンロードに時間がかかることがあります（特に「large」モデルの場合）。

### 2. 基本設定

1. アプリケーション起動後、右上の「⚙」アイコンをクリックして設定画面を開きます
2. 必要に応じて以下の設定を変更します：

#### モデル設定
- **モデルサイズ**: 精度と速度のバランスに応じて選択
  - 一般的には「small」または「medium」が推奨
  - GPUを搭載したPCでは「large」も高速に処理可能
  - 低スペックPCでは「tiny」または「base」を選択

#### 言語設定
- **言語**: 文字起こしを行う主な言語を選択
  - 日本語コンテンツが多い場合は「日本語」を選択
  - 複数言語が混在する場合は「自動検出」を選択

#### 出力設定
- **出力先**: 文字起こし結果を保存するフォルダを選択
- **タイムスタンプ**: 音声の区切りごとにタイムコードを表示するかどうか

### 3. 文字起こしの実行

1. 「ファイル追加」ボタンをクリックして音声・動画ファイルを選択
2. 複数ファイルを一度に追加することも可能
3. 「文字起こし開始」ボタンをクリックして処理を開始
4. 処理が完了すると結果が表示され、保存オプションが提示されます

## トラブルシューティング

### 一般的な問題と解決策

#### FFmpeg関連のエラー
- **エラーメッセージ**: `FFmpegが見つかりません`
- **解決策**: 
  1. FFmpegが正しくインストールされているか確認
  2. システムの環境変数「Path」にFFmpegのbinフォルダが追加されているか確認
  3. PCの再起動を試行

#### モデルダウンロードの問題
- **エラーメッセージ**: `モデルのロードに失敗しました`
- **解決策**:
  1. インターネット接続を確認
  2. ファイアウォールやウイルス対策ソフトが通信をブロックしていないか確認
  3. 一時的な問題の場合は、アプリを再起動して再試行

#### メモリ不足エラー
- **エラーメッセージ**: `メモリエラー`や`CUDA out of memory`
- **解決策**:
  1. より小さいモデルサイズ（tiny、baseなど）を選択
  2. バックグラウンドで実行中の他のアプリケーションを閉じる
  3. 長い音声ファイルの場合、小さなセグメントに分割して処理

#### 処理速度が遅い
- **問題**: 文字起こし処理に長時間かかる
- **解決策**:
  1. より小さいモデルサイズを選択
  2. GPU搭載のPCを使用（可能な場合）
  3. 短い音声ファイルから試す

### サポートの利用

さらに支援が必要な場合は、以下の方法でサポートを受けられます：

- [GitHub Issues](https://github.com/yourusername/koemoji-infinity/issues)で問題を報告
- [コミュニティフォーラム](https://example.com/forum)で質問
- メールでのサポート: support@example.com

---

このセットアップガイドについてご質問や改善提案がございましたら、お気軽にお知らせください。 