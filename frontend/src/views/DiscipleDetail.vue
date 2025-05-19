<template>
  <div class="disciple-detail-container">
    <div class="scroll-container">
      <div v-if="loading" class="loading">Loading disciple information...</div>
      <div v-else-if="error" class="error">{{ error }}</div>
      <div v-else class="disciple-info">
        <div class="disciple-header">
          <h1 class="disciple-name">{{ disciple.name }}</h1>
          <div class="disciple-realm">{{ disciple.stage_name }} {{ disciple.realm_name }}</div>
          <div class="disciple-path">{{ disciple.path }} Path</div>
          <div class="disciple-sect">{{ disciple.sect || 'Rogue Cultivator' }}</div>
        </div>
        
        <div class="disciple-stats">
          <div class="stat-group">
            <div class="stat">
              <div class="stat-label">Physical</div>
              <div class="stat-value">{{ disciple.physical }}</div>
            </div>
            <div class="stat">
              <div class="stat-label">Spiritual</div>
              <div class="stat-value">{{ disciple.spiritual }}</div>
            </div>
            <div class="stat">
              <div class="stat-label">Comprehension</div>
              <div class="stat-value">{{ disciple.comprehension }}</div>
            </div>
          </div>
          
          <div class="qi-bar">
            <div class="qi-label">Qi: {{ Math.floor(disciple.qi) }} / {{ disciple.max_qi }}</div>
            <div class="qi-progress">
              <div class="qi-fill" :style="{ width: `${(disciple.qi / disciple.max_qi) * 100}%` }"></div>
            </div>
          </div>
          
          <div class="combat-power">
            <div class="power-label">Combat Power</div>
            <div class="power-value">{{ formatNumber(disciple.combat_power) }}</div>
          </div>
        </div>
        
        <div class="cultivation-actions">
          <h2 class="section-title">Cultivation</h2>
          
          <!-- Bottleneck Status -->
          <div v-if="disciple.bottleneck !== 'none'" class="bottleneck-status">
            <div class="bottleneck-header">
              <span class="bottleneck-icon" v-if="disciple.bottleneck === 'minor'">🔄</span>
              <span class="bottleneck-icon" v-else>⚠️</span>
              <span class="bottleneck-type">{{ disciple.bottleneck === 'minor' ? 'Minor' : 'Major' }} Bottleneck</span>
            </div>
            
            <div class="bottleneck-description" v-if="disciple.bottleneck === 'minor'">
              This disciple has encountered a minor cultivation bottleneck. They need insights to advance further.
              <div class="insight-progress">
                <span>Insights: {{ disciple.bottleneck_insights }} / {{ disciple.insights_required }}</span>
                <div class="insight-bar">
                  <div class="insight-fill" :style="{ width: `${(disciple.bottleneck_insights / disciple.insights_required) * 100}%` }"></div>
                </div>
              </div>
              <button class="action-button bottleneck-action" @click="meditateForInsight">Meditate for Insight</button>
            </div>
            
            <div class="bottleneck-description" v-else>
              This disciple has encountered a major cultivation bottleneck. They need special treasures to overcome this barrier.
              <div class="treasure-options">
                <button 
                  v-for="(count, treasure) in sectTreasures" 
                  :key="treasure" 
                  class="treasure-button" 
                  :class="{ 'disabled': count <= 0 }"
                  :disabled="count <= 0"
                  @click="useTreasure(treasure)"
                >
                  {{ formatTreasureName(treasure) }} ({{ count }})
                </button>
              </div>
            </div>
          </div>
          
          <div class="action-buttons">
            <button class="action-button" @click="navigateToCultivation">Enter Cultivation Chamber</button>
            <button 
              class="action-button" 
              @click="attemptBreakthrough"
              :disabled="disciple.bottleneck !== 'none'"
            >
              Attempt Breakthrough
            </button>
          </div>
          <div v-if="actionMessage" class="action-message" :class="{ 'success': actionSuccess, 'error': !actionSuccess }">{{ actionMessage }}</div>
        </div>
        
        <div class="disciple-techniques">
          <h2 class="section-title">Techniques</h2>
          <div v-if="disciple.techniques.length === 0" class="empty-message">This disciple has not learned any techniques yet.</div>
          <div v-else class="technique-list">
            <div v-for="(technique, index) in disciple.techniques" :key="index" class="technique-item">
              {{ technique }}
            </div>
          </div>
        </div>
        
        <div class="back-link">
          <router-link to="/dashboard/disciples">← Return to Disciples Page</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'DiscipleDetail',
  props: {
    id: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      disciple: {},
      loading: true,
      error: null,
      actionMessage: null,
      actionSuccess: false,
      sectTreasures: {},
      playerSect: {}
    }
  },
  mounted() {
    this.fetchDiscipleDetails();
    this.fetchPlayerSect();
  },
  methods: {
    async fetchDiscipleDetails() {
      try {
        const response = await axios.get(`http://localhost:5000/api/disciples/${this.id}`);
        this.disciple = response.data;
        this.loading = false;
      } catch (err) {
        this.error = 'Failed to load disciple details. The records are sealed.';
        this.loading = false;
        console.error(err);
      }
    },
    navigateToCultivation() {
      // Check if we're already in a dashboard route
      if (this.$route.path.includes('/dashboard/')) {
        this.$router.push(`/dashboard/cultivation/${this.id}`);
      } else {
        // Fallback to the standalone cultivation route if not in dashboard
        this.$router.push(`/cultivation/${this.id}`);
      }
    },
    async attemptBreakthrough() {
      try {
        const response = await axios.post(`http://localhost:5000/api/disciples/${this.id}/breakthrough`);
        
        // Update the action message from the response
        this.actionMessage = response.data.message;
        this.actionSuccess = response.data.success;
        
        // Check if a bottleneck was encountered
        if (response.data.bottleneck !== 'none') {
          // Update disciple bottleneck data
          this.disciple.bottleneck = response.data.bottleneck;
          this.disciple.bottleneck_insights = 0;
          this.disciple.insights_required = response.data.insights_required || 0;
        }
        
        // Update disciple data
        if (response.data.realm_name) {
          this.disciple.realm_name = response.data.realm_name;
        }
        if (response.data.stage) {
          this.disciple.stage_name = response.data.stage;
        }
        if (response.data.qi) {
          this.disciple.qi = response.data.qi;
        }
        if (response.data.max_qi) {
          this.disciple.max_qi = response.data.max_qi;
        }
        
        // Refresh disciple details to get updated combat power
        this.fetchDiscipleDetails();
      } catch (err) {
        this.actionMessage = 'Failed to attempt breakthrough. Your dao heart is unstable.';
        this.actionSuccess = false;
        console.error(err);
      }
    },
    async fetchPlayerSect() {
      try {
        const response = await axios.get('http://localhost:5000/api/player-sect');
        this.playerSect = response.data;
        
        // Get treasures if available
        if (response.data.treasures) {
          this.sectTreasures = response.data.treasures;
        }
      } catch (err) {
        console.error('Failed to load player sect data:', err);
      }
    },
    
    async meditateForInsight() {
      try {
        const response = await axios.post(`http://localhost:5000/api/disciples/${this.id}/meditate`);
        
        // Update disciple data with the response
        if (response.data.disciple) {
          this.disciple.bottleneck = response.data.disciple.bottleneck;
          this.disciple.bottleneck_insights = response.data.disciple.bottleneck_insights;
          this.disciple.insights_required = response.data.disciple.insights_required;
          this.disciple.breakthrough_chance = response.data.disciple.breakthrough_chance;
        }
        
        // Set action message
        this.actionMessage = response.data.message;
        this.actionSuccess = response.data.success;
        
        // If bottleneck is overcome, refresh disciple details
        if (response.data.bottleneck_overcome) {
          this.fetchDiscipleDetails();
        }
      } catch (err) {
        this.actionMessage = 'Failed to meditate. Your mind is too restless.';
        this.actionSuccess = false;
        console.error(err);
      }
    },
    
    async useTreasure(treasureType) {
      try {
        const response = await axios.post(`http://localhost:5000/api/disciples/${this.id}/use-treasure`, {
          treasure_type: treasureType
        });
        
        // Update disciple data with the response
        if (response.data.disciple) {
          this.disciple.bottleneck = response.data.disciple.bottleneck;
          this.disciple.breakthrough_chance = response.data.disciple.breakthrough_chance;
        }
        
        // Update sect treasures
        if (response.data.treasures) {
          this.sectTreasures = response.data.treasures;
        }
        
        // Set action message
        this.actionMessage = response.data.message;
        this.actionSuccess = response.data.success;
        
        // If bottleneck is overcome, refresh disciple details
        if (response.data.bottleneck_overcome) {
          this.fetchDiscipleDetails();
        }
      } catch (err) {
        this.actionMessage = 'Failed to use treasure. The treasure was not compatible with your cultivation base.';
        this.actionSuccess = false;
        console.error(err);
      }
    },
    
    formatTreasureName(treasureType) {
      // Convert snake_case to Title Case with spaces
      return treasureType
        .split('_')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ');
    },
    
    formatNumber(num) {
      return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    }
  }
}
</script>

<style scoped>
.disciple-detail-container {
  width: 100%;
  max-width: 1200px;
  display: flex;
  justify-content: center;
}

.scroll-container {
  background-color: rgba(255, 248, 220, 0.9);
  border: 1px solid #d4af37;
  border-radius: 0.5rem;
  width: 90%;
  max-width: 800px;
  padding: 2rem;
  color: #3a3a3a;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.disciple-header {
  text-align: center;
  margin-bottom: 1.5rem;
  border-bottom: 2px solid #d4af37;
  padding-bottom: 1rem;
}

.disciple-name {
  font-size: 2rem;
  color: #8b4513;
  margin-bottom: 0.5rem;
}

.disciple-realm {
  font-size: 1.2rem;
  color: #8b4513;
  margin-bottom: 0.25rem;
}

.disciple-path {
  font-size: 1rem;
  color: #555;
  margin-bottom: 0.25rem;
}

.disciple-sect {
  font-size: 0.9rem;
  color: #666;
  font-style: italic;
}

.disciple-stats {
  margin-bottom: 1.5rem;
}

.stat-group {
  display: flex;
  justify-content: space-around;
  margin-bottom: 1rem;
}

.stat {
  text-align: center;
}

.stat-label {
  font-size: 0.9rem;
  color: #666;
}

.stat-value {
  font-size: 1.2rem;
  font-weight: bold;
  color: #8b4513;
}

.qi-bar {
  margin-bottom: 1rem;
}

.qi-label {
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 0.25rem;
}

.qi-progress {
  height: 1rem;
  background-color: #f0f0f0;
  border-radius: 0.5rem;
  overflow: hidden;
}

.qi-fill {
  height: 100%;
  background-color: #4caf50;
  transition: width 0.3s ease;
}

.combat-power {
  text-align: center;
  margin-top: 1rem;
}

.power-label {
  font-size: 0.9rem;
  color: #666;
}

.power-value {
  font-size: 1.5rem;
  font-weight: bold;
  color: #d4af37;
}

.section-title {
  font-size: 1.3rem;
  color: #8b4513;
  margin: 1.5rem 0 0.5rem;
  border-left: 4px solid #d4af37;
  padding-left: 0.5rem;
}

.action-buttons {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-bottom: 0.5rem;
}

.action-button {
  background-color: #d4af37;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0.25rem;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.3s ease;
}

.action-button:hover {
  background-color: #b8860b;
  transform: translateY(-2px);
}

.action-message {
  text-align: center;
  margin-top: 0.5rem;
  font-size: 0.9rem;
  padding: 0.5rem;
  border-radius: 0.25rem;
}

.action-message.success {
  background-color: rgba(76, 175, 80, 0.2);
  border: 1px solid rgba(76, 175, 80, 0.5);
  color: #2e7d32;
}

.action-message.error {
  background-color: rgba(244, 67, 54, 0.2);
  border: 1px solid rgba(244, 67, 54, 0.5);
  color: #c62828;
}

.bottleneck-status {
  margin: 1rem 0;
  padding: 1rem;
  border-radius: 0.5rem;
  background-color: rgba(255, 235, 205, 0.7);
  border: 1px solid #d4af37;
}

.bottleneck-header {
  display: flex;
  align-items: center;
  margin-bottom: 0.5rem;
  font-weight: bold;
  font-size: 1.1rem;
}

.bottleneck-icon {
  margin-right: 0.5rem;
  font-size: 1.2rem;
}

.bottleneck-type {
  color: #8B4513;
}

.bottleneck-description {
  margin-bottom: 1rem;
  line-height: 1.5;
}

.insight-progress {
  margin: 0.75rem 0;
}

.insight-bar {
  height: 0.5rem;
  background-color: rgba(255, 255, 255, 0.5);
  border-radius: 0.25rem;
  margin-top: 0.25rem;
  overflow: hidden;
}

.insight-fill {
  height: 100%;
  background-color: #4CAF50;
  border-radius: 0.25rem;
  transition: width 0.3s ease;
}

.bottleneck-action {
  margin-top: 0.5rem;
  background-color: rgba(212, 175, 55, 0.7);
}

.treasure-options {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 0.75rem;
}

.treasure-button {
  padding: 0.5rem 0.75rem;
  background-color: rgba(212, 175, 55, 0.7);
  border: 1px solid #d4af37;
  border-radius: 0.25rem;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.9rem;
  color: #8B4513;
}

.treasure-button:hover {
  background-color: rgba(212, 175, 55, 0.9);
}

.treasure-button.disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.technique-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.technique-item {
  background-color: rgba(212, 175, 55, 0.1);
  border: 1px solid #d4af37;
  border-radius: 0.25rem;
  padding: 0.5rem;
  font-size: 0.9rem;
}

.empty-message {
  font-style: italic;
  color: #666;
  font-size: 0.9rem;
  margin-top: 0.5rem;
}

.back-link {
  margin-top: 2rem;
  text-align: center;
}

.back-link a {
  color: #8b4513;
  text-decoration: none;
}

.back-link a:hover {
  text-decoration: underline;
}

.loading, .error {
  text-align: center;
  padding: 2rem;
  color: #8b4513;
}

.error {
  color: #a52a2a;
}
</style>
