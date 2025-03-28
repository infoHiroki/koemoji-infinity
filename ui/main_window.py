#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
メインウィンドウモジュール
アプリケーションのメインウィンドウを定義
"""

import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import threading
import datetime

from transcriber import VideoTranscriber, AudioTranscriber
from ui.settings_window import SettingsWindow
from ui.result_window import ResultWindow

# モダンなカラーパレット定義
COLORS = {
    "bg_primary": "#FAFAFA",        # 背景色（ほぼ白）
    "bg_secondary": "#FFFFFF",      # 白背景
    "accent": "#2196F3",            # アクセント色（青）
    "accent_hover": "#1976D2",      # ホバー時のアクセント色（濃い青）
    "success": "#4CAF50",           # 成功色（緑）
    "success_hover": "#388E3C",     # ホバー時の成功色（濃い緑）
    "warning": "#FF9800",           # 警告色（オレンジ）
    "error": "#F44336",             # エラー色（赤）
    "error_hover": "#D32F2F",       # ホバー時のエラー色（濃い赤）
    "text_primary": "#212121",      # 主要テキスト（黒に近いグレー）
    "text_secondary": "#757575",    # 副次テキスト（ミディアムグレー）
    "text_light": "#FFFFFF",        # 明るいテキスト（白）
    "border": "#E0E0E0",            # 標準ボーダー色（薄いグレー）
    "text_dark": "#000000",         # 真っ黒テキスト
    "error_dark": "#C62828",        # より暗い赤色
    "error_bright": "#FF5252",      # より明るい赤色
}

# マテリアルデザインのアイコン文字（Unicode）
ICONS = {
    "settings": "\u2699",           # ⚙ 設定アイコン
    "add": "\u002B",                # + 追加アイコン
    "delete": "\u2716",             # ✖ 削除アイコン
    "clear": "\u2715",              # ✕ クリアアイコン
    "start": "\u25B6",              # ▶ 開始アイコン
    "cancel": "\u2715",             # ✕ キャンセルアイコン
}

class MainWindow:
    """アプリケーションのメインウィンドウクラス"""
    
    def __init__(self, root, config_manager):
        """
        初期化
        
        Args:
            root (tk.Tk): ルートウィンドウ
            config_manager (ConfigManager): 設定管理オブジェクト
        """
        self.root = root
        self.config_manager = config_manager
        self.files = []  # 処理対象ファイルリスト
        self.is_processing = False  # 処理中フラグ
        self.cancel_flag = False  # キャンセルフラグ
        
        # ウィンドウの設定
        self.root.title("音声・動画文字起こしアプリ")
        self.root.minsize(600, 400)
        self.root.configure(bg=COLORS["bg_primary"])
        
        # 画像を読み込む
        self._load_images()
        
        # スタイルの設定
        self._setup_styles()
        
        # メインフレームレイアウト
        self._create_main_layout()
        
        # 初期ステータス表示
        self._update_status("ファイルを追加して文字起こしを開始してください")
    
    def _load_images(self):
        """アイコン画像を読み込む"""
        # 画像を保持するための辞書
        self.images = {}
        
        try:
            # ロゴ画像の読み込み
            logo_img = Image.open(os.path.join("resources", "koemoji-infinity-logo-48x48 px.png"))
            self.images["logo"] = ImageTk.PhotoImage(logo_img)
            
            # キャンセルボタン用画像
            cancel_img = Image.open(os.path.join("resources", "cancel.png"))
            self.images["cancel"] = ImageTk.PhotoImage(cancel_img)
            
            # 開始ボタン用画像
            start_img = Image.open(os.path.join("resources", "play.png"))
            self.images["start"] = ImageTk.PhotoImage(start_img)
            
            # 追加ボタン用画像
            add_img = Image.open(os.path.join("resources", "plus.png"))
            self.images["add"] = ImageTk.PhotoImage(add_img)
            
            # 設定ボタン用画像
            settings_img = Image.open(os.path.join("resources", "settings.png"))
            self.images["settings"] = ImageTk.PhotoImage(settings_img)
            
            # 削除ボタン用画像
            delete_img = Image.open(os.path.join("resources", "stop.png"))
            self.images["delete"] = ImageTk.PhotoImage(delete_img)
        
        except Exception as e:
            print(f"画像の読み込みに失敗しました: {e}")
            self.images["logo"] = None
            self.images["cancel"] = None
            self.images["start"] = None
            self.images["add"] = None
            self.images["settings"] = None
            self.images["delete"] = None

    def _setup_styles(self):
        """スタイルの設定"""
        style = ttk.Style()
        
        # 標準フォント定義
        heading_font = ("Segoe UI", 11, "bold")
        normal_font = ("Segoe UI", 10)
        small_font = ("Segoe UI", 9)
        
        # フレームのスタイル
        style.configure("TFrame", background=COLORS["bg_primary"])
        style.configure("Card.TFrame", background=COLORS["bg_secondary"], relief="flat")
        
        # ラベルのスタイル
        style.configure("TLabel", background=COLORS["bg_primary"], foreground=COLORS["text_primary"], font=normal_font)
        style.configure("Header.TLabel", background=COLORS["bg_primary"], foreground=COLORS["text_primary"], font=heading_font)
        style.configure("Card.TLabel", background=COLORS["bg_secondary"], foreground=COLORS["text_primary"], font=normal_font)
        style.configure("CardHeader.TLabel", background=COLORS["bg_secondary"], foreground=COLORS["text_primary"], font=heading_font)
        style.configure("Status.TLabel", background=COLORS["bg_primary"], foreground=COLORS["text_secondary"], font=small_font)
        
        # プログレスバーのスタイル
        style.configure("Horizontal.TProgressbar", 
                       background=COLORS["accent"], 
                       troughcolor=COLORS["bg_secondary"],
                       borderwidth=0,
                       thickness=6)

    def _create_main_layout(self):
        """メインレイアウトを作成"""
        # メインコンテナフレーム
        self.main_frame = ttk.Frame(self.root, style="TFrame")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # ヘッダーエリア
        self._create_header_area()
        
        # ファイルエリアカード
        self._create_files_card()
        
        # 制御エリア
        self._create_control_area()
        
        # ステータスエリア
        self._create_status_area()
    
    def _create_header_area(self):
        """ヘッダーエリアを作成"""
        header_frame = ttk.Frame(self.main_frame, style="TFrame")
        header_frame.pack(fill=tk.X, pady=(0, 15))
        
        # ロゴとアプリタイトルを横並びに
        logo_title_frame = ttk.Frame(header_frame, style="TFrame")
        logo_title_frame.pack(side=tk.LEFT)
        
        # ロゴ画像
        if self.images.get("logo"):
            logo_label = ttk.Label(
                logo_title_frame, 
                image=self.images["logo"],
                style="TLabel"
            )
            logo_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # アプリタイトル
        title_label = ttk.Label(
            logo_title_frame, 
            text="音声・動画文字起こし", 
            style="Header.TLabel"
        )
        title_label.pack(side=tk.LEFT, anchor=tk.W)
        
        # 設定ボタン
        settings_button = tk.Button(
            header_frame, 
            image=self.images["settings"],
            command=self._open_settings,
            bg=COLORS["bg_primary"],
            fg=COLORS["text_primary"],
            relief="flat",
            borderwidth=0,
            padx=4,
            pady=4,
            activebackground=COLORS["bg_secondary"],
            activeforeground=COLORS["text_primary"]
        )
        settings_button.pack(side=tk.RIGHT, padx=5)
    
    def _create_files_card(self):
        """ファイルカードエリアを作成"""
        # カードフレーム - 影の効果を持つ外側フレーム
        card_outer = ttk.Frame(self.main_frame, style="TFrame")
        card_outer.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # カードのメインフレーム
        card_frame = ttk.Frame(card_outer, style="Card.TFrame")
        card_frame.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        card_frame.configure(relief="flat", borderwidth=0)
        
        # カードヘッダー
        card_header = ttk.Frame(card_frame, style="Card.TFrame")
        card_header.pack(fill=tk.X, padx=15, pady=(15, 5))
        
        # カードタイトル
        card_title = ttk.Label(
            card_header, 
            text="処理するファイル", 
            style="CardHeader.TLabel"
        )
        card_title.pack(side=tk.LEFT, anchor=tk.W)
        
        # ファイルリスト領域
        file_area = ttk.Frame(card_frame, style="Card.TFrame")
        file_area.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 10))
        
        # ファイルリストボックス
        self.file_listbox = tk.Listbox(
            file_area, 
            selectmode=tk.EXTENDED,
            bg=COLORS["bg_secondary"],
            fg=COLORS["text_primary"],
            selectbackground=COLORS["accent"],
            selectforeground=COLORS["text_light"],
            font=("Segoe UI", 10),
            borderwidth=0,
            relief="flat",
            highlightthickness=0
        )
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # スクロールバー
        scrollbar = ttk.Scrollbar(file_area, orient=tk.VERTICAL, command=self.file_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.file_listbox.config(yscrollcommand=scrollbar.set)
        
        # ファイルボタンエリア
        file_btn_area = ttk.Frame(card_frame, style="Card.TFrame")
        file_btn_area.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        # ファイル追加ボタン
        add_btn = tk.Button(
            file_btn_area, 
            text="ファイル追加",
            image=self.images["add"],
            compound=tk.LEFT,
            command=self._add_files,
            bg=COLORS["accent"],
            fg=COLORS["text_light"],
            font=("Segoe UI", 10),
            relief="flat",
            borderwidth=0,
            padx=8,
            pady=4,
            activebackground=COLORS["accent_hover"],
            activeforeground=COLORS["text_light"]
        )
        add_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        # ファイル削除ボタン
        remove_btn = tk.Button(
            file_btn_area, 
            text="選択削除",
            image=self.images["delete"],
            compound=tk.LEFT,
            command=self._remove_files,
            bg=COLORS["bg_secondary"],
            fg=COLORS["text_primary"],
            font=("Segoe UI", 10),
            relief="flat",
            borderwidth=0,
            padx=8,
            pady=4,
            activebackground=COLORS["border"],
            activeforeground=COLORS["text_primary"]
        )
        remove_btn.pack(side=tk.LEFT, padx=5)
        
        # 全ファイル削除ボタン
        clear_btn = tk.Button(
            file_btn_area, 
            text="全て削除",
            image=self.images["delete"],
            compound=tk.LEFT,
            command=self._clear_files,
            bg=COLORS["bg_secondary"],
            fg=COLORS["text_primary"],
            font=("Segoe UI", 10),
            relief="flat",
            borderwidth=0,
            padx=8,
            pady=4,
            activebackground=COLORS["border"],
            activeforeground=COLORS["text_primary"]
        )
        clear_btn.pack(side=tk.LEFT, padx=5)
    
    def _create_control_area(self):
        """コントロールエリアを作成"""
        control_frame = ttk.Frame(self.main_frame, style="TFrame")
        control_frame.pack(fill=tk.X, pady=15)
        
        # 文字起こし開始ボタン（画像使用）
        self.start_button = tk.Button(
            control_frame, 
            text="文字起こし開始", 
            image=self.images["start"],
            compound=tk.LEFT,  # 画像を左に配置
            command=self._start_transcription,
            bg=COLORS["success"],
            fg=COLORS["text_light"],
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            borderwidth=0,
            padx=12,
            pady=6,
            activebackground=COLORS["success_hover"],
            activeforeground=COLORS["text_light"],
            highlightthickness=0
        )
        self.start_button.pack(side=tk.RIGHT, padx=5)
        
        # キャンセルボタン - 画像使用
        self.cancel_button = tk.Button(
            control_frame, 
            text="キャンセル", 
            image=self.images["cancel"],
            compound=tk.LEFT,  # 画像を左に配置
            command=self._cancel_transcription,
            bg=COLORS["error"],
            fg=COLORS["text_light"],
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            borderwidth=0,
            padx=10,
            pady=6,
            activebackground=COLORS["error_hover"],
            activeforeground=COLORS["text_light"],
            state=tk.DISABLED,
            highlightthickness=0
        )
        self.cancel_button.pack(side=tk.RIGHT, padx=5)
    
    def _create_status_area(self):
        """ステータスエリアを作成"""
        status_frame = ttk.Frame(self.main_frame, style="TFrame")
        status_frame.pack(fill=tk.X, pady=(5, 0))
        
        # ステータスラベル
        self.status_label = ttk.Label(
            status_frame, 
            text="", 
            style="Status.TLabel"
        )
        self.status_label.pack(side=tk.LEFT, anchor=tk.W)
        
        # プログレスフレーム
        progress_frame = ttk.Frame(self.main_frame, style="TFrame")
        progress_frame.pack(fill=tk.X, pady=(5, 0))
        
        # プログレスバー
        self.progress_bar = ttk.Progressbar(
            progress_frame, 
            orient=tk.HORIZONTAL, 
            mode='determinate', 
            style="Horizontal.TProgressbar"
        )
        self.progress_bar.pack(fill=tk.X)
    
    def _add_files(self):
        """ファイルを追加"""
        # ファイル選択ダイアログを表示
        file_types = [
            ("サポートされているファイル", "*.mp4 *.mp3 *.wav *.avi *.mov *.flac *.ogg *.mkv *.wmv *.flv *.webm"),
            ("動画ファイル", "*.mp4 *.avi *.mov *.mkv *.wmv *.flv *.webm"),
            ("音声ファイル", "*.mp3 *.wav *.ogg *.flac"),
            ("すべてのファイル", "*.*")
        ]
        new_files = filedialog.askopenfilenames(
            title="文字起こし対象のファイルを選択",
            filetypes=file_types
        )
        
        if new_files:
            # ファイルリストを更新
            for file_path in new_files:
                if file_path not in self.files:
                    self.files.append(file_path)
                    self.file_listbox.insert(tk.END, os.path.basename(file_path))
            
            # ステータス更新
            self._update_status(f"{len(self.files)}個のファイルが追加されています")
    
    def _remove_files(self):
        """選択されたファイルを削除"""
        selected_indices = self.file_listbox.curselection()
        if not selected_indices:
            return
        
        # 削除は後ろから行う（インデックスがずれるのを防ぐため）
        for i in sorted(selected_indices, reverse=True):
            self.file_listbox.delete(i)
            del self.files[i]
        
        # ステータス更新
        self._update_status(f"{len(self.files)}個のファイルが追加されています")
    
    def _clear_files(self):
        """全ファイルを削除"""
        self.file_listbox.delete(0, tk.END)
        self.files = []
        
        # ステータス更新
        self._update_status("ファイルを追加して文字起こしを開始してください")
    
    def _open_settings(self):
        """設定ウィンドウを開く"""
        SettingsWindow(self.root, self.config_manager)
    
    def _start_transcription(self):
        """文字起こしを開始"""
        if not self.files:
            messagebox.showwarning("警告", "処理対象のファイルが追加されていません。\n文字起こしを行うファイルを追加してください。")
            return
        
        # 処理中フラグを設定
        self.is_processing = True
        self.cancel_flag = False
        
        # ボタンの状態を更新
        self._update_buttons_state()
        
        # 設定を取得
        config = self.config_manager.get_config()
        model = config.get("model", "medium")
        language = config.get("language", "")
        output_dir = config.get("output_directory", "output")
        
        # 出力ディレクトリがなければ作成
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
        
        # プログレスバーをリセット
        self.progress_bar["value"] = 0
        
        # 処理スレッドを起動
        thread = threading.Thread(
            target=self._process_files,
            args=(self.files.copy(), model, language, output_dir)
        )
        thread.daemon = True
        thread.start()
    
    def _cancel_transcription(self):
        """文字起こしをキャンセル"""
        if self.is_processing:
            self.cancel_flag = True
            self._update_status("文字起こしをキャンセルしています...")
    
    def _process_files(self, file_list, model, language, output_dir):
        """
        ファイルの処理を実行
        
        Args:
            file_list (list): 処理対象ファイルのリスト
            model (str): Whisperモデル名
            language (str): 言語コード
            output_dir (str): 出力ディレクトリ
        """
        total_files = len(file_list)
        
        # 進捗更新用のコールバック関数
        def update_progress(status, progress):
            self._update_progress(status, progress)
        
        for i, file_path in enumerate(file_list):
            if self.cancel_flag:
                self._update_progress_gui("文字起こしがキャンセルされました", 0)
                break
            
            file_name = os.path.basename(file_path)
            file_extension = os.path.splitext(file_path)[1].lower()
            
            # 全体の進捗率を計算（ファイル単位）
            base_progress = (i / total_files) * 100
            
            try:
                # ファイル処理のステータス更新
                self._update_progress(f"処理中: {file_name} ({i+1}/{total_files})", base_progress)
                
                # ファイルの種類に応じたトランスクライバーを作成
                audio_extensions = ['.mp3', '.wav', '.flac', '.ogg']
                video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm']
                
                transcript = None
                result_file = None
                
                # 動画ファイルの場合
                if file_extension in video_extensions:
                    transcriber = VideoTranscriber(model_name=model, language=language, callback=update_progress)
                    result = transcriber.process_video(file_path)
                    # 処理結果を保存
                    transcript, result_file = self._save_result(result, file_path, output_dir, model, language)
                
                # 音声ファイルの場合
                elif file_extension in audio_extensions:
                    transcriber = AudioTranscriber(model_name=model, language=language, callback=update_progress)
                    result = transcriber.process_audio(file_path)
                    # 処理結果を保存
                    transcript, result_file = self._save_result(result, file_path, output_dir, model, language)
                
                # サポートされていないファイル形式
                else:
                    self._update_progress(f"エラー: サポートされていないファイル形式です - {file_extension}", base_progress)
                    continue
                
                # キャンセルされた場合
                if self.cancel_flag:
                    self._update_progress_gui("文字起こしがキャンセルされました", 0)
                    break
                
                # 文字起こし結果を表示
                if transcript:
                    self.root.after(0, lambda t=transcript, n=file_name: ResultWindow(self.root, t, n))
            
            except Exception as e:
                # エラーが発生した場合
                error_message = f"エラー: {file_name} の処理中にエラーが発生しました - {str(e)}"
                self._update_progress(error_message, base_progress)
                print(error_message)
        
        # 全ファイルの処理完了
        if not self.cancel_flag:
            self._update_progress_gui("文字起こしが完了しました", 100)
        
        # 処理完了
        self.is_processing = False
        self._update_buttons_state()
    
    def _save_result(self, result, file_path, output_dir, model, language):
        """
        文字起こし結果をファイルに保存
        
        Args:
            result (dict): 文字起こし結果
            file_path (str): 処理したファイルのパス
            output_dir (str): 出力ディレクトリ
            model (str): 使用したモデル
            language (str): 言語設定
            
        Returns:
            tuple: (テキスト, ファイルパス)
        """
        # 出力ディレクトリが存在しない場合は作成
        os.makedirs(output_dir, exist_ok=True)
        
        # ファイル名の準備
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        output_file = os.path.join(output_dir, f"{base_name}_{timestamp}.txt")
        
        # 結果をファイルに書き込み
        with open(output_file, "w", encoding="utf-8") as f:
            # 見出し情報を書き込み
            f.write(f"# 文字起こし: {os.path.basename(file_path)}\n")
            f.write(f"# 日時: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"# モデル: {model}\n")
            f.write(f"# 言語: {language if language else '自動検出'}\n\n")
            
            # テキスト全体を書き込み
            f.write(result["text"])
            
            # セグメント情報がある場合は詳細も書き込み
            if "segments" in result and result["segments"]:
                f.write("\n\n## 詳細タイムスタンプ\n\n")
                for segment in result["segments"]:
                    start_time = self._format_time(segment["start"])
                    end_time = self._format_time(segment["end"])
                    f.write(f"[{start_time} --> {end_time}] {segment['text']}\n")
        
        return result["text"], output_file
    
    def _format_time(self, seconds):
        """
        秒数を時:分:秒形式にフォーマット
        
        Args:
            seconds (float): 秒数
            
        Returns:
            str: フォーマットされた時間文字列
        """
        m, s = divmod(int(seconds), 60)
        h, m = divmod(m, 60)
        return f"{h:02d}:{m:02d}:{s:02d}"
    
    def _update_progress(self, status, progress):
        """
        進捗状況を更新
        
        Args:
            status (str): ステータスメッセージ
            progress (float): 進捗率(0-100)
        """
        # GUIの更新はメインスレッドで実行
        self.root.after(0, lambda: self._update_progress_gui(status, progress))
    
    def _update_progress_gui(self, status, progress):
        """
        GUI上の進捗表示を更新（メインスレッドから呼び出す）
        
        Args:
            status (str): ステータスメッセージ
            progress (float): 進捗率(0-100)
        """
        # ステータス更新
        self._update_status(status)
        
        # プログレスバー更新
        self.progress_bar["value"] = progress
    
    def _update_status(self, message):
        """ステータスメッセージを更新"""
        self.status_label.config(text=message)
    
    def _update_buttons_state(self):
        """ボタンの状態を更新"""
        if self.is_processing:
            # 処理中
            self.start_button.config(state=tk.DISABLED)
            self.cancel_button.config(state=tk.NORMAL)
        else:
            # 待機中
            self.start_button.config(state=tk.NORMAL)
            self.cancel_button.config(state=tk.DISABLED) 