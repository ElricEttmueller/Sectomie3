<template>
  <div class="disciples-view">
    <div class="page-header">
      <h1>Disciples Management</h1>
      <p>View and manage your sect's disciples</p>
    </div>
    
    <div class="disciples-content">
      <div class="disciples-stats">
        <div class="stat-card">
          <div class="stat-title">Total Disciples</div>
          <div class="stat-value">{{ disciples.length }}</div>
        </div>
        <div class="stat-card">
          <div class="stat-title">Average Cultivation</div>
          <div class="stat-value">{{ averageCultivation }}</div>
        </div>
        <div class="stat-card">
          <div class="stat-title">Highest Realm</div>
          <div class="stat-value">{{ highestRealm }}</div>
        </div>
        <div class="stat-card">
          <div class="stat-title">Recruitment Capacity</div>
          <div class="stat-value">{{ recruitmentCapacity }}</div>
        </div>
      </div>
      
      <div class="disciples-actions">
        <button class="action-button">
          <i class="fa fa-user-plus"></i>
          Recruit Disciple
        </button>
        <button class="action-button">
          <i class="fa fa-users-cog"></i>
          Assign Tasks
        </button>
        <button class="action-button">
          <i class="fa fa-fire"></i>
          Group Cultivation
        </button>
        <div class="search-container">
          <input type="text" v-model="searchQuery" placeholder="Search disciples..." class="search-input">
          <i class="fa fa-search search-icon"></i>
        </div>
      </div>
      
      <div class="disciples-list">
        <div class="list-header">
          <div class="header-name">Name</div>
          <div class="header-realm">Cultivation</div>
          <div class="header-stats">Attributes</div>
          <div class="header-status">Status</div>
          <div class="header-actions">Actions</div>
        </div>
        
        <div v-for="disciple in filteredDisciples" :key="disciple.id" class="disciple-row" @click="viewDisciple(disciple.id)">
          <div class="disciple-name">
            <div class="name">{{ disciple.name }}</div>
            <div class="path">{{ disciple.path }} Path</div>
          </div>
          <div class="disciple-realm">
            <div class="realm">{{ disciple.realm_name }}</div>
            <div class="stage">{{ disciple.stage_name }}</div>
            <div class="qi-bar">
              <div class="qi-fill" :style="{ width: `${(disciple.qi / disciple.max_qi) * 100}%` }"></div>
            </div>
          </div>
          <div class="disciple-stats">
            <div class="attribute">
              <span class="attribute-label">PHY</span>
              <span class="attribute-value">{{ disciple.physical }}</span>
            </div>
            <div class="attribute">
              <span class="attribute-label">SPR</span>
              <span class="attribute-value">{{ disciple.spiritual }}</span>
            </div>
            <div class="attribute">
              <span class="attribute-label">COM</span>
              <span class="attribute-value">{{ disciple.comprehension }}</span>
            </div>
          </div>
          <div class="disciple-status">
            <div class="status" :class="disciple.status ? disciple.status.toLowerCase() : 'normal'">{{ disciple.status || 'Normal' }}</div>
            <div class="activity">{{ disciple.activity || 'Cultivating' }}</div>
          </div>
          <div class="disciple-actions">
            <router-link :to="`/disciple/${disciple.id}`" class="detail-button">
              <i class="fa fa-user"></i>
              Details
            </router-link>
            <router-link :to="`/cultivation/${disciple.id}`" class="cultivation-button">
              <i class="fa fa-fire"></i>
              Cultivate
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { EventBus } from '@/services/eventBus.js';

export default {
  name: 'DisciplesView',
  data() {
    return {
      searchQuery: '',
      disciples: [],
      loading: true,
      error: null,
      recruitmentCapacityValue: 3
    };
  },
  mounted() {
    this.fetchDisciples();
    // Listen for turn-ended event
    EventBus.$on('turn-ended', this.handleTurnEnded);
  },
  beforeDestroy() {
    // Clean up event listener
    EventBus.$off('turn-ended', this.handleTurnEnded);
  },
  methods: {
    async fetchDisciples() {
      this.loading = true;
      try {
        const response = await axios.get('http://localhost:5000/api/disciples');
        this.disciples = response.data;
        this.loading = false;
      } catch (err) {
        console.error('Failed to fetch disciples:', err);
        this.error = 'Failed to load disciples data';
        this.loading = false;
      }
    },
    handleTurnEnded(turnData) {
      console.log('Turn ended event received in DisciplesView:', turnData);
      this.fetchDisciples();
    },
    viewDisciple(id) {
      this.$router.push(`/dashboard/disciples/${id}`);
    }
  },
  computed: {
    filteredDisciples() {
      if (!this.searchQuery) return this.disciples;
      
      const query = this.searchQuery.toLowerCase();
      return this.disciples.filter(disciple => {
        return disciple.name.toLowerCase().includes(query) || 
               (disciple.path && disciple.path.toLowerCase().includes(query)) ||
               (disciple.realm_name && disciple.realm_name.toLowerCase().includes(query)) ||
               (disciple.status && disciple.status.toLowerCase().includes(query));
      });
    },
    averageCultivation() {
      if (this.disciples.length === 0) return 'None';
      
      // Count occurrences of each realm
      const realmCounts = {};
      this.disciples.forEach(disciple => {
        if (!realmCounts[disciple.realm_name]) {
          realmCounts[disciple.realm_name] = 0;
        }
        realmCounts[disciple.realm_name]++;
      });
      
      // Find the most common realm
      let mostCommonRealm = 'None';
      let highestCount = 0;
      
      for (const realm in realmCounts) {
        if (realmCounts[realm] > highestCount) {
          mostCommonRealm = realm;
          highestCount = realmCounts[realm];
        }
      }
      
      return mostCommonRealm;
    },
    highestRealm() {
      if (this.disciples.length === 0) return 'None';
      
      // Realm hierarchy (simplified)
      const realmOrder = [
        'Mortal',
        'Qi Condensation',
        'Foundation Establishment',
        'Core Formation',
        'Nascent Soul',
        'Divine Sense',
        'Immortal Ascension'
      ];
      
      let highestRealmIndex = -1;
      
      this.disciples.forEach(disciple => {
        const realmIndex = realmOrder.indexOf(disciple.realm_name);
        if (realmIndex > highestRealmIndex) {
          highestRealmIndex = realmIndex;
        }
      });
      
      return highestRealmIndex >= 0 ? realmOrder[highestRealmIndex] : 'None';
    },
    recruitmentCapacity() {
      return `${this.recruitmentCapacityValue} / 10`;
    }
  }
};

</script>

<style scoped>
.disciples-view {
  width: 100%;
  max-width: 1200px;
}

.page-header {
  margin-bottom: 2rem;
  color: #d4af37;
}

.page-header h1 {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.page-header p {
  color: #e0e0e0;
}

.disciples-content {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.disciples-stats {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1rem;
}

.stat-card {
  background-color: rgba(0, 0, 0, 0.5);
  border: 1px solid rgba(212, 175, 55, 0.3);
  border-radius: 0.5rem;
  padding: 1rem;
  text-align: center;
}

.stat-title {
  color: #a0a0a0;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}

.stat-value {
  color: #d4af37;
  font-size: 1.5rem;
}

.disciples-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  align-items: center;
  background-color: rgba(0, 0, 0, 0.5);
  border: 1px solid rgba(212, 175, 55, 0.3);
  border-radius: 0.5rem;
  padding: 1rem;
}

.action-button {
  background-color: rgba(212, 175, 55, 0.2);
  border: 1px solid rgba(212, 175, 55, 0.5);
  color: #d4af37;
  padding: 0.75rem 1.25rem;
  border-radius: 0.25rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.2s ease;
}

.action-button:hover {
  background-color: rgba(212, 175, 55, 0.3);
  transform: translateY(-2px);
}

.search-container {
  position: relative;
  margin-left: auto;
}

.search-input {
  background-color: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(212, 175, 55, 0.3);
  color: #e0e0e0;
  padding: 0.75rem 1rem 0.75rem 2.5rem;
  border-radius: 0.25rem;
  width: 250px;
}

.search-icon {
  position: absolute;
  left: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  color: #a0a0a0;
}

.disciples-list {
  background-color: rgba(0, 0, 0, 0.5);
  border: 1px solid rgba(212, 175, 55, 0.3);
  border-radius: 0.5rem;
  overflow: hidden;
}

.list-header {
  display: grid;
  grid-template-columns: 2fr 2fr 2fr 2fr 2fr;
  padding: 1rem;
  background-color: rgba(0, 0, 0, 0.3);
  color: #d4af37;
  font-weight: bold;
  border-bottom: 1px solid rgba(212, 175, 55, 0.3);
}

.disciple-row {
  display: grid;
  grid-template-columns: 2fr 2fr 2fr 2fr 2fr;
  padding: 1rem;
  border-bottom: 1px solid rgba(0, 0, 0, 0.3);
  transition: all 0.2s ease;
  color: #e0e0e0;
}

.disciple-row:hover {
  background-color: rgba(212, 175, 55, 0.1);
}

.disciple-row:last-child {
  border-bottom: none;
}

.disciple-name .name {
  color: #d4af37;
  font-weight: bold;
  margin-bottom: 0.25rem;
}

.disciple-name .path {
  font-size: 0.8rem;
  color: #a0a0a0;
}

.disciple-realm .realm {
  margin-bottom: 0.25rem;
}

.disciple-realm .stage {
  font-size: 0.8rem;
  color: #a0a0a0;
  margin-bottom: 0.5rem;
}

.qi-bar {
  height: 0.5rem;
  background-color: rgba(0, 0, 0, 0.3);
  border-radius: 0.25rem;
  overflow: hidden;
}

.qi-fill {
  height: 100%;
  background-color: #4a90e2;
  border-radius: 0.25rem;
}

.disciple-stats {
  display: flex;
  gap: 1rem;
}

.attribute {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.attribute-label {
  font-size: 0.7rem;
  color: #a0a0a0;
}

.attribute-value {
  font-weight: bold;
}

.disciple-status .status {
  margin-bottom: 0.25rem;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  display: inline-block;
  font-size: 0.8rem;
}

.status.normal {
  background-color: rgba(0, 128, 0, 0.2);
  color: #90ee90;
}

.status.breakthrough {
  background-color: rgba(255, 215, 0, 0.2);
  color: #ffd700;
}

.status.injured {
  background-color: rgba(255, 0, 0, 0.2);
  color: #ff6b6b;
}

.disciple-status .activity {
  font-size: 0.8rem;
  color: #a0a0a0;
}

.disciple-actions {
  display: flex;
  gap: 0.5rem;
}

.detail-button, .cultivation-button {
  background-color: rgba(212, 175, 55, 0.2);
  border: 1px solid rgba(212, 175, 55, 0.5);
  color: #d4af37;
  padding: 0.5rem;
  border-radius: 0.25rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.8rem;
  text-decoration: none;
  transition: all 0.2s ease;
}

.detail-button:hover, .cultivation-button:hover {
  background-color: rgba(212, 175, 55, 0.3);
}

@media (max-width: 992px) {
  .list-header, .disciple-row {
    grid-template-columns: 2fr 2fr 2fr 2fr;
  }
  
  .header-actions, .disciple-actions {
    display: none;
  }
}

@media (max-width: 768px) {
  .list-header, .disciple-row {
    grid-template-columns: 1fr 1fr;
  }
  
  .header-stats, .disciple-stats,
  .header-status, .disciple-status {
    display: none;
  }
  
  .disciples-actions {
    flex-direction: column;
    align-items: stretch;
  }
  
  .search-container {
    margin-left: 0;
    width: 100%;
  }
  
  .search-input {
    width: 100%;
  }
}
</style>
