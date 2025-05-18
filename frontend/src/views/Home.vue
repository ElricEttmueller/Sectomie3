<template>
  <div class="home-container">
    <div class="scroll-container">
      <div class="scroll-header">
        <div class="scroll-title">Immortal Sects Directory</div>
      </div>
      
      <div class="scroll-content">
        <div class="section">
          <h2 class="section-title">Cultivation Sects</h2>
          <div v-if="loading" class="loading">Loading sects information...</div>
          <div v-else-if="error" class="error">{{ error }}</div>
          <div v-else class="sect-list">
            <div v-for="sect in sects" :key="sect.id" class="sect-card" @click="viewSect(sect.id)">
              <div class="sect-name">{{ sect.name }}</div>
              <div class="sect-heritage">{{ sect.dao_heritage }}</div>
              <div class="sect-tier">{{ getTierName(sect.tier) }} Tier</div>
              <div class="sect-info">
                <span>Disciples: {{ sect.disciples_count }}</span>
                <span>Spirit Stones: {{ formatNumber(sect.spirit_stones) }}</span>
              </div>
            </div>
          </div>
        </div>
        
        <div class="section">
          <h2 class="section-title">Disciples Registry</h2>
          <div v-if="loadingDisciples" class="loading">Loading disciples information...</div>
          <div v-else-if="errorDisciples" class="error">{{ errorDisciples }}</div>
          <div v-else class="disciple-list">
            <div v-for="disciple in disciples" :key="disciple.id" class="disciple-card" @click="viewDisciple(disciple.id)">
              <div class="disciple-name">{{ disciple.name }}</div>
              <div class="disciple-path">{{ disciple.path }} Path</div>
              <div class="disciple-realm">{{ disciple.stage }} {{ disciple.realm }}</div>
              <div class="disciple-sect">{{ disciple.sect || 'Rogue Cultivator' }}</div>
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
  name: 'Home',
  data() {
    return {
      sects: [],
      disciples: [],
      loading: true,
      loadingDisciples: true,
      error: null,
      errorDisciples: null
    }
  },
  mounted() {
    this.fetchSects();
    this.fetchDisciples();
  },
  methods: {
    async fetchSects() {
      try {
        const response = await axios.get('http://localhost:5000/api/sects');
        this.sects = response.data;
        this.loading = false;
      } catch (err) {
        this.error = 'Failed to load sects. The heavenly dao is in chaos.';
        this.loading = false;
        console.error(err);
      }
    },
    async fetchDisciples() {
      try {
        const response = await axios.get('http://localhost:5000/api/disciples');
        this.disciples = response.data;
        this.loadingDisciples = false;
      } catch (err) {
        this.errorDisciples = 'Failed to load disciples. The records are sealed.';
        this.loadingDisciples = false;
        console.error(err);
      }
    },
    viewSect(id) {
      this.$router.push(`/sect/${id}`);
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
.home-container {
  width: 100%;
  max-width: 1200px;
  display: flex;
  justify-content: center;
}

.scroll-container {
  background-image: url('/assets/backgrounds/scroll.png');
  background-size: 100% 100%;
  width: 90%;
  max-width: 900px;
  min-height: 600px;
  padding: 3rem 4rem;
  position: relative;
  color: #3a3a3a;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
}

.scroll-header {
  text-align: center;
  margin-bottom: 2rem;
  border-bottom: 2px solid #d4af37;
  padding-bottom: 1rem;
}

.scroll-title {
  font-family: 'Ma Shan Zheng', cursive;
  font-size: 2.5rem;
  color: #8b4513;
}

.section {
  margin-bottom: 2rem;
}

.section-title {
  font-size: 1.5rem;
  color: #8b4513;
  margin-bottom: 1rem;
  border-left: 4px solid #d4af37;
  padding-left: 0.5rem;
}

.sect-list, .disciple-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1rem;
}

.sect-card, .disciple-card {
  background-color: rgba(255, 248, 220, 0.7);
  border: 1px solid #d4af37;
  border-radius: 0.5rem;
  padding: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.sect-card:hover, .disciple-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
  background-color: rgba(255, 248, 220, 0.9);
}

.sect-name, .disciple-name {
  font-size: 1.2rem;
  font-weight: bold;
  color: #8b4513;
  margin-bottom: 0.5rem;
}

.sect-heritage, .disciple-path {
  font-size: 0.9rem;
  color: #555;
  margin-bottom: 0.25rem;
}

.sect-tier, .disciple-realm {
  font-size: 0.9rem;
  color: #8b4513;
  margin-bottom: 0.5rem;
}

.sect-info {
  display: flex;
  justify-content: space-between;
  font-size: 0.8rem;
  color: #666;
}

.disciple-sect {
  font-size: 0.8rem;
  color: #666;
  font-style: italic;
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
