// router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '../views/HomePage.vue';
import VideoPage from '../views/VideoPage.vue';

const routes = [
  { path: '/', name: 'Home', component: HomePage },
  { path: '/video/:id', name: 'VideoPage', component: VideoPage, props: true },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
