from flask import Flask, jsonify, send_file, request
from flask_cors import CORS
import os
import cv2
import urllib.parse

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}}, supports_credentials=True)

# 設定影片存放資料夾
VIDEO_FOLDER = '/Users/ponfu/Documents/.macos'
THUMBNAIL_FOLDER = '/Users/ponfu/Documents/.macos/thumbnail_folder'

# 讀取資料夾中的影片，生成縮圖
def generate_thumbnail(video_path, thumbnail_path):
    # 檢查影片檔案是否存在
    if not os.path.exists(video_path):
        print(f"影片不存在: {video_path}")
        return False

    # 打開影片
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"無法開啟影片: {video_path}")
        return False
    
    # 計算影片中間的幀數
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    middle_frame = frame_count // 3  # 取得中間幀位置

    # 設定影片到中間幀
    cap.set(cv2.CAP_PROP_POS_FRAMES, middle_frame)

    # 讀取中間幀
    ret, frame = cap.read()
    if ret:
        # 儲存縮圖
        cv2.imwrite(thumbnail_path, frame)
        print(f"縮圖已儲存至: {thumbnail_path}")
    else:
        print(f"無法讀取影片幀: {video_path}")

    # 釋放資源
    cap.release()
    return ret

# 獲取所有分類與影片資訊
@app.route('/api/categories')
def get_categories():
    categories = {}
    
    # 取得所有子資料夾及其影片
    for subfolder in os.listdir(VIDEO_FOLDER):
        subfolder_path = os.path.join(VIDEO_FOLDER, subfolder)
        if os.path.isdir(subfolder_path):
            videos = get_videos_from_folder(subfolder_path)
            categories[subfolder] = videos

    return jsonify(categories)

# 讀取指定資料夾中的影片資訊
def get_videos_from_folder(folder):
    videos = []
    for filename in os.listdir(folder):
        if filename.endswith(('.mp4', '.avi', '.mkv', '.mov')):
            thumbnail_path = os.path.join(THUMBNAIL_FOLDER, f"{filename}.jpg")

            # 檢查縮圖是否存在，如果不存在則生成
            if not os.path.exists(thumbnail_path):
                video_path = os.path.join(folder, filename)
                generate_thumbnail(video_path, thumbnail_path)

            # 使用 urllib.parse.quote 對檔名進行編碼
            encoded_filename = urllib.parse.quote(filename)
            videos.append({
                'title': filename,
                'thumbnail': f'http://127.0.0.1:5001/api/thumbnail/{encoded_filename}',
                'url': f'http://127.0.0.1:5001/api/video/{encoded_filename}'
            })
    return videos

# 提供縮圖
@app.route('/api/thumbnail/<path:filename>')
def get_thumbnail(filename):
    thumbnail_path = os.path.join(THUMBNAIL_FOLDER, f"{filename}.jpg")
    return send_file(thumbnail_path, mimetype='image/jpeg')

# 提供影片檔案
@app.route('/api/video/<path:filename>')
def get_video(filename):
    for subfolder in os.listdir(VIDEO_FOLDER):
        video_path = os.path.join(VIDEO_FOLDER, subfolder, filename)
        if os.path.exists(video_path):
            return send_file(video_path, mimetype='video/mp4')
    return "Video not found", 404

if __name__ == '__main__':
    if not os.path.exists(THUMBNAIL_FOLDER):
        os.makedirs(THUMBNAIL_FOLDER)
    app.run(debug=True, port=5001)
