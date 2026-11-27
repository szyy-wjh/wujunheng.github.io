import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
from DrissionPage import ChromiumPage, ChromiumOptions
import requests
import threading
import av
import os
import re
import time

"""
不需要登录抖音！！！！
运行代码后，在界面的输入框中填写视频详情页的地址栏网址，
可使用测试视频链接.txt中的网址
"""

class DouyinDownloader:
    def __init__(self, root=None, cli_mode=False):
        self.cli_mode = cli_mode
        self.base_dir = os.path.join(os.getcwd(), '视频处理')
        self.video_dir = os.path.join(self.base_dir, '01_原视频')
        self.audio_dir = os.path.join(self.base_dir, '02_音频')
        self.page = None

        if cli_mode:
            self._setup_cli_stubs()
            return

        self.root = root
        self.root.title('抖音视频下载器')
        self.root.geometry('900x640')
        self.root.minsize(900, 640)
        self.root.configure(bg='#f4f6fa')

        self.create_style()
        self.create_ui()

    def _setup_cli_stubs(self):
        """CLI模式：用桩对象替代GUI组件"""
        class _Stub:
            def config(self, *args, **kwargs): pass
            def after(self, delay, fn):
                try:
                    fn()
                except Exception:
                    pass
            def __setitem__(self, key, value): pass
        self.root = _Stub()
        self.video_title_label = _Stub()
        self.result_info_label = _Stub()
        self.open_btn = _Stub()
        self.download_btn = _Stub()
        self.progress = _Stub()
        self.percent_label = _Stub()
        self.stage_label = _Stub()
        self.log_text = _Stub()

    def cli_download(self, url):
        """CLI模式：直接下载（无GUI、无线程）"""
        print(f'开始下载：{url}')
        self.download_task(url)

    def create_style(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure(
            'Download.Horizontal.TProgressbar',
            troughcolor='#e9edf5',
            background='#4f46e5',
            bordercolor='#e9edf5',
            lightcolor='#4f46e5',
            darkcolor='#4f46e5',
            thickness=10
        )

    def create_ui(self):
        top = tk.Frame(self.root, bg='#f4f6fa')
        top.pack(fill='x', padx=40, pady=(28, 20))

        icon_box = tk.Canvas(top, width=46, height=46, bg='#f4f6fa', highlightthickness=0)
        icon_box.pack(side='left')
        icon_box.create_oval(2, 2, 44, 44, fill='#4f46e5', outline='')
        icon_box.create_text(23, 23, text='▶', fill='white', font=('Microsoft YaHei UI', 17, 'bold'))

        title_box = tk.Frame(top, bg='#f4f6fa')
        title_box.pack(side='left', padx=(12, 0))

        tk.Label(
            title_box,
            text='抖音视频下载器',
            font=('Microsoft YaHei UI', 20, 'bold'),
            bg='#f4f6fa',
            fg='#1f2937'
        ).pack(anchor='w')

        tk.Label(
            title_box,
            text='自动保存完整原视频和单独音频',
            font=('Microsoft YaHei UI', 9),
            bg='#f4f6fa',
            fg='#9299a8'
        ).pack(anchor='w', pady=(3, 0))

        card = tk.Frame(self.root, bg='white', highlightbackground='#e5e8ef', highlightthickness=1)
        card.pack(fill='x', padx=40)

        tk.Label(
            card,
            text='视频详情页链接',
            font=('Microsoft YaHei UI', 10, 'bold'),
            bg='white',
            fg='#374151'
        ).pack(anchor='w', padx=28, pady=(24, 10))

        input_wrap = tk.Frame(card, bg='white')
        input_wrap.pack(fill='x', padx=28)

        self.input_canvas = tk.Canvas(input_wrap, height=50, bg='white', highlightthickness=0)
        self.input_canvas.pack(side='left', fill='x', expand=True)
        self.input_canvas.bind('<Configure>', self.draw_input_bg)

        self.url_entry = tk.Entry(
            self.input_canvas,
            font=('Microsoft YaHei UI', 11),
            bd=0,
            relief='flat',
            bg='#f5f7fb',
            fg='#1f2937',
            insertbackground='#1f2937'
        )

        self.entry_window = self.input_canvas.create_window(16, 25, window=self.url_entry, anchor='w')

        self.paste_btn = tk.Button(
            input_wrap,
            text='粘贴链接',
            font=('Microsoft YaHei UI', 10),
            bg='#eef2ff',
            fg='#4f46e5',
            activebackground='#e0e7ff',
            activeforeground='#4338ca',
            relief='flat',
            bd=0,
            cursor='hand2',
            command=self.paste_url
        )
        self.paste_btn.pack(side='left', padx=(12, 0), ipadx=12, ipady=9)

        tk.Label(
            card,
            text='自动保存到「视频处理」文件夹，原视频和音频会自动分类',
            font=('Microsoft YaHei UI', 9),
            bg='white',
            fg='#9ca3af'
        ).pack(anchor='w', padx=28, pady=(10, 20))

        self.download_btn = tk.Button(
            card,
            text='开始下载',
            font=('Microsoft YaHei UI', 12, 'bold'),
            bg='#4f46e5',
            fg='white',
            activebackground='#4338ca',
            activeforeground='white',
            relief='flat',
            bd=0,
            cursor='hand2',
            command=self.start_download
        )
        self.download_btn.pack(fill='x', padx=28, ipady=11)

        progress_box = tk.Frame(card, bg='white')
        progress_box.pack(fill='x', padx=28, pady=(18, 24))

        progress_top = tk.Frame(progress_box, bg='white')
        progress_top.pack(fill='x')

        self.stage_label = tk.Label(
            progress_top,
            text='等待下载',
            font=('Microsoft YaHei UI', 9),
            bg='white',
            fg='#6b7280'
        )
        self.stage_label.pack(side='left')

        self.percent_label = tk.Label(
            progress_top,
            text='0%',
            font=('Microsoft YaHei UI', 9, 'bold'),
            bg='white',
            fg='#4f46e5'
        )
        self.percent_label.pack(side='right')

        self.progress = ttk.Progressbar(
            progress_box,
            style='Download.Horizontal.TProgressbar',
            orient='horizontal',
            mode='determinate',
            maximum=100
        )
        self.progress.pack(fill='x', pady=(8, 0))

        result_card = tk.Frame(
            self.root,
            bg='white',
            highlightbackground='#e5e8ef',
            highlightthickness=1
        )
        result_card.pack(fill='x', padx=40, pady=(18, 0))

        result_top = tk.Frame(result_card, bg='white')
        result_top.pack(fill='x', padx=24, pady=(18, 14))

        tk.Label(
            result_top,
            text='下载结果',
            font=('Microsoft YaHei UI', 10, 'bold'),
            bg='white',
            fg='#374151'
        ).pack(side='left')

        self.open_btn = tk.Button(
            result_top,
            text='打开文件夹',
            font=('Microsoft YaHei UI', 9),
            bg='#f3f4f6',
            fg='#374151',
            activebackground='#e5e7eb',
            relief='flat',
            bd=0,
            cursor='hand2',
            state='disabled',
            command=self.open_folder
        )
        self.open_btn.pack(side='right', ipadx=10, ipady=5)

        self.video_title_label = tk.Label(
            result_card,
            text='暂未下载视频',
            font=('Microsoft YaHei UI', 11),
            bg='white',
            fg='#9ca3af',
            anchor='w'
        )
        self.video_title_label.pack(fill='x', padx=24, pady=(0, 8))

        self.result_info_label = tk.Label(
            result_card,
            text='下载完成后会生成：原视频 MP4 / 音频 MP3',
            font=('Microsoft YaHei UI', 9),
            bg='white',
            fg='#9ca3af',
            anchor='w'
        )
        self.result_info_label.pack(fill='x', padx=24, pady=(0, 18))

        log_head = tk.Frame(self.root, bg='#f4f6fa')
        log_head.pack(fill='x', padx=40, pady=(18, 8))

        tk.Label(
            log_head,
            text='运行日志',
            font=('Microsoft YaHei UI', 10, 'bold'),
            bg='#f4f6fa',
            fg='#374151'
        ).pack(side='left')

        log_card = tk.Frame(
            self.root,
            bg='white',
            highlightbackground='#e5e8ef',
            highlightthickness=1
        )
        log_card.pack(fill='both', expand=True, padx=40, pady=(0, 26))

        self.log_text = ScrolledText(
            log_card,
            font=('Consolas', 10),
            bg='white',
            fg='#4b5563',
            bd=0,
            relief='flat',
            wrap='word',
            padx=14,
            pady=12
        )
        self.log_text.pack(fill='both', expand=True, padx=5, pady=5)

    def draw_input_bg(self, event):
        self.input_canvas.delete('bg')

        w = event.width
        h = event.height
        r = 14

        self.input_canvas.create_arc(0, 0, r * 2, r * 2, start=90, extent=90, fill='#f5f7fb', outline='', tags='bg')
        self.input_canvas.create_arc(w - r * 2, 0, w, r * 2, start=0, extent=90, fill='#f5f7fb', outline='', tags='bg')
        self.input_canvas.create_arc(0, h - r * 2, r * 2, h, start=180, extent=90, fill='#f5f7fb', outline='', tags='bg')
        self.input_canvas.create_arc(w - r * 2, h - r * 2, w, h, start=270, extent=90, fill='#f5f7fb', outline='', tags='bg')

        self.input_canvas.create_rectangle(r, 0, w - r, h, fill='#f5f7fb', outline='', tags='bg')
        self.input_canvas.create_rectangle(0, r, w, h - r, fill='#f5f7fb', outline='', tags='bg')

        self.input_canvas.tag_lower('bg')
        self.input_canvas.coords(self.entry_window, 16, h / 2)
        self.input_canvas.itemconfigure(self.entry_window, width=max(100, w - 32))

    def log(self, text):
        if self.cli_mode:
            print(text)
        else:
            self.root.after(0, lambda: self._write_log(text))

    def _write_log(self, text):
        self.log_text.insert(tk.END, text + '\n')
        self.log_text.see(tk.END)

    def set_stage(self, text):
        if self.cli_mode:
            print(f'[阶段] {text}')
        else:
            self.root.after(0, lambda: self.stage_label.config(text=text))

    def set_progress(self, value):
        if self.cli_mode:
            return
        value = max(0, min(100, value))

        def update():
            self.progress['value'] = value
            self.percent_label.config(text=f'{int(value)}%')

        self.root.after(0, update)

    def paste_url(self):
        try:
            text = self.root.clipboard_get()
            self.url_entry.delete(0, tk.END)
            self.url_entry.insert(0, text.strip())
        except Exception:
            messagebox.showwarning('提示', '剪贴板中没有可用内容')

    def clean_filename(self, name):
        name = re.sub(r'[\\/:*?"<>|]', '_', name)
        name = re.sub(r'\s+', ' ', name).strip()
        return name[:80] if name else '抖音视频'

    def get_video_title(self, page):
        title = ''

        try:
            title = page.title
        except Exception:
            pass

        if title:
            title = re.sub(r'\s*-\s*抖音.*$', '', title)
            title = re.sub(r'_抖音.*$', '', title)

        if not title or title in ['抖音', '抖音-记录美好生活']:
            try:
                desc = page.ele('meta@name=description')

                if desc:
                    title = desc.attr('content')
            except Exception:
                pass

        return self.clean_filename(title)

    def get_unique_name(self, title):
        number = 0

        while True:
            name = title if number == 0 else f'{title}({number})'

            video_path = os.path.join(self.video_dir, name + '.mp4')
            audio_path = os.path.join(self.audio_dir, name + '.mp3')

            if not os.path.exists(video_path) and not os.path.exists(audio_path):
                return name

            number += 1

    def is_media_packet(self, packet):
        """只筛选可能是音视频资源的请求"""
        try:
            content_type = str(packet.response.headers.get('content-type', '')).lower()
            url = packet.url.lower()

            if 'video/' in content_type or 'audio/' in content_type:
                return True

            if 'octet-stream' in content_type:
                return True

            keywords = [
                'douyinvod',
                'bytevideo',
                'video/tos',
                'audio/tos',
                'mime_type=video',
                'mime_type=audio',
                '.mp4',
                '.m4a'
            ]

            return any(word in url for word in keywords)

        except Exception:
            return False

    def get_content_length(self, packet):
        try:
            headers = packet.response.headers

            if headers.get('content-range'):
                result = re.search(r'/(\d+)', str(headers.get('content-range')))

                if result:
                    return int(result.group(1))

            if headers.get('content-length'):
                return int(headers.get('content-length'))

        except Exception:
            pass

        return 0

    def get_cookies(self, page):
        cookies = {}

        try:
            for cookie in page.cookies():
                cookies[cookie['name']] = cookie['value']
        except Exception:
            pass

        return cookies

    def get_headers(self, packet, page):
        headers = {}

        try:
            for key, value in packet.request.headers.items():

                if key.lower() in [
                    ':authority',
                    ':method',
                    ':path',
                    ':scheme',
                    'range',
                    'if-range',
                    'content-length'
                ]:
                    continue

                headers[key] = value

        except Exception:
            pass

        if 'User-Agent' not in headers:

            try:
                headers['User-Agent'] = page.user_agent

            except Exception:
                headers['User-Agent'] = (
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                    'AppleWebKit/537.36 Chrome/151.0.0.0 Safari/537.36'
                )

        headers['Referer'] = 'https://www.douyin.com/'
        headers['Accept-Encoding'] = 'identity'

        return headers

    def download_file(self, url, save_path, headers, cookies, name):
        self.log(f'正在下载{name}...')

        response = requests.get(
            url,
            headers=headers,
            cookies=cookies,
            stream=True,
            timeout=60,
            allow_redirects=True
        )

        response.raise_for_status()

        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024 * 512):

                if chunk:
                    f.write(chunk)

    def get_stream_types(self, file_path):
        """真正判断文件中包含哪些媒体轨"""
        try:
            with av.open(file_path) as container:
                has_video = any(
                    stream.type == 'video'
                    for stream in container.streams
                )
                has_audio = any(
                    stream.type == 'audio'
                    for stream in container.streams
                )

                return has_video, has_audio

        except Exception:
            return False, False

    def _create_audio_output_stream(self, output_container, input_stream, codec_name):
        """创建音频编码流，并返回输出流和对应的重采样器"""
        codec_context = input_stream.codec_context
        sample_rate = codec_context.sample_rate or 44100

        try:
            layout_name = codec_context.layout.name
        except Exception:
            layout_name = 'stereo'

        output_stream = output_container.add_stream(
            codec_name,
            rate=sample_rate
        )
        output_stream.layout = layout_name

        resampler = av.audio.resampler.AudioResampler(
            format='fltp',
            layout=layout_name,
            rate=sample_rate
        )

        return output_stream, resampler

    def _encode_audio_frames(self, input_container, input_stream,
                             output_container, output_stream, resampler):
        """解码、重采样并写入音频帧"""
        for frame in input_container.decode(input_stream):
            frame.pts = None

            converted_frames = resampler.resample(frame)

            for converted_frame in converted_frames:
                for packet in output_stream.encode(converted_frame):
                    output_container.mux(packet)

        for converted_frame in resampler.resample(None):
            for packet in output_stream.encode(converted_frame):
                output_container.mux(packet)

        for packet in output_stream.encode(None):
            output_container.mux(packet)

    def merge_video_audio(self, video_path, audio_path, output_path):
        self.log('正在合并视频和音频...')

        try:
            with av.open(video_path) as video_input, \
                    av.open(audio_path) as audio_input, \
                    av.open(output_path, mode='w', format='mp4') as output:

                video_stream = next(
                    stream for stream in video_input.streams
                    if stream.type == 'video'
                )
                audio_stream = next(
                    stream for stream in audio_input.streams
                    if stream.type == 'audio'
                )

                output_video_stream = output.add_stream_from_template(
                    video_stream
                )
                output_audio_stream, resampler = self._create_audio_output_stream(
                    output,
                    audio_stream,
                    'aac'
                )

                # 视频不重新编码，保持原画质并提高处理速度
                for packet in video_input.demux(video_stream):
                    if packet.dts is None:
                        continue

                    packet.stream = output_video_stream
                    output.mux(packet)

                self._encode_audio_frames(
                    audio_input,
                    audio_stream,
                    output,
                    output_audio_stream,
                    resampler
                )

        except Exception as e:
            try:
                if os.path.exists(output_path):
                    os.remove(output_path)
            except Exception:
                pass

            raise Exception(f'音视频合并失败：{e}')

    def extract_audio(self, video_path, audio_path):
        self.log('正在提取MP3音频...')

        try:
            with av.open(video_path) as input_container, \
                    av.open(audio_path, mode='w', format='mp3') as output:

                input_stream = next(
                    stream for stream in input_container.streams
                    if stream.type == 'audio'
                )

                output_stream, resampler = self._create_audio_output_stream(
                    output,
                    input_stream,
                    'libmp3lame'
                )

                self._encode_audio_frames(
                    input_container,
                    input_stream,
                    output,
                    output_stream,
                    resampler
                )

        except Exception as e:
            try:
                if os.path.exists(audio_path):
                    os.remove(audio_path)
            except Exception:
                pass

            raise Exception(f'MP3音频提取失败：{e}')

    def open_folder(self):
        os.makedirs(self.base_dir, exist_ok=True)

        try:
            os.startfile(self.base_dir)
        except Exception:
            messagebox.showinfo('保存位置', self.base_dir)

    def start_download(self):
        url = self.url_entry.get().strip()

        if not url:
            messagebox.showwarning('提示', '请先粘贴抖音视频链接')
            return

        if 'douyin.com' not in url:
            messagebox.showwarning('提示', '请输入正确的抖音详情页链接')
            return

        self.download_btn.config(state='disabled', text='正在下载...')
        self.open_btn.config(state='disabled')

        self.log_text.delete('1.0', tk.END)

        self.video_title_label.config(
            text='正在获取视频信息...',
            fg='#6b7280'
        )

        self.result_info_label.config(
            text='请稍候，正在处理视频资源...',
            fg='#9ca3af'
        )

        self.set_progress(0)
        self.set_stage('准备下载')

        threading.Thread(
            target=self.download_task,
            args=(url,),
            daemon=True
        ).start()

    def download_task(self, url):
        candidate_files = []

        try:
            os.makedirs(self.video_dir, exist_ok=True)
            os.makedirs(self.audio_dir, exist_ok=True)

            self.set_stage('启动浏览器')
            self.set_progress(5)
            self.log('正在启动浏览器...')

            options = ChromiumOptions()
            page = ChromiumPage(options)
            self.page = page

            page.listen.start()

            self.set_stage('打开视频页面')
            self.set_progress(10)
            self.log('正在打开抖音详情页...')

            page.get(url)

            # 尝试让页面视频真正播放
            time.sleep(2)

            try:
                page.run_js("""
                let v = document.querySelector('video');
                if(v){
                    v.muted = false;
                    v.volume = 1;
                    v.play().catch(()=>{});
                }
                """)
            except Exception:
                pass

            video_title = self.get_video_title(page)
            file_name = self.get_unique_name(video_title)

            self.root.after(
                0,
                lambda title=video_title: self.video_title_label.config(
                    text=title,
                    fg='#1f2937'
                )
            )

            self.log(f'视频名称：{video_title}')
            self.log('正在抓取媒体资源...')

            self.set_stage('分析媒体资源')
            self.set_progress(15)

            media_packets = []
            start_time = time.time()

            # 监听更久一点，音频通常会稍后加载
            while time.time() - start_time < 25:

                try:
                    packet = page.listen.wait(timeout=2)

                    if not packet:
                        continue

                    if not self.is_media_packet(packet):
                        continue

                    if any(p.url == packet.url for p in media_packets):
                        continue

                    media_packets.append(packet)

                except Exception:
                    pass

            if not media_packets:
                raise Exception('没有获取到媒体资源')

            # 大文件优先检查
            media_packets.sort(key=self.get_content_length, reverse=True)

            self.log(f'捕获到媒体资源：{len(media_packets)} 个')

            cookies = self.get_cookies(page)

            # 最多检查前8个，避免全部下载太慢
            media_packets = media_packets[:8]

            complete_file = None
            pure_video_file = None
            pure_audio_file = None

            self.set_stage('识别音视频资源')

            for index, packet in enumerate(media_packets):

                temp_path = os.path.join(
                    self.base_dir,
                    f'__candidate_{index}.mp4'
                )

                candidate_files.append(temp_path)

                headers = self.get_headers(packet, page)

                try:
                    self.log(f'正在识别媒体资源 {index + 1}/{len(media_packets)}...')

                    self.download_file(
                        packet.url,
                        temp_path,
                        headers,
                        cookies,
                        f'媒体资源{index + 1}'
                    )

                    has_video, has_audio = self.get_stream_types(temp_path)

                    if has_video and has_audio:
                        complete_file = temp_path
                        self.log('找到完整音视频')
                        break

                    if has_video and not has_audio and pure_video_file is None:
                        pure_video_file = temp_path
                        self.log('找到纯视频流')

                    if has_audio and not has_video and pure_audio_file is None:
                        pure_audio_file = temp_path
                        self.log('找到纯音频流')

                    if pure_video_file and pure_audio_file:
                        break

                except Exception:
                    pass

                self.set_progress(20 + (index + 1) / len(media_packets) * 45)

            original_path = os.path.join(
                self.video_dir,
                file_name + '.mp4'
            )

            audio_path = os.path.join(
                self.audio_dir,
                file_name + '.mp3'
            )

            # 情况1：直接找到完整视频
            if complete_file:

                self.set_stage('保存原视频')
                self.set_progress(72)

                os.replace(
                    complete_file,
                    original_path
                )

                if complete_file in candidate_files:
                    candidate_files.remove(complete_file)

            # 情况2：视频和音频分离
            elif pure_video_file and pure_audio_file:

                self.set_stage('合并音视频')
                self.set_progress(75)

                self.merge_video_audio(
                    pure_video_file,
                    pure_audio_file,
                    original_path
                )

            else:
                raise Exception('没有找到可配对的视频流和音频流')

            # 再从最终原视频提取MP3
            self.set_stage('提取MP3音频')
            self.set_progress(88)

            self.extract_audio(
                original_path,
                audio_path
            )

            self.set_stage('下载完成')
            self.set_progress(100)

            self.log('')
            self.log('全部处理完成！')
            self.log(f'原视频：{original_path}')
            self.log(f'音频：{audio_path}')

            self.root.after(
                0,
                lambda: self.result_info_label.config(
                    text='已生成：原视频 MP4  ·  音频 MP3',
                    fg='#16a34a'
                )
            )

            self.root.after(
                0,
                lambda: self.open_btn.config(
                    state='normal'
                )
            )

        except Exception as e:
            error_msg = str(e)

            self.log('')
            self.log(f'下载失败：{error_msg}')
            self.set_stage('下载失败')

            self.root.after(
                0,
                lambda msg=error_msg: self.result_info_label.config(
                    text=f'处理失败：{msg}',
                    fg='#dc2626'
                )
            )

        finally:
            # 删除识别过程中产生的临时文件
            for file_path in candidate_files:

                try:
                    if os.path.exists(file_path):
                        os.remove(file_path)
                except Exception:
                    pass

            try:
                if self.page:
                    self.page.quit()
            except Exception:
                pass

            self.page = None

            self.root.after(
                0,
                lambda: self.download_btn.config(
                    state='normal',
                    text='开始下载'
                )
            )

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and 'douyin.com' in sys.argv[1]:
        app = DouyinDownloader(cli_mode=True)
        app.cli_download(sys.argv[1])
    else:
        root = tk.Tk()
        app = DouyinDownloader(root)
        root.mainloop()
