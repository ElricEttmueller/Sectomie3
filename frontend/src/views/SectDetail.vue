<template>
  <div class="sect-detail-container">
    <div class="scroll-container">
      <div v-if="loading" class="loading">Loading sect information...</div>
      <div v-else-if="error" class="error">{{ error }}</div>
      <div v-else class="sect-info">
        <div class="sect-header">
          <h1 class="sect-name">{{ sect.name }}</h1>
          <div class="sect-tier">{{ getTierName(sect.tier) }} Tier {{ sect.dao_heritage }} Sect</div>
        </div>
        
        <div class="sect-description">{{ sect.description }}</div>
        
        <div class="sect-stats">
          <div class="stat-group">
            <div class="stat">
              <div class="stat-label">Spirit Stones</div>
              <div class="stat-value">{{ formatNumber(sect.spirit_stones) }}</div>
            </div>
            <div class="stat">
              <div class="stat-label">Influence</div>
              <div class="stat-value">{{ sect.sect_influence }}</div>
            </div>
            <div class="stat">
              <div class="stat-label">Formation Strength</div>
              <div class="stat-value">{{ sect.formation_strength }}</div>
            </div>
          </div>
        </div>
        
        <div class="sect-resources">
          <h2 class="section-title">Resources</h2>
          <div class="resource-list">
            <div class="resource">
              <div class="resource-label">Spirit Veins</div>
              <div class="resource-value">{{ sect.spirit_veins.length }}</div>
            </div>
            <div class="resource">
              <div class="resource-label">Elixir Fields</div>
              <div class="resource-value">{{ sect.elixir_fields }}</div>
            </div>
            <div class="resource">
              <div class="resource-label">Territories</div>
              <div class="resource-value">{{ sect.territories.length }}</div>
            </div>
          </div>
          
          <button class="action-button" @click="collectResources">Collect Resources</button>
          <div v-if="resourceMessage" class="resource-message">{{ resourceMessage }}</div>
        </div>
        
        <div class="sect-disciples">
          <h2 class="section-title">Disciples</h2>
          <div v-if="sect.disciples.length === 0" class="empty-message">This sect has no disciples yet.</div>
          <div v-else class="disciple-list">
            <div v-for="disciple in sect.disciples" :key="disciple.id" class="disciple-item" @click="viewDisciple(disciple.id)">
              {{ disciple.name }}
            </div>
          </div>
        </div>
        
        <div class="sect-techniques">
          <h2 class="section-title">Techniques</h2>
          <div v-if="sect.techniques.length === 0" class="empty-message">This sect has no techniques yet.</div>
          <div v-else class="technique-list">
            <div v-for="(technique, index) in sect.techniques" :key="index" class="technique-item">
              {{ technique }}
            </div>
          </div>
        </div>
        
        <div class="back-link">
          <router-link to="/">← Return to Sect Directory</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'SectDetail',
  props: {
    id: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      sect: {},
      loading: true,
      error: null,
      resourceMessage: null
    }
  },
  mounted() {
    this.fetchSectDetails();
  },
  methods: {
    async fetchSectDetails() {
      try {
        const response = await axios.get(`http://localhost:5000/api/sects/${this.id}`);
        this.sect = response.data;
        this.loading = false;
      } catch (err) {
        this.error = 'Failed to load sect details. The records are sealed.';
        this.loading = false;
        console.error(err);
      }
    },
    async collectResources() {
      try {
        const response = await axios.post(`http://localhost:5000/api/sects/${this.id}/collect-resources`);
        const { initial_stones, income, current_stones } = response.data;
        this.resourceMessage = `Collected ${this.formatNumber(income)} spirit stones from spirit veins. Total: ${this.formatNumber(current_stones)}`;
        this.sect.spirit_stones = current_stones;
      } catch (err) {
        this.resourceMessage = 'Failed to collect resources.';
        console.error(err);
      }
    },
    viewDisciple(id) {
      this.$router.push(`/disciple/${id}`);
    },
    getTierName(tier) {
      const tiers = [
        "Mortal",
        "Spirit Gathering",
        "Foundation",
        "Core",
        "Nascent",
        "Spirit",
        "Dao",
        "Immortal",
        "Celestial"
      ];
      
      if (tier >= 1 && tier <= tiers.length) {
        return tiers[tier - 1];
      }
      return "Unknown";
    },
    formatNumber(num) {
      return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    }
  }
}
</script>

<style scoped>
.sect-detail-container {
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

.sect-header {
  text-align: center;
  margin-bottom: 1.5rem;
  border-bottom: 2px solid #d4af37;
  padding-bottom: 1rem;
}

.sect-name {
  font-size: 2rem;
  color: #8b4513;
  margin-bottom: 0.5rem;
}

.sect-tier {
  font-size: 1.2rem;
  color: #8b4513;
}

.sect-description {
  font-style: italic;
  margin-bottom: 1.5rem;
  text-align: center;
  color: #555;
}

.sect-stats {
  margin-bottom: 1.5rem;
}

.stat-group {
  display: flex;
  justify-content: space-around;
  flex-wrap: wrap;
}

.stat {
  text-align: center;
  padding: 0.5rem;
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

.section-title {
  font-size: 1.3rem;
  color: #8b4513;
  margin: 1.5rem 0 0.5rem;
  border-left: 4px solid #d4af37;
  padding-left: 0.5rem;
}

.resource-list {
  display: flex;
  justify-content: space-around;
  margin-bottom: 1rem;
}

.resource {
  text-align: center;
}

.resource-label {
  font-size: 0.9rem;
  color: #666;
}

.resource-value {
  font-size: 1.1rem;
  font-weight: bold;
  color: #8b4513;
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
  margin: 0 auto;
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
  color: #8b4513;
}

.disciple-list, .technique-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.disciple-item, .technique-item {
  background-color: rgba(212, 175, 55, 0.1);
  border: 1px solid #d4af37;
  border-radius: 0.25rem;
  padding: 0.5rem;
  font-size: 0.9rem;
}

.disciple-item {
  cursor: pointer;
}

.disciple-item:hover {
  background-color: rgba(212, 175, 55, 0.3);
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
