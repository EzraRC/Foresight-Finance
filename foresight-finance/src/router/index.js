import { createRouter, createWebHashHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AboutView from '../views/AboutView.vue'
import GoldStandardLearningView from '../views/GoldStandardLearningView.vue'
import AIPatternRecognizerView from '../views/AIPatternRecognizerView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/about',
    name: 'about',
    component: AboutView
  },
  {
    path: '/GSLearning',
    name: 'GSLearning',
    component: GoldStandardLearningView
  },
  {
    path: '/AIPR',
    name: 'AIPR',
    component: AIPatternRecognizerView
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
