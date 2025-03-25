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

# 標準的なカラーパレット定義
COLORS = {
    "bg_primary": "#F0F0F0",        # 標準的な背景色（薄いグレー）
    "bg_secondary": "#FFFFFF",      # 白背景
    "accent": "#0078D7",            # Windows標準の青
    "accent_hover": "#106EBE",      # ホバー時の青
    "success": "#107C10",           # 成功色（緑）
    "warning": "#D83B01",           # 警告色（オレンジ）
    "error": "#E81123",             # エラー色（赤）
    "text_primary": "#000000",      # 主要テキスト（黒）
    "text_secondary": "#666666",    # 副次テキスト（グレー）
    "text_light": "#FFFFFF",        # 明るいテキスト（白）
    "border": "#CCCCCC",            # 標準ボーダー色
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
        
        # スタイルの設定
        self._setup_styles()
        
        # メインフレームの作成
        self.main_frame = ttk.Frame(self.root, padding=10, style="TFrame")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # ファイル選択エリアの作成
        self._create_file_selection_area()
        
        # コントロールボタンの作成
        self._create_control_buttons()
        
        # ステータスバーの作成
        self._create_status_bar()
    
    def _setup_styles(self):
        """スタイルの設定"""
        style = ttk.Style()
        
        # 標準フォント定義
        heading_font = ("Yu Gothic UI", 11, "bold")
        normal_font = ("Yu Gothic UI", 10)
        small_font = ("Yu Gothic UI", 9)
        
        # フレームのスタイル
        style.configure("TFrame", background=COLORS["bg_primary"])
        style.configure("White.TFrame", background=COLORS["bg_secondary"])
        
        # ラベルフレームのスタイル
        style.configure("TLabelframe", background=COLORS["bg_primary"])
        style.configure("TLabelframe.Label", 
                       background=COLORS["bg_primary"], 
                       foreground=COLORS["text_primary"], 
                       font=heading_font)
        
        # ラベルのスタイル
        style.configure("TLabel", 
                       background=COLORS["bg_primary"], 
                       foreground=COLORS["text_primary"], 
                       font=normal_font)
        
        # プログレスバーのスタイル
        style.configure("Horizontal.TProgressbar", 
                       background=COLORS["accent"], 
                       troughcolor=COLORS["bg_secondary"],
                       borderwidth=0,
                       thickness=8)
    
    def _create_file_selection_area(self):
        """ファイル選択エリアを作成"""
        # フレームの作成
        file_frame = ttk.LabelFrame(self.main_frame, text="処理対象ファイル", padding=8)
        file_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # ファイルリストボックスの作成
        self.file_listbox = tk.Listbox(
            file_frame, 
            selectmode=tk.EXTENDED,
            bg=COLORS["bg_secondary"],
            fg=COLORS["text_primary"],
            selectbackground=COLORS["accent"],
            selectforeground=COLORS["text_light"],
            font=("Yu Gothic UI", 10),
            borderwidth=1,
            relief="solid"
        )
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # スクロールバーの作成
        scrollbar = ttk.Scrollbar(file_frame, orient=tk.VERTICAL, command=self.file_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.file_listbox.config(yscrollcommand=scrollbar.set)
        
        # ファイル操作ボタンフレームの作成
        file_button_frame = ttk.Frame(self.main_frame, style="TFrame")
        file_button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # ファイル追加ボタン
        add_button = tk.Button(
            file_button_frame, 
            text="ファイル追加", 
            command=self._add_files,
            bg=COLORS["accent"],
            fg=COLORS["text_light"],
            font=("Yu Gothic UI", 10),
            relief="flat",
            borderwidth=1,
            padx=10,
            pady=3,
            activebackground=COLORS["accent_hover"],
            activeforeground=COLORS["text_light"]
        )
        add_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        # ファイル削除ボタン
        remove_button = tk.Button(
            file_button_frame, 
            text="選択ファイル削除", 
            command=self._remove_files,
            bg=COLORS["accent"],
            fg=COLORS["text_light"],
            font=("Yu Gothic UI", 10),
            relief="flat",
            borderwidth=1,
            padx=10,
            pady=3,
            activebackground=COLORS["accent_hover"],
            activeforeground=COLORS["text_light"]
        )
        remove_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        # 全ファイル削除ボタン
        clear_button = tk.Button(
            file_button_frame, 
            text="全ファイル削除", 
            command=self._clear_files,
            bg=COLORS["accent"],
            fg=COLORS["text_light"],
            font=("Yu Gothic UI", 10),
            relief="flat",
            borderwidth=1,
            padx=10,
            pady=3,
            activebackground=COLORS["accent_hover"],
            activeforeground=COLORS["text_light"]
        )
        clear_button.pack(side=tk.LEFT, padx=5, pady=5)
    
    def _create_control_buttons(self):
        """操作ボタンエリアを作成"""
        # フレームの作成
        control_frame = ttk.Frame(self.main_frame, style="TFrame")
        control_frame.pack(fill=tk.X, padx=5, pady=10)
        
        # 設定ボタン
        settings_button = tk.Button(
            control_frame, 
            text="設定", 
            command=self._open_settings,
            bg=COLORS["bg_primary"],
            fg=COLORS["text_primary"],
            font=("Yu Gothic UI", 10),
            relief="solid",
            borderwidth=1,
            padx=10,
            pady=3,
            activebackground=COLORS["bg_secondary"],
            activeforeground=COLORS["text_primary"]
        )
        settings_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        # 履歴ボタン
        history_button = tk.Button(
            control_frame, 
            text="履歴", 
            command=self._open_history,
            bg=COLORS["bg_primary"],
            fg=COLORS["text_primary"],
            font=("Yu Gothic UI", 10),
            relief="solid",
            borderwidth=1,
            padx=10,
            pady=3,
            activebackground=COLORS["bg_secondary"],
            activeforeground=COLORS["text_primary"]
        )
        history_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        # 文字起こし開始ボタン
        self.start_button = tk.Button(
            control_frame, 
            text="文字起こし開始", 
            command=self._start_transcription,
            bg=COLORS["success"],
            fg=COLORS["text_light"],
            font=("Yu Gothic UI", 10, "bold"),
            relief="flat",
            borderwidth=1,
            padx=15,
            pady=5,
            activebackground="#0B6A0B",
            activeforeground=COLORS["text_light"]
        )
        self.start_button.pack(side=tk.RIGHT, padx=5, pady=5)
        
        # キャンセルボタン
        self.cancel_button = tk.Button(
            control_frame, 
            text="キャンセル", 
            command=self._cancel_transcription,
            bg=COLORS["warning"],
            fg=COLORS["text_light"],
            font=("Yu Gothic UI", 10),
            relief="flat",
            borderwidth=1,
            padx=15,
            pady=5,
            activebackground=COLORS["error"],
            activeforeground=COLORS["text_light"],
            state=tk.DISABLED
        )
        self.cancel_button.pack(side=tk.RIGHT, padx=5, pady=5)
    
    def _create_status_bar(self):
        """ステータスバーを作成"""
        # フレームの作成
        status_frame = ttk.Frame(self.main_frame, style="TFrame")
        status_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # ステータスラベル
        self.status_label = ttk.Label(status_frame, text="準備完了", style="TLabel")
        self.status_label.pack(side=tk.LEFT, padx=10, pady=8)
        
        # 進捗バー
        self.progress_bar = ttk.Progressbar(status_frame, orient=tk.HORIZONTAL, length=300, mode='determinate', style="Horizontal.TProgressbar")
        self.progress_bar.pack(side=tk.RIGHT, padx=10, pady=8)
    
    def _add_files(self):
        """ファイル追加ダイアログを表示"""
        file_paths = filedialog.askopenfilenames(
            title="ファイルを選択",
            filetypes=[
                ("すべての対応ファイル", "*.mp4 *.avi *.mov *.mkv *.wmv *.flv *.webm *.mp3 *.wav *.ogg *.flac"),
                ("動画ファイル", "*.mp4 *.avi *.mov *.mkv *.wmv *.flv *.webm"),
                ("音声ファイル", "*.mp3 *.wav *.ogg *.flac"),
                ("すべてのファイル", "*.*")
            ]
        )
        
        if file_paths:
            for file_path in file_paths:
                if file_path not in self.files:
                    self.files.append(file_path)
                    self.file_listbox.insert(tk.END, os.path.basename(file_path))
    
    def _remove_files(self):
        """選択されたファイルを削除"""
        selected_indices = self.file_listbox.curselection()
        
        # 逆順に削除（インデックスがずれるのを防ぐため）
        for i in sorted(selected_indices, reverse=True):
            del self.files[i]
            self.file_listbox.delete(i)
    
    def _clear_files(self):
        """すべてのファイルを削除"""
        self.files.clear()
        self.file_listbox.delete(0, tk.END)
    
    def _open_settings(self):
        """設定画面を開く"""
        SettingsWindow(self.root, self.config_manager)
    
    def _open_history(self):
        """履歴を表示"""
        # 履歴ウィンドウを作成
        history_window = tk.Toplevel(self.root)
        history_window.title("処理履歴")
        history_window.geometry("700x500")
        history_window.transient(self.root)
        history_window.grab_set()
        history_window.configure(bg=COLORS["bg_primary"])
        
        # 履歴リストの作成
        history_frame = ttk.Frame(history_window, padding=10, style="TFrame")
        history_frame.pack(fill=tk.BOTH, expand=True)
        
        # ツリービューの作成
        columns = ("file", "output", "timestamp")
        history_tree = ttk.Treeview(history_frame, columns=columns, show="headings")
        
        # カラム設定
        history_tree.heading("file", text="元ファイル")
        history_tree.heading("output", text="出力ファイル")
        history_tree.heading("timestamp", text="処理日時")
        
        history_tree.column("file", width=300)
        history_tree.column("output", width=300)
        history_tree.column("timestamp", width=150)
        
        # 履歴データの取得と表示
        history_data = self.config_manager.get_history()
        for i, item in enumerate(history_data):
            values = (
                os.path.basename(item.get("file", "")),
                item.get("output", ""),
                item.get("timestamp", "")
            )
            history_tree.insert("", tk.END, values=values, tags=('evenrow' if i % 2 == 0 else 'oddrow',))
        
        # ツリービューのスタイル設定
        history_tree.configure(
            background=COLORS["bg_secondary"],
            foreground=COLORS["text_primary"],
            selectbackground=COLORS["accent"],
            selectforeground=COLORS["text_light"]
        )
        history_tree.tag_configure("evenrow", background=COLORS["bg_secondary"])
        history_tree.tag_configure("oddrow", background="#F6F6F6")
        
        history_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # スクロールバーの作成
        scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=history_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        history_tree.configure(yscrollcommand=scrollbar.set)
        
        # ボタンフレームの作成
        button_frame = ttk.Frame(history_window, padding=5, style="TFrame")
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # 閉じるボタン
        close_button = tk.Button(
            button_frame, 
            text="閉じる", 
            command=history_window.destroy,
            bg=COLORS["bg_primary"],
            fg=COLORS["text_primary"],
            font=("Yu Gothic UI", 10),
            relief="solid",
            borderwidth=1,
            padx=10,
            pady=3,
            activebackground=COLORS["bg_secondary"],
            activeforeground=COLORS["text_primary"]
        )
        close_button.pack(side=tk.RIGHT, padx=5, pady=5)
    
    def _start_transcription(self):
        """文字起こし処理を開始"""
        if not self.files:
            messagebox.showwarning("警告", "処理対象ファイルが選択されていません。")
            return
        
        if self.is_processing:
            return
        
        # 処理中フラグを設定
        self.is_processing = True
        
        # ボタンの状態を更新
        self.start_button.config(state=tk.DISABLED)
        self.cancel_button.config(state=tk.NORMAL)
        
        # 進捗バーをリセット
        self.progress_bar["value"] = 0
        
        # 設定を取得
        model = self.config_manager.get_model()
        language = self.config_manager.get_language()
        output_dir = self.config_manager.get_output_directory()
        
        # 処理スレッドを開始
        self.current_task = threading.Thread(
            target=self._process_files,
            args=(self.files.copy(), model, language, output_dir)
        )
        self.current_task.daemon = True
        self.current_task.start()
    
    def _cancel_transcription(self):
        """文字起こし処理をキャンセル"""
        if not self.is_processing:
            return
        
        # 処理中フラグを解除
        self.is_processing = False
        
        # ステータスを更新
        self.status_label.config(text="処理をキャンセルしました")
        
        # ボタンの状態を更新
        self.start_button.config(state=tk.NORMAL)
        self.cancel_button.config(state=tk.DISABLED)
    
    def _process_files(self, file_list, model, language, output_dir):
        """
        ファイルの処理を実行
        
        Args:
            file_list (list): 処理対象ファイルリスト
            model (str): Whisperモデル名
            language (str): 言語コード
            output_dir (str): 出力ディレクトリ
        """
        results = []
        
        try:
            # 進捗更新関数
            def update_progress(status, progress):
                self._update_progress(status, progress)
            
            # ファイルごとに処理
            for i, file_path in enumerate(file_list):
                if not self.is_processing:
                    # 処理が中断された場合
                    break
                
                file_name = os.path.basename(file_path)
                overall_progress = int((i / len(file_list)) * 100)
                self._update_progress(f"ファイル {i+1}/{len(file_list)}: {file_name} 処理中...", overall_progress)
                
                try:
                    # ファイルの拡張子を確認
                    ext = os.path.splitext(file_path)[1].lower()
                    
                    # 音声ファイルか動画ファイルか判断
                    if ext in ['.mp3', '.wav', '.ogg', '.flac']:
                        # 音声ファイルの場合
                        transcriber = AudioTranscriber(model_name=model, language=language, callback=update_progress)
                        result = transcriber.process_audio(file_path)
                    else:
                        # 動画ファイルの場合
                        transcriber = VideoTranscriber(model_name=model, language=language, callback=update_progress)
                        result = transcriber.process_video(file_path)
                    
                    # 結果を保存
                    if result:
                        # ファイル名（拡張子なし）を取得
                        base_name = os.path.splitext(file_name)[0]
                        
                        # 出力ファイル名を設定
                        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                        output_path = os.path.join(output_dir, f"{base_name}_{timestamp}.txt")
                        
                        # テキストファイルとして保存
                        with open(output_path, "w", encoding="utf-8") as f:
                            # 見出し情報を書き込み
                            f.write(f"# 文字起こし: {file_name}\n")
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
                        
                        # 結果リストに追加
                        results.append({
                            "file_name": file_name,
                            "output_path": output_path,
                            "text": result["text"],
                            "segments": result.get("segments", [])
                        })
                
                except Exception as e:
                    # エラーメッセージを表示
                    messagebox.showerror("処理エラー", f"ファイル {file_name} の処理中にエラーが発生しました:\n{str(e)}")
            
            # 全ての処理が完了
            if self.is_processing:
                self._update_progress("すべての処理が完了しました", 100)
                
                # 結果画面を表示
                if results:
                    # 各ファイルごとに結果表示ウィンドウを作成
                    for result in results:
                        file_name = result.get("file_name", "不明なファイル")
                        transcript = result.get("text", "")
                        self.root.after(500, lambda file=file_name, text=transcript: 
                                        ResultWindow(self.root, text, file))
        
        except Exception as e:
            # エラーメッセージを表示
            messagebox.showerror("処理エラー", f"処理中にエラーが発生しました:\n{str(e)}")
        
        finally:
            # 処理状態をリセット
            self.is_processing = False
            
            # GUIの状態を更新
            self.root.after(0, self._update_buttons_state)
    
    def _format_time(self, seconds):
        """
        秒数を時:分:秒形式に変換
        
        Args:
            seconds (float): 秒数
            
        Returns:
            str: 時:分:秒形式の文字列
        """
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        return f"{int(h):02d}:{int(m):02d}:{int(s):02d}.{int((seconds % 1) * 1000):03d}"
    
    def _update_progress(self, status, progress):
        """
        進捗状況を更新
        
        Args:
            status (str): ステータスメッセージ
            progress (int): 進捗値（0-100）
        """
        # GUIスレッドで実行
        self.root.after(0, lambda: self._update_progress_gui(status, progress))
    
    def _update_progress_gui(self, status, progress):
        """
        GUIスレッドでの進捗状況更新
        
        Args:
            status (str): ステータスメッセージ
            progress (int): 進捗値（0-100）
        """
        # ステータスラベルを更新
        self.status_label.config(text=status)
        
        # 進捗バーを更新
        if progress >= 0:
            self.progress_bar["value"] = progress
    
    def _update_buttons_state(self):
        """ボタンの状態を更新"""
        if self.is_processing:
            self.start_button.config(state=tk.DISABLED)
            self.cancel_button.config(state=tk.NORMAL)
        else:
            self.start_button.config(state=tk.NORMAL)
            self.cancel_button.config(state=tk.DISABLED) 