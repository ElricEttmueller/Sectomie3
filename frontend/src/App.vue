<template>
  <div class="app-container" :style="{ backgroundImage: `url(${currentBackground})` }">
    <div class="overlay">
      <!-- Header Bar with Sect Emblem and Game Info -->
      <header class="app-header">
        <div class="sect-emblem">
          <h1 class="app-title">Sectomie</h1>
          <div class="cultivation-world">Cultivation Sect Management</div>
        </div>
        <div class="game-info">
          <div class="game-date">Year {{ gameYear }}, Month {{ gameMonth }}</div>
          <div class="turn-counter">Turn {{ gameTurn }}</div>
          <div class="resources-dashboard">
            <div class="resource">
              <i class="fa fa-gem"></i>
              <span>{{ spiritStones }}</span>
            </div>
            <div class="resource">
              <i class="fa fa-leaf"></i>
              <span>{{ herbs }}</span>
            </div>
            <div class="resource">
              <i class="fa fa-scroll"></i>
              <span>{{ treasures }}</span>
            </div>
          </div>
        </div>
      </header>
      
      <!-- Main Navigation Tabs -->
      <nav class="main-nav">
        <router-link to="/" class="nav-item">
          <i class="fa fa-home nav-icon"></i>
          <span class="nav-text">Home</span>
        </router-link>
        <router-link to="/sect" class="nav-item">
          <i class="fa fa-mountain nav-icon"></i>
          <span class="nav-text">Sect</span>
        </router-link>
        <router-link to="/disciples" class="nav-item">
          <i class="fa fa-user nav-icon"></i>
          <span class="nav-text">Disciples</span>
        </router-link>
        <router-link to="/cultivation" class="nav-item">
          <i class="fa fa-fire nav-icon"></i>
          <span class="nav-text">Cultivation</span>
        </router-link>
        <router-link to="/territories" class="nav-item">
          <i class="fa fa-map nav-icon"></i>
          <span class="nav-text">Territories</span>
        </router-link>
        <router-link to="/events" class="nav-item">
          <i class="fa fa-bolt nav-icon"></i>
          <span class="nav-text">Events</span>
        </router-link>
        <router-link to="/logs" class="nav-item">
          <i class="fa fa-book nav-icon"></i>
          <span class="nav-text">Logs</span>
        </router-link>
        <router-link to="/testingdb" class="nav-item">
          <i class="fa fa-vial nav-icon"></i>
          <span class="nav-text">Testing</span>
        </router-link>
      </nav>
      
      <!-- Main Content with Sidebar and Content Area -->
      <div class="content-wrapper">
        <aside class="sidebar-navigation" v-if="!hideSidebar">
          <div class="sidebar-section" v-for="(section, index) in sidebarSections" :key="index">
            <h3 class="sidebar-title">{{ section.title }}</h3>
            <ul class="sidebar-items">
              <li v-for="(item, itemIndex) in section.items" :key="itemIndex" class="sidebar-item">
                {{ item }}
              </li>
            </ul>
          </div>
        </aside>
        
        <main class="main-content">
          <router-view/>
        </main>
      </div>
      
      <!-- Status Bar -->
      <footer class="status-bar">
        <div class="notifications">
          <i class="fa fa-bell"></i>
          <span>{{ notifications.length }} Notifications</span>
        </div>
        
        <div class="quick-actions">
          <button class="action-button" v-for="(action, index) in quickActions" :key="index">
            <i :class="`fa ${action.icon}`"></i>
            {{ action.label }}
          </button>
        </div>
        
        <div class="end-turn">
          <button class="end-turn-button" @click="endTurn">
            <i class="fa fa-forward"></i>
            End Turn
          </button>
        </div>
      </footer>
    </div>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      // Background settings
      backgrounds: [
        '/assets/backgrounds/mountain.jpg',
        '/assets/backgrounds/temple.jpg',
        '/assets/backgrounds/cloud.jpg',
        require('@/assets/backgrounds/Landscape01.png')
      ],
      currentBackground: require('@/assets/backgrounds/Landscape01.png'),
      
      // Game state
      gameYear: 1,
      gameMonth: 1,
      gameTurn: 1,
      
      // Resources
      spiritStones: 1000,
      herbs: 50,
      treasures: 3,
      
      // Sidebar settings
      hideSidebar: false,
      sidebarSections: [
        {
          title: 'Quick Actions',
          items: ['Cultivate Disciples', 'Manage Resources', 'Explore Territory']
        },
        {
          title: 'Sect Status',
          items: ['Reputation: Rising', 'Territory: 3 Areas', 'Members: 5 Disciples']
        },
        {
          title: 'Current Tasks',
          items: ['Recruit New Disciples', 'Expand Territory', 'Research Cultivation Methods']
        }
      ],
      
      // Status bar
      notifications: [
        { id: 1, message: 'Disciple Li Mei is approaching breakthrough' },
        { id: 2, message: 'New cultivation method discovered' }
      ],
      quickActions: [
        { icon: 'fa-user-plus', label: 'Recruit' },
        { icon: 'fa-search', label: 'Explore' },
        { icon: 'fa-book-open', label: 'Research' }
      ]
    }
  },
  methods: {
    endTurn() {
      // Placeholder for end turn functionality
      this.gameTurn++;
      if (this.gameMonth < 12) {
        this.gameMonth++;
      } else {
        this.gameMonth = 1;
        this.gameYear++;
      }
      
      // Add a notification for demonstration
      this.notifications.push({
        id: this.notifications.length + 1,
        message: `Turn ${this.gameTurn} completed. Resources updated.`
      });
      
      // Update resources for demonstration
      this.spiritStones += 100;
      this.herbs += 5;
      
      // Alert the user
      alert(`Turn ${this.gameTurn} completed. New date: Year ${this.gameYear}, Month ${this.gameMonth}`);
    },
    
    toggleSidebar() {
      this.hideSidebar = !this.hideSidebar;
    },
    
    updateSidebarContent(route) {
      // Update sidebar content based on current route
      console.log(`Updating sidebar for route: ${route}`);
      
      // Default sidebar content
      let sections = [
        {
          title: 'Quick Actions',
          items: ['Cultivate Disciples', 'Manage Resources', 'Explore Territory']
        },
        {
          title: 'Sect Status',
          items: ['Reputation: Rising', 'Territory: 3 Areas', 'Members: 5 Disciples']
        }
      ];
      
      // Route-specific sidebar content
      if (route.includes('/sect')) {
        sections = [
          {
            title: 'Sect Management',
            items: ['Upgrade Facilities', 'Manage Resources', 'Sect Policies']
          },
          {
            title: 'Sect Facilities',
            items: ['Main Hall (Level 3)', 'Cultivation Chamber (Level 2)', 'Alchemy Lab (Level 1)', 'Spirit Garden (Level 2)']
          },
          {
            title: 'Sect Status',
            items: ['Reputation: Rising', 'Territory: 3 Areas', 'Members: 5 Disciples']
          }
        ];
      } else if (route.includes('/disciples')) {
        sections = [
          {
            title: 'Disciple Management',
            items: ['Recruit New Disciples', 'Assign Tasks', 'Group Cultivation']
          },
          {
            title: 'Disciple Categories',
            items: ['Inner Disciples', 'Outer Disciples', 'Core Disciples', 'Elders']
          },
          {
            title: 'Disciple Status',
            items: ['Total: 5 Disciples', 'Cultivating: 3', 'On Tasks: 1', 'Idle: 1']
          }
        ];
      } else if (route.includes('/cultivation')) {
        sections = [
          {
            title: 'Cultivation Methods',
            items: ['Azure Flame Refinement', 'Water Ripple Meditation', 'Mountain Heart Stance', 'Wind Walking Method', 'Thunder Essence Gathering']
          },
          {
            title: 'Resource Allocation',
            items: ['Spirit Stones: 1000', 'Allocated: 550', 'Remaining: 450']
          },
          {
            title: 'Cultivation Stats',
            items: ['Sect Bonus: +15%', 'Breakthrough Rate: Average', 'Efficiency: Good']
          }
        ];
      } else if (route.includes('/territories')) {
        sections = [
          {
            title: 'Territories',
            items: ['Azure Peak', 'Mystic Cloud', 'Verdant Valley']
          },
          {
            title: 'Resource Nodes',
            items: ['Spirit Stone Veins: 3', 'Herb Gardens: 2', 'Special Locations: 3']
          },
          {
            title: 'Territory Actions',
            items: ['Explore New Areas', 'Defend Borders', 'Harvest Resources']
          }
        ];
      } else if (route.includes('/events')) {
        sections = [
          {
            title: 'Active Events',
            items: ['Spirit Stone Vein Dispute', 'Mysterious Herb Discovery', 'Demonic Beast Incursion']
          },
          {
            title: 'Upcoming Events',
            items: ['Immortal Ascension Conference', 'Heavenly Tribulation']
          },
          {
            title: 'Event Actions',
            items: ['Make Decisions', 'Assign Disciples', 'Prepare Defenses']
          }
        ];
      } else if (route.includes('/logs')) {
        sections = [
          {
            title: 'Chronicle Categories',
            items: ['Sect Development', 'Disciple Progress', 'Battles & Conflicts', 'Discoveries']
          },
          {
            title: 'Notable Events',
            items: ['Sect Founding', 'First Territory Expansion', 'Azure Flame Method Acquisition']
          },
          {
            title: 'Time Periods',
            items: ['Current Year', 'Current Month', 'All History']
          }
        ];
      }
      
      this.sidebarSections = sections;
    }
  },
  mounted() {
    // Always use Landscape01.png as the background
    this.currentBackground = require('@/assets/backgrounds/Landscape01.png');
    
    // Update sidebar based on initial route
    this.updateSidebarContent(this.$route.path);
  },
  watch: {
    // Watch for route changes to update sidebar content
    '$route'(to) {
      this.updateSidebarContent(to.path);
    }
  }
}
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Ma+Shan+Zheng&family=Noto+Serif+SC:wght@400;700&display=swap');

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Noto Serif SC', serif;
  color: #333;
  line-height: 1.6;
}

.app-container {
  min-height: 100vh;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  position: relative;
}

.overlay {
  min-height: 100vh;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  flex-direction: column;
}

/* Header Styles */
.app-header {
  padding: 1rem 2rem;
  color: #f8f8f8;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 2px solid #d4af37;
}

.sect-emblem {
  text-align: center;
}

.app-title {
  font-family: 'Ma Shan Zheng', cursive;
  font-size: 2.5rem;
  margin-bottom: 0.25rem;
  text-shadow: 0 0 10px rgba(255, 215, 0, 0.7);
  color: #ffd700;
}

.cultivation-world {
  font-size: 1rem;
  color: #e0e0e0;
}

.game-info {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.game-date, .turn-counter {
  font-size: 1rem;
  color: #e0e0e0;
}

.resources-dashboard {
  display: flex;
  gap: 1rem;
}

.resource {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background-color: rgba(212, 175, 55, 0.2);
  padding: 0.5rem 1rem;
  border-radius: 0.25rem;
  color: #d4af37;
}

/* Navigation Styles */
.main-nav {
  display: flex;
  justify-content: center;
  padding: 0.75rem;
  background-color: rgba(0, 0, 0, 0.7);
  border-bottom: 1px solid rgba(212, 175, 55, 0.3);
}

.nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 0.5rem 1rem;
  color: #d4af37;
  text-decoration: none;
  border-radius: 0.25rem;
  transition: all 0.3s ease;
  margin: 0 0.5rem;
}

.nav-item:hover {
  background-color: rgba(212, 175, 55, 0.2);
  transform: translateY(-2px);
}

.router-link-active {
  background-color: rgba(212, 175, 55, 0.3);
  border-bottom: 2px solid #d4af37;
}

.nav-icon {
  font-size: 1.25rem;
  margin-bottom: 0.25rem;
}

.nav-text {
  font-size: 0.75rem;
}

/* Content Layout */
.content-wrapper {
  display: flex;
  flex: 1;
  background-color: rgba(0, 0, 0, 0.3);
}

.sidebar-navigation {
  width: 250px;
  background-color: rgba(0, 0, 0, 0.6);
  color: #e0e0e0;
  padding: 1rem;
  border-right: 1px solid rgba(212, 175, 55, 0.3);
  overflow-y: auto;
}

.sidebar-section {
  margin-bottom: 1.5rem;
}

.sidebar-title {
  font-size: 1rem;
  color: #d4af37;
  margin-bottom: 0.75rem;
  padding-bottom: 0.25rem;
  border-bottom: 1px solid rgba(212, 175, 55, 0.3);
}

.sidebar-items {
  list-style: none;
}

.sidebar-item {
  padding: 0.5rem 0;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.sidebar-item:hover {
  color: #d4af37;
  padding-left: 0.5rem;
}

.main-content {
  flex: 1;
  padding: 1.5rem;
  overflow-y: auto;
  display: flex;
  justify-content: center;
}

/* Status Bar */
.status-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 2rem;
  background-color: rgba(0, 0, 0, 0.7);
  color: #e0e0e0;
  border-top: 1px solid rgba(212, 175, 55, 0.3);
}

.notifications {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.quick-actions {
  display: flex;
  gap: 1rem;
}

.action-button {
  background-color: rgba(212, 175, 55, 0.2);
  border: 1px solid rgba(212, 175, 55, 0.5);
  color: #d4af37;
  padding: 0.5rem 1rem;
  border-radius: 0.25rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.2s ease;
}

.action-button:hover {
  background-color: rgba(212, 175, 55, 0.3);
}

.end-turn-button {
  background-color: #d4af37;
  color: #000;
  padding: 0.5rem 1.5rem;
  border: none;
  border-radius: 0.25rem;
  cursor: pointer;
  font-weight: bold;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.2s ease;
}

.end-turn-button:hover {
  background-color: #ffd700;
  transform: translateY(-2px);
}

/* For router transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Responsive Design */
@media (max-width: 1200px) {
  .app-header {
    flex-direction: column;
    gap: 1rem;
  }
  
  .game-info {
    flex-direction: column;
    gap: 0.5rem;
  }
}

@media (max-width: 992px) {
  .content-wrapper {
    flex-direction: column;
  }
  
  .sidebar-navigation {
    width: 100%;
    border-right: none;
    border-bottom: 1px solid rgba(212, 175, 55, 0.3);
  }
}

@media (max-width: 768px) {
  .main-nav {
    flex-wrap: wrap;
  }
  
  .status-bar {
    flex-direction: column;
    gap: 1rem;
  }
}
</style>
