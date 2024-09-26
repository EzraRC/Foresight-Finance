import { createRouter, createWebHashHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import GoldStandardLearningView from '../views/GoldStandardLearningView.vue';
import AIPatternRecognizerView from '../views/AIPatternRecognizerView.vue';
import LogInSignUpView from '@/views/LogInSignUpView.vue';
import LearningView from '@/views/LearningView.vue';

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
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
  },
  {
    path: '/LoginSignUp',
    name: 'LogInSignUp',
    component: LogInSignUpView
  }, 
  {
    path: '/Learning/:lessonID',
    name: 'LearningView',
    component: LearningView,
    props: true
  }
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    return { top: 0 }; // Always scroll to top
  }
});

export default router;
