<template>
  <div class="cultivation-assignment">
    <h2 class="section-title">Cultivation Assignment</h2>
    
    <div v-if="loading" class="loading">Loading cultivation methods...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    
    <div v-else class="assignment-container">
      <!-- Current Assignment Banner -->
      <div v-if="currentAssignment" class="current-assignment-banner">
        <div class="banner-content">
          <div class="banner-icon"><i class="fa fa-scroll"></i></div>
          <div class="banner-text">
            <div class="banner-title">Current Assignment</div>
            <div class="banner-details">{{ getMethodName(currentAssignment) }} with {{ currentResourceAllocation }} spirit stones</div>
          </div>
        </div>
      </div>
      <div class="method-selection">
        <h3>Available Methods</h3>
        <div class="methods-grid">
          <div 
            v-for="(method, key) in methods" 
            :key="key"
            class="method-card"
            :class="{ 
              'selected': selectedMethod === key,
              'effectiveness-1': method.effectiveness === 1,
              'effectiveness-2': method.effectiveness === 2,
              'effectiveness-3': method.effectiveness === 3,
              'effectiveness-4': method.effectiveness === 4,
              'effectiveness-5': method.effectiveness === 5
            }"
            @click="selectMethod(key)"
          >
            <div class="method-header">
              <span class="method-name">{{ method.name }}</span>
              <div class="effectiveness-stars">
                <span 
                  v-for="n in 5" 
                  :key="n" 
                  class="star"
                  :class="{ 'filled': n <= method.effectiveness }"
                >★</span>
              </div>
            </div>
            
            <div class="method-description">{{ method.description }}</div>
            
            <div class="method-recommendation">
              <strong>Recommended for:</strong> {{ method.recommended_for }}
            </div>
          </div>
        </div>
      </div>
      
      <div class="resource-allocation">
        <h3>Resource Allocation</h3>
        <div class="resource-info">
          <div class="spirit-stones-available">
            <span>Available Spirit Stones:</span>
            <span class="value">{{ sectResources.spirit_stones }}</span>
          </div>
        </div>
        
        <div class="allocation-slider">
          <label for="resource-slider">Allocate Spirit Stones:</label>
          <input 
            type="range" 
            id="resource-slider" 
            v-model.number="resourceAllocation" 
            min="0" 
            :max="maxAllocation"
            step="10"
          >
          <div class="allocation-value">{{ resourceAllocation }}</div>
        </div>
        
        <div class="allocation-effects">
          <h4>Monthly Benefits</h4>
          <div class="effect-item">
            <span class="effect-label">Cultivation Speed:</span>
            <span class="effect-value">+{{ calculateSpeedBonus() }}%</span>
          </div>
          <div class="effect-item">
            <span class="effect-label">Breakthrough Chance:</span>
            <span class="effect-value">+{{ calculateBreakthroughBonus() }}%</span>
          </div>
          <div class="effect-item">
            <span class="effect-label">Deviation Resistance:</span>
            <span class="effect-value">+{{ calculateDeviationResistance() }}%</span>
          </div>
        </div>
        
        <div class="cultivation-forecast">
          <h4>Monthly Forecast</h4>
          <div class="forecast-item">
            <span class="forecast-label">Est. Qi Gain:</span>
            <span class="forecast-value">{{ calculateEstimatedQiGain() }}</span>
          </div>
          <div class="forecast-item">
            <span class="forecast-label">Months to Breakthrough:</span>
            <span class="forecast-value">{{ calculateMonthsToBreakthrough() }}</span>
          </div>
          <div class="forecast-item">
            <span class="forecast-label">Resource Efficiency:</span>
            <span class="forecast-value" :class="resourceEfficiencyClass">{{ resourceEfficiencyRating }}</span>
          </div>
        </div>
      </div>
      
      <div class="selected-method-details" v-if="selectedMethod">
        <h3>Selected Method: {{ methods[selectedMethod].name }}</h3>
        
        <div class="method-scroll">
          <div class="method-scroll-content">
            {{ methods[selectedMethod].description }}
          </div>
        </div>
        
        <div class="details-grid">
          <div class="detail-item">
            <span class="detail-label">Effectiveness:</span>
            <div class="effectiveness-stars">
              <span 
                v-for="n in 5" 
                :key="n" 
                class="star"
                :class="{ 'filled': n <= methods[selectedMethod].effectiveness }"
              >★</span>
            </div>
          </div>
          
          <div class="detail-item">
            <span class="detail-label">Resource Boost:</span>
            <span class="detail-value">+{{ calculateSpeedBonus() }}%</span>
          </div>
        </div>
        
        <div class="method-attributes">
          <h4>Method Attributes</h4>
          <div class="attribute-grid">
            <div class="attribute-item">
              <div class="attribute-icon qi-icon"><i class="fa fa-bolt"></i></div>
              <div class="attribute-details">
                <div class="attribute-name">Qi Generation</div>
                <div class="attribute-rating">
                  <div class="rating-bar">
                    <div class="rating-fill" :style="{width: getMethodRating(selectedMethod, 'qi') + '%'}"></div>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="attribute-item">
              <div class="attribute-icon breakthrough-icon"><i class="fa fa-sync"></i></div>
              <div class="attribute-details">
                <div class="attribute-name">Breakthrough Bonus</div>
                <div class="attribute-rating">
                  <div class="rating-bar">
                    <div class="rating-fill" :style="{width: getMethodRating(selectedMethod, 'breakthrough') + '%'}"></div>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="attribute-item">
              <div class="attribute-icon safety-icon"><i class="fa fa-shield-alt"></i></div>
              <div class="attribute-details">
                <div class="attribute-name">Safety</div>
                <div class="attribute-rating">
                  <div class="rating-bar">
                    <div class="rating-fill" :style="{width: getMethodRating(selectedMethod, 'safety') + '%'}"></div>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="attribute-item">
              <div class="attribute-icon attribute-icon"><i class="fa fa-brain"></i></div>
              <div class="attribute-details">
                <div class="attribute-name">Attribute Growth</div>
                <div class="attribute-rating">
                  <div class="rating-bar">
                    <div class="rating-fill" :style="{width: getMethodRating(selectedMethod, 'attributes') + '%'}"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="method-compatibility">
          <h4>Compatibility with {{ discipleName }}</h4>
          <div class="compatibility-meter">
            <div class="compatibility-fill" :style="{width: calculateMethodCompatibility() + '%'}"></div>
            <div class="compatibility-label">{{ getCompatibilityRating() }}</div>
          </div>
          <div class="compatibility-notes">
            {{ getCompatibilityNotes() }}
          </div>
        </div>
      </div>
      
      <div class="assignment-actions">
        <button 
          class="assign-button" 
          @click="assignMethod" 
          :disabled="!selectedMethod || assigning"
        >
          {{ assigning ? 'Assigning...' : 'Assign Cultivation Method' }}
        </button>
        
        <button class="cancel-button" @click="$emit('cancel')">Cancel</button>
      </div>
      
      <div v-if="assignmentMessage" class="assignment-message" :class="{ 'success': assignmentSuccess, 'error': !assignmentSuccess }">
        {{ assignmentMessage }}
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'CultivationAssignment',
  props: {
    discipleId: {
      type: Number,
      required: true
    }
  },
  data() {
    return {
      loading: true,
      error: null,
      methods: {},
      selectedMethod: null,
      resourceAllocation: 0,
      sectResources: {
        spirit_stones: 0
      },
      assigning: false,
      assignmentMessage: '',
      assignmentSuccess: false,
      currentAssignment: null,
      currentResourceAllocation: 0,
      discipleName: '',
      discipleAttributes: {
        physical: 50,
        spiritual: 50,
        comprehension: 50
      },
      methodRatings: {
        'qi_circulation': { qi: 60, breakthrough: 50, safety: 80, attributes: 50 },
        'essence_refinement': { qi: 80, breakthrough: 40, safety: 30, attributes: 60 },
        'dao_heart_tempering': { qi: 40, breakthrough: 80, safety: 60, attributes: 70 },
        'foundation_building': { qi: 50, breakthrough: 60, safety: 90, attributes: 40 },
        'heavenly_tribulation': { qi: 90, breakthrough: 90, safety: 10, attributes: 80 }
      }
    };
  },
  computed: {
    maxAllocation() {
      return Math.min(this.sectResources.spirit_stones, 500);
    },
    resourceEfficiencyRating() {
      const allocation = this.resourceAllocation;
      if (allocation === 0) return 'N/A';
      
      // Calculate efficiency based on method effectiveness and allocation
      if (this.selectedMethod) {
        const effectiveness = this.methods[this.selectedMethod].effectiveness;
        const efficiency = (effectiveness * 20) / (allocation / 100);
        
        if (efficiency > 1.5) return 'Excellent';
        if (efficiency > 1.0) return 'Good';
        if (efficiency > 0.5) return 'Average';
        return 'Poor';
      }
      
      return 'N/A';
    },
    resourceEfficiencyClass() {
      const rating = this.resourceEfficiencyRating;
      if (rating === 'Excellent') return 'excellent';
      if (rating === 'Good') return 'good';
      if (rating === 'Average') return 'average';
      if (rating === 'Poor') return 'poor';
      return '';
    }
  },
  mounted() {
    this.fetchCultivationMethods();
    this.fetchSectResources();
    this.fetchDiscipleDetails();
  },
  methods: {
    fetchCultivationMethods() {
      this.loading = true;
      axios.get(`http://localhost:5000/api/disciples/${this.discipleId}/cultivation-methods`)
        .then(response => {
          if (response.data.success) {
            this.methods = response.data.methods;
            this.currentAssignment = response.data.disciple.assigned_method;
            this.currentResourceAllocation = response.data.disciple.resource_allocation || 0;
            this.resourceAllocation = response.data.disciple.resource_allocation || 0;
            
            // Pre-select the current method if one is assigned
            if (this.currentAssignment) {
              this.selectedMethod = this.currentAssignment;
            }
            
            this.loading = false;
          } else {
            this.error = response.data.message;
            this.loading = false;
          }
        })
        .catch(error => {
          this.error = `Error fetching cultivation methods: ${error.message}`;
          this.loading = false;
        });
    },
    
    fetchSectResources() {
      axios.get('http://localhost:5000/api/player-sect/resources')
        .then(response => {
          this.sectResources = response.data;
        })
        .catch(error => {
          console.error('Error fetching sect resources:', error);
        });
    },
    
    selectMethod(methodKey) {
      this.selectedMethod = methodKey;
      this.assignmentMessage = '';
    },
    
    fetchDiscipleDetails() {
      axios.get(`http://localhost:5000/api/disciples/${this.discipleId}`)
        .then(response => {
          this.discipleName = response.data.name;
          this.discipleAttributes = {
            physical: response.data.physical,
            spiritual: response.data.spiritual,
            comprehension: response.data.comprehension
          };
        })
        .catch(error => {
          console.error('Error fetching disciple details:', error);
        });
    },
    
    calculateSpeedBonus() {
      return this.resourceAllocation / 10; // Each 10 spirit stones gives 1% boost
    },
    
    calculateBreakthroughBonus() {
      return Math.floor(this.resourceAllocation / 20); // Each 20 spirit stones gives 1% breakthrough chance
    },
    
    calculateDeviationResistance() {
      return Math.floor(this.resourceAllocation / 25); // Each 25 spirit stones gives 1% deviation resistance
    },
    
    calculateEstimatedQiGain() {
      if (!this.selectedMethod) return 'N/A';
      
      const baseGain = 50; // Base qi gain per month
      const methodEffectiveness = this.methods[this.selectedMethod].effectiveness;
      const spiritualBonus = this.discipleAttributes.spiritual / 100;
      const resourceBonus = 1 + (this.resourceAllocation / 1000);
      
      const estimatedGain = baseGain * methodEffectiveness * spiritualBonus * resourceBonus;
      return Math.floor(estimatedGain);
    },
    
    calculateMonthsToBreakthrough() {
      if (!this.selectedMethod) return 'N/A';
      
      const estimatedQiGain = this.calculateEstimatedQiGain();
      if (estimatedQiGain === 'N/A' || estimatedQiGain <= 0) return 'N/A';
      
      // Assuming a disciple needs 1000 qi for breakthrough (simplified calculation)
      const qiNeeded = 1000;
      const months = Math.ceil(qiNeeded / estimatedQiGain);
      
      return months > 36 ? '36+' : months;
    },
    
    getMethodRating(methodKey, attribute) {
      if (this.methodRatings[methodKey] && this.methodRatings[methodKey][attribute]) {
        return this.methodRatings[methodKey][attribute];
      }
      return 50; // Default to 50%
    },
    
    calculateMethodCompatibility() {
      if (!this.selectedMethod) return 50;
      
      const method = this.selectedMethod;
      const attributes = this.discipleAttributes;
      
      let compatibility = 50; // Base compatibility
      
      // Different methods favor different attributes
      if (method === 'qi_circulation') {
        // Balanced method - favors balanced attributes
        const balance = 100 - (Math.abs(attributes.physical - attributes.spiritual) + 
                            Math.abs(attributes.spiritual - attributes.comprehension) + 
                            Math.abs(attributes.comprehension - attributes.physical)) / 3;
        compatibility += balance / 2;
      } else if (method === 'essence_refinement') {
        // Favors spiritual
        compatibility += (attributes.spiritual - 50) * 0.8;
      } else if (method === 'dao_heart_tempering') {
        // Favors comprehension
        compatibility += (attributes.comprehension - 50) * 0.8;
      } else if (method === 'foundation_building') {
        // Favors physical
        compatibility += (attributes.physical - 50) * 0.8;
      } else if (method === 'heavenly_tribulation') {
        // Favors high comprehension and spiritual
        compatibility += ((attributes.comprehension + attributes.spiritual) / 2 - 50) * 0.8;
      }
      
      // Ensure compatibility is between 0 and 100
      return Math.min(100, Math.max(0, compatibility));
    },
    
    getCompatibilityRating() {
      const compatibility = this.calculateMethodCompatibility();
      
      if (compatibility >= 90) return 'Perfect Match';
      if (compatibility >= 75) return 'Excellent';
      if (compatibility >= 60) return 'Good';
      if (compatibility >= 40) return 'Average';
      if (compatibility >= 25) return 'Poor';
      return 'Incompatible';
    },
    
    getMethodName(methodKey) {
      if (!methodKey || !this.methods || !this.methods[methodKey]) {
        return 'None';
      }
      return this.methods[methodKey].name;
    },
    
    getCompatibilityNotes() {
      if (!this.selectedMethod) return '';
      
      const method = this.selectedMethod;
      const attributes = this.discipleAttributes;
      const compatibility = this.calculateMethodCompatibility();
      
      if (compatibility >= 75) {
        return `This method is well-suited for ${this.discipleName}'s attributes and cultivation base.`;
      }
      
      if (method === 'qi_circulation' && Math.abs(attributes.physical - attributes.spiritual) > 30) {
        return `${this.discipleName}'s attributes are imbalanced. This method works best with balanced attributes.`;
      } else if (method === 'essence_refinement' && attributes.spiritual < 50) {
        return `${this.discipleName}'s spiritual attribute is too low for optimal results with this method.`;
      } else if (method === 'dao_heart_tempering' && attributes.comprehension < 50) {
        return `${this.discipleName}'s comprehension attribute is too low for optimal results with this method.`;
      } else if (method === 'foundation_building' && attributes.physical < 50) {
        return `${this.discipleName}'s physical attribute is too low for optimal results with this method.`;
      } else if (method === 'heavenly_tribulation' && (attributes.comprehension + attributes.spiritual) / 2 < 60) {
        return `${this.discipleName}'s spiritual and comprehension attributes are too low for this dangerous method.`;
      }
      
      return `This method provides average results for ${this.discipleName}'s current cultivation base.`;
    },
    
    assignMethod() {
      if (!this.selectedMethod) return;
      
      this.assigning = true;
      this.assignmentMessage = '';
      
      axios.post(`http://localhost:5000/api/disciples/${this.discipleId}/assign-cultivation-method`, {
        method: this.selectedMethod,
        resource_allocation: this.resourceAllocation
      })
        .then(response => {
          if (response.data.success) {
            this.assignmentSuccess = true;
            this.assignmentMessage = response.data.message;
            this.currentAssignment = this.selectedMethod;
            
            // Update available spirit stones
            this.fetchSectResources();
            
            // Emit success event
            this.$emit('assigned', {
              method: this.selectedMethod,
              resourceAllocation: this.resourceAllocation
            });
          } else {
            this.assignmentSuccess = false;
            this.assignmentMessage = response.data.message;
          }
          this.assigning = false;
        })
        .catch(error => {
          this.assignmentSuccess = false;
          this.assignmentMessage = `Error assigning cultivation method: ${error.message}`;
          this.assigning = false;
        });
    }
  }
};
</script>

<style scoped>
.cultivation-assignment {
  background-color: rgba(255, 248, 220, 0.9);
  border: 1px solid #d4af37;
  border-radius: 0.5rem;
  padding: 1.5rem;
  max-width: 900px;
  margin: 0 auto;
  font-family: 'Arial', sans-serif;
}

.section-title {
  font-size: 1.5rem;
  color: #8b4513;
  margin-bottom: 1.5rem;
  text-align: center;
  border-bottom: 2px solid #d4af37;
  padding-bottom: 0.5rem;
}

.assignment-container {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.method-selection h3,
.resource-allocation h3,
.selected-method-details h3 {
  font-size: 1.2rem;
  color: #8b4513;
  margin-bottom: 0.75rem;
  border-left: 4px solid #d4af37;
  padding-left: 0.5rem;
}

.methods-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1rem;
  margin-bottom: 1rem;
}

.method-card {
  background-color: rgba(255, 255, 255, 0.7);
  border: 1px solid #d4af37;
  border-radius: 0.25rem;
  padding: 1rem;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.method-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.method-card.selected {
  background-color: rgba(212, 175, 55, 0.2);
  border: 2px solid #d4af37;
}

.method-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.method-name {
  font-weight: bold;
  color: #8b4513;
}

.effectiveness-stars {
  display: flex;
}

.star {
  color: #ccc;
  margin-left: 2px;
}

.star.filled {
  color: #d4af37;
}

.method-description {
  font-size: 0.9rem;
  color: #555;
  margin-bottom: 0.75rem;
  flex-grow: 1;
}

.method-recommendation {
  font-size: 0.8rem;
  color: #666;
  font-style: italic;
}

.resource-allocation {
  background-color: rgba(255, 255, 255, 0.7);
  border: 1px solid #d4af37;
  border-radius: 0.25rem;
  padding: 1rem;
}

.resource-info {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1rem;
}

.spirit-stones-available {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.value {
  font-weight: bold;
  color: #d4af37;
}

.allocation-slider {
  display: flex;
  flex-direction: column;
  margin-bottom: 1rem;
}

.allocation-slider label {
  margin-bottom: 0.5rem;
  color: #555;
}

.allocation-value {
  text-align: center;
  font-weight: bold;
  color: #8b4513;
  margin-top: 0.5rem;
}

.allocation-effects {
  background-color: rgba(255, 255, 255, 0.5);
  border-radius: 0.25rem;
  padding: 0.75rem;
}

.effect-item {
  display: flex;
  justify-content: space-between;
}

.effect-label {
  color: #555;
}

.effect-value {
  font-weight: bold;
  color: #4caf50;
}

.selected-method-details {
  background-color: rgba(255, 255, 255, 0.7);
  border: 1px solid #d4af37;
  border-radius: 0.25rem;
  padding: 1rem;
}

.details-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-bottom: 1rem;
}

/* Current Assignment Banner */
.current-assignment-banner {
  background-color: rgba(212, 175, 55, 0.15);
  border: 1px solid #d4af37;
  border-radius: 0.25rem;
  padding: 0.75rem;
  margin-bottom: 1.5rem;
}

.banner-content {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.banner-icon {
  font-size: 1.5rem;
  color: #d4af37;
}

.banner-title {
  font-weight: bold;
  color: #8b4513;
  margin-bottom: 0.25rem;
}

.banner-details {
  color: #666;
  font-size: 0.9rem;
}

/* Method Scroll */
.method-scroll {
  background-color: rgba(255, 248, 220, 0.7);
  border: 1px solid #d4af37;
  border-radius: 0.25rem;
  padding: 1rem;
  margin-bottom: 1rem;
  max-height: 100px;
  overflow-y: auto;
  position: relative;
}

.method-scroll::before {
  content: '"'; /* Opening quote */
  font-size: 2rem;
  color: rgba(212, 175, 55, 0.3);
  position: absolute;
  top: 0;
  left: 0.5rem;
}

.method-scroll::after {
  content: '"'; /* Closing quote */
  font-size: 2rem;
  color: rgba(212, 175, 55, 0.3);
  position: absolute;
  bottom: 0;
  right: 0.5rem;
}

.method-scroll-content {
  font-style: italic;
  color: #555;
  padding: 0 1.5rem;
  text-align: center;
}

/* Method Attributes */
.method-attributes,
.method-compatibility,
.cultivation-forecast {
  background-color: rgba(255, 255, 255, 0.7);
  border: 1px solid #d4af37;
  border-radius: 0.25rem;
  padding: 1rem;
  margin-top: 1rem;
}

.method-attributes h4,
.method-compatibility h4,
.cultivation-forecast h4,
.allocation-effects h4 {
  font-size: 1rem;
  color: #8b4513;
  margin-bottom: 0.75rem;
  border-bottom: 1px solid rgba(212, 175, 55, 0.3);
  padding-bottom: 0.25rem;
}

.attribute-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.attribute-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.attribute-icon {
  font-size: 1.25rem;
  width: 2rem;
  height: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: rgba(212, 175, 55, 0.2);
  border-radius: 50%;
}

.attribute-details {
  flex-grow: 1;
}

.attribute-name {
  font-size: 0.85rem;
  color: #555;
  margin-bottom: 0.25rem;
}

.attribute-rating {
  width: 100%;
}

.rating-bar {
  height: 0.5rem;
  background-color: rgba(0, 0, 0, 0.1);
  border-radius: 0.25rem;
  overflow: hidden;
}

.rating-fill {
  height: 100%;
  background-color: #d4af37;
  border-radius: 0.25rem;
}

/* Compatibility Meter */
.compatibility-meter {
  height: 1rem;
  background-color: rgba(0, 0, 0, 0.1);
  border-radius: 0.5rem;
  overflow: hidden;
  position: relative;
  margin-bottom: 0.5rem;
}

.compatibility-fill {
  height: 100%;
  background: linear-gradient(to right, #f44336, #ffc107, #4caf50);
  border-radius: 0.5rem;
}

.compatibility-label {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: white;
  font-size: 0.75rem;
  font-weight: bold;
  text-shadow: 0 0 2px rgba(0, 0, 0, 0.5);
}

.compatibility-notes {
  font-size: 0.85rem;
  color: #666;
  font-style: italic;
  text-align: center;
  padding: 0.5rem;
  background-color: rgba(255, 255, 255, 0.5);
  border-radius: 0.25rem;
}

/* Forecast Items */
.forecast-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px dotted rgba(212, 175, 55, 0.3);
}

.forecast-item:last-child {
  margin-bottom: 0;
  padding-bottom: 0;
  border-bottom: none;
}

.forecast-label {
  color: #555;
}

.forecast-value {
  font-weight: bold;
  color: #8b4513;
}

.forecast-value.excellent {
  color: #4caf50;
}

.forecast-value.good {
  color: #8bc34a;
}

.forecast-value.average {
  color: #ffc107;
}

.forecast-value.poor {
  color: #f44336;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.detail-label {
  color: #555;
}

.detail-value {
  font-weight: bold;
  color: #4caf50;
}

.assignment-actions {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-top: 1rem;
}

.assign-button, .cancel-button {
  padding: 0.75rem 1.5rem;
  border-radius: 0.25rem;
  border: none;
  cursor: pointer;
  font-weight: bold;
  transition: all 0.2s ease;
}

.assign-button {
  background-color: #d4af37;
  color: white;
}

.assign-button:hover:not(:disabled) {
  background-color: #b8860b;
  transform: translateY(-2px);
}

.assign-button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.cancel-button {
  background-color: #f5f5f5;
  color: #555;
  border: 1px solid #ccc;
}

.cancel-button:hover {
  background-color: #e5e5e5;
}

.assignment-message {
  text-align: center;
  margin-top: 1rem;
  padding: 0.75rem;
  border-radius: 0.25rem;
}

.assignment-message.success {
  background-color: rgba(76, 175, 80, 0.2);
  border: 1px solid rgba(76, 175, 80, 0.5);
  color: #2e7d32;
}

.assignment-message.error {
  background-color: rgba(244, 67, 54, 0.2);
  border: 1px solid rgba(244, 67, 54, 0.5);
  color: #c62828;
}

.loading, .error {
  text-align: center;
  padding: 2rem;
  color: #8b4513;
}

.error {
  color: #a52a2a;
}

/* Effectiveness color indicators */
.effectiveness-1 {
  border-left: 5px solid #f44336; /* Red */
}

.effectiveness-2 {
  border-left: 5px solid #ff9800; /* Orange */
}

.effectiveness-3 {
  border-left: 5px solid #ffc107; /* Yellow */
}

.effectiveness-4 {
  border-left: 5px solid #8bc34a; /* Light Green */
}

.effectiveness-5 {
  border-left: 5px solid #4caf50; /* Green */
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .methods-grid {
    grid-template-columns: 1fr;
  }
  
  .details-grid {
    grid-template-columns: 1fr;
  }
}
</style>
