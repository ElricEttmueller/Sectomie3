<template>
  <div class="cultivation-view">
    <div class="page-header">
      <h1>Cultivation System</h1>
      <p>Manage cultivation methods and assignments for your disciples</p>
    </div>
    
    <div class="cultivation-content">
      <div class="cultivation-stats">
        <div class="stat-card">
          <div class="stat-title">Available Methods</div>
          <div class="stat-value">{{ cultivationMethods.length }}</div>
        </div>
        <div class="stat-card">
          <div class="stat-title">Sect Cultivation Bonus</div>
          <div class="stat-value">+{{ sectCultivationBonus }}%</div>
        </div>
        <div class="stat-card">
          <div class="stat-title">Spirit Stone Efficiency</div>
          <div class="stat-value">{{ spiritStoneEfficiency }}</div>
        </div>
        <div class="stat-card">
          <div class="stat-title">Breakthrough Rate</div>
          <div class="stat-value">{{ breakthroughRate }}</div>
        </div>
      </div>
      
      <div class="cultivation-tabs">
        <div class="tab" :class="{ active: activeTab === 'disciples' }" @click="activeTab = 'disciples'">
          <i class="fa fa-users"></i>
          Disciple Assignments
        </div>
        <div class="tab" :class="{ active: activeTab === 'methods' }" @click="activeTab = 'methods'">
          <i class="fa fa-book"></i>
          Cultivation Methods
        </div>
        <div class="tab" :class="{ active: activeTab === 'resources' }" @click="activeTab = 'resources'">
          <i class="fa fa-gem"></i>
          Resource Allocation
        </div>
      </div>
      
      <!-- Disciples Tab -->
      <div v-if="activeTab === 'disciples'" class="tab-content">
        <div class="disciples-assignments">
          <div v-for="disciple in disciples" :key="disciple.id" class="assignment-card">
            <div class="disciple-info">
              <div class="disciple-name">{{ disciple.name }}</div>
              <div class="disciple-realm">{{ disciple.realm_name }} ({{ disciple.stage_name }})</div>
              <div class="qi-progress">
                <div class="qi-bar">
                  <div class="qi-fill" :style="{ width: `${(disciple.qi / disciple.max_qi) * 100}%` }"></div>
                </div>
                <div class="qi-text">{{ Math.floor(disciple.qi) }} / {{ disciple.max_qi }} Qi</div>
              </div>
            </div>
            
            <div class="assignment-info">
              <div class="method-name">{{ disciple.assigned_method || 'No Method Assigned' }}</div>
              <div class="method-effectiveness" v-if="disciple.assigned_method">
                Effectiveness: 
                <span class="rating">
                  <i v-for="n in 5" :key="n" class="fa" 
                     :class="n <= disciple.method_effectiveness ? 'fa-star' : 'fa-star-o'"></i>
                </span>
              </div>
              <div class="resource-allocation" v-if="disciple.assigned_method">
                <i class="fa fa-gem"></i> {{ disciple.spirit_stones_allocated }} Spirit Stones/month
              </div>
            </div>
            
            <div class="assignment-actions">
              <router-link :to="`/cultivation/${disciple.id}`" class="assign-button">
                <i class="fa fa-edit"></i>
                Assign Method
              </router-link>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Methods Tab -->
      <div v-if="activeTab === 'methods'" class="tab-content">
        <div class="methods-grid">
          <div v-for="(method, index) in cultivationMethods" :key="index" class="method-card">
            <div class="method-header">
              <div class="method-name">{{ method.name }}</div>
              <div class="method-type">{{ method.type }} Method</div>
            </div>
            
            <div class="method-description">{{ method.description }}</div>
            
            <div class="method-attributes">
              <div class="attribute">
                <div class="attribute-label">Qi Generation</div>
                <div class="attribute-rating">
                  <i v-for="n in 5" :key="n" class="fa" 
                     :class="n <= method.qi_generation ? 'fa-star' : 'fa-star-o'"></i>
                </div>
              </div>
              <div class="attribute">
                <div class="attribute-label">Breakthrough</div>
                <div class="attribute-rating">
                  <i v-for="n in 5" :key="n" class="fa" 
                     :class="n <= method.breakthrough ? 'fa-star' : 'fa-star-o'"></i>
                </div>
              </div>
              <div class="attribute">
                <div class="attribute-label">Safety</div>
                <div class="attribute-rating">
                  <i v-for="n in 5" :key="n" class="fa" 
                     :class="n <= method.safety ? 'fa-star' : 'fa-star-o'"></i>
                </div>
              </div>
              <div class="attribute">
                <div class="attribute-label">Attribute Growth</div>
                <div class="attribute-rating">
                  <i v-for="n in 5" :key="n" class="fa" 
                     :class="n <= method.attribute_growth ? 'fa-star' : 'fa-star-o'"></i>
                </div>
              </div>
            </div>
            
            <div class="method-requirements">
              <div class="requirement" v-for="(req, reqIndex) in method.requirements" :key="reqIndex">
                <i class="fa fa-check-circle" v-if="req.met"></i>
                <i class="fa fa-times-circle" v-else></i>
                {{ req.description }}
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Resources Tab -->
      <div v-if="activeTab === 'resources'" class="tab-content">
        <div class="resources-allocation">
          <div class="resource-summary">
            <h3>Monthly Resource Allocation</h3>
            <div class="summary-stats">
              <div class="summary-stat">
                <div class="stat-label">Total Spirit Stones</div>
                <div class="stat-value">{{ totalSpiritStones }}</div>
              </div>
              <div class="summary-stat">
                <div class="stat-label">Allocated</div>
                <div class="stat-value">{{ allocatedSpiritStones }}</div>
              </div>
              <div class="summary-stat">
                <div class="stat-label">Remaining</div>
                <div class="stat-value">{{ remainingSpiritStones }}</div>
              </div>
            </div>
          </div>
          
          <div class="allocation-table">
            <div class="table-header">
              <div class="header-disciple">Disciple</div>
              <div class="header-method">Method</div>
              <div class="header-allocation">Allocation</div>
              <div class="header-efficiency">Efficiency</div>
            </div>
            
            <div v-for="disciple in disciples" :key="disciple.id" class="allocation-row">
              <div class="row-disciple">{{ disciple.name }}</div>
              <div class="row-method">{{ disciple.assigned_method || 'None' }}</div>
              <div class="row-allocation">
                <i class="fa fa-gem"></i> {{ disciple.spirit_stones_allocated }}
              </div>
              <div class="row-efficiency">
                {{ disciple.efficiency || 'N/A' }}
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
import { EventBus } from '../services/eventBus';

export default {
  name: 'CultivationView',
  data() {
    return {
      activeTab: 'disciples',
      sectCultivationBonus: 0,
      spiritStoneEfficiency: 'Unknown',
      breakthroughRate: 'Unknown',
      totalSpiritStones: 0,
      allocatedSpiritStones: 0,
      disciples: [],
      cultivationMethods: [
        {
          name: 'Azure Flame Refinement',
          type: 'Fire',
          description: 'A powerful fire-based cultivation method that refines the body and spirit through intense heat.',
          qi_generation: 4,
          breakthrough: 3,
          safety: 2,
          attribute_growth: 5,
          requirements: [
            { description: 'Fire Affinity', met: true },
            { description: 'Foundation Establishment Realm', met: true }
          ]
        },
        {
          name: 'Water Ripple Meditation',
          type: 'Water',
          description: 'A gentle yet profound method that circulates qi like flowing water, building a solid foundation.',
          qi_generation: 3,
          breakthrough: 4,
          safety: 5,
          attribute_growth: 2,
          requirements: [
            { description: 'Water Affinity', met: true },
            { description: 'Qi Condensation Realm', met: true }
          ]
        },
        {
          name: 'Mountain Heart Stance',
          type: 'Earth',
          description: 'Builds a powerful physical foundation by emulating the stability and strength of mountains.',
          qi_generation: 2,
          breakthrough: 3,
          safety: 5,
          attribute_growth: 4,
          requirements: [
            { description: 'Earth Affinity', met: true },
            { description: 'Physical > 30', met: true }
          ]
        },
        {
          name: 'Wind Walking Method',
          type: 'Wind',
          description: 'A swift cultivation method that enhances agility and spiritual perception.',
          qi_generation: 3,
          breakthrough: 4,
          safety: 3,
          attribute_growth: 3,
          requirements: [
            { description: 'Wind Affinity', met: true },
            { description: 'Spiritual > 30', met: true }
          ]
        },
        {
          name: 'Thunder Essence Gathering',
          type: 'Lightning',
          description: 'Harnesses the power of lightning to rapidly increase qi but with higher risks.',
          qi_generation: 5,
          breakthrough: 5,
          safety: 1,
          attribute_growth: 3,
          requirements: [
            { description: 'Lightning Affinity', met: true },
            { description: 'Comprehension > 30', met: true }
          ]
        },
        {
          name: 'Five Elements Harmony',
          type: 'Balanced',
          description: 'A balanced method that cultivates all aspects evenly, suitable for most disciples.',
          qi_generation: 3,
          breakthrough: 3,
          safety: 4,
          attribute_growth: 3,
          requirements: [
            { description: 'No specific affinity required', met: true },
            { description: 'Balanced attributes', met: true }
          ]
        }
      ]
    }
  },
  computed: {
    remainingSpiritStones() {
      return this.totalSpiritStones - this.allocatedSpiritStones;
    }
  },
  methods: {
    async fetchSectData() {
      try {
        const response = await axios.get('http://localhost:5000/api/player-sect');
        if (response.data) {
          this.totalSpiritStones = response.data.spirit_stones || 0;
          
          // Calculate sect cultivation bonus based on facilities
          const cultivationChambers = response.data.cultivation_chambers || 0;
          this.sectCultivationBonus = cultivationChambers * 5; // 5% bonus per chamber
          
          // Determine breakthrough rate based on sect facilities
          if (response.data.technique_manuals && response.data.technique_manuals.length > 0) {
            this.breakthroughRate = 'Good';
          } else if (cultivationChambers > 0) {
            this.breakthroughRate = 'Average';
          } else {
            this.breakthroughRate = 'Poor';
          }
        }
      } catch (error) {
        console.error('Error fetching sect data:', error);
      }
    },
    
    async fetchDisciplesData() {
      try {
        const response = await axios.get('http://localhost:5000/api/disciples');
        if (response.data) {
          // Get detailed information for each disciple
          const disciplePromises = response.data.map(async (disciple) => {
            try {
              // Get detailed disciple info
              const discipleResponse = await axios.get(`http://localhost:5000/api/disciples/${disciple.id}`);
              
              // Get cultivation methods for this disciple
              const methodsResponse = await axios.get(`http://localhost:5000/api/disciples/${disciple.id}/cultivation-methods`);
              
              const discipleData = discipleResponse.data;
              const assignedMethod = methodsResponse.data.disciple.assigned_method;
              const methodEffectiveness = assignedMethod && methodsResponse.data.methods[assignedMethod] ? 
                methodsResponse.data.methods[assignedMethod].effectiveness : 0;
              
              return {
                id: disciple.id,
                name: discipleData.name,
                realm_name: discipleData.realm_name,
                stage_name: discipleData.stage_name,
                qi: discipleData.qi,
                max_qi: discipleData.max_qi,
                assigned_method: assignedMethod ? methodsResponse.data.methods[assignedMethod].name : null,
                method_effectiveness: methodEffectiveness,
                spirit_stones_allocated: methodsResponse.data.disciple.resource_allocation || 0,
                efficiency: this.getEfficiencyRating(methodEffectiveness)
              };
            } catch (error) {
              console.error(`Error fetching details for disciple ${disciple.id}:`, error);
              return null;
            }
          });
          
          const disciplesData = await Promise.all(disciplePromises);
          this.disciples = disciplesData.filter(d => d !== null);
          
          // Calculate total allocated spirit stones
          this.allocatedSpiritStones = this.disciples.reduce((total, disciple) => {
            return total + (disciple.spirit_stones_allocated || 0);
          }, 0);
        }
      } catch (error) {
        console.error('Error fetching disciples data:', error);
      }
    },
    
    getEfficiencyRating(effectiveness) {
      if (effectiveness >= 5) return 'Excellent';
      if (effectiveness >= 4) return 'Good';
      if (effectiveness >= 3) return 'Average';
      if (effectiveness >= 2) return 'Poor';
      return 'Very Poor';
    }
  },
  
  mounted() {
    this.fetchSectData();
    this.fetchDisciplesData();
    
    // Listen for turn-ended events from other components
    EventBus.$on('turn-ended', () => {
      console.log('Turn ended event received in CultivationView, refreshing data');
      // Refresh all data after a turn ends
      this.fetchSectData();
      this.fetchDisciplesData();
    });
  },
  
  beforeDestroy() {
    // Clean up event listeners when component is destroyed
    EventBus.$off('turn-ended');
  }
}
</script>

<style scoped>
.cultivation-view {
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

.cultivation-content {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.cultivation-stats {
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

.cultivation-tabs {
  display: flex;
  background-color: rgba(0, 0, 0, 0.5);
  border: 1px solid rgba(212, 175, 55, 0.3);
  border-radius: 0.5rem 0.5rem 0 0;
  overflow: hidden;
}

.tab {
  padding: 1rem 1.5rem;
  color: #e0e0e0;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.2s ease;
}

.tab:hover {
  background-color: rgba(212, 175, 55, 0.1);
}

.tab.active {
  background-color: rgba(212, 175, 55, 0.2);
  color: #d4af37;
  border-bottom: 2px solid #d4af37;
}

.tab-content {
  background-color: rgba(0, 0, 0, 0.5);
  border: 1px solid rgba(212, 175, 55, 0.3);
  border-top: none;
  border-radius: 0 0 0.5rem 0.5rem;
  padding: 1.5rem;
}

/* Disciples Tab Styles */
.disciples-assignments {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.assignment-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(212, 175, 55, 0.3);
  border-radius: 0.5rem;
  padding: 1rem;
  transition: all 0.2s ease;
}

.assignment-card:hover {
  border-color: rgba(212, 175, 55, 0.6);
}

.disciple-info {
  flex: 1;
}

.disciple-name {
  color: #d4af37;
  font-weight: bold;
  margin-bottom: 0.25rem;
}

.disciple-realm {
  font-size: 0.9rem;
  color: #e0e0e0;
  margin-bottom: 0.5rem;
}

.qi-progress {
  width: 100%;
  max-width: 200px;
}

.qi-bar {
  height: 0.5rem;
  background-color: rgba(0, 0, 0, 0.3);
  border-radius: 0.25rem;
  overflow: hidden;
  margin-bottom: 0.25rem;
}

.qi-fill {
  height: 100%;
  background-color: #4a90e2;
  border-radius: 0.25rem;
}

.qi-text {
  font-size: 0.8rem;
  color: #a0a0a0;
}

.assignment-info {
  flex: 1;
  padding: 0 1rem;
}

.method-name {
  color: #d4af37;
  margin-bottom: 0.5rem;
}

.method-effectiveness {
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}

.rating {
  color: #ffd700;
}

.resource-allocation {
  font-size: 0.9rem;
  color: #a0a0a0;
}

.assignment-actions {
  flex: 0 0 auto;
}

.assign-button {
  background-color: rgba(212, 175, 55, 0.2);
  border: 1px solid rgba(212, 175, 55, 0.5);
  color: #d4af37;
  padding: 0.75rem 1.25rem;
  border-radius: 0.25rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  text-decoration: none;
  transition: all 0.2s ease;
}

.assign-button:hover {
  background-color: rgba(212, 175, 55, 0.3);
  transform: translateY(-2px);
}

/* Methods Tab Styles */
.methods-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.method-card {
  background-color: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(212, 175, 55, 0.3);
  border-radius: 0.5rem;
  padding: 1rem;
  transition: all 0.2s ease;
}

.method-card:hover {
  border-color: rgba(212, 175, 55, 0.6);
  transform: translateY(-2px);
}

.method-header {
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid rgba(212, 175, 55, 0.3);
}

.method-name {
  color: #d4af37;
  font-weight: bold;
  margin-bottom: 0.25rem;
}

.method-type {
  font-size: 0.9rem;
  color: #a0a0a0;
}

.method-description {
  margin-bottom: 1rem;
  font-size: 0.9rem;
  color: #e0e0e0;
}

.method-attributes {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-bottom: 1rem;
}

.attribute-label {
  font-size: 0.8rem;
  color: #a0a0a0;
  margin-bottom: 0.25rem;
}

.attribute-rating {
  color: #ffd700;
  font-size: 0.9rem;
}

.method-requirements {
  margin-top: 1rem;
  padding-top: 0.5rem;
  border-top: 1px solid rgba(212, 175, 55, 0.3);
}

.requirement {
  font-size: 0.9rem;
  margin-bottom: 0.25rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.fa-check-circle {
  color: #90ee90;
}

.fa-times-circle {
  color: #ff6b6b;
}

/* Resources Tab Styles */
.resources-allocation {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.resource-summary {
  background-color: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(212, 175, 55, 0.3);
  border-radius: 0.5rem;
  padding: 1rem;
}

.resource-summary h3 {
  color: #d4af37;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid rgba(212, 175, 55, 0.3);
}

.summary-stats {
  display: flex;
  justify-content: space-around;
}

.summary-stat {
  text-align: center;
}

.stat-label {
  font-size: 0.9rem;
  color: #a0a0a0;
  margin-bottom: 0.5rem;
}

.stat-value {
  font-size: 1.25rem;
  color: #d4af37;
}

.allocation-table {
  background-color: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(212, 175, 55, 0.3);
  border-radius: 0.5rem;
  overflow: hidden;
}

.table-header {
  display: grid;
  grid-template-columns: 2fr 2fr 1fr 1fr;
  padding: 1rem;
  background-color: rgba(0, 0, 0, 0.3);
  color: #d4af37;
  font-weight: bold;
  border-bottom: 1px solid rgba(212, 175, 55, 0.3);
}

.allocation-row {
  display: grid;
  grid-template-columns: 2fr 2fr 1fr 1fr;
  padding: 1rem;
  border-bottom: 1px solid rgba(0, 0, 0, 0.3);
  transition: all 0.2s ease;
  color: #e0e0e0;
}

.allocation-row:hover {
  background-color: rgba(212, 175, 55, 0.1);
}

.allocation-row:last-child {
  border-bottom: none;
}

.row-disciple {
  color: #d4af37;
}

@media (max-width: 992px) {
  .methods-grid {
    grid-template-columns: 1fr;
  }
  
  .table-header, .allocation-row {
    grid-template-columns: 2fr 2fr 1fr;
  }
  
  .header-efficiency, .row-efficiency {
    display: none;
  }
}

@media (max-width: 768px) {
  .cultivation-tabs {
    flex-direction: column;
  }
  
  .assignment-card {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .assignment-info {
    padding: 0;
  }
  
  .table-header, .allocation-row {
    grid-template-columns: 1fr 1fr;
  }
  
  .header-allocation, .row-allocation {
    display: none;
  }
  
  .summary-stats {
    flex-direction: column;
    gap: 1rem;
  }
}
</style>
