#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
設定ウィンドウモジュール
アプリケーションの設定画面を定義
"""

import os
import customtkinter as ctk
from tkinter import filedialog, messagebox

class SettingsWindow:
    """設定ウィンドウクラス"""
    
    def __init__(self, parent, config_manager, colors):
        """
        初期化
        
        Args:
            parent (ctk.CTk): 親ウィンドウ
            config_manager (ConfigManager): 設定管理オブジェクト
            colors (dict): カラーパレット
        """
        self.parent = parent
        self.config_manager = config_manager
        self.colors = colors
        
        # 設定ウィンドウを作成
        self.window = ctk.CTkToplevel(parent)
        self.window.title("詳細設定")
        self.window.geometry("550x580")
        self.window.transient(parent)
        self.window.grab_set()
        self.window.focus_set()
        
        # タブビューの作成
        self.tab_view = ctk.CTkTabview(
            self.window,
            fg_color=self.colors["bg_light"],
            segmented_button_fg_color=self.colors["primary"],
            segmented_button_selected_color=self.colors["primary_hover"],
            segmented_button_selected_hover_color=self.colors["primary_hover"],
            segmented_button_unselected_color=self.colors["primary"],
            segmented_button_unselected_hover_color=self.colors["primary_hover"],
            text_color=self.colors["text_light"]
        )
        self.tab_view.pack(fill="both", expand=True, padx=20, pady=20)
        
        # タブの追加
        self.tab_view.add("モデル設定")
        self.tab_view.add("出力設定")
        self.tab_view.add("システム設定")
        
        # 各タブの内容を作成
        self._create_model_settings_tab()
        self._create_output_settings_tab()
        self._create_system_settings_tab()
        
        # ボタンフレーム
        button_frame = ctk.CTkFrame(self.window, fg_color=self.colors["bg_light"])
        button_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # キャンセルボタン
        cancel_button = ctk.CTkButton(
            button_frame, 
            text="キャンセル", 
            command=self.window.destroy,
            fg_color=self.colors["bg_dark"],
            hover_color="#E0E0E0",
            text_color=self.colors["text_dark"],
            font=ctk.CTkFont(family="Yu Gothic UI", size=12),
            height=35,
            corner_radius=8
        )
        cancel_button.pack(side="left", padx=(0, 10))
        
        # 保存ボタン
        save_button = ctk.CTkButton(
            button_frame, 
            text="設定を保存", 
            command=self._save_settings,
            fg_color=self.colors["success"],
            hover_color="#3D9A40",
            text_color=self.colors["text_light"],
            font=ctk.CTkFont(family="Yu Gothic UI", size=12, weight="bold"),
            height=35,
            corner_radius=8
        )
        save_button.pack(side="right")
        
        # 初期設定を読み込み
        self._load_settings()
    
    def _create_model_settings_tab(self):
        """モデル設定タブの内容を作成"""
        tab = self.tab_view.tab("モデル設定")
        
        # ヘッダー
        header = ctk.CTkLabel(
            tab, 
            text="Whisperモデル詳細設定",
            font=ctk.CTkFont(family="Yu Gothic UI", size=16, weight="bold"),
            text_color=self.colors["text_dark"]
        )
        header.pack(anchor="w", pady=(0, 20))
        
        # モデルサイズ選択
        model_frame = ctk.CTkFrame(tab, fg_color=self.colors["bg_dark"], corner_radius=10)
        model_frame.pack(fill="x", pady=(0, 20))
        
        model_label = ctk.CTkLabel(
            model_frame, 
            text="モデルサイズ:",
            font=ctk.CTkFont(family="Yu Gothic UI", size=14),
            text_color=self.colors["text_dark"]
        )
        model_label.pack(anchor="w", padx=15, pady=(15, 10))
        
        self.model_var = ctk.StringVar(value=self.config_manager.get("model", "small"))
        
        # モデルサイズのラジオボタン
        self.model_radio_tiny = ctk.CTkRadioButton(
            model_frame, 
            text="tiny (超小型: 75MB, 高速・低精度)",
            variable=self.model_var,
            value="tiny",
            font=ctk.CTkFont(family="Yu Gothic UI", size=12),
            fg_color=self.colors["primary"],
            hover_color=self.colors["primary_hover"],
            border_color=self.colors["primary"]
        )
        self.model_radio_tiny.pack(anchor="w", padx=30, pady=5)
        
        self.model_radio_base = ctk.CTkRadioButton(
            model_frame, 
            text="base (小型: 140MB, 速い・中程度の精度)",
            variable=self.model_var,
            value="base",
            font=ctk.CTkFont(family="Yu Gothic UI", size=12),
            fg_color=self.colors["primary"],
            hover_color=self.colors["primary_hover"],
            border_color=self.colors["primary"]
        )
        self.model_radio_base.pack(anchor="w", padx=30, pady=5)
        
        self.model_radio_small = ctk.CTkRadioButton(
            model_frame, 
            text="small (中型: 460MB, 標準・良好な精度)",
            variable=self.model_var,
            value="small",
            font=ctk.CTkFont(family="Yu Gothic UI", size=12),
            fg_color=self.colors["primary"],
            hover_color=self.colors["primary_hover"],
            border_color=self.colors["primary"]
        )
        self.model_radio_small.pack(anchor="w", padx=30, pady=5)
        
        self.model_radio_medium = ctk.CTkRadioButton(
            model_frame, 
            text="medium (大型: 1.5GB, やや遅い・高精度)",
            variable=self.model_var,
            value="medium",
            font=ctk.CTkFont(family="Yu Gothic UI", size=12),
            fg_color=self.colors["primary"],
            hover_color=self.colors["primary_hover"],
            border_color=self.colors["primary"]
        )
        self.model_radio_medium.pack(anchor="w", padx=30, pady=5)
        
        self.model_radio_large = ctk.CTkRadioButton(
            model_frame, 
            text="large (超大型: 3GB, 低速・最高精度)",
            variable=self.model_var,
            value="large",
            font=ctk.CTkFont(family="Yu Gothic UI", size=12),
            fg_color=self.colors["primary"],
            hover_color=self.colors["primary_hover"],
            border_color=self.colors["primary"]
        )
        self.model_radio_large.pack(anchor="w", padx=30, pady=5)
        
        model_note = ctk.CTkLabel(
            model_frame, 
            text="※大きいモデルほど精度が上がりますが、処理に時間がかかり、\nメモリ使用量も増加します。",
            font=ctk.CTkFont(family="Yu Gothic UI", size=10),
            text_color=self.colors["text_muted"]
        )
        model_note.pack(anchor="w", padx=15, pady=(5, 15))
        
        # 言語設定
        lang_frame = ctk.CTkFrame(tab, fg_color=self.colors["bg_dark"], corner_radius=10)
        lang_frame.pack(fill="x", pady=(0, 10))
        
        lang_label = ctk.CTkLabel(
            lang_frame, 
            text="言語設定:",
            font=ctk.CTkFont(family="Yu Gothic UI", size=14),
            text_color=self.colors["text_dark"]
        )
        lang_label.pack(anchor="w", padx=15, pady=(15, 10))
        
        lang_input_frame = ctk.CTkFrame(lang_frame, fg_color=self.colors["bg_dark"])
        lang_input_frame.pack(fill="x", padx=15, pady=(0, 5))
        
        lang_code_label = ctk.CTkLabel(
            lang_input_frame, 
            text="言語コード:",
            font=ctk.CTkFont(family="Yu Gothic UI", size=12),
            text_color=self.colors["text_dark"]
        )
        lang_code_label.pack(side="left", padx=(0, 10))
        
        self.lang_var = ctk.StringVar(value=self.config_manager.get("language", ""))
        self.lang_entry = ctk.CTkEntry(
            lang_input_frame, 
            textvariable=self.lang_var,
            font=ctk.CTkFont(family="Yu Gothic UI", size=12),
            width=100,
            placeholder_text="自動検出"
        )
        self.lang_entry.pack(side="left")
        
        lang_note = ctk.CTkLabel(
            lang_frame, 
            text="主要言語コード: ja (日本語), en (英語), zh (中国語), de (ドイツ語),\nes (スペイン語), ru (ロシア語), ko (韓国語), fr (フランス語)\n※空欄の場合は自動検出します。",
            font=ctk.CTkFont(family="Yu Gothic UI", size=10),
            text_color=self.colors["text_muted"]
        )
        lang_note.pack(anchor="w", padx=15, pady=(5, 15))
    
    def _create_output_settings_tab(self):
        """出力設定タブの内容を作成"""
        tab = self.tab_view.tab("出力設定")
        
        # ヘッダー
        header = ctk.CTkLabel(
            tab, 
            text="文字起こし出力設定",
            font=ctk.CTkFont(family="Yu Gothic UI", size=16, weight="bold"),
            text_color=self.colors["text_dark"]
        )
        header.pack(anchor="w", pady=(0, 20))
        
        # 出力ディレクトリ設定
        output_frame = ctk.CTkFrame(tab, fg_color=self.colors["bg_dark"], corner_radius=10)
        output_frame.pack(fill="x", pady=(0, 20))
        
        output_label = ctk.CTkLabel(
            output_frame, 
            text="出力ディレクトリ:",
            font=ctk.CTkFont(family="Yu Gothic UI", size=14),
            text_color=self.colors["text_dark"]
        )
        output_label.pack(anchor="w", padx=15, pady=(15, 10))
        
        output_input_frame = ctk.CTkFrame(output_frame, fg_color=self.colors["bg_dark"])
        output_input_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        self.output_var = ctk.StringVar(value=self.config_manager.get("output_dir", os.path.join(os.path.expanduser("~"), "Documents")))
        self.output_entry = ctk.CTkEntry(
            output_input_frame, 
            textvariable=self.output_var,
            font=ctk.CTkFont(family="Yu Gothic UI", size=12),
            width=300
        )
        self.output_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        output_button = ctk.CTkButton(
            output_input_frame, 
            text="参照",
            command=self._browse_output_dir,
            fg_color=self.colors["secondary"],
            hover_color="#FFB0C0",
            text_color=self.colors["text_dark"],
            font=ctk.CTkFont(family="Yu Gothic UI", size=12),
            width=80,
            corner_radius=4
        )
        output_button.pack(side="right")
        
        # タイムスタンプ形式
        timestamp_frame = ctk.CTkFrame(tab, fg_color=self.colors["bg_dark"], corner_radius=10)
        timestamp_frame.pack(fill="x", pady=(0, 20))
        
        timestamp_label = ctk.CTkLabel(
            timestamp_frame, 
            text="タイムスタンプ形式:",
            font=ctk.CTkFont(family="Yu Gothic UI", size=14),
            text_color=self.colors["text_dark"]
        )
        timestamp_label.pack(anchor="w", padx=15, pady=(15, 10))
        
        self.timestamp_format_var = ctk.StringVar(value=self.config_manager.get("timestamp_format", "[%H:%M:%S.%f]"))
        
        timestamp_formats = [
            "[00:00:00.000]",
            "00:00:00",
            "00m00s",
            "(0:00)"
        ]
        
        timestamp_format_frame = ctk.CTkFrame(timestamp_frame, fg_color=self.colors["bg_dark"])
        timestamp_format_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        # ラジオボタンでフォーマット選択
        self.format_radio1 = ctk.CTkRadioButton(
            timestamp_format_frame, 
            text="[00:00:00.000]",
            variable=self.timestamp_format_var,
            value="[%H:%M:%S.%f]",
            font=ctk.CTkFont(family="Yu Gothic UI", size=12),
            fg_color=self.colors["primary"],
            hover_color=self.colors["primary_hover"],
            border_color=self.colors["primary"]
        )
        self.format_radio1.pack(anchor="w", pady=5)
        
        self.format_radio2 = ctk.CTkRadioButton(
            timestamp_format_frame, 
            text="00:00:00",
            variable=self.timestamp_format_var,
            value="%H:%M:%S",
            font=ctk.CTkFont(family="Yu Gothic UI", size=12),
            fg_color=self.colors["primary"],
            hover_color=self.colors["primary_hover"],
            border_color=self.colors["primary"]
        )
        self.format_radio2.pack(anchor="w", pady=5)
        
        self.format_radio3 = ctk.CTkRadioButton(
            timestamp_format_frame, 
            text="00m00s",
            variable=self.timestamp_format_var,
            value="%Mm%Ss",
            font=ctk.CTkFont(family="Yu Gothic UI", size=12),
            fg_color=self.colors["primary"],
            hover_color=self.colors["primary_hover"],
            border_color=self.colors["primary"]
        )
        self.format_radio3.pack(anchor="w", pady=5)
        
        self.format_radio4 = ctk.CTkRadioButton(
            timestamp_format_frame, 
            text="(0:00)",
            variable=self.timestamp_format_var,
            value="(%M:%S)",
            font=ctk.CTkFont(family="Yu Gothic UI", size=12),
            fg_color=self.colors["primary"],
            hover_color=self.colors["primary_hover"],
            border_color=self.colors["primary"]
        )
        self.format_radio4.pack(anchor="w", pady=5)
    
    def _create_system_settings_tab(self):
        """システム設定タブの内容を作成"""
        tab = self.tab_view.tab("システム設定")
        
        # ヘッダー
        header = ctk.CTkLabel(
            tab, 
            text="システム設定",
            font=ctk.CTkFont(family="Yu Gothic UI", size=16, weight="bold"),
            text_color=self.colors["text_dark"]
        )
        header.pack(anchor="w", pady=(0, 20))
        
        # ハードウェア設定
        hw_frame = ctk.CTkFrame(tab, fg_color=self.colors["bg_dark"], corner_radius=10)
        hw_frame.pack(fill="x", pady=(0, 20))
        
        hw_label = ctk.CTkLabel(
            hw_frame, 
            text="ハードウェア設定:",
            font=ctk.CTkFont(family="Yu Gothic UI", size=14),
            text_color=self.colors["text_dark"]
        )
        hw_label.pack(anchor="w", padx=15, pady=(15, 10))
        
        # GPU使用設定
        self.use_gpu_var = ctk.BooleanVar(value=self.config_manager.get("use_gpu", True))
        use_gpu_cb = ctk.CTkCheckBox(
            hw_frame,
            text="GPU高速化を有効にする（CUDA/ROCm対応GPUがある場合）",
            variable=self.use_gpu_var,
            font=ctk.CTkFont(family="Yu Gothic UI", size=12),
            fg_color=self.colors["primary"],
            hover_color=self.colors["primary_hover"],
            border_color=self.colors["primary"]
        )
        use_gpu_cb.pack(anchor="w", padx=15, pady=5)
        
        # スレッド数設定
        threads_frame = ctk.CTkFrame(hw_frame, fg_color=self.colors["bg_dark"])
        threads_frame.pack(fill="x", padx=15, pady=(5, 15))
        
        threads_label = ctk.CTkLabel(
            threads_frame, 
            text="CPU処理スレッド数:",
            font=ctk.CTkFont(family="Yu Gothic UI", size=12),
            text_color=self.colors["text_dark"]
        )
        threads_label.pack(side="left", padx=(0, 10))
        
        self.threads_var = ctk.StringVar(value=str(self.config_manager.get("threads", 4)))
        threads_entry = ctk.CTkEntry(
            threads_frame, 
            textvariable=self.threads_var,
            font=ctk.CTkFont(family="Yu Gothic UI", size=12),
            width=60
        )
        threads_entry.pack(side="left")
        
        hw_note = ctk.CTkLabel(
            hw_frame, 
            text="※GPUを使用すると処理が高速化されますが、より多くのメモリを使用します。\n※スレッド数は、お使いのCPUのコア数に応じて設定してください。",
            font=ctk.CTkFont(family="Yu Gothic UI", size=10),
            text_color=self.colors["text_muted"]
        )
        hw_note.pack(anchor="w", padx=15, pady=(0, 15))
        
        # 外観設定
        theme_frame = ctk.CTkFrame(tab, fg_color=self.colors["bg_dark"], corner_radius=10)
        theme_frame.pack(fill="x", pady=(0, 20))
        
        theme_label = ctk.CTkLabel(
            theme_frame, 
            text="外観設定:",
            font=ctk.CTkFont(family="Yu Gothic UI", size=14),
            text_color=self.colors["text_dark"]
        )
        theme_label.pack(anchor="w", padx=15, pady=(15, 10))
        
        # テーマモード設定
        self.theme_mode_var = ctk.StringVar(value=self.config_manager.get("theme_mode", "light"))
        theme_mode_frame = ctk.CTkFrame(theme_frame, fg_color=self.colors["bg_dark"])
        theme_mode_frame.pack(fill="x", padx=15, pady=(5, 15))
        
        # テーマモードラジオボタン
        self.theme_light_radio = ctk.CTkRadioButton(
            theme_mode_frame, 
            text="ライトモード",
            variable=self.theme_mode_var,
            value="light",
            font=ctk.CTkFont(family="Yu Gothic UI", size=12),
            fg_color=self.colors["primary"],
            hover_color=self.colors["primary_hover"],
            border_color=self.colors["primary"]
        )
        self.theme_light_radio.pack(side="left", padx=(0, 20))
        
        self.theme_dark_radio = ctk.CTkRadioButton(
            theme_mode_frame, 
            text="ダークモード",
            variable=self.theme_mode_var,
            value="dark",
            font=ctk.CTkFont(family="Yu Gothic UI", size=12),
            fg_color=self.colors["primary"],
            hover_color=self.colors["primary_hover"],
            border_color=self.colors["primary"]
        )
        self.theme_dark_radio.pack(side="left")
        
        # テーマ変更ノート
        theme_note = ctk.CTkLabel(
            theme_frame, 
            text="※テーマの変更は次回起動時に反映されます。",
            font=ctk.CTkFont(family="Yu Gothic UI", size=10),
            text_color=self.colors["text_muted"]
        )
        theme_note.pack(anchor="w", padx=15, pady=(0, 15))
    
    def _browse_output_dir(self):
        """出力ディレクトリを選択"""
        output_dir = filedialog.askdirectory(
            title="出力先フォルダを選択",
            initialdir=self.output_var.get()
        )
        
        if output_dir:
            self.output_var.set(output_dir)
    
    def _load_settings(self):
        """設定を読み込み"""
        # モデル設定
        model = self.config_manager.get("model", "small")
        self.model_var.set(model)
        
        # 言語設定
        language = self.config_manager.get("language", "")
        self.lang_var.set(language)
        
        # 出力ディレクトリ
        output_dir = self.config_manager.get("output_dir", os.path.join(os.path.expanduser("~"), "Documents"))
        self.output_var.set(output_dir)
        
        # タイムスタンプ形式
        timestamp_format = self.config_manager.get("timestamp_format", "[%H:%M:%S.%f]")
        self.timestamp_format_var.set(timestamp_format)
        
        # GPU使用設定
        use_gpu = self.config_manager.get("use_gpu", True)
        self.use_gpu_var.set(use_gpu)
        
        # スレッド数
        threads = self.config_manager.get("threads", 4)
        self.threads_var.set(str(threads))
        
        # テーマモード
        theme_mode = self.config_manager.get("theme_mode", "light")
        self.theme_mode_var.set(theme_mode)
    
    def _save_settings(self):
        """設定を保存"""
        try:
            # モデル設定
            self.config_manager.set("model", self.model_var.get())
            
            # 言語設定
            self.config_manager.set("language", self.lang_var.get())
            
            # 出力ディレクトリ
            self.config_manager.set("output_dir", self.output_var.get())
            
            # タイムスタンプ形式
            self.config_manager.set("timestamp_format", self.timestamp_format_var.get())
            
            # GPU使用設定
            self.config_manager.set("use_gpu", self.use_gpu_var.get())
            
            # スレッド数 (整数チェック)
            try:
                threads = int(self.threads_var.get())
                if threads <= 0:
                    raise ValueError("スレッド数は1以上の整数にしてください")
                self.config_manager.set("threads", threads)
            except ValueError as e:
                messagebox.showerror("エラー", str(e))
                return
            
            # テーマモード
            self.config_manager.set("theme_mode", self.theme_mode_var.get())
            
            # 設定を保存
            self.config_manager.save()
            
            # ウィンドウを閉じる
            self.window.destroy()
            
            # 保存完了メッセージ
            messagebox.showinfo("設定保存", "設定を保存しました。一部の設定は次回起動時に反映されます。")
            
        except Exception as e:
            messagebox.showerror("エラー", f"設定の保存中にエラーが発生しました: {str(e)}") 