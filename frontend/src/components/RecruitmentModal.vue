<template>
  <div v-if="show" class="modal-overlay" @click.self="closeModal">
    <div class="modal-container">
      <div class="modal-header">
        <h2 class="modal-title">Recruit New Disciples</h2>
        <button class="close-button" @click="closeModal">&times;</button>
      </div>
      
      <div class="modal-body">
        <div v-if="loading" class="loading-message">
          <div class="loading-icon">⏳</div>
          <div>Searching for potential disciples...</div>
        </div>
        
        <div v-else-if="error" class="error-message">
          {{ error }}
        </div>
        
        <div v-else class="candidates-container">
          <div v-for="candidate in candidates" :key="candidate.id" class="candidate-card">
            <div class="candidate-header">
              <h3 class="candidate-name">{{ candidate.name }}</h3>
              <div class="candidate-path">{{ candidate.path }} Path</div>
            </div>
            
            <div class="candidate-realm">{{ candidate.stage }} {{ candidate.realm }}</div>
            
            <div class="candidate-stats">
              <div class="stat-item">
                <span class="stat-label">Physical:</span>
                <span class="stat-value">{{ candidate.physical_foundation }}</span>
              </div>
              <div class="stat-item">
                <span class="stat-label">Spiritual:</span>
                <span class="stat-value">{{ candidate.spiritual_sensitivity }}</span>
              </div>
              <div class="stat-item">
                <span class="stat-label">Dao:</span>
                <span class="stat-value">{{ candidate.dao_comprehension }}</span>
              </div>
            </div>
            
            <div class="candidate-actions">
              <button 
                class="recruit-button" 
                @click="recruitDisciple(candidate)"
                :disabled="recruiting || spiritStones < recruitCost"
              >
                Recruit
              </button>
            </div>
          </div>
        </div>
      </div>
      
      <div class="modal-footer">
        <div class="cost-display">
          <span class="cost-label">Cost:</span>
          <span class="cost-value">{{ recruitCost }} Spirit Stones</span>
        </div>
        <div class="spirit-stones">
          <span class="stone-icon">💰</span>
          <span class="stone-count" :class="{ 'insufficient': spiritStones < recruitCost }">
            {{ formatNumber(spiritStones) }}
          </span>
        </div>
        <button class="refresh-button" @click="fetchCandidates" :disabled="loading || recruiting">
          Find New Candidates
        </button>
        <button class="cancel-button" @click="closeModal" :disabled="recruiting">Cancel</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'RecruitmentModal',
  props: {
    show: {
      type: Boolean,
      default: false
    },
    spiritStones: {
      type: Number,
      default: 0
    }
  },
  data() {
    return {
      candidates: [],
      loading: false,
      recruiting: false,
      error: null,
      recruitCost: 500 // Base cost to recruit a disciple
    }
  },
  watch: {
    show(newVal) {
      if (newVal) {
        this.fetchCandidates();
      }
    }
  },
  methods: {
    async fetchCandidates() {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await axios.get('http://localhost:5000/api/recruitment/candidates');
        this.candidates = response.data;
        this.loading = false;
      } catch (err) {
        this.error = 'Failed to find potential disciples. Please try again later.';
        this.loading = false;
        console.error(err);
      }
    },
    async recruitDisciple(candidate) {
      if (this.spiritStones < this.recruitCost) {
        this.error = 'Insufficient spirit stones for recruitment.';
        return;
      }
      
      this.recruiting = true;
      
      try {
        await axios.post('http://localhost:5000/api/recruitment/select', {
          candidate_id: candidate.id
        });
        
        this.$emit('disciple-recruited', {
          success: true,
          cost: this.recruitCost,
          disciple: candidate
        });
        
        this.closeModal();
      } catch (err) {
        this.error = 'Failed to recruit disciple. Please try again.';
        console.error(err);
      } finally {
        this.recruiting = false;
      }
    },
    closeModal() {
      if (!this.recruiting) {
        this.$emit('close');
      }
    },
    formatNumber(num) {
      return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    }
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-container {
  background-color: rgba(255, 248, 220, 0.95);
  border: 2px solid #d4af37;
  border-radius: 0.5rem;
  width: 90%;
  max-width: 900px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.5);
}

.modal-header {
  background-color: rgba(42, 107, 93, 0.9);
  padding: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-title {
  color: #f8f8f8;
  font-size: 1.5rem;
  margin: 0;
  font-family: 'Noto Serif SC', serif;
}

.close-button {
  background: none;
  border: none;
  color: #f8f8f8;
  font-size: 1.5rem;
  cursor: pointer;
}

.modal-body {
  padding: 1.5rem;
}

.candidates-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.candidate-card {
  background-color: rgba(255, 255, 255, 0.8);
  border: 1px solid #d4af37;
  border-radius: 0.5rem;
  padding: 1rem;
  transition: all 0.3s ease;
}

.candidate-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.candidate-header {
  border-bottom: 1px solid #d4af37;
  padding-bottom: 0.5rem;
  margin-bottom: 0.5rem;
}

.candidate-name {
  color: #2a6b5d;
  margin: 0 0 0.25rem;
  font-size: 1.2rem;
}

.candidate-path {
  color: #666;
  font-size: 0.9rem;
}

.candidate-realm {
  color: #8b4513;
  font-weight: bold;
  margin-bottom: 0.5rem;
}

.candidate-stats {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  font-size: 0.9rem;
}

.stat-label {
  color: #666;
}

.stat-value {
  color: #2a6b5d;
  font-weight: bold;
}

.candidate-actions {
  display: flex;
  justify-content: center;
}

.recruit-button {
  background-color: #2a6b5d;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0.25rem;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.3s ease;
}

.recruit-button:hover:not(:disabled) {
  background-color: #1a4b3d;
}

.recruit-button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.modal-footer {
  background-color: rgba(42, 107, 93, 0.2);
  padding: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top: 1px solid #d4af37;
}

.cost-display {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.cost-label {
  color: #666;
}

.cost-value {
  color: #d4af37;
  font-weight: bold;
}

.spirit-stones {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.stone-icon {
  color: #d4af37;
}

.stone-count {
  color: #2a6b5d;
  font-weight: bold;
}

.stone-count.insufficient {
  color: #a52a2a;
}

.refresh-button, .cancel-button {
  padding: 0.5rem 1rem;
  border-radius: 0.25rem;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.3s ease;
}

.refresh-button {
  background-color: #d4af37;
  color: #3a2718;
  border: none;
}

.refresh-button:hover:not(:disabled) {
  background-color: #c49b27;
}

.cancel-button {
  background-color: transparent;
  color: #3a2718;
  border: 1px solid #3a2718;
}

.cancel-button:hover:not(:disabled) {
  background-color: rgba(58, 39, 24, 0.1);
}

.refresh-button:disabled, .cancel-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.loading-message, .error-message {
  text-align: center;
  padding: 2rem;
}

.loading-icon {
  font-size: 2rem;
  margin-bottom: 1rem;
  animation: spin 2s infinite linear;
}

.error-message {
  color: #a52a2a;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

@media (max-width: 768px) {
  .modal-footer {
    flex-direction: column;
    gap: 1rem;
  }
  
  .candidates-container {
    grid-template-columns: 1fr;
  }
}
</style>
