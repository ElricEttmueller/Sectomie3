<template>
  <div class="sect-view">
    <div class="page-header">
      <h1>Sect Management</h1>
      <p>Manage your sect's resources, facilities, and overall development</p>
    </div>
    
    <div class="sect-content">
      <div class="sect-info-card">
        <div class="sect-name">{{ sectName }}</div>
        <div class="sect-level">Level {{ sectLevel }} Sect</div>
        <div class="sect-reputation">Reputation: {{ sectReputation }}</div>
        
        <div class="sect-stats">
          <div class="stat">
            <div class="stat-label">Disciples</div>
            <div class="stat-value">{{ disciples.length }}</div>
          </div>
          <div class="stat">
            <div class="stat-label">Territories</div>
            <div class="stat-value">{{ territories.length }}</div>
          </div>
          <div class="stat">
            <div class="stat-label">Resources</div>
            <div class="stat-value">{{ resourceTypes.length }} Types</div>
          </div>
        </div>
      </div>
      
      <div class="sect-actions">
        <h2>Sect Actions</h2>
        <div class="action-buttons">
          <button class="action-button">
            <i class="fa fa-building"></i>
            Upgrade Facilities
          </button>
          <button class="action-button">
            <i class="fa fa-users"></i>
            Manage Disciples
          </button>
          <button class="action-button">
            <i class="fa fa-map-marked"></i>
            Explore Territories
          </button>
          <button class="action-button">
            <i class="fa fa-scroll"></i>
            Research Methods
          </button>
        </div>
      </div>
      
      <div class="sect-facilities">
        <h2>Sect Facilities</h2>
        <div class="facilities-grid">
          <div v-for="(facility, index) in facilities" :key="index" class="facility-card">
            <div class="facility-name">{{ facility.name }}</div>
            <div class="facility-level">Level {{ facility.level }}</div>
            <div class="facility-description">{{ facility.description }}</div>
            <div class="facility-effects">
              <div v-for="(effect, effectIndex) in facility.effects" :key="effectIndex" class="effect">
                {{ effect }}
              </div>
            </div>
            <button class="upgrade-button" v-if="facility.canUpgrade">Upgrade</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SectView',
  data() {
    return {
      sectName: 'Azure Peak Sect',
      sectLevel: 3,
      sectReputation: 'Rising',
      disciples: [
        { id: 1, name: 'Li Mei' },
        { id: 2, name: 'Zhang Wei' },
        { id: 3, name: 'Hui Wu' },
        { id: 4, name: 'Ling Zhou' },
        { id: 5, name: 'Ji Mei' }
      ],
      territories: [
        { id: 1, name: 'Azure Peak' },
        { id: 2, name: 'Mystic Cloud' },
        { id: 3, name: 'Verdant Valley' }
      ],
      resourceTypes: [
        { id: 1, name: 'Spirit Stones' },
        { id: 2, name: 'Herbs' },
        { id: 3, name: 'Treasures' }
      ],
      facilities: [
        {
          name: 'Main Hall',
          level: 3,
          description: 'The central administrative building of the sect',
          effects: ['+10% Sect Reputation', '+5 Maximum Disciples'],
          canUpgrade: true
        },
        {
          name: 'Cultivation Chamber',
          level: 2,
          description: 'A specialized chamber for disciples to cultivate',
          effects: ['+15% Cultivation Speed', '+5% Breakthrough Chance'],
          canUpgrade: true
        },
        {
          name: 'Alchemy Lab',
          level: 1,
          description: 'Facility for creating pills and elixirs',
          effects: ['+10% Pill Effectiveness', 'Unlock Basic Pill Recipes'],
          canUpgrade: true
        },
        {
          name: 'Spirit Garden',
          level: 2,
          description: 'Garden for growing spiritual herbs and plants',
          effects: ['+20 Herbs per month', '+5% Herb Quality'],
          canUpgrade: true
        }
      ]
    }
  },
  methods: {
    // Methods will be implemented as needed
  },
  mounted() {
    // Fetch sect data from API
    console.log('SectView mounted, would fetch sect data here');
  }
}
</script>

<style scoped>
.sect-view {
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

.sect-content {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.sect-info-card {
  background-color: rgba(0, 0, 0, 0.5);
  border: 1px solid rgba(212, 175, 55, 0.3);
  border-radius: 0.5rem;
  padding: 1.5rem;
  color: #e0e0e0;
}

.sect-name {
  font-size: 1.5rem;
  color: #d4af37;
  margin-bottom: 0.5rem;
}

.sect-level {
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
}

.sect-reputation {
  margin-bottom: 1rem;
}

.sect-stats {
  display: flex;
  gap: 2rem;
  margin-top: 1rem;
}

.stat {
  text-align: center;
}

.stat-label {
  font-size: 0.9rem;
  color: #a0a0a0;
  margin-bottom: 0.25rem;
}

.stat-value {
  font-size: 1.25rem;
  color: #d4af37;
}

.sect-actions, .sect-facilities {
  background-color: rgba(0, 0, 0, 0.5);
  border: 1px solid rgba(212, 175, 55, 0.3);
  border-radius: 0.5rem;
  padding: 1.5rem;
}

.sect-actions h2, .sect-facilities h2 {
  color: #d4af37;
  font-size: 1.25rem;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid rgba(212, 175, 55, 0.3);
}

.action-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
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

.facilities-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-top: 1rem;
}

.facility-card {
  background-color: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(212, 175, 55, 0.3);
  border-radius: 0.25rem;
  padding: 1rem;
  transition: all 0.2s ease;
}

.facility-card:hover {
  border-color: rgba(212, 175, 55, 0.6);
  transform: translateY(-2px);
}

.facility-name {
  font-size: 1.1rem;
  color: #d4af37;
  margin-bottom: 0.25rem;
}

.facility-level {
  font-size: 0.9rem;
  color: #a0a0a0;
  margin-bottom: 0.5rem;
}

.facility-description {
  font-size: 0.9rem;
  margin-bottom: 0.75rem;
}

.facility-effects {
  margin-bottom: 1rem;
}

.effect {
  font-size: 0.85rem;
  color: #7fbf7f;
  margin-bottom: 0.25rem;
}

.upgrade-button {
  background-color: rgba(212, 175, 55, 0.3);
  border: 1px solid rgba(212, 175, 55, 0.5);
  color: #d4af37;
  padding: 0.5rem;
  border-radius: 0.25rem;
  cursor: pointer;
  width: 100%;
  transition: all 0.2s ease;
}

.upgrade-button:hover {
  background-color: rgba(212, 175, 55, 0.4);
}

@media (max-width: 768px) {
  .sect-stats {
    flex-direction: column;
    gap: 1rem;
  }
  
  .facilities-grid {
    grid-template-columns: 1fr;
  }
}
</style>
