<template>
  <div class="territories-view">
    <div class="page-header">
      <h1>Territories</h1>
      <p>Manage and explore your sect's territories and resources</p>
    </div>
    
    <div class="territories-content">
      <div class="territories-stats">
        <div class="stat-card">
          <div class="stat-title">Total Territories</div>
          <div class="stat-value">{{ territories.length }}</div>
        </div>
        <div class="stat-card">
          <div class="stat-title">Resource Nodes</div>
          <div class="stat-value">{{ totalResourceNodes }}</div>
        </div>
        <div class="stat-card">
          <div class="stat-title">Monthly Income</div>
          <div class="stat-value">{{ monthlyIncome }} <i class="fa fa-gem"></i></div>
        </div>
        <div class="stat-card">
          <div class="stat-title">Exploration Points</div>
          <div class="stat-value">{{ explorationPoints }}</div>
        </div>
      </div>
      
      <div class="territory-actions">
        <button class="action-button">
          <i class="fa fa-search"></i>
          Explore New Territory
        </button>
        <button class="action-button">
          <i class="fa fa-hammer"></i>
          Build Structure
        </button>
        <button class="action-button">
          <i class="fa fa-shield-alt"></i>
          Defend Territory
        </button>
        <button class="action-button">
          <i class="fa fa-users"></i>
          Assign Disciples
        </button>
      </div>
      
      <div class="territories-map">
        <h2>Territory Map</h2>
        <div class="map-container">
          <div class="map-grid">
            <div v-for="(territory, index) in territories" :key="index" 
                 class="territory-tile" 
                 :class="{ 'active': selectedTerritory === territory.id }"
                 @click="selectTerritory(territory.id)">
              <div class="territory-icon">
                <i :class="`fa ${territory.icon}`"></i>
              </div>
              <div class="territory-name">{{ territory.name }}</div>
            </div>
          </div>
        </div>
      </div>
      
      <div v-if="selectedTerritory" class="territory-detail">
        <div class="detail-header">
          <h2>{{ selectedTerritoryData.name }}</h2>
          <div class="territory-type">{{ selectedTerritoryData.type }} Territory</div>
        </div>
        
        <div class="detail-content">
          <div class="detail-description">{{ selectedTerritoryData.description }}</div>
          
          <div class="detail-stats">
            <div class="detail-stat">
              <div class="stat-label">Level</div>
              <div class="stat-value">{{ selectedTerritoryData.level }}</div>
            </div>
            <div class="detail-stat">
              <div class="stat-label">Resource Quality</div>
              <div class="stat-value">{{ selectedTerritoryData.resourceQuality }}</div>
            </div>
            <div class="detail-stat">
              <div class="stat-label">Security</div>
              <div class="stat-value">{{ selectedTerritoryData.security }}</div>
            </div>
            <div class="detail-stat">
              <div class="stat-label">Development</div>
              <div class="stat-value">{{ selectedTerritoryData.development }}%</div>
            </div>
          </div>
          
          <div class="resource-nodes">
            <h3>Resource Nodes</h3>
            <div class="nodes-grid">
              <div v-for="(node, nodeIndex) in selectedTerritoryData.resourceNodes" :key="nodeIndex" class="node-card">
                <div class="node-icon">
                  <i :class="`fa ${node.icon}`"></i>
                </div>
                <div class="node-info">
                  <div class="node-name">{{ node.name }}</div>
                  <div class="node-yield">Yield: {{ node.yield }}</div>
                  <div class="node-quality">Quality: {{ node.quality }}</div>
                </div>
              </div>
            </div>
          </div>
          
          <div class="territory-structures">
            <h3>Structures</h3>
            <div class="structures-grid">
              <div v-for="(structure, structureIndex) in selectedTerritoryData.structures" :key="structureIndex" class="structure-card">
                <div class="structure-name">{{ structure.name }}</div>
                <div class="structure-level">Level {{ structure.level }}</div>
                <div class="structure-effect">{{ structure.effect }}</div>
              </div>
              <div class="empty-structure-slot" v-if="selectedTerritoryData.structures.length < 3">
                <i class="fa fa-plus"></i>
                <div>Build New Structure</div>
              </div>
            </div>
          </div>
          
          <div class="assigned-disciples">
            <h3>Assigned Disciples</h3>
            <div class="disciples-list">
              <div v-for="(disciple, discipleIndex) in selectedTerritoryData.assignedDisciples" :key="discipleIndex" class="assigned-disciple">
                <div class="disciple-name">{{ disciple.name }}</div>
                <div class="disciple-task">{{ disciple.task }}</div>
                <button class="remove-button">
                  <i class="fa fa-times"></i>
                </button>
              </div>
              <div class="empty-disciple-slot" v-if="selectedTerritoryData.assignedDisciples.length < 3">
                <i class="fa fa-user-plus"></i>
                <div>Assign Disciple</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TerritoriesView',
  data() {
    return {
      selectedTerritory: null,
      explorationPoints: 5,
      territories: [
        {
          id: 1,
          name: 'Azure Peak',
          type: 'Mountain',
          icon: 'fa-mountain',
          description: 'The main mountain where your sect is located. Rich in spiritual energy and natural resources.',
          level: 3,
          resourceQuality: 'High',
          security: 'Secure',
          development: 75,
          resourceNodes: [
            { name: 'Spirit Stone Vein', icon: 'fa-gem', yield: '100/month', quality: 'High' },
            { name: 'Herb Garden', icon: 'fa-leaf', yield: '20/month', quality: 'Medium' },
            { name: 'Spirit Spring', icon: 'fa-tint', yield: 'Special', quality: 'High' }
          ],
          structures: [
            { name: 'Main Sect Hall', level: 3, effect: '+15% Sect Reputation' },
            { name: 'Disciple Dormitories', level: 2, effect: '+5 Max Disciples' }
          ],
          assignedDisciples: [
            { name: 'Li Mei', task: 'Managing Resources' },
            { name: 'Hui Wu', task: 'Patrolling' }
          ]
        },
        {
          id: 2,
          name: 'Mystic Cloud',
          type: 'Sky',
          icon: 'fa-cloud',
          description: 'A mysterious area high in the clouds, accessible only to flying cultivators. Contains rare treasures.',
          level: 2,
          resourceQuality: 'Very High',
          security: 'Vulnerable',
          development: 35,
          resourceNodes: [
            { name: 'Lightning Essence', icon: 'fa-bolt', yield: '30/month', quality: 'Very High' },
            { name: 'Cloud Silk', icon: 'fa-wind', yield: '10/month', quality: 'High' }
          ],
          structures: [
            { name: 'Sky Pavilion', level: 1, effect: '+20% Lightning Cultivation' }
          ],
          assignedDisciples: [
            { name: 'Zhang Wei', task: 'Gathering Resources' }
          ]
        },
        {
          id: 3,
          name: 'Verdant Valley',
          type: 'Forest',
          icon: 'fa-tree',
          description: 'A lush valley filled with medicinal herbs and plants. Perfect for alchemy and healing.',
          level: 2,
          resourceQuality: 'Medium',
          security: 'Moderate',
          development: 50,
          resourceNodes: [
            { name: 'Herb Fields', icon: 'fa-seedling', yield: '50/month', quality: 'High' },
            { name: 'Spirit Beast Habitat', icon: 'fa-paw', yield: 'Special', quality: 'Medium' },
            { name: 'Clear Stream', icon: 'fa-water', yield: '15/month', quality: 'Medium' }
          ],
          structures: [
            { name: 'Alchemy Lab', level: 2, effect: '+25% Pill Effectiveness' },
            { name: 'Beast Taming Area', level: 1, effect: '+10% Beast Taming Success' }
          ],
          assignedDisciples: [
            { name: 'Ling Zhou', task: 'Herb Gathering' }
          ]
        }
      ]
    }
  },
  computed: {
    totalResourceNodes() {
      return this.territories.reduce((total, territory) => {
        return total + territory.resourceNodes.length;
      }, 0);
    },
    monthlyIncome() {
      // This is a placeholder calculation
      return 250;
    },
    selectedTerritoryData() {
      if (!this.selectedTerritory) return null;
      return this.territories.find(t => t.id === this.selectedTerritory);
    }
  },
  methods: {
    selectTerritory(id) {
      this.selectedTerritory = id;
    }
  },
  mounted() {
    // Set default selected territory
    if (this.territories.length > 0) {
      this.selectedTerritory = this.territories[0].id;
    }
    
    // Fetch territories data from API
    console.log('TerritoriesView mounted, would fetch territories data here');
  }
}
</script>

<style scoped>
.territories-view {
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

.territories-content {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.territories-stats {
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

.territory-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
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

.territories-map {
  background-color: rgba(0, 0, 0, 0.5);
  border: 1px solid rgba(212, 175, 55, 0.3);
  border-radius: 0.5rem;
  padding: 1.5rem;
}

.territories-map h2 {
  color: #d4af37;
  margin-bottom: 1.5rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid rgba(212, 175, 55, 0.3);
}

.map-container {
  overflow-x: auto;
}

.map-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 1.5rem;
  padding: 1rem;
}

.territory-tile {
  background-color: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(212, 175, 55, 0.3);
  border-radius: 0.5rem;
  padding: 1.5rem 1rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.territory-tile:hover {
  transform: translateY(-5px);
  border-color: rgba(212, 175, 55, 0.6);
}

.territory-tile.active {
  background-color: rgba(212, 175, 55, 0.2);
  border-color: #d4af37;
}

.territory-icon {
  font-size: 2rem;
  color: #d4af37;
  margin-bottom: 1rem;
}

.territory-name {
  color: #e0e0e0;
  font-weight: bold;
}

.territory-detail {
  background-color: rgba(0, 0, 0, 0.5);
  border: 1px solid rgba(212, 175, 55, 0.3);
  border-radius: 0.5rem;
  padding: 1.5rem;
}

.detail-header {
  margin-bottom: 1.5rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid rgba(212, 175, 55, 0.3);
}

.detail-header h2 {
  color: #d4af37;
  margin-bottom: 0.5rem;
}

.territory-type {
  color: #a0a0a0;
}

.detail-content {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.detail-description {
  color: #e0e0e0;
  line-height: 1.6;
}

.detail-stats {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 1rem;
  background-color: rgba(0, 0, 0, 0.3);
  border-radius: 0.5rem;
  padding: 1rem;
}

.detail-stat {
  text-align: center;
}

.stat-label {
  color: #a0a0a0;
  font-size: 0.8rem;
  margin-bottom: 0.25rem;
}

.stat-value {
  color: #d4af37;
  font-size: 1.1rem;
}

.resource-nodes h3,
.territory-structures h3,
.assigned-disciples h3 {
  color: #d4af37;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid rgba(212, 175, 55, 0.3);
}

.nodes-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1rem;
}

.node-card {
  background-color: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(212, 175, 55, 0.3);
  border-radius: 0.5rem;
  padding: 1rem;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.node-icon {
  font-size: 1.5rem;
  color: #d4af37;
}

.node-name {
  color: #e0e0e0;
  font-weight: bold;
  margin-bottom: 0.25rem;
}

.node-yield, .node-quality {
  font-size: 0.8rem;
  color: #a0a0a0;
}

.structures-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1rem;
}

.structure-card {
  background-color: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(212, 175, 55, 0.3);
  border-radius: 0.5rem;
  padding: 1rem;
}

.structure-name {
  color: #d4af37;
  font-weight: bold;
  margin-bottom: 0.25rem;
}

.structure-level {
  font-size: 0.8rem;
  color: #a0a0a0;
  margin-bottom: 0.5rem;
}

.structure-effect {
  font-size: 0.9rem;
  color: #7fbf7f;
}

.empty-structure-slot {
  background-color: rgba(0, 0, 0, 0.2);
  border: 1px dashed rgba(212, 175, 55, 0.3);
  border-radius: 0.5rem;
  padding: 1rem;
  text-align: center;
  color: #a0a0a0;
  cursor: pointer;
  transition: all 0.2s ease;
}

.empty-structure-slot i {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
}

.empty-structure-slot:hover {
  border-color: rgba(212, 175, 55, 0.6);
  color: #d4af37;
}

.disciples-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1rem;
}

.assigned-disciple {
  background-color: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(212, 175, 55, 0.3);
  border-radius: 0.5rem;
  padding: 1rem;
  position: relative;
}

.disciple-name {
  color: #d4af37;
  font-weight: bold;
  margin-bottom: 0.5rem;
}

.disciple-task {
  font-size: 0.9rem;
  color: #e0e0e0;
}

.remove-button {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  background: none;
  border: none;
  color: #a0a0a0;
  cursor: pointer;
  transition: all 0.2s ease;
}

.remove-button:hover {
  color: #ff6b6b;
}

.empty-disciple-slot {
  background-color: rgba(0, 0, 0, 0.2);
  border: 1px dashed rgba(212, 175, 55, 0.3);
  border-radius: 0.5rem;
  padding: 1rem;
  text-align: center;
  color: #a0a0a0;
  cursor: pointer;
  transition: all 0.2s ease;
}

.empty-disciple-slot i {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
}

.empty-disciple-slot:hover {
  border-color: rgba(212, 175, 55, 0.6);
  color: #d4af37;
}

@media (max-width: 992px) {
  .nodes-grid,
  .structures-grid,
  .disciples-list {
    grid-template-columns: 1fr 1fr;
  }
}

@media (max-width: 768px) {
  .territory-actions {
    flex-direction: column;
  }
  
  .nodes-grid,
  .structures-grid,
  .disciples-list {
    grid-template-columns: 1fr;
  }
}
</style>
