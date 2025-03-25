#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
文字起こし処理モジュール
動画ファイルから音声を抽出し、Whisperモデルを使用して文字起こしを行う
また、音声ファイルから直接文字起こしを行う機能も提供する
"""

import os
import tempfile
import subprocess
import sys
import datetime
import torch

# FFmpegの絶対パスを指定（環境変数が設定されていない場合に使用）
FFMPEG_PATH = "ffmpeg"  # デフォルトはコマンド名のみ
# Windowsの場合はFFmpegの絶対パスを指定することもできます
# FFMPEG_PATH = r"C:\ffmpeg\bin\ffmpeg.exe"  # 必要に応じてコメントを外して正しいパスを設定

try:
    import whisper
except ImportError:
    print("Whisperモジュールがインストールされていません。pip install openai-whisperを実行してインストールしてください。")
    sys.exit(1)

from tqdm import tqdm

class BaseTranscriber:
    """文字起こしの基本クラス"""
    
    def __init__(self, audio_path=None, model_name="small", language=None, progress_callback=None):
        """
        初期化
        
        Args:
            audio_path (str, optional): 音声/動画ファイルのパス
            model_name (str): Whisperモデル名 (tiny, base, small, medium, large)
            language (str, optional): 言語コード (None=自動検出)
            progress_callback (function, optional): 進捗報告用コールバック関数
        """
        self.audio_path = audio_path
        self.model_name = model_name
        self.language = language
        self.progress_callback = progress_callback
        self.model = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {self.device}")
        
    def load_model(self):
        """Whisperモデルをロード"""
        if self.progress_callback:
            self.progress_callback(f"モデル '{self.model_name}' をロード中...", 0)
        
        try:
            self.model = whisper.load_model(self.model_name, device=self.device)
            
            if self.progress_callback:
                self.progress_callback(f"モデル '{self.model_name}' のロード完了", 10)
                
            return True
        except Exception as e:
            error_message = f"モデルのロードに失敗しました: {str(e)}"
            print(error_message)
            if self.progress_callback:
                self.progress_callback(error_message, -1)
            return False
    
    def transcribe_audio(self, audio_path):
        """
        音声ファイルを文字起こし
        
        Args:
            audio_path (str): 音声ファイルのパス
            
        Returns:
            dict: 文字起こし結果
        """
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"ファイルが見つかりません: {audio_path}")
            
        if self.progress_callback:
            self.progress_callback(f"文字起こし中: {os.path.basename(audio_path)}", 40)
        
        # モデルがロードされていない場合はロード
        if self.model is None:
            if not self.load_model():
                raise Exception("モデルのロードに失敗しました")
        
        # 文字起こしオプション
        options = {
            "task": "transcribe",
            "verbose": True
        }
        
        if self.language:
            options["language"] = self.language
        
        try:
            # 文字起こし実行
            result = self.model.transcribe(audio_path, **options)
            
            if self.progress_callback:
                self.progress_callback("文字起こし完了", 90)
                
            return result
        except Exception as e:
            error_message = f"文字起こしに失敗しました: {str(e)}"
            print(error_message)
            if self.progress_callback:
                self.progress_callback(error_message, -1)
            raise

class VideoTranscriber(BaseTranscriber):
    """動画ファイルから文字起こしを行うクラス"""
    
    def __init__(self, video_path, model_name="small", language=None, progress_callback=None):
        """
        初期化
        
        Args:
            video_path (str): 動画ファイルのパス
            model_name (str): Whisperモデル名 (tiny, base, small, medium, large)
            language (str, optional): 言語コード (None=自動検出)
            progress_callback (function, optional): 進捗報告用コールバック関数
        """
        super().__init__(video_path, model_name, language, progress_callback)
        self.video_path = video_path
        
    def extract_audio(self):
        """
        動画ファイルから音声を抽出
        
        Returns:
            str: 抽出した音声ファイルのパス
        """
        if self.progress_callback:
            self.progress_callback(f"音声を抽出中: {os.path.basename(self.video_path)}", 20)
        
        # 一時ファイルを作成
        temp_dir = tempfile.gettempdir()
        # ファイル名から無効な文字を削除し、安全なファイル名を生成
        base_name = os.path.splitext(os.path.basename(self.video_path))[0]
        # 無効な文字を置換
        safe_name = "".join([c if c.isalnum() or c in ['-', '_', '.'] else '_' for c in base_name])
        # 一意のファイル名を生成するために現在時刻を追加
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        audio_path = os.path.join(temp_dir, f"{safe_name}_{timestamp}.wav")
        
        # FFmpegを使用して音声を抽出
        try:
            # FFmpegコマンドを実行
            subprocess.run(
                [FFMPEG_PATH, "-i", self.video_path, "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le", "-y", audio_path],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
        except subprocess.CalledProcessError as e:
            error_message = f"音声抽出に失敗しました: {str(e)}"
            print(error_message)
            if self.progress_callback:
                self.progress_callback(error_message, -1)
            raise Exception(error_message)
        except FileNotFoundError:
            error_message = "FFmpegが見つかりません。FFmpegをインストールして環境変数に追加してください。"
            print(error_message)
            if self.progress_callback:
                self.progress_callback(error_message, -1)
            raise Exception(error_message)
        
        if self.progress_callback:
            self.progress_callback("音声抽出完了", 30)
            
        return audio_path
    
    def transcribe(self, output_dir="output", base_progress=0):
        """
        動画ファイルを処理して文字起こしを行う
        
        Args:
            output_dir (str): 出力ディレクトリ
            base_progress (float): 進捗の基準値
            
        Returns:
            tuple: (文字起こしテキスト, 出力ファイルパス)
        """
        try:
            # 音声抽出
            audio_path = self.extract_audio()
            
            # 文字起こし
            result = self.transcribe_audio(audio_path)
            
            # 出力ファイルの準備
            os.makedirs(output_dir, exist_ok=True)
            base_name = os.path.splitext(os.path.basename(self.video_path))[0]
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            output_file = os.path.join(output_dir, f"{base_name}_{timestamp}.txt")
            
            # 結果をファイルに書き込み
            with open(output_file, "w", encoding="utf-8") as f:
                # 見出し情報を書き込み
                f.write(f"# 文字起こし: {os.path.basename(self.video_path)}\n")
                f.write(f"# 日時: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"# モデル: {self.model_name}\n")
                f.write(f"# 言語: {self.language if self.language else '自動検出'}\n\n")
                
                # テキスト全体を書き込み
                f.write(result["text"])
                
                # セグメント情報がある場合は詳細も書き込み
                if "segments" in result and result["segments"]:
                    f.write("\n\n## 詳細タイムスタンプ\n\n")
                    for segment in result["segments"]:
                        start_time = self._format_time(segment["start"])
                        end_time = self._format_time(segment["end"])
                        f.write(f"[{start_time} --> {end_time}] {segment['text']}\n")
            
            # 一時ファイルを削除
            try:
                os.remove(audio_path)
            except:
                pass
            
            if self.progress_callback:
                self.progress_callback("処理完了", 100)
                
            return result["text"], output_file
            
        except Exception as e:
            error_message = f"エラー: {str(e)}"
            print(error_message)
            if self.progress_callback:
                self.progress_callback(error_message, -1)
            raise
    
    def _format_time(self, seconds):
        """秒数を時:分:秒形式に変換"""
        m, s = divmod(int(seconds), 60)
        h, m = divmod(m, 60)
        return f"{h:02d}:{m:02d}:{s:02d}"

class AudioTranscriber(BaseTranscriber):
    """音声ファイルから直接文字起こしを行うクラス"""
    
    def __init__(self, audio_path, model_name="small", language=None, progress_callback=None):
        """
        初期化
        
        Args:
            audio_path (str): 音声ファイルのパス
            model_name (str): Whisperモデル名 (tiny, base, small, medium, large)
            language (str, optional): 言語コード (None=自動検出)
            progress_callback (function, optional): 進捗報告用コールバック関数
        """
        super().__init__(audio_path, model_name, language, progress_callback)
        self.audio_path = audio_path
    
    def preprocess_audio(self):
        """
        音声ファイルを前処理（必要に応じてフォーマット変換）
        
        Returns:
            str: 処理済み音声ファイルのパス
        """
        if self.progress_callback:
            self.progress_callback(f"音声ファイルを処理中: {os.path.basename(self.audio_path)}", 20)
        
        # 一時ファイルを作成
        temp_dir = tempfile.gettempdir()
        # ファイル名から無効な文字を削除し、安全なファイル名を生成
        base_name = os.path.splitext(os.path.basename(self.audio_path))[0]
        # 無効な文字を置換
        safe_name = "".join([c if c.isalnum() or c in ['-', '_', '.'] else '_' for c in base_name])
        # 一意のファイル名を生成するために現在時刻を追加
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        processed_audio_path = os.path.join(temp_dir, f"{safe_name}_{timestamp}.wav")
        
        # FFmpegを使用して音声を変換（サンプリングレートとチャンネル数を調整）
        try:
            # FFmpegコマンドを実行
            subprocess.run(
                [FFMPEG_PATH, "-i", self.audio_path, "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le", "-y", processed_audio_path],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
        except subprocess.CalledProcessError as e:
            error_message = f"音声変換に失敗しました: {str(e)}"
            print(error_message)
            if self.progress_callback:
                self.progress_callback(error_message, -1)
            raise Exception(error_message)
        except FileNotFoundError:
            error_message = "FFmpegが見つかりません。FFmpegをインストールして環境変数に追加してください。"
            print(error_message)
            if self.progress_callback:
                self.progress_callback(error_message, -1)
            raise Exception(error_message)
        
        if self.progress_callback:
            self.progress_callback("音声前処理完了", 30)
            
        return processed_audio_path
    
    def transcribe(self, output_dir="output", base_progress=0):
        """
        音声ファイルを処理して文字起こしを行う
        
        Args:
            output_dir (str): 出力ディレクトリ
            base_progress (float): 進捗の基準値
            
        Returns:
            tuple: (文字起こしテキスト, 出力ファイルパス)
        """
        try:
            # 音声前処理
            processed_audio_path = self.preprocess_audio()
            
            # 文字起こし
            result = self.transcribe_audio(processed_audio_path)
            
            # 出力ファイルの準備
            os.makedirs(output_dir, exist_ok=True)
            base_name = os.path.splitext(os.path.basename(self.audio_path))[0]
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            output_file = os.path.join(output_dir, f"{base_name}_{timestamp}.txt")
            
            # 結果をファイルに書き込み
            with open(output_file, "w", encoding="utf-8") as f:
                # 見出し情報を書き込み
                f.write(f"# 文字起こし: {os.path.basename(self.audio_path)}\n")
                f.write(f"# 日時: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"# モデル: {self.model_name}\n")
                f.write(f"# 言語: {self.language if self.language else '自動検出'}\n\n")
                
                # テキスト全体を書き込み
                f.write(result["text"])
                
                # セグメント情報がある場合は詳細も書き込み
                if "segments" in result and result["segments"]:
                    f.write("\n\n## 詳細タイムスタンプ\n\n")
                    for segment in result["segments"]:
                        start_time = self._format_time(segment["start"])
                        end_time = self._format_time(segment["end"])
                        f.write(f"[{start_time} --> {end_time}] {segment['text']}\n")
            
            # 一時ファイルを削除
            try:
                os.remove(processed_audio_path)
            except:
                pass
            
            if self.progress_callback:
                self.progress_callback("処理完了", 100)
                
            return result["text"], output_file
            
        except Exception as e:
            error_message = f"エラー: {str(e)}"
            print(error_message)
            if self.progress_callback:
                self.progress_callback(error_message, -1)
            raise
    
    def _format_time(self, seconds):
        """秒数を時:分:秒形式に変換"""
        m, s = divmod(int(seconds), 60)
        h, m = divmod(m, 60)
        return f"{h:02d}:{m:02d}:{s:02d}" 