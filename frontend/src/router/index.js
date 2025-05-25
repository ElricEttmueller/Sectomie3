import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import SectDetail from '../views/SectDetail.vue'
import DiscipleDetail from '../views/DiscipleDetail.vue'
import Cultivation from '../views/Cultivation.vue'
import TestingDB from '../views/TestingDB.vue'

// Main views for new navigation
import SectView from '../views/SectView.vue'
import DisciplesView from '../views/DisciplesView.vue'
import CultivationView from '../views/CultivationView.vue'
import TerritoriesView from '../views/TerritoriesView.vue'
import EventsView from '../views/EventsView.vue'
import LogsView from '../views/LogsView.vue'

// Dashboard components (legacy)
import DashboardLayout from '../components/DashboardLayout.vue'
import SectDashboard from '../views/SectDashboard.vue'
import DisciplesPage from '../views/DisciplesPage.vue'
import EventsPage from '../views/EventsPage.vue'

const routes = [
  // Main navigation routes
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/sect',
    name: 'SectView',
    component: SectView
  },
  {
    path: '/sect/:id',
    name: 'SectDetail',
    component: SectDetail,
    props: true
  },
  {
    path: '/disciples',
    name: 'DisciplesView',
    component: DisciplesView
  },
  {
    path: '/disciple/:id',
    name: 'DiscipleDetail',
    component: DiscipleDetail,
    props: true
  },
  {
    path: '/cultivation',
    name: 'CultivationView',
    component: CultivationView
  },
  {
    path: '/cultivation/:id',
    name: 'Cultivation',
    redirect: to => {
      return { path: `/disciple/${to.params.id}`, query: { showCultivationAssignment: 'true' } }
    }
  },
  {
    path: '/territories',
    name: 'TerritoriesView',
    component: TerritoriesView
  },
  {
    path: '/events',
    name: 'EventsView',
    component: EventsView
  },
  {
    path: '/logs',
    name: 'LogsView',
    component: LogsView
  },
  {
    path: '/testingdb',
    name: 'TestingDB',
    component: TestingDB
  },
  
  // Legacy Dashboard routes
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
        redirect: to => {
          return { path: `/dashboard/disciples/${to.params.id}`, query: { showCultivationAssignment: 'true' } }
        }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
