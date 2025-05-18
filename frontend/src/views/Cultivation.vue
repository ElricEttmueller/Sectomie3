<template>
  <div class="cultivation-container">
    <div class="scroll-container">
      <div v-if="loading" class="loading">Loading disciple information...</div>
      <div v-else-if="error" class="error">{{ error }}</div>
      <div v-else class="cultivation-content">
        <div class="cultivation-header">
          <h1 class="cultivation-title">Cultivation Chamber</h1>
          <div class="disciple-name">{{ disciple.name }}</div>
          <div class="disciple-realm">{{ disciple.stage_name }} {{ disciple.realm_name }}</div>
        </div>
        
        <div class="qi-status">
          <div class="qi-label">Qi: {{ Math.floor(disciple.qi) }} / {{ disciple.max_qi }}</div>
          <div class="qi-progress">
            <div class="qi-fill" :style="{ width: `${(disciple.qi / disciple.max_qi) * 100}%` }"></div>
          </div>
          <div class="breakthrough-chance">
            <span>Breakthrough Chance: {{ Math.floor(disciple.breakthrough_chance) }}%</span>
          </div>
        </div>
        
        <div class="cultivation-options">
          <h2 class="option-title">Cultivation Methods</h2>
          
          <div class="method-cards">
            <!-- Qi Circulation Method -->
            <div class="method-card" :class="{ 'selected': selectedMethod === 'qi_circulation' }" @click="selectMethod('qi_circulation')">
              <div class="method-header">
                <h3 class="method-name">Qi Circulation</h3>
                <div class="method-cost">
                  <span class="spirit-stone-icon">💰</span> 50
                </div>
              </div>
              <div class="method-description">
                The disciple circulates qi through meridians, slowly building foundation.
              </div>
              <div class="method-effects">
                <div class="effect">+10% Qi</div>
                <div class="effect">+1% Breakthrough Chance</div>
              </div>
            </div>
            
            <!-- Essence Refinement Method -->
            <div class="method-card" :class="{ 'selected': selectedMethod === 'essence_refinement' }" @click="selectMethod('essence_refinement')">
              <div class="method-header">
                <h3 class="method-name">Essence Refinement</h3>
                <div class="method-cost">
                  <span class="spirit-stone-icon">💰</span> 200
                </div>
              </div>
              <div class="method-description">
                Refines external energies into pure essence, strengthening the cultivation base.
              </div>
              <div class="method-effects">
                <div class="effect">+20% Qi</div>
                <div class="effect">+2% Breakthrough Chance</div>
              </div>
            </div>
            
            <!-- Dao Heart Tempering Method -->
            <div class="method-card" :class="{ 'selected': selectedMethod === 'dao_heart_tempering', 'disabled': sectResources.spirit_herbs < 1 || sectResources.spirit_stones < 400 }" @click="selectMethod('dao_heart_tempering')">
              <div class="method-header">
                <h3 class="method-name">Dao Heart Tempering</h3>
                <div class="method-cost">
                  <span class="spirit-stone-icon">💰</span> 400
                  <span class="herb-icon">🌿</span> 1
                </div>
              </div>
              <div class="method-description">
                Meditates on dao principles, purifying the cultivator's intent.
              </div>
              <div class="method-effects">
                <div class="effect">+30% Qi</div>
                <div class="effect">+4% Breakthrough Chance</div>
                <div class="effect">15% chance to improve Comprehension</div>
                <div class="effect warning">2% risk of cultivation deviation</div>
              </div>
            </div>
            
            <!-- Heavenly Tribulation Simulation Method -->
            <div class="method-card" :class="{ 'selected': selectedMethod === 'heavenly_tribulation', 'disabled': sectResources.dao_crystals < 1 || sectResources.spirit_stones < 800 }" @click="selectMethod('heavenly_tribulation')">
              <div class="method-header">
                <h3 class="method-name">Heavenly Tribulation Simulation</h3>
                <div class="method-cost">
                  <span class="spirit-stone-icon">💰</span> 800
                  <span class="crystal-icon">💎</span> 1
                </div>
              </div>
              <div class="method-description">
                Simulates tribulation energy to prepare the body for breakthrough.
              </div>
              <div class="method-effects">
                <div class="effect">+15% Qi</div>
                <div class="effect highlight">+10% Breakthrough Chance</div>
                <div class="effect warning">10% risk of cultivation deviation</div>
              </div>
            </div>
          </div>
          
          <div class="sect-resources">
            <h3 class="resources-title">Sect Resources</h3>
            <div class="resources-list">
              <div class="resource-item">
                <span class="resource-icon">💰</span>
                <span class="resource-name">Spirit Stones:</span>
                <span class="resource-value">{{ formatNumber(sectResources.spirit_stones) }}</span>
              </div>
              <div class="resource-item">
                <span class="resource-icon">🌿</span>
                <span class="resource-name">Spirit Herbs:</span>
                <span class="resource-value">{{ sectResources.spirit_herbs }}</span>
              </div>
              <div class="resource-item">
                <span class="resource-icon">💎</span>
                <span class="resource-name">Dao Crystals:</span>
                <span class="resource-value">{{ sectResources.dao_crystals }}</span>
              </div>
            </div>
          </div>
          
          <div class="action-buttons">
            <button class="action-button" @click="cultivate" :disabled="!selectedMethod">Begin Cultivation</button>
            <button class="action-button" @click="attemptBreakthrough">Attempt Breakthrough</button>
          </div>
          
          <div v-if="actionMessage" class="action-message" :class="{ 'success': actionSuccess, 'error': !actionSuccess }">
            {{ actionMessage }}
          </div>
        </div>
        
        <div class="cultivation-stats">
          <h2 class="stats-title">Cultivation Stats</h2>
          <div class="stats-grid">
            <div class="stat-item">
              <div class="stat-label">Physical</div>
              <div class="stat-value">{{ disciple.physical }}</div>
            </div>
            <div class="stat-item">
              <div class="stat-label">Spiritual</div>
              <div class="stat-value">{{ disciple.spiritual }}</div>
            </div>
            <div class="stat-item">
              <div class="stat-label">Comprehension</div>
              <div class="stat-value">{{ disciple.comprehension }}</div>
            </div>
            <div class="stat-item">
              <div class="stat-label">Combat Power</div>
              <div class="stat-value">{{ formatNumber(disciple.combat_power) }}</div>
            </div>
          </div>
        </div>
        
        <div class="back-link">
          <router-link :to="getBackLink()">← Return to Disciple Profile</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Cultivation',
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
      actionSuccess: true,
      selectedMethod: 'qi_circulation',
      sectResources: {
        spirit_stones: 0,
        spirit_herbs: 0,
        dao_crystals: 0
      }
    }
  },
  mounted() {
    this.fetchDiscipleDetails();
    this.fetchSectResources();
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
    async fetchSectResources() {
      try {
        const response = await axios.get(`http://localhost:5000/api/game-state`);
        this.sectResources.spirit_stones = response.data.spirit_stones;
        
        // Get additional resources
        const sectResponse = await axios.get(`http://localhost:5000/api/player-sect`);
        if (sectResponse.data) {
          this.sectResources.spirit_herbs = sectResponse.data.spirit_herbs || 0;
          this.sectResources.dao_crystals = sectResponse.data.dao_crystals || 0;
        }
      } catch (err) {
        console.error('Failed to fetch sect resources:', err);
      }
    },
    
    selectMethod(method) {
      // Check if method is disabled due to resource constraints
      if (method === 'dao_heart_tempering' && 
          (this.sectResources.spirit_herbs < 1 || this.sectResources.spirit_stones < 400)) {
        this.actionMessage = 'Not enough resources for Dao Heart Tempering';
        this.actionSuccess = false;
        return;
      }
      
      if (method === 'heavenly_tribulation' && 
          (this.sectResources.dao_crystals < 1 || this.sectResources.spirit_stones < 800)) {
        this.actionMessage = 'Not enough resources for Heavenly Tribulation Simulation';
        this.actionSuccess = false;
        return;
      }
      
      this.selectedMethod = method;
      this.actionMessage = null;
    },
    
    async cultivate() {
      if (!this.selectedMethod) {
        this.actionMessage = 'Please select a cultivation method first.';
        this.actionSuccess = false;
        return;
      }
      
      try {
        const response = await axios.post(`http://localhost:5000/api/disciples/${this.id}/cultivate-method`, {
          method: this.selectedMethod
        });
        
        const results = response.data;
        
        if (!results.success) {
          this.actionMessage = results.error || 'Cultivation failed.';
          this.actionSuccess = false;
          return;
        }
        
        // Update disciple data
        if (results.disciple) {
          this.disciple.qi = results.disciple.qi;
          this.disciple.max_qi = results.disciple.max_qi;
          this.disciple.breakthrough_chance = results.disciple.breakthrough_chance;
          this.disciple.physical = results.disciple.physical;
          this.disciple.spiritual = results.disciple.spiritual;
          this.disciple.comprehension = results.disciple.comprehension;
        }
        
        // Update sect resources
        if (results.resources) {
          this.sectResources = results.resources;
        }
        
        // Build success message
        let message = `Cultivation successful! Gained ${Math.floor(results.qi_gained)} qi and increased breakthrough chance by ${results.breakthrough_increase}%.`;
        
        if (results.attribute_increase) {
          message += ` Your ${results.attribute_increase} attribute improved to ${results.attribute_value}!`;
        }
        
        if (results.cultivation_deviation) {
          message += ' However, you experienced a cultivation deviation and lost some progress.';
        }
        
        this.actionMessage = message;
        this.actionSuccess = true;
      } catch (err) {
        if (err.response && err.response.data && err.response.data.error) {
          this.actionMessage = err.response.data.error;
        } else {
          this.actionMessage = 'Failed to cultivate. Your qi is in chaos.';
        }
        this.actionSuccess = false;
        console.error(err);
      }
    },
    async attemptBreakthrough() {
      try {
        const response = await axios.post(`http://localhost:5000/api/disciples/${this.id}/breakthrough`);
        const { success, realm, stage, qi, max_qi } = response.data;
        
        if (success) {
          this.actionMessage = `Breakthrough successful! Advanced to ${stage} ${realm}!`;
        } else {
          this.actionMessage = `Breakthrough failed. Current realm: ${stage} ${realm}`;
        }
        
        // Update disciple data
        this.disciple.realm_name = realm;
        this.disciple.stage_name = stage;
        this.disciple.qi = qi;
        this.disciple.max_qi = max_qi;
        
        // Refresh disciple details to get updated combat power
        this.fetchDiscipleDetails();
      } catch (err) {
        this.actionMessage = 'Failed to attempt breakthrough. Your dao heart is unstable.';
        console.error(err);
      }
    },
    formatNumber(num) {
      return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    },
    
    getBackLink() {
      // Check if we're in a dashboard route
      if (this.$route.path.includes('/dashboard/')) {
        return `/dashboard/disciples/${this.id}`;
      } else {
        // Fallback to the standalone disciple route
        return `/disciple/${this.id}`;
      }
    }
  }
}
</script>

<style scoped>
.cultivation-container {
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

.cultivation-header {
  text-align: center;
  margin-bottom: 1.5rem;
  border-bottom: 2px solid #d4af37;
  padding-bottom: 1rem;
}

.cultivation-title {
  font-size: 2rem;
  color: #8b4513;
  margin-bottom: 0.5rem;
}

.disciple-name {
  font-size: 1.5rem;
  color: #8b4513;
  margin-bottom: 0.25rem;
}

.disciple-realm {
  font-size: 1.2rem;
  color: #555;
}

.qi-status {
  margin-bottom: 1.5rem;
}

.qi-label {
  font-size: 1rem;
  color: #666;
  margin-bottom: 0.25rem;
}

.qi-progress {
  height: 1rem;
  background-color: #f0f0f0;
  border-radius: 0.5rem;
  overflow: hidden;
  margin-bottom: 0.5rem;
}

.qi-fill {
  height: 100%;
  background-color: #4caf50;
  transition: width 0.3s ease;
}

.breakthrough-chance {
  text-align: right;
  font-size: 0.9rem;
  color: #666;
}

.cultivation-options {
  margin-bottom: 1.5rem;
}

.option-title {
  font-size: 1.2rem;
  color: #8b4513;
  margin-bottom: 0.5rem;
}

.method-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.method-card {
  background-color: rgba(255, 255, 255, 0.7);
  border: 1px solid #d4af37;
  border-radius: 0.5rem;
  padding: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
}

.method-card:hover:not(.disabled) {
  transform: translateY(-3px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.method-card.selected {
  background-color: rgba(212, 175, 55, 0.2);
  border: 2px solid #d4af37;
}

.method-card.disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.method-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
  border-bottom: 1px solid rgba(212, 175, 55, 0.3);
  padding-bottom: 0.5rem;
}

.method-name {
  margin: 0;
  color: #8b4513;
  font-size: 1.1rem;
}

.method-cost {
  color: #d4af37;
  font-weight: bold;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.spirit-stone-icon, .herb-icon, .crystal-icon {
  font-size: 1.2rem;
}

.method-description {
  color: #555;
  font-size: 0.9rem;
  margin-bottom: 0.75rem;
  flex-grow: 1;
}

.method-effects {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.effect {
  font-size: 0.9rem;
  color: #555;
}

.effect.highlight {
  color: #2a6b5d;
  font-weight: bold;
}

.effect.warning {
  color: #a52a2a;
}

.sect-resources {
  background-color: rgba(255, 255, 255, 0.7);
  border: 1px solid #d4af37;
  border-radius: 0.5rem;
  padding: 1rem;
  margin-bottom: 1.5rem;
}

.resources-title {
  margin-top: 0;
  margin-bottom: 0.75rem;
  color: #8b4513;
  font-size: 1.1rem;
}

.resources-list {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.resource-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.resource-icon {
  font-size: 1.2rem;
}

.resource-name {
  color: #555;
}

.resource-value {
  font-weight: bold;
  color: #8b4513;
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
  padding: 0.75rem;
  border-radius: 0.25rem;
}

.action-message.success {
  background-color: rgba(76, 175, 80, 0.2);
  color: #2e7d32;
  border: 1px solid rgba(76, 175, 80, 0.5);
}

.action-message.error {
  background-color: rgba(244, 67, 54, 0.2);
  color: #c62828;
  border: 1px solid rgba(244, 67, 54, 0.5);
}

.cultivation-stats {
  margin-bottom: 1.5rem;
}

.stats-title {
  font-size: 1.2rem;
  color: #8b4513;
  margin-bottom: 0.5rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

.stat-item {
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

.back-link {
  margin-top: 1.5rem;
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
