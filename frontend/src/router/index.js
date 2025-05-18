import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import SectDetail from '../views/SectDetail.vue'
import DiscipleDetail from '../views/DiscipleDetail.vue'
import Cultivation from '../views/Cultivation.vue'

// Dashboard components
import DashboardLayout from '../components/DashboardLayout.vue'
import SectDashboard from '../views/SectDashboard.vue'
import DisciplesPage from '../views/DisciplesPage.vue'
import EventsPage from '../views/EventsPage.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/sect/:id',
    name: 'SectDetail',
    component: SectDetail,
    props: true
  },
  {
    path: '/disciple/:id',
    name: 'DiscipleDetail',
    component: DiscipleDetail,
    props: true
  },
  {
    path: '/cultivation/:id',
    name: 'Cultivation',
    component: Cultivation,
    props: true
  },
  
  // Dashboard routes
  {
    path: '/dashboard',
    component: DashboardLayout,
    children: [
      {
        path: '',
        name: 'SectDashboard',
        component: SectDashboard
      },
      {
        path: 'disciples',
        name: 'DisciplesPage',
        component: DisciplesPage
      },
      {
        path: 'disciples/:id',
        name: 'DashboardDiscipleDetail',
        component: DiscipleDetail,
        props: true
      },
      {
        path: 'events',
        name: 'EventsPage',
        component: EventsPage
      },
      {
        path: 'resources',
        name: 'ResourcesPage',
        component: EventsPage, // Temporarily using EventsPage as placeholder
        meta: { underConstruction: true }
      },
      {
        path: 'knowledge',
        name: 'KnowledgePage',
        component: EventsPage, // Temporarily using EventsPage as placeholder
        meta: { underConstruction: true }
      },
      {
        path: 'cultivation/:id',
        name: 'DashboardCultivation',
        component: Cultivation,
        props: true
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
