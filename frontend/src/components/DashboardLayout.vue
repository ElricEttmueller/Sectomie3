<template>
  <div class="dashboard-container" :style="{ backgroundImage: `url(${currentBackground})` }">
    <div class="overlay">
      <header class="dashboard-header">
        <div class="sect-title">{{ sectName }}</div>
        <div class="header-info">
          <div class="game-date">{{ gameDate }}</div>
          <div class="sect-tier">{{ sectTier }}</div>
        </div>
      </header>
      
      <div class="dashboard-content">
        <aside class="sidebar">
          <div class="sidebar-header">
            <div class="sidebar-title">Sect Management</div>
          </div>
          
          <nav class="sidebar-nav">
            <router-link to="/dashboard" class="nav-item" exact>
              <span class="nav-icon">🏠</span>
              <span class="nav-text">Dashboard</span>
            </router-link>
            <router-link to="/dashboard/disciples" class="nav-item">
              <span class="nav-icon">👤</span>
              <span class="nav-text">Disciples</span>
            </router-link>
            <router-link to="/dashboard/events" class="nav-item">
              <span class="nav-icon">📅</span>
              <span class="nav-text">Events</span>
            </router-link>
            <router-link to="/dashboard/resources" class="nav-item">
              <span class="nav-icon">💎</span>
              <span class="nav-text">Resources</span>
            </router-link>
            <router-link to="/dashboard/knowledge" class="nav-item">
              <span class="nav-icon">📚</span>
              <span class="nav-text">Knowledge</span>
            </router-link>
          </nav>
          
          <div class="sidebar-footer">
            <div class="spirit-stones">
              <span class="stone-icon">💰</span>
              <span class="stone-count">{{ formatNumber(spiritStones) }}</span>
            </div>
            <button class="end-turn-button" @click="endTurn" :disabled="endingTurn">
              {{ endingTurn ? 'Processing...' : 'End Turn' }}
            </button>
          </div>
        </aside>
        
        <main class="main-content">
          <div class="content-container">
            <router-view />
          </div>
        </main>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'DashboardLayout',
  data() {
    return {
      backgrounds: [
        '/assets/backgrounds/mountain.jpg',
        '/assets/backgrounds/temple.jpg',
        '/assets/backgrounds/cloud.jpg'
      ],
      currentBackground: '/assets/backgrounds/mountain.jpg',
      sectName: 'Loading...',
      sectTier: '',
      spiritStones: 0,
      gameDate: 'Year 1, Month 1',
      currentTurn: 1,
      endingTurn: false,
      turnResults: null,
      loading: true,
      error: null
    }
  },
  mounted() {
    // Randomly select a background on load
    this.currentBackground = this.backgrounds[Math.floor(Math.random() * this.backgrounds.length)];
    
    // Fetch player sect data
    this.fetchSectData();
    
    // Fetch game state
    this.fetchGameState();
    
    // Set up interval to refresh data every minute
    this.dataRefreshInterval = setInterval(() => {
      this.fetchSectData();
    }, 60000);
  },
  beforeUnmount() {
    // Clear interval when component is unmounted
    clearInterval(this.dataRefreshInterval);
  },
  methods: {
    async fetchGameState() {
      try {
        const response = await axios.get('http://localhost:5000/api/game-state');
        this.currentTurn = response.data.current_turn;
        this.gameDate = response.data.game_date;
        // Spirit stones are already fetched in fetchSectData
      } catch (err) {
        console.error('Failed to fetch game state:', err);
      }
    },
    
    async endTurn() {
      this.endingTurn = true;
      this.turnResults = null;
      
      try {
        const response = await axios.post('http://localhost:5000/api/end-turn');
        
        // Update game state
        this.currentTurn = response.data.new_turn;
        this.gameDate = response.data.game_date;
        this.turnResults = response.data.results;
        
        // Show results in a modal or notification
        this.showTurnResults();
        
        // Refresh sect data
        await this.fetchSectData();
        
        // Emit event for other components to refresh their data
        this.$root.$emit('turn-ended', this.currentTurn);
      } catch (err) {
        console.error('Failed to end turn:', err);
        alert('Failed to end turn. Please try again.');
      } finally {
        this.endingTurn = false;
      }
    },
    
    showTurnResults() {
      // If there are resource gains, show them
      if (this.turnResults && this.turnResults.resource_income) {
        const spiritStones = this.turnResults.resource_income.spirit_stones;
        if (spiritStones) {
          alert(`Turn completed! You gained ${this.formatNumber(spiritStones)} spirit stones from your spirit veins.`);
        }
      }
      
      // TODO: Show more detailed results in a proper modal
    },
    
    async fetchSectData() {
      try {
        const response = await axios.get('http://localhost:5000/api/player-sect');
        const sect = response.data;
        
        this.sectName = sect.name;
        this.sectTier = `${this.getTierName(sect.tier)} Tier ${sect.dao_heritage} Sect`;
        this.spiritStones = sect.spirit_stones;
        this.loading = false;
      } catch (err) {
        this.error = 'Failed to load sect data';
        this.loading = false;
        console.error(err);
      }
    },
    getTierName(tier) {
      const tiers = [
        "Mortal",
        "Spirit Gathering",
        "Foundation",
        "Core",
        "Nascent",
        "Spirit",
        "Dao",
        "Immortal",
        "Celestial"
      ];
      
      if (tier >= 1 && tier <= tiers.length) {
        return tiers[tier - 1];
      }
      return "Unknown";
    },
    formatNumber(num) {
      return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    }
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Ma+Shan+Zheng&family=Noto+Serif+SC:wght@400;700&display=swap');

.dashboard-container {
  min-height: 100vh;
  height: 100vh; /* Fixed height */
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  position: relative;
}

.overlay {
  min-height: 100vh;
  height: 100vh; /* Fixed height */
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  flex-direction: column;
}

.dashboard-header {
  padding: 0.75rem 2rem;
  background-color: rgba(0, 0, 0, 0.7);
  color: #f8f8f8;
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 60px; /* Fixed height */
}

.sect-title {
  font-family: 'Ma Shan Zheng', cursive;
  font-size: 2rem;
  color: #d4af37;
  text-shadow: 0 0 10px rgba(255, 215, 0, 0.5);
}

.header-info {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.game-date {
  font-size: 0.9rem;
  color: #d4af37;
  margin-bottom: 0.25rem;
}

.sect-tier {
  font-size: 1rem;
  color: #e0e0e0;
}

.dashboard-content {
  flex: 1;
  display: flex;
  height: calc(100vh - 60px); /* Subtract header height */
  overflow: hidden; /* Prevent overall scrolling */
}

.sidebar {
  width: 240px;
  background-color: rgba(42, 107, 93, 0.9);
  color: #f8f8f8;
  display: flex;
  flex-direction: column;
  height: 100%; /* Full height */
}

.sidebar-header {
  padding: 1.25rem 1rem;
  text-align: center;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.sidebar-title {
  font-family: 'Noto Serif SC', serif;
  font-size: 1.2rem;
  color: #d4af37;
}

.sidebar-nav {
  flex: 1;
  padding: 1rem 0;
  overflow-y: auto; /* Scrollable if needed */
}

.nav-item {
  display: flex;
  align-items: center;
  padding: 0.75rem 1.5rem;
  color: #f8f8f8;
  text-decoration: none;
  transition: all 0.3s ease;
}

.nav-item:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.nav-item.router-link-active {
  background-color: rgba(212, 175, 55, 0.3);
  border-left: 4px solid #d4af37;
}

.nav-icon {
  font-size: 1.2rem;
  margin-right: 0.75rem;
}

.sidebar-footer {
  padding: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.spirit-stones {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: rgba(0, 0, 0, 0.3);
  padding: 0.5rem;
  border-radius: 0.25rem;
}

.stone-icon {
  margin-right: 0.5rem;
}

.stone-count {
  font-weight: bold;
  color: #d4af37;
}

.end-turn-button {
  background-color: #d4af37;
  color: #3a2718;
  border: none;
  padding: 0.75rem;
  border-radius: 0.25rem;
  cursor: pointer;
  font-weight: bold;
  transition: all 0.3s ease;
  text-align: center;
}

.end-turn-button:hover:not(:disabled) {
  background-color: #c49b27;
  transform: translateY(-2px);
}

.end-turn-button:disabled {
  background-color: #a58a20;
  opacity: 0.7;
  cursor: not-allowed;
}

.main-content {
  flex: 1;
  height: 100%; /* Full height */
  overflow-y: auto; /* Scrollable content */
  padding: 1.5rem;
  position: relative;
}

.content-container {
  max-width: 1400px; /* Wider content area */
  min-width: 1240px; /* Minimum width to prevent too narrow content */
  margin: 0 auto;
  height: 100%;
  width: 100%; /* Ensure full width */
}

@media (max-width: 1024px) {
  .content-container {
    min-width: auto; /* Remove minimum width on smaller screens */
  }
}

@media (max-width: 768px) {
  .dashboard-content {
    flex-direction: column;
  }
  
  .sidebar {
    width: 100%;
    height: auto;
  }
  
  .sidebar-nav {
    display: flex;
    overflow-x: auto;
    padding: 0.5rem;
  }
  
  .nav-item {
    flex-direction: column;
    padding: 0.5rem;
  }
  
  .nav-icon {
    margin-right: 0;
    margin-bottom: 0.25rem;
  }
}
</style>
