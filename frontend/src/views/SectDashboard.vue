<template>
  <div class="sect-dashboard">
    <div class="dashboard-grid">
      <!-- Sect Overview Widget -->
      <div class="dashboard-widget sect-overview">
        <div class="widget-header">
          <h2 class="widget-title">Sect Overview</h2>
        </div>
        <div class="widget-content">
          <div v-if="loading" class="loading">Loading sect information...</div>
          <div v-else-if="error" class="error">{{ error }}</div>
          <div v-else class="sect-info">
            <div class="sect-description">{{ sect.description }}</div>
            <div class="sect-stats">
              <div class="stat-item">
                <div class="stat-label">Influence</div>
                <div class="stat-value">{{ sect.sect_influence }}</div>
              </div>
              <div class="stat-item">
                <div class="stat-label">Reputation</div>
                <div class="stat-value">{{ sect.reputation }}</div>
              </div>
              <div class="stat-item">
                <div class="stat-label">Formation</div>
                <div class="stat-value">{{ sect.formation_strength }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Resources Widget -->
      <div class="dashboard-widget resources">
        <div class="widget-header">
          <h2 class="widget-title">Resources</h2>
        </div>
        <div class="widget-content">
          <div v-if="loadingResources" class="loading">Loading resources...</div>
          <div v-else-if="errorResources" class="error">{{ errorResources }}</div>
          <div v-else class="resource-info">
            <div class="resource-stats">
              <div class="stat-item">
                <div class="stat-label">Spirit Stones</div>
                <div class="stat-value">{{ formatNumber(resources.spirit_stones) }}</div>
              </div>
              <div class="stat-item">
                <div class="stat-label">Spirit Veins</div>
                <div class="stat-value">{{ resources.spirit_veins.length }}</div>
              </div>
              <div class="stat-item">
                <div class="stat-label">Elixir Fields</div>
                <div class="stat-value">{{ resources.elixir_fields }}</div>
              </div>
              <div class="stat-item">
                <div class="stat-label">Monthly Income</div>
                <div class="stat-value">{{ formatNumber(resources.monthly_income) }}</div>
              </div>
            </div>
            <button class="action-button" @click="collectResources">Collect Resources</button>
            <div v-if="resourceMessage" class="resource-message">{{ resourceMessage }}</div>
          </div>
        </div>
      </div>
      
      <!-- Disciples Widget -->
      <div class="dashboard-widget disciples">
        <div class="widget-header">
          <h2 class="widget-title">Disciples</h2>
          <router-link to="/dashboard/disciples" class="widget-action">View All</router-link>
        </div>
        <div class="widget-content">
          <div v-if="loadingDisciples" class="loading">Loading disciples...</div>
          <div v-else-if="errorDisciples" class="error">{{ errorDisciples }}</div>
          <div v-else class="disciple-info">
            <div v-if="disciples.length === 0" class="empty-message">No disciples found.</div>
            <div v-else>
              <div class="disciple-count">Total Disciples: {{ disciples.length }}</div>
              <div class="top-disciples">
                <h3 class="section-title">Top Disciples</h3>
                <div class="disciple-list">
                  <div v-for="disciple in topDisciples" :key="disciple.id" class="disciple-item" @click="viewDisciple(disciple.id)">
                    <div class="disciple-name">{{ disciple.name }}</div>
                    <div class="disciple-realm">{{ disciple.stage }} {{ disciple.realm }}</div>
                    <div class="disciple-power">Power: {{ formatNumber(disciple.combat_power) }}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Knowledge Widget -->
      <div class="dashboard-widget knowledge">
        <div class="widget-header">
          <h2 class="widget-title">Knowledge</h2>
          <router-link to="/dashboard/knowledge" class="widget-action">View All</router-link>
        </div>
        <div class="widget-content">
          <div v-if="loadingKnowledge" class="loading">Loading knowledge assets...</div>
          <div v-else-if="errorKnowledge" class="error">{{ errorKnowledge }}</div>
          <div v-else class="knowledge-info">
            <div class="knowledge-stats">
              <div class="stat-item">
                <div class="stat-label">Techniques</div>
                <div class="stat-value">{{ knowledge.techniques.length }}</div>
              </div>
              <div class="stat-item">
                <div class="stat-label">Secret Manuals</div>
                <div class="stat-value">{{ knowledge.secret_manuals.length }}</div>
              </div>
              <div class="stat-item">
                <div class="stat-label">Alchemy Recipes</div>
                <div class="stat-value">{{ knowledge.alchemy_recipes.length }}</div>
              </div>
              <div class="stat-item">
                <div class="stat-label">Formation Diagrams</div>
                <div class="stat-value">{{ knowledge.formation_diagrams.length }}</div>
              </div>
            </div>
            <div v-if="knowledge.techniques.length > 0" class="recent-knowledge">
              <h3 class="section-title">Core Techniques</h3>
              <div class="technique-list">
                <div v-for="(technique, index) in knowledge.techniques.slice(0, 3)" :key="index" class="technique-item">
                  {{ technique }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'SectDashboard',
  data() {
    return {
      sect: {},
      resources: {
        spirit_stones: 0,
        spirit_veins: [],
        elixir_fields: 0,
        monthly_income: 0,
        territories: []
      },
      disciples: [],
      knowledge: {
        techniques: [],
        secret_manuals: [],
        alchemy_recipes: [],
        formation_diagrams: [],
        artifact_blueprints: []
      },
      loading: true,
      loadingResources: true,
      loadingDisciples: true,
      loadingKnowledge: true,
      error: null,
      errorResources: null,
      errorDisciples: null,
      errorKnowledge: null,
      resourceMessage: null
    }
  },
  computed: {
    topDisciples() {
      // Return top 3 disciples by combat power
      return [...this.disciples]
        .sort((a, b) => b.combat_power - a.combat_power)
        .slice(0, 3);
    }
  },
  mounted() {
    this.fetchSectData();
    this.fetchResourcesData();
    this.fetchDisciplesData();
    this.fetchKnowledgeData();
  },
  methods: {
    async fetchSectData() {
      try {
        const response = await axios.get('http://localhost:5000/api/player-sect');
        this.sect = response.data;
        this.loading = false;
      } catch (err) {
        this.error = 'Failed to load sect data';
        this.loading = false;
        console.error(err);
      }
    },
    async fetchResourcesData() {
      try {
        const response = await axios.get('http://localhost:5000/api/player-sect/resources');
        this.resources = response.data;
        this.loadingResources = false;
      } catch (err) {
        this.errorResources = 'Failed to load resource data';
        this.loadingResources = false;
        console.error(err);
      }
    },
    async fetchDisciplesData() {
      try {
        const response = await axios.get('http://localhost:5000/api/player-sect/disciples');
        this.disciples = response.data;
        this.loadingDisciples = false;
      } catch (err) {
        this.errorDisciples = 'Failed to load disciple data';
        this.loadingDisciples = false;
        console.error(err);
      }
    },
    async fetchKnowledgeData() {
      try {
        const response = await axios.get('http://localhost:5000/api/player-sect/knowledge');
        this.knowledge = response.data;
        this.loadingKnowledge = false;
      } catch (err) {
        this.errorKnowledge = 'Failed to load knowledge data';
        this.loadingKnowledge = false;
        console.error(err);
      }
    },
    async collectResources() {
      try {
        const response = await axios.post('http://localhost:5000/api/player-sect/collect-resources');
        const { initial_stones, income, current_stones } = response.data;
        this.resourceMessage = `Collected ${this.formatNumber(income)} spirit stones from spirit veins.`;
        this.resources.spirit_stones = current_stones;
        
        // Update the spirit stones in parent component if possible
        if (this.$parent && this.$parent.spiritStones !== undefined) {
          this.$parent.spiritStones = current_stones;
        }
      } catch (err) {
        this.resourceMessage = 'Failed to collect resources.';
        console.error(err);
      }
    },
    viewDisciple(id) {
      this.$router.push(`/dashboard/disciples/${id}`);
    },
    formatNumber(num) {
      return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    }
  }
}
</script>

<style scoped>
.sect-dashboard {
  width: 100%;
  height: 100%;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  grid-template-rows: calc(50% - 0.75rem) calc(50% - 0.75rem); /* Fixed height rows */
  gap: 1.5rem;
  height: 100%;
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
  height: 100%; /* Full height */
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

.widget-action {
  color: #d4af37;
  text-decoration: none;
  font-size: 0.9rem;
}

.widget-action:hover {
  text-decoration: underline;
}

.widget-content {
  padding: 1rem;
  color: #3a2718;
  flex: 1;
  overflow-y: auto; /* Scrollable content */
  display: flex;
  flex-direction: column;
}

.sect-description {
  font-style: italic;
  margin-bottom: 1rem;
  text-align: center;
}

.sect-info, .resource-info, .knowledge-info, .disciple-info {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.sect-stats, .resource-stats, .knowledge-stats {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-around;
}

.stat-item {
  text-align: center;
  padding: 0.5rem;
  min-width: 80px;
}

.stat-label {
  font-size: 0.8rem;
  color: #666;
}

.stat-value {
  font-size: 1.2rem;
  font-weight: bold;
  color: #2a6b5d;
}

.action-button {
  background-color: #d4af37;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0.25rem;
  cursor: pointer;
  font-size: 0.9rem;
  display: block;
  margin: 1rem auto 0;
  transition: all 0.3s ease;
}

.action-button:hover {
  background-color: #b8860b;
  transform: translateY(-2px);
}

.resource-message {
  text-align: center;
  margin-top: 0.5rem;
  font-size: 0.9rem;
  color: #2a6b5d;
}

.disciple-count {
  text-align: center;
  margin-bottom: 0.5rem;
}

.section-title {
  font-size: 1rem;
  color: #2a6b5d;
  margin: 0.5rem 0;
  border-left: 3px solid #d4af37;
  padding-left: 0.5rem;
}

.disciple-list, .technique-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  overflow-y: auto;
  flex: 1;
}

.disciple-item {
  background-color: rgba(42, 107, 93, 0.1);
  border: 1px solid #2a6b5d;
  border-radius: 0.25rem;
  padding: 0.5rem;
  cursor: pointer;
}

.disciple-item:hover {
  background-color: rgba(42, 107, 93, 0.2);
}

.disciple-name {
  font-weight: bold;
  color: #2a6b5d;
}

.disciple-realm {
  font-size: 0.8rem;
  color: #666;
}

.disciple-power {
  font-size: 0.8rem;
  color: #d4af37;
  text-align: right;
}

.technique-item {
  background-color: rgba(212, 175, 55, 0.1);
  border: 1px solid #d4af37;
  border-radius: 0.25rem;
  padding: 0.5rem;
  font-size: 0.9rem;
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
  .dashboard-grid {
    grid-template-columns: 1fr;
    grid-template-rows: repeat(4, minmax(300px, 1fr));
    height: auto;
  }
  
  .dashboard-widget {
    min-height: 300px;
  }
}
</style>
