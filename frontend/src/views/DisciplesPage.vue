<template>
  <div class="disciples-page">
    <div class="disciples-header">
      <h1 class="page-title">Sect Disciples</h1>
      <div class="header-actions">
        <div class="search-box">
          <input type="text" v-model="searchQuery" placeholder="Search disciples..." class="search-input">
        </div>
        <div class="filter-box">
          <select v-model="realmFilter" class="filter-select">
            <option value="">All Realms</option>
            <option value="Mortal">Mortal</option>
            <option value="Qi Condensation">Qi Condensation</option>
            <option value="Foundation Establishment">Foundation Establishment</option>
            <option value="Core Formation">Core Formation</option>
            <option value="Nascent Soul">Nascent Soul</option>
          </select>
        </div>
      </div>
    </div>
    
    <div class="dashboard-grid">
      <!-- Disciples List Widget -->
      <div class="dashboard-widget disciples-list">
        <div class="widget-header">
          <h2 class="widget-title">Disciples Directory</h2>
        </div>
        <div class="widget-content">
          <div v-if="loading" class="loading">Loading disciples information...</div>
          <div v-else-if="error" class="error">{{ error }}</div>
          <div v-else>
            <div v-if="filteredDisciples.length === 0" class="empty-message">
              No disciples found matching your criteria.
            </div>
            <div v-else class="disciples-grid">
              <div v-for="disciple in filteredDisciples" :key="disciple.id" class="disciple-card" @click="viewDisciple(disciple.id)">
                <div class="disciple-header">
                  <h3 class="disciple-name">{{ disciple.name }}</h3>
                  <div class="disciple-path">{{ disciple.path }} Path</div>
                </div>
                <div class="disciple-realm">{{ disciple.stage }} {{ disciple.realm }}</div>
                <div class="disciple-stats">
                  <div class="disciple-age">Age: {{ disciple.age }}</div>
                  <div class="disciple-power">Power: {{ formatNumber(disciple.combat_power) }}</div>
                </div>
                <div class="card-actions">
                  <button class="action-button" @click.stop="navigateToCultivation(disciple.id)">Cultivate</button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Disciples by Realm Widget -->
      <div class="dashboard-widget realm-stats">
        <div class="widget-header">
          <h2 class="widget-title">Disciples by Realm</h2>
        </div>
        <div class="widget-content">
          <div v-if="loading" class="loading">Loading disciples information...</div>
          <div v-else-if="error" class="error">{{ error }}</div>
          <div v-else>
            <div class="realm-distribution">
              <div v-for="(count, realm) in realmDistribution" :key="realm" class="realm-item">
                <div class="realm-name">{{ realm }}</div>
                <div class="realm-count">{{ count }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Cultivation Paths Widget -->
      <div class="dashboard-widget path-stats">
        <div class="widget-header">
          <h2 class="widget-title">Cultivation Paths</h2>
        </div>
        <div class="widget-content">
          <div v-if="loading" class="loading">Loading disciples information...</div>
          <div v-else-if="error" class="error">{{ error }}</div>
          <div v-else>
            <div class="path-distribution">
              <div v-for="(count, path) in pathDistribution" :key="path" class="path-item">
                <div class="path-name">{{ path }}</div>
                <div class="path-count">{{ count }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Disciple Actions Widget -->
      <div class="dashboard-widget disciple-actions">
        <div class="widget-header">
          <h2 class="widget-title">Sect Management</h2>
        </div>
        <div class="widget-content">
          <div class="action-buttons">
            <button class="sect-action-button" @click="openRecruitmentModal">
              <div class="action-icon">👤</div>
              <div class="action-text">
                <div class="action-title">Recruit Disciples</div>
                <div class="action-desc">Find new talents for your sect</div>
              </div>
            </button>
            
            <button class="sect-action-button" disabled>
              <div class="action-icon">📚</div>
              <div class="action-text">
                <div class="action-title">Train Disciples</div>
                <div class="action-desc">Group training session (coming soon)</div>
              </div>
            </button>
            
            <button class="sect-action-button" disabled>
              <div class="action-icon">🏆</div>
              <div class="action-text">
                <div class="action-title">Sect Competition</div>
                <div class="action-desc">Hold internal competitions (coming soon)</div>
              </div>
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Recruitment Modal -->
    <recruitment-modal 
      :show="showRecruitmentModal" 
      :spirit-stones="spiritStones" 
      @close="closeRecruitmentModal"
      @disciple-recruited="handleDiscipleRecruitment"
    />
  </div>
</template>

<script>
import axios from 'axios';
import RecruitmentModal from '@/components/RecruitmentModal.vue';

export default {
  name: 'DisciplesPage',
  components: {
    RecruitmentModal
  },
  data() {
    return {
      disciples: [],
      loading: true,
      error: null,
      searchQuery: '',
      realmFilter: '',
      showRecruitmentModal: false,
      spiritStones: 0
    }
  },
  computed: {
    filteredDisciples() {
      return this.disciples.filter(disciple => {
        // Apply search filter
        const matchesSearch = this.searchQuery === '' || 
          disciple.name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          disciple.path.toLowerCase().includes(this.searchQuery.toLowerCase());
        
        // Apply realm filter
        const matchesRealm = this.realmFilter === '' || disciple.realm === this.realmFilter;
        
        return matchesSearch && matchesRealm;
      });
    },
    realmDistribution() {
      const distribution = {};
      this.disciples.forEach(disciple => {
        if (!distribution[disciple.realm]) {
          distribution[disciple.realm] = 0;
        }
        distribution[disciple.realm]++;
      });
      return distribution;
    },
    pathDistribution() {
      const distribution = {};
      this.disciples.forEach(disciple => {
        if (!distribution[disciple.path]) {
          distribution[disciple.path] = 0;
        }
        distribution[disciple.path]++;
      });
      return distribution;
    }
  },
  mounted() {
    this.fetchDisciplesData();
    this.fetchSpiritStones();
  },
  methods: {
    openRecruitmentModal() {
      this.showRecruitmentModal = true;
    },
    
    closeRecruitmentModal() {
      this.showRecruitmentModal = false;
    },
    
    async handleDiscipleRecruitment(event) {
      if (event.success) {
        // Refresh disciples list and spirit stones
        await this.fetchDisciplesData();
        await this.fetchSpiritStones();
        
        // Show success message
        alert(`Successfully recruited ${event.disciple.name} to your sect!`);
      }
    },
    
    async fetchSpiritStones() {
      try {
        const response = await axios.get('http://localhost:5000/api/player-sect');
        this.spiritStones = response.data.spirit_stones;
      } catch (err) {
        console.error('Failed to fetch spirit stones:', err);
      }
    },
    
    async fetchDisciplesData() {
      try {
        const response = await axios.get('http://localhost:5000/api/player-sect/disciples');
        this.disciples = response.data;
        this.loading = false;
      } catch (err) {
        this.error = 'Failed to load disciples data';
        this.loading = false;
        console.error(err);
      }
    },
    viewDisciple(id) {
      this.$router.push(`/dashboard/disciples/${id}`);
    },
    navigateToCultivation(id) {
      this.$router.push(`/dashboard/cultivation/${id}`);
    },
    formatNumber(num) {
      return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    }
  }
}
</script>

<style scoped>
.disciples-page {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

  .page-title {
    color: #f8f8f8;
    font-size: 1.8rem;
    margin: 0;
    text-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
  }

  .header-actions {
    display: flex;
    gap: 0.75rem;
    align-items: center;
  }

  .search-input, .filter-select {
    padding: 0.5rem;
    border: 1px solid #d4af37;
    border-radius: 0.25rem;
    background-color: rgba(255, 255, 255, 0.9);
  }

  .recruit-button {
    background-color: #d4af37;
    color: #3a2718;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 0.25rem;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    transition: all 0.3s ease;
  }

  .recruit-button:hover {
    background-color: #c49b27;
    transform: translateY(-2px);
  }

  .recruit-icon {
    font-size: 0.9rem;
  }

  .dashboard-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    grid-template-rows: 1fr 1fr;
    gap: 1rem;
    height: calc(100% - 60px);
    overflow: hidden;
  }

  .dashboard-widget {
    background-color: rgba(255, 248, 220, 0.9);
    border: 1px solid #d4af37;
    border-radius: 0.5rem;
    overflow: hidden;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    display: flex;
    flex-direction: column;
    height: 100%;
  }

  .widget-header {
    background-color: rgba(42, 107, 93, 0.8);
    padding: 0.75rem 1rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .widget-title {
    color: #f8f8f8;
    font-size: 1.2rem;
    margin: 0;
    font-weight: normal;
  }

  .widget-content {
    padding: 0.75rem;
    color: #3a2718;
    flex: 1;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
  }

  /* Specific widget styling */
  .disciples-list {
    grid-column: 1 / 2;
    grid-row: 1 / 3;
  }

  .disciples-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
    gap: 0.75rem;
    width: 100%;
  }

  .disciple-card {
    background-color: rgba(255, 255, 255, 0.7);
    border: 1px solid #d4af37;
    border-radius: 0.5rem;
    padding: 0.75rem;
    cursor: pointer;
    transition: all 0.3s ease;
  }

  .disciple-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
  }

  .disciple-header {
    border-bottom: 1px solid #d4af37;
    padding-bottom: 0.5rem;
    margin-bottom: 0.5rem;
  }

  .disciple-name {
    color: #2a6b5d;
    margin: 0 0 0.25rem;
    font-size: 1.1rem;
  }

  .disciple-path {
    color: #666;
    font-size: 0.9rem;
  }

  .disciple-stats {
    display: flex;
    justify-content: space-between;
    font-size: 0.9rem;
    color: #666;
    margin-bottom: 0.75rem;
  }

  .disciple-power {
    color: #d4af37;
    font-weight: bold;
  }

  .action-button {
  background-color: #2a6b5d;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0.25rem;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.3s ease;
}

  .action-button:hover:not(:disabled) {
  background-color: #1a4b3d;
}

  .action-button:disabled {
    background-color: #ccc;
    cursor: not-allowed;
  }

  /* Realm stats widget */
  .realm-distribution, .path-distribution {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  .realm-item, .path-item {
    display: flex;
    justify-content: space-between;
    padding: 0.5rem;
    background-color: rgba(255, 255, 255, 0.7);
    border-radius: 0.25rem;
    border-left: 3px solid #2a6b5d;
  }

  .realm-name, .path-name {
    color: #3a2718;
  }

  .realm-count, .path-count {
    font-weight: bold;
    color: #2a6b5d;
  }

  /* Action buttons */
  .action-buttons {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }

  .sect-action-button {
    display: flex;
    align-items: center;
    gap: 1rem;
    background-color: rgba(255, 255, 255, 0.7);
    border: 1px solid #d4af37;
    border-radius: 0.5rem;
    padding: 0.75rem;
    cursor: pointer;
    transition: all 0.3s ease;
    text-align: left;
  }

  .sect-action-button:hover:not(:disabled) {
    background-color: rgba(212, 175, 55, 0.2);
    transform: translateY(-2px);
  }

  .sect-action-button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  .action-icon {
    font-size: 1.5rem;
    color: #2a6b5d;
  }

  .action-text {
    flex: 1;
  }

  .action-title {
    font-weight: bold;
    color: #2a6b5d;
    margin-bottom: 0.25rem;
  }

  .action-desc {
    font-size: 0.8rem;
    color: #666;
  }

  .loading, .error, .empty-message {
    text-align: center;
    padding: 1rem;
  }

  .error {
    color: #a52a2a;
  }

  .empty-message {
    font-style: italic;
    color: #666;
  }

  @media (max-width: 768px) {
    .disciples-header {
      flex-direction: column;
      align-items: flex-start;
      gap: 0.75rem;
    }
    
    .header-actions {
      width: 100%;
      flex-wrap: wrap;
    }
    
    .dashboard-grid {
      grid-template-columns: 1fr;
      grid-template-rows: auto;
    }
    
    .disciples-list {
      grid-column: auto;
      grid-row: auto;
    }
  }
</style>
