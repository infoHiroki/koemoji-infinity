#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
メインウィンドウモジュール
アプリケーションのメインウィンドウを定義
"""

import os
import threading
import datetime
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

from transcriber import VideoTranscriber, AudioTranscriber
from ui.settings_window import SettingsWindow
from ui.result_window import ResultWindow

class MainWindow:
    """アプリケーションのメインウィンドウクラス"""
    
    def __init__(self, root, config_manager, colors):
        """
        初期化
        
        Args:
            root (ctk.CTk): ルートウィンドウ
            config_manager (ConfigManager): 設定管理オブジェクト
            colors (dict): カラーパレット
        """
        self.root = root
        self.config_manager = config_manager
        self.colors = colors
        self.files = []  # 処理対象ファイルリスト
        self.is_processing = False  # 処理中フラグ
        self.cancel_flag = False  # キャンセルフラグ
        
        # UIコンポーネントの初期化
        self._create_layout()
        
    def _create_layout(self):
        """メインレイアウトを作成"""
        # メインフレーム
        self.main_frame = ctk.CTkFrame(self.root, fg_color=self.colors["bg_light"])
        self.main_frame.pack(fill="both", expand=True)
        
        # ヘッダーフレーム（アプリロゴとタイトル）
        self._create_header()
        
        # コンテンツフレーム（メインコンテンツ）
        content_frame = ctk.CTkFrame(self.main_frame, fg_color=self.colors["bg_light"])
        content_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # 左右のカラムを作成
        left_frame = ctk.CTkFrame(content_frame, fg_color=self.colors["bg_light"])
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        right_frame = ctk.CTkFrame(content_frame, fg_color=self.colors["bg_light"])
        right_frame.pack(side="right", fill="both", expand=True, padx=(10, 0), pady=10, ipadx=10)
        
        # 左側: ファイル選択エリア
        self._create_file_selection_area(left_frame)
        
        # 右側: 設定とコントロールエリア
        self._create_settings_area(right_frame)
        self._create_control_buttons(right_frame)
        
        # フッター（ステータスバー）
        self._create_status_bar()
    
    def _create_header(self):
        """ヘッダーエリアを作成"""
        header_frame = ctk.CTkFrame(self.main_frame, fg_color=self.colors["primary"], height=80)
        header_frame.pack(fill="x", pady=(0, 20))
        
        # ロゴラベル
        logo_label = ctk.CTkLabel(
            header_frame, 
            text="音声・動画文字起こしアプリ", 
            font=ctk.CTkFont(family="Yu Gothic UI", size=20, weight="bold"),
            text_color=self.colors["text_light"]
        )
        logo_label.pack(side="left", padx=20, pady=20)
        
        # アイコンの読み込み（あれば）
        if os.path.exists("resources/logo.png"):
            try:
                logo_image = Image.open("resources/logo.png")
                logo_image = logo_image.resize((50, 50))
                logo_photo = ImageTk.PhotoImage(logo_image)
                
                logo_icon = ctk.CTkLabel(header_frame, image=logo_photo, text="")
                logo_icon.image = logo_photo  # 参照を保持
                logo_icon.pack(side="right", padx=20, pady=15)
            except Exception:
                pass
    
    def _create_file_selection_area(self, parent_frame):
        """ファイル選択エリアを作成"""
        # タイトルラベル
        file_label = ctk.CTkLabel(
            parent_frame, 
            text="処理対象ファイル", 
            font=ctk.CTkFont(family="Yu Gothic UI", size=16, weight="bold"),
            text_color=self.colors["text_dark"]
        )
        file_label.pack(anchor="w", pady=(0, 10))
        
        # ファイルリストフレーム
        file_frame = ctk.CTkFrame(parent_frame, fg_color=self.colors["bg_dark"], corner_radius=10)
        file_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        # ファイルリストボックス
        self.file_listbox = ctk.CTkTextbox(
            file_frame,
            wrap="none",
            fg_color=self.colors["bg_dark"],
            text_color=self.colors["text_dark"],
            font=ctk.CTkFont(family="Yu Gothic UI", size=12),
            border_width=0
        )
        self.file_listbox.pack(fill="both", expand=True, padx=10, pady=10)
        
        # ファイル操作ボタンフレーム
        button_frame = ctk.CTkFrame(parent_frame, fg_color=self.colors["bg_light"])
        button_frame.pack(fill="x", pady=10)
        
        # ファイル追加ボタン
        add_button = ctk.CTkButton(
            button_frame, 
            text="ファイル追加", 
            command=self._add_files,
            fg_color=self.colors["primary"],
            hover_color=self.colors["primary_hover"],
            text_color=self.colors["text_light"],
            font=ctk.CTkFont(family="Yu Gothic UI", size=12),
            corner_radius=8,
            height=35
        )
        add_button.pack(side="left", padx=(0, 5), pady=5, fill="x", expand=True)
        
        # ファイル削除ボタン
        remove_button = ctk.CTkButton(
            button_frame, 
            text="選択ファイル削除", 
            command=self._remove_selected_file,
            fg_color=self.colors["error"],
            hover_color="#FF3B3B",
            text_color=self.colors["text_light"],
            font=ctk.CTkFont(family="Yu Gothic UI", size=12),
            corner_radius=8,
            height=35
        )
        remove_button.pack(side="right", padx=(5, 0), pady=5, fill="x", expand=True)
    
    def _create_settings_area(self, parent_frame):
        """設定エリアを作成"""
        # 設定タイトル
        settings_label = ctk.CTkLabel(
            parent_frame, 
            text="文字起こし設定", 
            font=ctk.CTkFont(family="Yu Gothic UI", size=16, weight="bold"),
            text_color=self.colors["text_dark"]
        )
        settings_label.pack(anchor="w", pady=(0, 10))
        
        # 設定フレーム
        settings_frame = ctk.CTkFrame(parent_frame, fg_color=self.colors["bg_dark"], corner_radius=10)
        settings_frame.pack(fill="x", pady=(0, 20))
        
        # モデルサイズ設定
        model_frame = ctk.CTkFrame(settings_frame, fg_color=self.colors["bg_dark"])
        model_frame.pack(fill="x", padx=15, pady=10)
        
        model_label = ctk.CTkLabel(
            model_frame, 
            text="Whisperモデル:", 
            font=ctk.CTkFont(family="Yu Gothic UI", size=12),
            text_color=self.colors["text_dark"]
        )
        model_label.pack(side="left", padx=(0, 10))
        
        self.model_var = ctk.StringVar(value=self.config_manager.get("model", "small"))
        model_options = ["tiny", "base", "small", "medium", "large"]
        model_menu = ctk.CTkOptionMenu(
            model_frame, 
            values=model_options,
            variable=self.model_var,
            fg_color=self.colors["primary"],
            button_color=self.colors["primary"],
            button_hover_color=self.colors["primary_hover"],
            text_color=self.colors["text_light"],
            font=ctk.CTkFont(family="Yu Gothic UI", size=12),
            dropdown_font=ctk.CTkFont(family="Yu Gothic UI", size=12),
            width=120
        )
        model_menu.pack(side="right")
        
        # 言語設定
        lang_frame = ctk.CTkFrame(settings_frame, fg_color=self.colors["bg_dark"])
        lang_frame.pack(fill="x", padx=15, pady=10)
        
        lang_label = ctk.CTkLabel(
            lang_frame, 
            text="言語:", 
            font=ctk.CTkFont(family="Yu Gothic UI", size=12),
            text_color=self.colors["text_dark"]
        )
        lang_label.pack(side="left", padx=(0, 10))
        
        self.lang_var = ctk.StringVar(value=self.config_manager.get("language", ""))
        lang_entry = ctk.CTkEntry(
            lang_frame, 
            textvariable=self.lang_var,
            font=ctk.CTkFont(family="Yu Gothic UI", size=12),
            width=120,
            placeholder_text="自動検出"
        )
        lang_entry.pack(side="right")
        
        # 言語ヒント
        lang_hint = ctk.CTkLabel(
            settings_frame, 
            text="言語コード例: ja (日本語), en (英語), zh (中国語), 空欄=自動検出",
            font=ctk.CTkFont(family="Yu Gothic UI", size=10),
            text_color=self.colors["text_muted"]
        )
        lang_hint.pack(fill="x", padx=15, pady=(0, 10))
        
        # 出力ディレクトリ設定
        output_frame = ctk.CTkFrame(settings_frame, fg_color=self.colors["bg_dark"])
        output_frame.pack(fill="x", padx=15, pady=10)
        
        output_label = ctk.CTkLabel(
            output_frame, 
            text="出力先:", 
            font=ctk.CTkFont(family="Yu Gothic UI", size=12),
            text_color=self.colors["text_dark"]
        )
        output_label.pack(side="left", padx=(0, 10))
        
        self.output_var = ctk.StringVar(value=self.config_manager.get("output_dir", os.path.join(os.path.expanduser("~"), "Documents")))
        output_button = ctk.CTkButton(
            output_frame, 
            text="参照",
            command=self._browse_output_dir,
            fg_color=self.colors["secondary"],
            hover_color="#FFB0C0",
            text_color=self.colors["text_dark"],
            font=ctk.CTkFont(family="Yu Gothic UI", size=12),
            width=60,
            corner_radius=4
        )
        output_button.pack(side="right", padx=(10, 0))
        
        output_entry = ctk.CTkEntry(
            output_frame, 
            textvariable=self.output_var,
            font=ctk.CTkFont(family="Yu Gothic UI", size=12),
            width=150
        )
        output_entry.pack(side="right", fill="x", expand=True)
        
        # 詳細設定ボタン
        settings_button = ctk.CTkButton(
            settings_frame, 
            text="詳細設定",
            command=self._open_settings,
            fg_color=self.colors["secondary"],
            hover_color="#FFB0C0",
            text_color=self.colors["text_dark"],
            font=ctk.CTkFont(family="Yu Gothic UI", size=12),
            corner_radius=8,
            height=30
        )
        settings_button.pack(padx=15, pady=15)
    
    def _create_control_buttons(self, parent_frame):
        """コントロールボタンエリアを作成"""
        # 処理開始ボタン
        self.start_button = ctk.CTkButton(
            parent_frame, 
            text="文字起こし開始",
            command=self._start_transcription,
            fg_color=self.colors["success"],
            hover_color="#3D9A40",
            text_color=self.colors["text_light"],
            font=ctk.CTkFont(family="Yu Gothic UI", size=14, weight="bold"),
            corner_radius=10,
            height=45
        )
        self.start_button.pack(fill="x", pady=(20, 10))
        
        # キャンセルボタン（初期状態では無効）
        self.cancel_button = ctk.CTkButton(
            parent_frame, 
            text="キャンセル",
            command=self._cancel_transcription,
            fg_color=self.colors["error"],
            hover_color="#FF3B3B",
            text_color=self.colors["text_light"],
            font=ctk.CTkFont(family="Yu Gothic UI", size=14, weight="bold"),
            corner_radius=10,
            height=45,
            state="disabled"
        )
        self.cancel_button.pack(fill="x", pady=(0, 10))
    
    def _create_status_bar(self):
        """ステータスバーを作成"""
        # ステータスフレーム
        status_frame = ctk.CTkFrame(self.main_frame, fg_color=self.colors["bg_dark"], height=30)
        status_frame.pack(fill="x", side="bottom")
        
        # ステータスラベル
        self.status_label = ctk.CTkLabel(
            status_frame, 
            text="準備完了",
            font=ctk.CTkFont(family="Yu Gothic UI", size=10),
            text_color=self.colors["text_muted"]
        )
        self.status_label.pack(side="left", padx=10)
        
        # プログレスバー
        self.progress_bar = ctk.CTkProgressBar(
            status_frame, 
            width=200,
            height=10,
            progress_color=self.colors["primary"],
            corner_radius=2
        )
        self.progress_bar.pack(side="right", padx=10, pady=10)
        self.progress_bar.set(0)
    
    def _add_files(self):
        """ファイルを追加"""
        # ファイル選択ダイアログを表示
        file_types = [
            ("対応ファイル", "*.mp4 *.avi *.mov *.mkv *.wmv *.flv *.webm *.mp3 *.wav *.ogg *.flac"),
            ("動画ファイル", "*.mp4 *.avi *.mov *.mkv *.wmv *.flv *.webm"),
            ("音声ファイル", "*.mp3 *.wav *.ogg *.flac"),
            ("すべてのファイル", "*.*")
        ]
        
        new_files = filedialog.askopenfilenames(
            title="文字起こしするファイルを選択",
            filetypes=file_types
        )
        
        if not new_files:
            return
        
        # ファイルリストに追加
        for file_path in new_files:
            if file_path not in self.files:
                self.files.append(file_path)
        
        # ファイルリストを更新
        self._update_file_list()
    
    def _remove_selected_file(self):
        """選択されたファイルを削除"""
        # 現在のテキスト位置を取得
        try:
            current_line = self.file_listbox.index("insert")
            line_start = f"{int(float(current_line))}.0"
            line_end = f"{int(float(current_line))}.end"
            selected_line = self.file_listbox.get(line_start, line_end).strip()
            
            # 選択されたファイルを見つける
            for i, file_path in enumerate(self.files):
                if os.path.basename(file_path) in selected_line:
                    del self.files[i]
                    break
            
            # ファイルリストを更新
            self._update_file_list()
        except Exception:
            messagebox.showwarning("選択エラー", "削除するファイルを選択してください。")
    
    def _update_file_list(self):
        """ファイルリストを更新"""
        # テキストボックスをクリア
        self.file_listbox.delete("0.0", "end")
        
        # ファイルリストを表示
        for i, file_path in enumerate(self.files):
            file_name = os.path.basename(file_path)
            file_size = os.path.getsize(file_path) / (1024 * 1024)  # MBに変換
            file_info = f"{i+1}. {file_name} ({file_size:.1f} MB)\n"
            self.file_listbox.insert("end", file_info)
    
    def _browse_output_dir(self):
        """出力ディレクトリを選択"""
        output_dir = filedialog.askdirectory(
            title="出力先フォルダを選択",
            initialdir=self.output_var.get()
        )
        
        if output_dir:
            self.output_var.set(output_dir)
            # 設定を保存
            self.config_manager.set("output_dir", output_dir)
            self.config_manager.save()
    
    def _open_settings(self):
        """詳細設定画面を開く"""
        SettingsWindow(self.root, self.config_manager, self.colors)
    
    def _start_transcription(self):
        """文字起こし処理を開始"""
        if not self.files:
            messagebox.showwarning("エラー", "処理対象ファイルが選択されていません。")
            return
        
        # 処理中フラグを設定
        self.is_processing = True
        self.cancel_flag = False
        
        # ボタンの状態を更新
        self._update_buttons_state()
        
        # 設定を保存
        model = self.model_var.get()
        language = self.lang_var.get()
        output_dir = self.output_var.get()
        
        self.config_manager.set("model", model)
        self.config_manager.set("language", language)
        self.config_manager.set("output_dir", output_dir)
        self.config_manager.save()
        
        # 処理スレッドを開始
        thread = threading.Thread(
            target=self._process_files,
            args=(self.files.copy(), model, language, output_dir)
        )
        thread.daemon = True
        thread.start()
    
    def _cancel_transcription(self):
        """文字起こし処理をキャンセル"""
        self.cancel_flag = True
        self._update_status("キャンセル中...", -1)
    
    def _process_files(self, file_list, model, language, output_dir):
        """
        ファイルを順に処理
        
        Args:
            file_list (list): 処理対象ファイルのリスト
            model (str): Whisperモデル名
            language (str): 言語コード
            output_dir (str): 出力ディレクトリ
        """
        total_files = len(file_list)
        processed_files = 0
        
        for file_path in file_list:
            if self.cancel_flag:
                break
            
            # ファイル名を取得
            file_name = os.path.basename(file_path)
            file_base_name = os.path.splitext(file_name)[0]
            
            # 進捗状況の更新関数
            def update_progress(status, progress):
                if progress >= 0:
                    # 全体の進捗を計算
                    overall_progress = (processed_files + progress / 100) / total_files
                    self._update_status(f"{file_name}: {status}", overall_progress)
                else:
                    self._update_status(f"{file_name}: {status}", -1)
            
            try:
                # ファイル拡張子から処理方法を判断
                ext = os.path.splitext(file_path)[1].lower()
                if ext in ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm']:
                    # 動画ファイルの処理
                    transcriber = VideoTranscriber(model, language, update_progress)
                    result = transcriber.process_video(file_path)
                elif ext in ['.mp3', '.wav', '.ogg', '.flac']:
                    # 音声ファイルの処理
                    transcriber = AudioTranscriber(model, language, update_progress)
                    result = transcriber.process_audio(file_path)
                else:
                    raise Exception(f"未対応のファイル形式です: {ext}")
                
                # キャンセルされた場合は結果を保存しない
                if self.cancel_flag:
                    continue
                
                # 出力ディレクトリが存在しない場合は作成
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                
                # 結果を保存
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                output_file = os.path.join(output_dir, f"{file_base_name}_{timestamp}.txt")
                
                # 整形された文字起こし結果
                formatted_result = ""
                
                # タイムスタンプ付きの文字起こし結果を作成
                for segment in result["segments"]:
                    start_time = self._format_time(segment["start"])
                    end_time = self._format_time(segment["end"])
                    text = segment["text"].strip()
                    formatted_result += f"[{start_time} --> {end_time}] {text}\n\n"
                
                # ファイルに保存
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(formatted_result)
                
                # 結果画面を表示
                self.root.after(0, lambda: ResultWindow(self.root, formatted_result, file_name, self.colors))
                
                # 処理済みファイル数をインクリメント
                processed_files += 1
                
            except Exception as e:
                # エラーメッセージを表示
                error_msg = f"エラー: {str(e)}"
                self.root.after(0, lambda msg=error_msg: messagebox.showerror("処理エラー", msg))
                
                # 進捗状況を更新
                self._update_status(f"エラー: {file_name}", -1)
        
        # 処理完了時
        if self.cancel_flag:
            self._update_status("処理がキャンセルされました", 0)
        else:
            self._update_status(f"処理完了: {processed_files}/{total_files}ファイル", 1)
        
        # 処理中フラグをクリア
        self.is_processing = False
        self.cancel_flag = False
        
        # ボタンの状態を更新
        self.root.after(0, self._update_buttons_state)
    
    def _format_time(self, seconds):
        """
        秒数を時:分:秒.ミリ秒 形式にフォーマット
        
        Args:
            seconds (float): 秒数
            
        Returns:
            str: フォーマットされた時間
        """
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = seconds % 60
        return f"{hours:02}:{minutes:02}:{seconds:06.3f}"
    
    def _update_status(self, status, progress):
        """
        ステータスと進捗を更新
        
        Args:
            status (str): ステータステキスト
            progress (float): 進捗率 (0.0 to 1.0, -1 for indeterminate)
        """
        self.root.after(0, lambda: self._update_status_gui(status, progress))
    
    def _update_status_gui(self, status, progress):
        """
        GUIスレッドでステータスと進捗を更新
        
        Args:
            status (str): ステータステキスト
            progress (float): 進捗率 (0.0 to 1.0, -1 for indeterminate)
        """
        # ステータスラベルを更新
        self.status_label.configure(text=status)
        
        # プログレスバーを更新
        if progress >= 0:
            self.progress_bar.set(progress)
        else:
            # 不定状態の表示（今回は0に設定）
            self.progress_bar.set(0)
    
    def _update_buttons_state(self):
        """ボタンの状態を更新"""
        if self.is_processing:
            self.start_button.configure(state="disabled")
            self.cancel_button.configure(state="normal")
        else:
            self.start_button.configure(state="normal")
            self.cancel_button.configure(state="disabled") 