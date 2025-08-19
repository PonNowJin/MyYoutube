<template>
  <div class="video-page">
    <div class="main-content">
      <!-- 左側：影片 + 留言 -->
      <div class="left-panel">
        <h1 class="video-title">{{ videoData.title }}</h1>

        <!-- video.js player -->
        <div data-vjs-player>
          <video
            ref="player"
            class="video-js vjs-default-skin video-player"
            controls
            preload="auto"
            playsinline
          ></video>
        </div>

        <!-- 留言區 -->
        <section class="comments">
          <h2>留言區</h2>

          <!-- 留言表單 -->
          <form @submit.prevent="submitComment" class="comment-form">
            <input v-model="newComment.user" type="text" placeholder="你的名字" required />
            <textarea v-model="newComment.text" placeholder="寫下你的留言..." required></textarea>
            <button type="submit">送出留言</button>
          </form>

          <!-- 留言列表 -->
          <div v-for="(comment, i) in comments" :key="i" class="comment">
            <strong>{{ comment.user }}:</strong> {{ comment.text }}
          </div>
        </section>
      </div>

      <!-- 右側：推薦影片 -->
      <div class="right-panel">
        <h2>推薦影片</h2>
        <ul class="recommendations">
          <li v-for="rec in recommended" :key="rec.title" class="recommendation" @click="navigateToVideo(rec.id)">
            <img :src="rec.thumbnail" class="thumbnail" />
            <div class="rec-title">{{ rec.title }}</div>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import videojs from 'video.js';
import 'video.js/dist/video-js.css';

export default {
  props: ['id'],
  data() {
    return {
      videoData: {},
      comments: [],
      recommended: [],
      newComment: {
        user: '',
        text: '',
      },
      player: null,
    };
  },
  watch: {
    id: {
      immediate: true,
      handler() {
        this.loadVideoData();
      },
    },
  },
  methods: {
    async loadVideoData() {
      try {
        const res = await axios.get(`http://127.0.0.1:5001/api/video-info/${this.id}`);
        this.videoData = res.data;

        const allRes = await axios.get('http://127.0.0.1:5001/api/categories');
        const allVideos = Object.values(allRes.data).flat();

        this.recommended = allVideos.filter(v => v.id !== this.id).slice(0, 5);

        this.comments = [
          { user: 'Alice', text: '超好看！' },
          { user: 'Bob', text: '推推推' },
        ];

        // 初始化/更新播放器
        this.$nextTick(() => {
          if (this.player) {
            this.player.src({ type: 'video/mp4', src: this.videoData.url });
            this.player.play();
          } else {
            this.player = videojs(this.$refs.player, {
              controls: true,
              autoplay: true,
              preload: 'auto',
              // responsive: true,
              fluid: true,
            });
            this.player.src({ type: 'video/mp4', src: this.videoData.url });
          }
        });
      } catch (err) {
        console.error('讀取影片資料錯誤:', err);
      }
    },
    navigateToVideo(newId) {
      this.$router.push({ name: 'VideoPage', params: { id: newId } });
    },
    submitComment() {
      if (this.newComment.user && this.newComment.text) {
        this.comments.unshift({ ...this.newComment });
        this.newComment.user = '';
        this.newComment.text = '';
      }
    },
  },
  beforeUnmount() {
    if (this.player) {
      this.player.dispose();
    }
  },
};
</script>

<style scoped>
.video-page {
  padding: 16px;
  background-color: #f9f9f9;
}

.main-content {
  display: flex;
  flex-direction: row;
  gap: 24px;
}

.left-panel {
  flex: 2;
}

.video-title {
  font-size: 1.5rem;
  margin-bottom: 8px;
}

.video-player {
  width: 100%;
  max-height: 60vh;
  height: auto;
  border-radius: 8px;
  margin-bottom: 24px;
  background: #000;
  object-fit: contain; /* 保持比例不裁切 */
}

/* 強制 video 元素置中 */
.video-js {
  max-height: 60vh;
  height: auto !important;
  aspect-ratio: unset !important;
}

.video-js .vjs-tech {
  object-fit: contain !important;
  max-height: 60vh;
  width: 100%;
  height: auto;
  margin: 0 auto;
  display: block;
}


/* 留言區 */
.comments {
  background-color: #fff;
  padding: 16px;
  border-radius: 8px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
}

.comment-form {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 16px;
}

.comment-form input,
.comment-form textarea {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1rem;
}

.comment-form button {
  align-self: flex-start;
  padding: 6px 12px;
  background-color: #1976d2;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.comment {
  padding: 8px 0;
  border-bottom: 1px solid #eee;
}

.right-panel {
  flex: 1;
  background-color: #fff;
  padding: 16px;
  border-radius: 8px;
  height: fit-content;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
}

.recommendations {
  list-style: none;
  padding: 0;
  margin: 0;
}

.recommendation {
  display: flex;
  align-items: center;
  margin-bottom: 16px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.recommendation:hover {
  background-color: #f0f0f0;
  border-radius: 6px;
  padding: 4px;
}

.thumbnail {
  width: 120px;
  height: 70px;
  object-fit: cover;
  border-radius: 4px;
  margin-right: 12px;
}

.rec-title {
  font-size: 0.95rem;
  color: #333;
}
</style>
