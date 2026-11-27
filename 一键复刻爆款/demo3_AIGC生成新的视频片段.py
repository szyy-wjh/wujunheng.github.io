# RunningHub ComfyUI 工作流 API 调用脚本
# 功能：通过RunningHub API调用云端的ComfyUI工作流，支持任务提交、状态查询、文件上传和结果下载
# 文档：https://www.runninghub.cn

import requests       # 发送HTTP请求
import time           # 用于轮询等待
import os             # 文件路径操作

# ============ 配置区 ============
# API Key：RunningHub为每位用户生成的32位密钥，用于认证API请求
# 获取方式：登录RunningHub后台 -> API Key管理 -> 复制密钥
API_KEY = "c13f1241d29f415facca9f58d"

# 工作流ID：要调用的ComfyUI工作流的唯一标识
# 获取方式：RunningHub工作流详情页URL中获取，如 https://www.runninghub.cn/openapi/v2/run/workflow/{WORKFLOW_ID}
WORKFLOW_ID = "2079816909545107457"

# ============ API端点配置 ============
# RunningHub API 基础地址
BASE_URL = "https://www.runninghub.cn/openapi/v2"

# 提交工作流任务的接口地址
# POST请求，提交后返回taskId
RUN_URL = f"{BASE_URL}/run/workflow/{WORKFLOW_ID}"

# 查询任务状态的接口地址
# POST请求，传入taskId查询任务执行状态和结果
QUERY_URL = f"{BASE_URL}/query"

# 上传文件的接口地址
# POST请求，上传本地文件获取URL供工作流使用
UPLOAD_URL = f"{BASE_URL}/media/upload/binary"


def submit_workflow(node_info_list=None, instance_type="default", use_personal_queue=False):
    """
    提交工作流任务到RunningHub云端执行

    Args:
        node_info_list (list): 节点参数列表，用于动态修改工作流中的节点参数
            示例：[{"nodeId": "3", "fieldName": "image", "fieldValue": "api/xxx.png"}]
            - nodeId: ComfyUI工作流中的节点ID
            - fieldName: 节点中要修改的字段名
            - fieldValue: 字段值（上传文件时使用 fileName；可以是URL、数值、字符串等）
        instance_type (str): 运行实例类型
            - "default": 24G显存，适合大多数任务
            - "plus": 48G显存，适合大模型或高分辨率任务
        use_personal_queue (bool): 是否使用个人独占队列
            - True: 使用独占队列，减少排队时间（需要企业级API Key）
            - False: 使用共享队列

    Returns:
        tuple: (task_id, response)
            - task_id: 任务ID，用于后续查询状态
            - response: 完整的API响应
    """
    # 构造请求头，包含认证信息
    headers = {
        "Content-Type": "application/json",           # 请求体为JSON格式
        "Authorization": f"Bearer {API_KEY}"          # Bearer Token认证
    }

    # 构造请求体
    payload = {
        "addMetadata": True,                          # 在输出图片中添加工作流元数据
        "nodeInfoList": node_info_list or [],         # 节点参数列表，为空则使用默认参数
        "instanceType": instance_type,                # 实例类型
        "usePersonalQueue": str(use_personal_queue).lower()  # 是否使用个人队列（需转为字符串）
    }

    # 发送POST请求提交任务，遇到421并发限制自动重试
    print(f"提交工作流任务: {WORKFLOW_ID}")
    max_retries = 10
    retry_wait = 60  # 每次重试等待秒数
    for attempt in range(1, max_retries + 1):
        response = requests.post(RUN_URL, headers=headers, json=payload)
        result = response.json()

        # 提交成功时状态为 RUNNING(运行中) 或 QUEUED(排队中)
        if result.get("status") in ["RUNNING", "QUEUED"]:
            print(f"任务已提交! taskId: {result['taskId']}, 状态: {result['status']}")
            return result["taskId"], result

        # 421并发限制 - 等待后重试
        if result.get("errorCode") == "421":
            print(f"[{attempt}/{max_retries}] 并发限制，{retry_wait}秒后重试... (taskId为空: {result.get('errorMessage')})")
            time.sleep(retry_wait)
            continue

        # 其他错误，直接返回失败
        print(f"提交失败: {result}")
        return None, result

    # 重试次数用尽
    print(f"重试{max_retries}次后仍失败")
    return None, None


def query_task(task_id):
    """
    查询任务执行状态
    
    Args:
        task_id (str): 任务ID，由submit_workflow()返回
    
    Returns:
        dict: API响应，包含以下字段：
            - taskId: 任务ID
            - status: 任务状态 (QUEUED/RUNNING/SUCCESS/FAILED)
            - results: 结果列表（任务成功时）
            - errorCode: 错误码（任务失败时）
            - errorMessage: 错误信息（任务失败时）
    """
    # 构造请求头
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    # 构造请求体，只需传入taskId
    payload = {"taskId": task_id}
    
    # 发送POST请求查询状态
    response = requests.post(QUERY_URL, headers=headers, json=payload)
    return response.json()


def wait_for_result(task_id, interval=5, max_wait=600):
    """
    轮询等待任务完成
    
    Args:
        task_id (str): 任务ID
        interval (int): 轮询间隔，单位秒，默认5秒
        max_wait (int): 最大等待时间，单位秒，默认600秒(10分钟)
    
    Returns:
        dict: 任务成功时返回完整响应，失败时返回错误响应，超时返回None
    """
    print(f"等待任务完成 (taskId: {task_id})...")
    waited = 0  # 已等待时间
    
    # 循环轮询，直到任务完成或超时
    while waited < max_wait:
        result = query_task(task_id)       # 查询任务状态
        status = result.get("status")      # 获取状态
        
        if status == "SUCCESS":
            # 任务成功完成
            print("任务完成!")
            return result
        elif status == "FAILED":
            # 任务执行失败
            print(f"任务失败: {result.get('errorMessage')}")
            return result
        else:
            # 任务仍在执行中（QUEUED或RUNNING）
            print(f"状态: {status}, 等待中... ({waited}秒)")
            time.sleep(interval)           # 等待指定时间
            waited += interval             # 累计已等待时间
    
    # 超时仍未完成
    print("等待超时")
    return None


def upload_file(file_path):
    """
    上传本地文件到RunningHub服务器
    
    用途：当工作流需要输入文件（如图片、视频）时，先上传获取URL
    上传后的链接有效期为1天
    
    Args:
        file_path (str): 本地文件的绝对路径或相对路径
    
    Returns:
        tuple: (file_name, download_url) 上传成功返回(服务器文件名, 下载URL)，失败返回(None, None)
            - file_name: 用于传给 LoadImage 节点的 fieldValue
            - download_url: 文件的临时下载URL
    """
    # 构造请求头（文件上传不需要Content-Type，会自动设置multipart/form-data）
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    
    # 获取文件名
    filename = os.path.basename(file_path)
    
    # 以二进制方式读取文件
    with open(file_path, "rb") as f:
        files = {"file": (filename, f)}    # 构造multipart/form-data格式
        print(f"上传文件: {filename}")
        response = requests.post(UPLOAD_URL, headers=headers, files=files)
    
    # 解析响应
    result = response.json()
    if result.get("code") == 0:
        # 上传成功，返回 fileName（用于工作流节点）和 download_url
        file_name = result["data"]["fileName"]
        download_url = result["data"]["download_url"]
        print(f"上传成功: fileName={file_name}")
        return file_name, download_url
    else:
        # 上传失败
        print(f"上传失败: {result}")
        return None, None


def download_result(url, save_path):
    """
    下载任务生成的结果文件
    
    注意：结果URL有效期为24小时，请及时下载保存
    
    Args:
        url (str): 结果文件的URL，由任务响应中的results[].url获取
        save_path (str): 本地保存路径（包含文件名）
    """
    print(f"下载结果: {url}")
    
    # 发送GET请求下载文件
    response = requests.get(url)
    
    # 以二进制方式写入本地文件
    with open(save_path, "wb") as f:
        f.write(response.content)
    
    print(f"已保存到: {save_path}")


# ============ 使用示例 ============
if __name__ == "__main__":
    import glob
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from config import FRAMES_DIR, get_generated_dir, natural_sort_key

    # ============ 自动识别最近一组抽帧 ============
    frame_files_all = glob.glob(os.path.join(FRAMES_DIR, "*.jpg"))
    if not frame_files_all:
        print(f"未找到抽帧图片，请先运行 demo2")
        print(f"抽帧目录：{FRAMES_DIR}")
        sys.exit(1)

    # 文件名格式：视频名_1.jpg、视频名_2.jpg……
    latest_frame = max(frame_files_all, key=os.path.getmtime)
    latest_name = os.path.splitext(os.path.basename(latest_frame))[0]
    video_name = latest_name.rsplit("_", 1)[0] if "_" in latest_name else latest_name
    print(f"自动识别视频名：{video_name}")

    LOAD_IMAGE_NODE_ID = "35"
    generated_dir = get_generated_dir(video_name)

    # 只处理当前视频对应的抽帧
    frame_files = [
        f for f in frame_files_all
        if os.path.splitext(os.path.basename(f))[0].startswith(video_name + "_")
    ]
    frame_files = sorted(frame_files, key=natural_sort_key)

    print(f"共发现 {len(frame_files)} 帧待处理")
    print(f"抽帧目录：{FRAMES_DIR}")
    print(f"AIGC视频片段目录：{generated_dir}")

    success_count = 0
    fail_count = 0

    # 只处理第一帧
    frame_files = frame_files[:1]
    for idx, frame_path in enumerate(frame_files, 1):
        frame_name = os.path.splitext(os.path.basename(frame_path))[0]
        expected_mp4 = os.path.join(generated_dir, f"{frame_name}.mp4")
        if os.path.exists(expected_mp4):
            print(f"[{idx}/{len(frame_files)}] 跳过已完成：{frame_name}")
            success_count += 1
            continue

        print("\n" + "=" * 60)
        print(f"[{idx}/{len(frame_files)}] 处理：{frame_path}")
        print("=" * 60)

        file_name, _ = upload_file(frame_path)
        if not file_name:
            print(f"上传失败，跳过：{frame_path}")
            fail_count += 1
            continue

        node_info_list = [{
            "nodeId": LOAD_IMAGE_NODE_ID,
            "fieldName": "image",
            "fieldValue": file_name
        }]
        task_id, _ = submit_workflow(node_info_list=node_info_list)
        if not task_id:
            print(f"提交任务失败，跳过：{frame_path}")
            fail_count += 1
            continue

        result = wait_for_result(task_id, interval=10, max_wait=900)
        if not result or result.get("status") != "SUCCESS":
            print(f"任务未成功完成：{frame_path}")
            fail_count += 1
            continue

        results = result.get("results", [])
        print(f"任务完成，共 {len(results)} 个结果文件")
        used_names = {}

        for item_idx, item in enumerate(results, 1):
            url = item.get("url")
            output_type = item.get("outputType")
            if not url:
                continue

            ext = f".{output_type}" if output_type else ""
            base_name = f"{frame_name}{ext}"
            if base_name in used_names:
                used_names[base_name] += 1
                save_name = f"{frame_name}_{used_names[base_name]}{ext}"
            else:
                used_names[base_name] = 1
                save_name = base_name

            save_path = os.path.join(generated_dir, save_name)
            print(f"  下载结果 {item_idx}：{save_name}")
            download_result(url, save_path)

        success_count += 1

    print("\n" + "=" * 60)
    print(f"全部完成！成功：{success_count}，失败：{fail_count}")
    print(f"AIGC视频片段保存在：{generated_dir}")
    print("=" * 60)
