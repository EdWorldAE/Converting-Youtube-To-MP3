import os
import subprocess
import tkinter as tk
from tkinter import ttk, filedialog, messagebox


class YTDownloaderApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("YouTube MP3 Downloader")

        self.url_label = ttk.Label(self, text="YouTube Link:")
        self.url_label.pack(pady=15)
        self.url_entry = ttk.Entry(self, width=50)
        self.url_entry.pack(pady=15)

        self.bitrate_label = ttk.Label(self, text="Select Bitrate Quality:")
        self.bitrate_label.pack(pady=15)
        self.bitrate = ttk.Combobox(self, values=["64k", "128k", "192k", "256k", "320k"], state="readonly")
        self.bitrate.set("128k")
        self.bitrate.pack(pady=15)

        # ffmpeg path UI
        self.ffmpeg_path_label = ttk.Label(self, text="Path to ffmpeg.exe:")
        self.ffmpeg_path_label.pack(pady=15)
        self.ffmpeg_path_entry = ttk.Entry(self, width=50)
        self.ffmpeg_path_entry.pack(pady=5)
        self.ffmpeg_path_btn = ttk.Button(self, text="Browse", command=self.browse_ffmpeg_path)
        self.ffmpeg_path_btn.pack(pady=15)

        # yt-dlp path UI
        self.ytdlp_path_label = ttk.Label(self, text="Path to yt-dlp.exe:")
        self.ytdlp_path_label.pack(pady=15)
        self.ytdlp_path_entry = ttk.Entry(self, width=50)
        self.ytdlp_path_entry.pack(pady=5)
        self.ytdlp_path_btn = ttk.Button(self, text="Browse", command=self.browse_ytdlp_path)
        self.ytdlp_path_btn.pack(pady=15)

        self.save_path_label = ttk.Label(self, text="Save MP3 to:")
        self.save_path_label.pack(pady=15)
        self.save_path_entry = ttk.Entry(self, width=50)
        self.save_path_entry.pack(pady=5)
        self.save_path_btn = ttk.Button(self, text="Browse", command=self.browse)
        self.save_path_btn.pack(pady=15)

        self.download_btn = ttk.Button(self, text="Download & Convert", command=self.download_and_convert)
        self.download_btn.pack(pady=20)

    def browse(self):
        save_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3")])
        if save_path:
            self.save_path_entry.delete(0, tk.END)
            self.save_path_entry.insert(0, save_path)

    def browse_ffmpeg_path(self):
        ffmpeg_path = filedialog.askopenfilename(title="Select ffmpeg executable", filetypes=[("Executable files", "*.exe")])
        if ffmpeg_path:
            self.ffmpeg_path_entry.delete(0, tk.END)
            self.ffmpeg_path_entry.insert(0, ffmpeg_path)

    def browse_ytdlp_path(self):
        ytdlp_path = filedialog.askopenfilename(title="Select yt-dlp executable", filetypes=[("Executable files", "*.exe")])
        if ytdlp_path:
            self.ytdlp_path_entry.delete(0, tk.END)
            self.ytdlp_path_entry.insert(0, ytdlp_path)

    def download_and_convert(self):
        url = self.url_entry.get()
        save_path = self.save_path_entry.get()
        bitrate = self.bitrate.get()
        ffmpeg_exe_path = self.ffmpeg_path_entry.get()  # Updated to get from UI
        yt_dlp_path = self.ytdlp_path_entry.get()  # Updated to get from UI

        if not url or not save_path or not ffmpeg_exe_path or not yt_dlp_path:
            messagebox.showerror("Error", "All fields must be filled.")
            return

        try:
            cmd = [
                yt_dlp_path,  # Using the correct path to yt-dlp.exe here
                '--extract-audio',
                '--audio-format', 'mp3',
                '--audio-quality', bitrate,
                '--ffmpeg-location', ffmpeg_exe_path,  # Pointing directly to ffmpeg executable
                '-o', save_path,
                url
            ]

            subprocess.run(cmd, check=True)

            self.url_entry.delete(0, tk.END)
            self.save_path_entry.delete(0, tk.END)

            messagebox.showinfo("Success", "Download and conversion complete!")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")


if __name__ == '__main__':
    app = YTDownloaderApp()
    app.mainloop()
