# 视频拼接脚本 - 拼接AIGC视频片段，并添加同目录中的音频
import os
import re
import shutil
import sys
import time


AIGC_VIDEO_DIR = '视频处理/所有新生成的视频片段'
FINAL_VIDEO_DIR = '视频处理'
FINAL_VIDEO_BACKUP_DIR = '视频处理/05_最终视频'

try:
    from moviepy import AudioFileClip, VideoFileClip, concatenate_videoclips
except ImportError:
    print("正在安装 moviepy...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "moviepy"])
    from moviepy import AudioFileClip, VideoFileClip, concatenate_videoclips

video_extensions = (".mp4", ".avi", ".mov", ".mkv", ".flv", ".wmv")
audio_extensions = (".mp3", ".wav", ".m4a", ".aac", ".flac", ".ogg", ".wma")


def natural_sort_key(path):
    """按照文件名中的数字自然排序，例如：片段_2 排在片段_10 前面。"""
    filename = os.path.basename(path)
    return [int(part) if part.isdigit() else part.lower()
            for part in re.split(r"(\d+)", filename)]

def elapsed(start):
    return f"{time.time() - start:.1f}秒"

# ============ 找到最近生成的一组AIGC视频片段 ============
all_segments = []
if os.path.isdir(AIGC_VIDEO_DIR):
    for f in os.listdir(AIGC_VIDEO_DIR):
        path = os.path.join(AIGC_VIDEO_DIR, f)
        if (
            os.path.isfile(path)
            and f.lower().endswith(".mp4")
            and not f.endswith("_最终视频.mp4")
        ):
            all_segments.append(path)

if not all_segments:
    print("未找到AIGC视频片段！")
    print(f"请先运行 demo3，片段目录：{AIGC_VIDEO_DIR}")
    sys.exit(1)

latest_segment = max(all_segments, key=os.path.getmtime)
latest_name = os.path.splitext(os.path.basename(latest_segment))[0]
parts = latest_name.rsplit("_", 1)
video_name = parts[0] if len(parts) == 2 and parts[1].isdigit() else latest_name

video_files = []
for path in all_segments:
    name = os.path.splitext(os.path.basename(path))[0]
    if name.startswith(video_name + "_"):
        video_files.append(path)
video_files = sorted(video_files, key=natural_sort_key)

print("=" * 60)
print("自动识别结果")
print("=" * 60)
print(f"视频名称：{video_name}")
print(f"AIGC片段目录：{AIGC_VIDEO_DIR}")
print(f"共发现 {len(video_files)} 个视频片段")

for i, f in enumerate(video_files, 1):
    print(f"  {i}. {os.path.basename(f)}")

# ============ 在视频片段目录中查找对应音频 ============
audio_path = None

# 优先查找与视频名称完全相同的音频，例如：测试视频.mp3
for extension in audio_extensions:
    exact_path = os.path.join(AIGC_VIDEO_DIR, video_name + extension)
    if os.path.isfile(exact_path):
        audio_path = exact_path
        break

# 没有完全同名文件时，再查找名称以视频名称开头的音频
if not audio_path:
    for f in os.listdir(AIGC_VIDEO_DIR):
        path = os.path.join(AIGC_VIDEO_DIR, f)
        name, extension = os.path.splitext(f)
        if (
            os.path.isfile(path)
            and extension.lower() in audio_extensions
            and (name == video_name or name.startswith(video_name))
        ):
            audio_path = path
            break

if not audio_path:
    print("\n未找到对应音频，无法继续！")
    print(f"音频目录：{AIGC_VIDEO_DIR}")
    print("支持的音频格式：" + "、".join(audio_extensions))
    print(f"建议将音频命名为：{video_name}.mp3")
    sys.exit(1)

print(f"音频文件：{audio_path}")

# ============ 第一步：拼接视频 ============
print("\n" + "=" * 60)
print("第一步：拼接AIGC视频片段")
print("=" * 60)

t0 = time.time()
video_clips = []
for i, video_file in enumerate(video_files, 1):
    print(f"加载 [{i}/{len(video_files)}]：{os.path.basename(video_file)}")
    video_clips.append(VideoFileClip(video_file))

final_video = concatenate_videoclips(video_clips, method="compose")
print(f"拼接完成，总时长：{final_video.duration:.2f}秒，耗时：{elapsed(t0)}")

# ============ 第二步：添加同目录中的音频 ============
print("\n" + "=" * 60)
print("第二步：添加音频")
print("=" * 60)

original_audio = AudioFileClip(audio_path)

final_duration = min(final_video.duration, original_audio.duration)
if hasattr(final_video, "subclipped"):
    final_video = final_video.subclipped(0, final_duration)
    final_audio = original_audio.subclipped(0, final_duration)
else:
    final_video = final_video.subclip(0, final_duration)
    final_audio = original_audio.subclip(0, final_duration)

if hasattr(final_video, "with_audio"):
    final_video = final_video.with_audio(final_audio)
else:
    final_video = final_video.set_audio(final_audio)

print(f"最终时长：{final_duration:.2f}秒")
print("已添加同目录中的音频")

# ============ 第三步：输出最终视频 ============
# 最终视频保存到“视频处理”文件夹。
# 如果“视频处理/05_最终视频”已经存在，则再复制一份到该文件夹。
os.makedirs(FINAL_VIDEO_DIR, exist_ok=True)
output_video_path = os.path.join(FINAL_VIDEO_DIR, f"{video_name}_最终视频.mp4")
backup_video_path = os.path.join(FINAL_VIDEO_BACKUP_DIR, f"{video_name}_最终视频.mp4")

print("\n" + "=" * 60)
print("第三步：生成最终视频")
print("=" * 60)
print(f"保存到：{output_video_path}")

final_video.write_videofile(
    output_video_path,
    fps=30,
    codec="libx264",
    audio_codec="aac",
    temp_audiofile="temp-audio.m4a",
    remove_temp=True,
    threads=4,
    preset="medium",
    bitrate="5000k",
    logger="bar"
)



for clip in video_clips:
    clip.close()
final_video.close()
final_audio.close()
original_audio.close()

print("\n" + "=" * 60)
print("全部完成！")
print("=" * 60)
print(f"最终视频：{output_video_path}")

if os.path.exists(output_video_path):
    size_mb = os.path.getsize(output_video_path) / (1024 * 1024)
    print(f"文件大小：{size_mb:.2f} MB")
