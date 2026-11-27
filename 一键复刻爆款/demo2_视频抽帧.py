# 视频抽帧脚本 - 每5秒抽取一帧
import cv2
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import ORIGINAL_VIDEO_DIR, get_frames_dir, natural_sort_key

# ============ 配置区 ============
interval_seconds = 5
video_extensions = (".mp4", ".avi", ".mov", ".mkv", ".flv", ".wmv")

# ============ 自动查找原视频 ============
video_files = []
if os.path.isdir(ORIGINAL_VIDEO_DIR):
    for f in os.listdir(ORIGINAL_VIDEO_DIR):
        path = os.path.join(ORIGINAL_VIDEO_DIR, f)
        if os.path.isfile(path) and f.lower().endswith(video_extensions):
            video_files.append(path)

if not video_files:
    print("=" * 50)
    print("未找到原视频！")
    print(f"请把视频放到：{ORIGINAL_VIDEO_DIR}")
    print("=" * 50)
    sys.exit(1)

# 默认处理最近修改的原视频
video_path = max(video_files, key=os.path.getmtime)
video_name = os.path.splitext(os.path.basename(video_path))[0]
frames_dir = get_frames_dir(video_name)

print("自动识别：")
print(f"  原视频：{video_path}")
print(f"  视频名称：{video_name}")
print(f"  抽帧间隔：{interval_seconds}秒")
print(f"  抽帧保存：{frames_dir}")

# ============ 打开视频 ============
cap = cv2.VideoCapture(video_path)
fps = cap.get(cv2.CAP_PROP_FPS)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
duration = total_frames / fps if fps > 0 else 0

if fps <= 0:
    print("错误：无法获取视频帧率，视频可能已损坏")
    cap.release()
    sys.exit(1)

print("视频信息：")
print(f"  帧率：{fps:.2f} FPS")
print(f"  总帧数：{total_frames}")
print(f"  时长：{duration:.2f} 秒")

interval_frames = max(1, int(fps * interval_seconds))
frame_count = 0
saved_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break
    if frame_count % interval_frames == 0:
        saved_count += 1
        timestamp = frame_count / fps
        output_path = os.path.join(frames_dir, f"{video_name}_{saved_count}.jpg")
        success, encoded_img = cv2.imencode(".jpg", frame)
        if success:
            with open(output_path, "wb") as f:
                f.write(encoded_img.tobytes())
            print(f"  保存第{saved_count}帧：{os.path.basename(output_path)}（{timestamp:.1f}秒）")
        else:
            print(f"  保存失败：{output_path}")
    frame_count += 1

cap.release()
print(f"\n抽帧完成！共保存 {saved_count} 张图片")
print(f"保存位置：{frames_dir}")
