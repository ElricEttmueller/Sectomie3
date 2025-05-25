<template>
  <div class="testing-dashboard">
    <h1 class="dashboard-title">Testing Dashboard</h1>
    
    <div class="dashboard-layout">
      <!-- Left Column: Controls and Testing -->  
      <div class="main-column">
        <div class="dashboard-section">
          <h2 class="section-title">Game State</h2>
          <div class="button-group">
            <button @click="fetchGameState" class="action-button">Fetch Game State</button>
            <button @click="resetGameState" class="action-button danger">Reset Game State</button>
            <button @click="endTurn" class="action-button primary">End Turn (Test Auto-Cultivation)</button>
          </div>
          <div v-if="gameState" class="data-display">
            <pre>{{ JSON.stringify(gameState, null, 2) }}</pre>
          </div>
        </div>
        
        <div class="dashboard-section">
          <h2 class="section-title">Disciple Testing</h2>
          
          <div class="select-container">
            <label>Select Disciple:</label>
            <select v-model="selectedDiscipleId" class="select-input">
              <option v-for="disciple in disciples" :key="disciple.id" :value="disciple.id">
                {{ disciple.name }} ({{ disciple.realm_name }}, {{ disciple.stage_name }})
              </option>
            </select>
            <button @click="fetchDisciples" class="refresh-button">🔄</button>
          </div>
          
          <div class="button-group">
            <button @click="fetchDiscipleDetails" class="action-button">Fetch Details</button>
            <button @click="forcePeakStage" class="action-button">Force Peak Stage</button>
            <button @click="clearBottleneck" class="action-button">Clear Bottleneck</button>
            <button @click="attemptBreakthrough" class="action-button">Attempt Breakthrough</button>
            <button @click="testCultivationAssignment" class="action-button primary">Test Cultivation Assignment</button>
          </div>
          
          <div class="attribute-controls" v-if="selectedDisciple">
            <h3>Modify Attributes</h3>
            <div class="attribute-grid">
              <div class="attribute-item">
                <label>Physical:</label>
                <input type="number" v-model.number="selectedDisciple.physical" min="0" max="100" class="number-input">
              </div>
              <div class="attribute-item">
                <label>Spiritual:</label>
                <input type="number" v-model.number="selectedDisciple.spiritual" min="0" max="100" class="number-input">
              </div>
              <div class="attribute-item">
                <label>Comprehension:</label>
                <input type="number" v-model.number="selectedDisciple.comprehension" min="0" max="100" class="number-input">
              </div>
              <div class="attribute-item">
                <label>Qi:</label>
                <input type="number" v-model.number="selectedDisciple.qi" min="0" :max="selectedDisciple.max_qi" class="number-input">
              </div>
              <div class="attribute-item">
                <label>Max Qi:</label>
                <input type="number" v-model.number="selectedDisciple.max_qi" min="100" class="number-input">
              </div>
              <div class="attribute-item">
                <label>Breakthrough Chance:</label>
                <input type="number" v-model.number="selectedDisciple.breakthrough_chance" min="0" max="100" class="number-input">
              </div>
            </div>
            <button @click="updateDiscipleAttributes" class="action-button">Update Attributes</button>
          </div>
          
          <div class="bottleneck-controls" v-if="selectedDisciple">
            <h3>Bottleneck Testing</h3>
            <div class="button-group">
              <button @click="createMinorBottleneck" class="action-button">Create Minor Bottleneck</button>
              <button @click="createMajorBottleneck" class="action-button">Create Major Bottleneck</button>
              <button @click="clearBottleneck" class="action-button">Clear Bottleneck</button>
            </div>
            
            <!-- New Bottleneck Visualizer Component -->
            <bottleneck-visualizer :disciple="selectedDisciple">
              <template v-slot:actions>
                <!-- Actions for minor bottleneck -->
                <div v-if="selectedDisciple.bottleneck === 'minor'" class="action-buttons">
                  <button @click="meditateForInsight" class="action-button primary">Meditate for Insight</button>
                </div>
                
                <!-- Actions for major bottleneck -->
                <div v-if="selectedDisciple.bottleneck === 'major'" class="action-buttons">
                  <div class="treasure-selection">
                    <label>Select Treasure:</label>
                    <select v-model="selectedTreasure" class="select-input">
                      <option value="spirit_pill">Spirit Pill</option>
                      <option value="dao_comprehension_stone">Dao Comprehension Stone</option>
                      <option value="heaven_and_earth_spirit_fruit">Heaven and Earth Spirit Fruit</option>
                      <option value="nine_transformation_pill">Nine Transformation Pill</option>
                      <option value="immortal_ascension_stone">Immortal Ascension Stone</option>
                    </select>
                  </div>
                  <div class="button-group">
                    <button @click="addTreasure" class="action-button">Add Treasure</button>
                    <button @click="useTreasure" class="action-button primary">Use Treasure</button>
                  </div>
                </div>
              </template>
            </bottleneck-visualizer>
          </div>
          
          <div v-if="selectedDisciple" class="data-display">
            <h3>Disciple Data</h3>
            <pre>{{ JSON.stringify(selectedDisciple, null, 2) }}</pre>
          </div>
        </div>
        
        <div class="dashboard-section">
          <h2 class="section-title">Sect Testing</h2>
          <div class="button-group">
            <button @click="fetchPlayerSect" class="action-button">Fetch Sect Data</button>
          </div>
          <div v-if="sectData" class="data-display">
            <pre>{{ JSON.stringify(sectData, null, 2) }}</pre>
          </div>
        </div>
      </div>
      
      <!-- Right Column: API Response Log (Fixed) -->
      <div class="log-column">
        <div class="dashboard-section fixed-section">
          <h2 class="section-title">API Response Log</h2>
          <button @click="clearLog" class="action-button danger">Clear Log</button>
          <div class="log-display">
            <div v-for="(entry, index) in apiLog" :key="index" class="log-entry" :class="{ 'success': entry.success, 'error': !entry.success }">
              <div class="log-header">
                <span class="log-timestamp">{{ entry.timestamp }}</span>
                <span class="log-endpoint">{{ entry.endpoint }}</span>
                <span class="log-status">{{ entry.success ? 'SUCCESS' : 'ERROR' }}</span>
              </div>
              <pre class="log-data">{{ JSON.stringify(entry.data, null, 2) }}</pre>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import BottleneckVisualizer from '@/components/BottleneckVisualizer.vue';

export default {
  name: 'TestingDB',
  components: {
    BottleneckVisualizer
  },
  data() {
    return {
      gameState: null,
      disciples: [],
      selectedDiscipleId: null,
      selectedDisciple: null,
      sectData: null,
      selectedTreasure: 'spirit_pill',
      treasureQuantity: 5,
      apiLog: [],
      apiBaseUrl: 'http://127.0.0.1:5000/api'
    };
  },
  mounted() {
    this.fetchDisciples();
  },
  methods: {
    // Logging helper
    logApiCall(endpoint, data, success) {
      this.apiLog.unshift({
        timestamp: new Date().toLocaleTimeString(),
        endpoint,
        data,
        success
      });
    },
    
    // Game State Methods
    async fetchGameState() {
      try {
        const response = await axios.get(`${this.apiBaseUrl}/game-state`);
        this.gameState = response.data;
        this.logApiCall('/game-state', response.data, true);
      } catch (error) {
        console.error('Error fetching game state:', error);
        this.logApiCall('/game-state', error.response && error.response.data ? error.response.data : error.message || error.message, false);
      }
    },
    
    async endTurn() {
      try {
        const response = await axios.post(`${this.apiBaseUrl}/end-turn`);
        this.logApiCall('/end-turn', response.data, true);
        
        // Display cultivation progress results
        if (response.data.results && response.data.results.cultivation_progress) {
          const progress = response.data.results.cultivation_progress;
          let message = 'Turn ended. Automatic cultivation results:\n\n';
          
          for (const discipleId in progress) {
            const disciple = progress[discipleId];
            message += `${disciple.name}:\n`;
            message += `- Gained ${Math.floor(disciple.qi_gained)} qi\n`;
            message += `- Current qi: ${Math.floor(disciple.current_qi)}/${disciple.max_qi}\n`;
            message += `- Breakthrough chance: ${Math.floor(disciple.breakthrough_chance)}%\n`;
            
            if (disciple.method_used) {
              message += `- Method used: ${disciple.method_used}\n`;
            }
            
            message += '\n';
          }
          
          // Show deviations if any
          if (response.data.results.cultivation_deviations && response.data.results.cultivation_deviations.length > 0) {
            message += '\nCultivation Deviations:\n';
            for (const deviation of response.data.results.cultivation_deviations) {
              message += `- ${deviation.name}: ${deviation.message}\n`;
            }
          }
          
          // Show attribute increases if any
          if (response.data.results.attribute_increases && response.data.results.attribute_increases.length > 0) {
            message += '\nAttribute Increases:\n';
            for (const increase of response.data.results.attribute_increases) {
              message += `- ${increase.name}: ${increase.attribute} increased to ${increase.value}\n`;
            }
          }
          
          // Show breakthrough events if any
          if (response.data.results.events && response.data.results.events.length > 0) {
            message += '\nBreakthrough Events:\n';
            for (const event of response.data.results.events) {
              if (event.type === 'breakthrough') {
                message += `- ${event.name}: ${event.message}\n`;
              }
            }
          }
          
          alert(message);
        } else {
          alert('Turn ended successfully. New turn: ' + response.data.new_turn);
        }
        
        // Refresh game state and disciples
        this.fetchGameState();
        this.fetchDisciples();
        
        // Refresh selected disciple details if one is selected
        if (this.selectedDiscipleId !== null) {
          this.fetchDiscipleDetails();
        }
      } catch (error) {
        console.error('Error ending turn:', error);
        this.logApiCall('/end-turn', error.response && error.response.data ? error.response.data : error.message || error.message, false);
        alert('Failed to end turn: ' + (error.response && error.response.data && error.response.data.message ? error.response.data.message : error.message));
      }
    },
    
    async resetGameState() {
      if (!confirm('Are you sure you want to reset the game state? This cannot be undone.')) return;
      
      try {
        // This endpoint doesn't exist yet - you'd need to implement it
        const response = await axios.post(`${this.apiBaseUrl}/reset-game`);
        this.logApiCall('/reset-game', response.data, true);
        alert('Game state reset successfully');
        this.fetchGameState();
        this.fetchDisciples();
      } catch (error) {
        console.error('Error resetting game state:', error);
        this.logApiCall('/reset-game', error.response && error.response.data ? error.response.data : error.message || error.message, false);
        alert('Failed to reset game state: ' + (error.response && error.response.data && error.response.data.message ? error.response.data.message : error.message));
      }
    },
    
    // Disciple Methods
    async fetchDisciples() {
      try {
        const response = await axios.get(`${this.apiBaseUrl}/disciples`);
        this.disciples = response.data.map((disciple, index) => ({
          ...disciple,
          id: index
        }));
        this.logApiCall('/disciples', response.data, true);
        
        if (this.disciples.length > 0 && !this.selectedDiscipleId) {
          this.selectedDiscipleId = this.disciples[0].id;
          this.fetchDiscipleDetails();
        }
      } catch (error) {
        console.error('Error fetching disciples:', error);
        this.logApiCall('/disciples', error.response && error.response.data ? error.response.data : error.message || error.message, false);
      }
    },
    
    async fetchDiscipleDetails() {
      if (this.selectedDiscipleId === null) return;
      
      try {
        const response = await axios.get(`${this.apiBaseUrl}/disciples/${this.selectedDiscipleId}`);
        this.selectedDisciple = response.data;
        this.logApiCall(`/disciples/${this.selectedDiscipleId}`, response.data, true);
      } catch (error) {
        console.error('Error fetching disciple details:', error);
        this.logApiCall(`/disciples/${this.selectedDiscipleId}`, error.response && error.response.data ? error.response.data : error.message || error.message, false);
      }
    },
    
    async forcePeakStage() {
      if (this.selectedDiscipleId === null) return;
      
      try {
        const response = await axios.post(`${this.apiBaseUrl}/disciples/${this.selectedDiscipleId}/force-peak`);
        this.logApiCall(`/disciples/${this.selectedDiscipleId}/force-peak`, response.data, true);
        this.fetchDiscipleDetails();
      } catch (error) {
        console.error('Error forcing peak stage:', error);
        this.logApiCall(`/disciples/${this.selectedDiscipleId}/force-peak`, error.response && error.response.data ? error.response.data : error.message || error.message, false);
      }
    },
    
    async clearBottleneck() {
      if (this.selectedDiscipleId === null) return;
      
      try {
        const response = await axios.post(`${this.apiBaseUrl}/disciples/${this.selectedDiscipleId}/clear-bottleneck`);
        this.logApiCall(`/disciples/${this.selectedDiscipleId}/clear-bottleneck`, response.data, true);
        this.fetchDiscipleDetails();
      } catch (error) {
        console.error('Error clearing bottleneck:', error);
        this.logApiCall(`/disciples/${this.selectedDiscipleId}/clear-bottleneck`, error.response && error.response.data ? error.response.data : error.message || error.message, false);
      }
    },
    
    async attemptBreakthrough() {
      if (this.selectedDiscipleId === null) return;
      
      try {
        const response = await axios.post(`${this.apiBaseUrl}/disciples/${this.selectedDiscipleId}/breakthrough`);
        this.logApiCall(`/disciples/${this.selectedDiscipleId}/breakthrough`, response.data, true);
        this.fetchDiscipleDetails();
      } catch (error) {
        console.error('Error attempting breakthrough:', error);
        this.logApiCall(`/disciples/${this.selectedDiscipleId}/breakthrough`, error.response && error.response.data ? error.response.data : error.message || error.message, false);
      }
    },
    
    async updateDiscipleAttributes() {
      if (!this.selectedDisciple) return;
      
      try {
        const response = await axios.post(`${this.apiBaseUrl}/disciples/${this.selectedDiscipleId}/update-attributes`, {
          physical: this.selectedDisciple.physical,
          spiritual: this.selectedDisciple.spiritual,
          comprehension: this.selectedDisciple.comprehension,
          qi: this.selectedDisciple.qi,
          max_qi: this.selectedDisciple.max_qi,
          breakthrough_chance: this.selectedDisciple.breakthrough_chance
        });
        this.logApiCall(`/disciples/${this.selectedDiscipleId}/update-attributes`, response.data, true);
        this.fetchDiscipleDetails();
      } catch (error) {
        console.error('Error updating attributes:', error);
        this.logApiCall(`/disciples/${this.selectedDiscipleId}/update-attributes`, error.response && error.response.data ? error.response.data : error.message || error.message, false);
        alert('Failed to update attributes. Please check the API response log for details.');
      }
    },
    
    // Bottleneck Testing Methods
    async createMinorBottleneck() {
      if (this.selectedDiscipleId === null) return;
      
      try {
        const response = await axios.post(`${this.apiBaseUrl}/disciples/${this.selectedDiscipleId}/create-bottleneck`, {
          type: 'minor',
          insights_required: 5
        });
        this.logApiCall(`/disciples/${this.selectedDiscipleId}/create-bottleneck`, response.data, true);
        this.fetchDiscipleDetails();
      } catch (error) {
        console.error('Error creating minor bottleneck:', error);
        this.logApiCall(`/disciples/${this.selectedDiscipleId}/create-bottleneck`, error.response && error.response.data ? error.response.data : error.message || error.message, false);
        alert('Failed to create minor bottleneck. Please check the API response log for details.');
      }
    },
    
    async createMajorBottleneck() {
      if (this.selectedDiscipleId === null) return;
      
      try {
        const response = await axios.post(`${this.apiBaseUrl}/disciples/${this.selectedDiscipleId}/create-bottleneck`, {
          type: 'major',
          insights_required: 0
        });
        this.logApiCall(`/disciples/${this.selectedDiscipleId}/create-bottleneck`, response.data, true);
        this.fetchDiscipleDetails();
      } catch (error) {
        console.error('Error creating major bottleneck:', error);
        this.logApiCall(`/disciples/${this.selectedDiscipleId}/create-bottleneck`, error.response && error.response.data ? error.response.data : error.message || error.message, false);
        alert('Failed to create major bottleneck. Please check the API response log for details.');
      }
    },
    
    async testCultivationAssignment() {
      if (this.selectedDiscipleId === null) return;
      
      try {
        // First, get available cultivation methods for this disciple
        const methodsResponse = await axios.get(`${this.apiBaseUrl}/disciples/${this.selectedDiscipleId}/cultivation-methods`);
        this.logApiCall(`/disciples/${this.selectedDiscipleId}/cultivation-methods`, methodsResponse.data, true);
        
        if (!methodsResponse.data.success) {
          alert('Failed to get cultivation methods. Please check the API response log for details.');
          return;
        }
        
        // Get the methods from the response
        const methods = methodsResponse.data.methods;
        const methodKeys = Object.keys(methods);
        
        if (methodKeys.length === 0) {
          alert('No cultivation methods available for this disciple.');
          return;
        }
        
        // Choose a random method
        const randomMethod = methodKeys[Math.floor(Math.random() * methodKeys.length)];
        
        // Assign the method with some resource allocation
        const assignResponse = await axios.post(`${this.apiBaseUrl}/disciples/${this.selectedDiscipleId}/assign-cultivation-method`, {
          method: randomMethod,
          resource_allocation: 100 // Allocate 100 spirit stones
        });
        
        this.logApiCall(`/disciples/${this.selectedDiscipleId}/assign-cultivation-method`, assignResponse.data, true);
        
        if (assignResponse.data.success) {
          alert(`Successfully assigned ${methods[randomMethod].name} cultivation method with 100 spirit stones allocation.`);
        } else {
          alert('Failed to assign cultivation method. Please check the API response log for details.');
        }
        
        // Refresh disciple details
        this.fetchDiscipleDetails();
      } catch (error) {
        console.error('Error testing cultivation assignment:', error);
        this.logApiCall('cultivation-assignment-test', error.response && error.response.data ? error.response.data : error.message || error.message, false);
        alert('Failed to test cultivation assignment. Please check the API response log for details.');
      }
    },
    
    async meditateForInsight() {
      if (this.selectedDiscipleId === null) return;
      
      try {
        const response = await axios.post(`${this.apiBaseUrl}/disciples/${this.selectedDiscipleId}/meditate`);
        this.logApiCall(`/disciples/${this.selectedDiscipleId}/meditate`, response.data, true);
        this.fetchDiscipleDetails();
      } catch (error) {
        console.error('Error meditating for insight:', error);
        this.logApiCall(`/disciples/${this.selectedDiscipleId}/meditate`, error.response && error.response.data ? error.response.data : error.message || error.message, false);
      }
    },
    
    async addTreasure() {
      try {
        const response = await axios.post(`${this.apiBaseUrl}/add-treasure`, {
          treasure_type: this.selectedTreasure,
          quantity: this.treasureQuantity
        });
        this.logApiCall('/add-treasure', response.data, true);
        this.fetchPlayerSect();
      } catch (error) {
        console.error('Error adding treasure:', error);
        this.logApiCall('/add-treasure', error.response && error.response.data ? error.response.data : error.message || error.message, false);
      }
    },
    
    async useTreasure() {
      if (this.selectedDiscipleId === null) return;
      
      try {
        const response = await axios.post(`${this.apiBaseUrl}/disciples/${this.selectedDiscipleId}/use-treasure`, {
          treasure_type: this.selectedTreasure
        });
        this.logApiCall(`/disciples/${this.selectedDiscipleId}/use-treasure`, response.data, true);
        this.fetchDiscipleDetails();
        this.fetchPlayerSect();
      } catch (error) {
        console.error('Error using treasure:', error);
        this.logApiCall(`/disciples/${this.selectedDiscipleId}/use-treasure`, error.response && error.response.data ? error.response.data : error.message || error.message, false);
      }
    },
    
    // Sect Methods
    async fetchPlayerSect() {
      try {
        const response = await axios.get(`${this.apiBaseUrl}/player-sect`);
        this.sectData = response.data;
        this.logApiCall('/player-sect', response.data, true);
      } catch (error) {
        console.error('Error fetching player sect:', error);
        this.logApiCall('/player-sect', error.response && error.response.data ? error.response.data : error.message || error.message, false);
      }
    },
    
    // Utility Methods
    calculateInsightProgress() {
      if (!this.selectedDisciple || !this.selectedDisciple.insights_required || this.selectedDisciple.insights_required === 0) {
        return 0;
      }
      return (this.selectedDisciple.bottleneck_insights / this.selectedDisciple.insights_required) * 100;
    },
    
    clearLog() {
      this.apiLog = [];
    }
  }
};
</script>

<style scoped>
.testing-dashboard {
  padding: 20px;
  max-width: 100%;
  margin: 0 auto;
  background-color: #f9f6f0;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.dashboard-layout {
  display: flex;
  gap: 20px;
  position: relative;
}

.main-column {
  flex: 1;
  min-width: 0; /* Allows column to shrink below content size */
}

.log-column {
  width: 400px;
  position: sticky;
  align-self: flex-start;
  top: 20px;
  max-height: calc(100vh - 40px);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.fixed-section {
  max-height: calc(100vh - 40px);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.dashboard-title {
  color: #8b4513;
  text-align: center;
  margin-bottom: 20px;
  font-size: 2rem;
  border-bottom: 2px solid #d4af37;
  padding-bottom: 10px;
}

.dashboard-section {
  margin-bottom: 30px;
  padding: 15px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 1px 5px rgba(0, 0, 0, 0.05);
}

.section-title {
  color: #8b4513;
  font-size: 1.5rem;
  margin-bottom: 15px;
  border-left: 4px solid #d4af37;
  padding-left: 10px;
}

.button-group {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 15px;
}

.action-button {
  background-color: #d4af37;
  color: white;
  border: none;
  padding: 8px 12px;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.9rem;
}

.action-button:hover {
  background-color: #b8860b;
  transform: translateY(-2px);
}

.action-button.danger {
  background-color: #e74c3c;
}

.action-button.danger:hover {
  background-color: #c0392b;
}

.action-button.primary {
  background-color: #3498db;
  font-weight: bold;
}

.action-button.primary:hover {
  background-color: #2980b9;
}

.data-display {
  background-color: #f5f5f5;
  border-radius: 4px;
  padding: 10px;
  max-height: 300px;
  overflow-y: auto;
  font-family: monospace;
  font-size: 0.9rem;
  margin-top: 10px;
}

.select-container {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 15px;
}

.select-input {
  padding: 8px;
  border-radius: 4px;
  border: 1px solid #ccc;
  flex-grow: 1;
}

.refresh-button {
  background-color: #4caf50;
  color: white;
  border: none;
  padding: 8px 12px;
  border-radius: 4px;
  cursor: pointer;
}

.attribute-controls, .bottleneck-controls {
  margin-top: 20px;
  padding: 15px;
  background-color: #f9f9f9;
  border-radius: 4px;
  border: 1px solid #eee;
}

.attribute-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 15px;
  margin-bottom: 15px;
}

.attribute-item {
  display: flex;
  flex-direction: column;
}

.number-input {
  padding: 8px;
  border-radius: 4px;
  border: 1px solid #ccc;
}

.bottleneck-actions {
  margin-top: 15px;
  padding: 10px;
  background-color: #fff;
  border-radius: 4px;
  border: 1px solid #eee;
}

.progress-display {
  margin-top: 10px;
}

.progress-bar {
  height: 10px;
  background-color: #f0f0f0;
  border-radius: 5px;
  overflow: hidden;
  margin-top: 5px;
}

.progress-fill {
  height: 100%;
  background-color: #4caf50;
  transition: width 0.3s ease;
}

.treasure-selection {
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.log-display {
  flex: 1;
  overflow-y: auto;
  margin-top: 10px;
  max-height: calc(100vh - 120px);
}

.log-entry {
  margin-bottom: 10px;
  padding: 10px;
  border-radius: 4px;
  border-left: 4px solid #ccc;
}

.log-entry.success {
  background-color: rgba(76, 175, 80, 0.1);
  border-left-color: #4caf50;
}

.log-entry.error {
  background-color: rgba(244, 67, 54, 0.1);
  border-left-color: #f44336;
}

.log-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 5px;
  font-size: 0.9rem;
}

.log-timestamp {
  color: #666;
}

.log-endpoint {
  font-weight: bold;
}

.log-status {
  font-weight: bold;
}

.log-status.success {
  color: #4caf50;
}

.log-status.error {
  color: #f44336;
}

.log-data {
  font-size: 0.8rem;
  margin: 0;
  white-space: pre-wrap;
}
</style>