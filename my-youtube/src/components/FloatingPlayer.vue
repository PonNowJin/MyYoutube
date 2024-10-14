<template>
    <div
      v-if="video"
      class="floating-player"
      :style="{ left: position.x + 'px', top: position.y + 'px', width: playerWidth + 'px', height: playerHeight + 'px' }"
      @mousedown="onMouseDown"
    >
      <div class="close-btn" @click.stop="closePlayer">✖</div>
      <video :src="video.url" controls autoplay></video>
      <div class="resizer" @mousedown.stop="startResize"></div>
    </div>
</template>

<script>
export default {
    props: {
        video: {
            type: Object,
            default: null,
        },
    },
    data() {
        return {
            isDragging: false,
            isResizing: false,
            offset: { x: 0, y: 0 },
            position: { x: 100, y: 100 }, // 初始位置
            playerWidth: 800, // 播放器初始寬度
            playerHeight: 450, // 播放器初始高度
            longPressTimeout: null, // 用於長按的定時器
        };
    },
    methods: {
        closePlayer() {
            this.$emit('close'); // 通知父組件關閉播放器
        },
        onMouseDown(event) {
            event.preventDefault(); // 防止事件影響視頻控制

            this.longPressTimeout = setTimeout(() => {
                this.startDrag(event);
                document.body.style.cursor = 'move'; // 更改游標樣式
            }, 200); // 長按300毫秒進入移動模式

            // 添加 mousemove 事件監聽器
            window.addEventListener('mousemove', this.onMove);
            window.addEventListener('mouseup', this.stopDrag);
        },
        startDrag(event) {
            this.isDragging = true;
            this.offset.x = event.clientX - this.position.x;
            this.offset.y = event.clientY - this.position.y;
        },
        onMove(event) {
            if (this.isDragging) {
                this.position.x = event.clientX - this.offset.x;
                this.position.y = event.clientY - this.offset.y;
            }
        },
        stopDrag() {
            this.isDragging = false;
            clearTimeout(this.longPressTimeout);
            this.longPressTimeout = null; // 清除定時器
            document.body.style.cursor = ''; // 還原游標樣式
            
            // 移除 mousemove 和 mouseup 事件監聽器
            window.removeEventListener('mousemove', this.onMove);
            window.removeEventListener('mouseup', this.stopDrag);
        },
        startResize() {
            this.isResizing = true;
            window.addEventListener('mousemove', this.onResize);
            window.addEventListener('mouseup', this.stopResize);
        },
        onResize(event) {
            if (this.isResizing) {
                const newWidth = event.clientX - this.position.x;
                const newHeight = event.clientY - this.position.y;
                if (newWidth > 200) this.playerWidth = newWidth; // 限制最小寬度
                if (newHeight > 100) this.playerHeight = newHeight; // 限制最小高度
            }
        },
        stopResize() {
            this.isResizing = false;
            window.removeEventListener('mousemove', this.onResize);
            window.removeEventListener('mouseup', this.stopResize);
        },
    },
};
</script>

<style scoped>
.floating-player {
    position: fixed;
    background: #000;
    z-index: 1000; /* 確保懸浮播放器在最上層 */
    border-radius: 10px; /* 圓角效果 */
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.5); /* 陰影效果 */
    cursor: default; /* 初始游標樣式 */
}
.floating-player video {
    width: 100%; /* 設定懸浮播放器的寬度 */
    height: 100%; /* 設定懸浮播放器的高度 */
}
.close-btn {
    position: absolute;
    top: 10px;
    right: 10px;
    color: white;
    cursor: pointer;
    font-size: 24px; /* 關閉按鈕的字體大小 */
}
.resizer {
    position: absolute;
    bottom: 0;
    right: 0;
    width: 20px;
    height: 20px;
    background: rgba(255, 255, 255, 0.5); /* 調整大小的手柄 */
    cursor: nwse-resize; /* 調整大小的游標樣式 */
}
</style>
