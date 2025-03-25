#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
結果表示ウィンドウモジュール
文字起こし結果を表示するウィンドウを定義
"""

import os
import customtkinter as ctk
from tkinter import messagebox, filedialog
import platform
import subprocess

class ResultWindow:
    """文字起こし結果表示ウィンドウクラス"""
    
    def __init__(self, parent, transcript, title, colors):
        """
        結果ウィンドウを初期化
        
        Args:
            parent (ctk.CTk): 親ウィンドウ
            transcript (str): 文字起こしの結果
            title (str): ファイル名
            colors (dict): カラーパレット
        """
        self.colors = colors
        
        # ウィンドウの設定
        self.window = ctk.CTkToplevel(parent)
        self.window.title(f"文字起こし結果 - {title}")
        self.window.geometry("800x600")
        self.window.minsize(500, 400)
        self.window.transient(parent)
        self.window.grab_set()
        
        # メインレイアウト
        self._create_layout(transcript, title)
    
    def _create_layout(self, transcript, title):
        """レイアウトを作成"""
        # メインフレーム
        main_frame = ctk.CTkFrame(self.window, fg_color=self.colors["bg_light"])
        main_frame.pack(fill="both", expand=True)
        
        # ヘッダー
        header_frame = ctk.CTkFrame(main_frame, fg_color=self.colors["primary"], height=60)
        header_frame.pack(fill="x")
        
        # タイトルラベル
        title_label = ctk.CTkLabel(
            header_frame, 
            text=f"文字起こし結果: {title}", 
            font=ctk.CTkFont(family="Yu Gothic UI", size=18, weight="bold"),
            text_color=self.colors["text_light"]
        )
        title_label.pack(side="left", padx=20, pady=15)
        
        # コンテンツエリア
        content_frame = ctk.CTkFrame(main_frame, fg_color=self.colors["bg_light"])
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # 説明ラベル
        info_label = ctk.CTkLabel(
            content_frame, 
            text="以下に文字起こし結果を表示しています。結果をクリップボードにコピーしたり、ファイルに保存できます。",
            font=ctk.CTkFont(family="Yu Gothic UI", size=12),
            text_color=self.colors["text_muted"],
            wraplength=760
        )
        info_label.pack(anchor="w", pady=(0, 10))
        
        # テキストエリア
        text_frame = ctk.CTkFrame(content_frame, fg_color=self.colors["bg_dark"], corner_radius=10)
        text_frame.pack(fill="both", expand=True, pady=(0, 15))
        
        self.text_widget = ctk.CTkTextbox(
            text_frame,
            width=760,
            height=400,
            fg_color=self.colors["bg_dark"],
            text_color=self.colors["text_dark"],
            font=ctk.CTkFont(family="Yu Gothic UI", size=12),
            corner_radius=0,
            border_width=0,
            wrap="none"
        )
        self.text_widget.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 結果テキストの挿入
        self.text_widget.insert("0.0", transcript)
        self.text_widget.configure(state="disabled")  # 読み取り専用
        
        # ボタンフレーム
        button_frame = ctk.CTkFrame(content_frame, fg_color=self.colors["bg_light"])
        button_frame.pack(fill="x")
        
        # 保存ボタン
        save_button = ctk.CTkButton(
            button_frame,
            text="名前を付けて保存",
            command=self._save_as,
            fg_color=self.colors["primary"],
            hover_color=self.colors["primary_hover"],
            text_color=self.colors["text_light"],
            font=ctk.CTkFont(family="Yu Gothic UI", size=12),
            corner_radius=8,
            height=35
        )
        save_button.pack(side="left", padx=(0, 10))
        
        # コピーボタン
        copy_button = ctk.CTkButton(
            button_frame,
            text="クリップボードにコピー",
            command=self._copy_to_clipboard,
            fg_color=self.colors["secondary"],
            hover_color="#FFB0C0",
            text_color=self.colors["text_dark"],
            font=ctk.CTkFont(family="Yu Gothic UI", size=12),
            corner_radius=8,
            height=35
        )
        copy_button.pack(side="left", padx=(0, 10))
        
        # フォルダを開くボタン
        open_folder_button = ctk.CTkButton(
            button_frame,
            text="出力フォルダを開く",
            command=lambda: self._open_folder(os.path.dirname(title)),
            fg_color=self.colors["bg_dark"],
            hover_color="#E0E0E0",
            text_color=self.colors["text_dark"],
            font=ctk.CTkFont(family="Yu Gothic UI", size=12),
            corner_radius=8,
            height=35
        )
        open_folder_button.pack(side="left")
        
        # 閉じるボタン
        close_button = ctk.CTkButton(
            button_frame,
            text="閉じる",
            command=self.window.destroy,
            fg_color=self.colors["error"],
            hover_color="#FF3B3B",
            text_color=self.colors["text_light"],
            font=ctk.CTkFont(family="Yu Gothic UI", size=12),
            corner_radius=8,
            height=35
        )
        close_button.pack(side="right")
    
    def _copy_to_clipboard(self):
        """テキストをクリップボードにコピー"""
        self.text_widget.configure(state="normal")  # 一時的に編集可能にする
        text = self.text_widget.get("0.0", "end")
        self.text_widget.configure(state="disabled")  # 再度読み取り専用に戻す
        
        self.window.clipboard_clear()
        self.window.clipboard_append(text)
        messagebox.showinfo("コピー完了", "文字起こし結果をクリップボードにコピーしました。")
    
    def _save_as(self):
        """テキストをファイルに保存"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[
                ("テキストファイル", "*.txt"),
                ("すべてのファイル", "*.*")
            ],
            title="文字起こし結果を保存"
        )
        
        if file_path:
            try:
                self.text_widget.configure(state="normal")  # 一時的に編集可能にする
                text = self.text_widget.get("0.0", "end")
                self.text_widget.configure(state="disabled")  # 再度読み取り専用に戻す
                
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(text)
                messagebox.showinfo("保存完了", f"文字起こし結果を保存しました: {file_path}")
                
                # 保存先のフォルダを記憶
                self.last_save_folder = os.path.dirname(file_path)
            except Exception as e:
                messagebox.showerror("エラー", f"保存中にエラーが発生しました: {e}")
    
    def _open_folder(self, folder_path):
        """フォルダを開く"""
        try:
            # OSによって適切なコマンドを実行
            if platform.system() == "Windows":
                os.startfile(folder_path)
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["open", folder_path])
            else:  # Linux
                subprocess.run(["xdg-open", folder_path])
        except Exception as e:
            messagebox.showerror("エラー", f"フォルダを開く際にエラーが発生しました: {e}")