<template>
  <div class="bottleneck-visualizer" v-if="disciple && disciple.bottleneck !== 'none'">
    <div class="bottleneck-container" :class="disciple.bottleneck">
      <div class="bottleneck-icon">
        <span v-if="disciple.bottleneck === 'minor'" class="icon">🔸</span>
        <span v-else-if="disciple.bottleneck === 'major'" class="icon">🔶</span>
      </div>
      
      <div class="bottleneck-content">
        <div class="bottleneck-header">
          <h3 class="bottleneck-title">
            {{ disciple.bottleneck === 'minor' ? 'Minor' : 'Major' }} Bottleneck
          </h3>
          <div class="bottleneck-realm">
            {{ disciple.realm_name }} ({{ disciple.stage_name }})
          </div>
        </div>
        
        <div class="bottleneck-description">
          <p>{{ getBottleneckDescription() }}</p>
        </div>
        
        <div v-if="disciple.bottleneck === 'minor'" class="insight-progress">
          <div class="progress-label">
            <span>Insights: {{ disciple.bottleneck_insights || 0 }}/{{ disciple.insights_required || 0 }}</span>
            <span class="percentage">{{ calculateInsightPercentage() }}%</span>
          </div>
          <div class="progress-bar">
            <div class="progress-fill" :style="{ width: `${calculateInsightPercentage()}%` }"></div>
          </div>
          <div class="progress-steps">
            <div v-for="step in getInsightSteps()" :key="step.position" 
                 class="step" 
                 :class="{ active: step.active }"
                 :style="{ left: `${step.position}%` }">
              <div class="step-marker"></div>
              <div class="step-label">{{ step.label }}</div>
            </div>
          </div>
        </div>
        
        <div v-if="disciple.bottleneck === 'major'" class="treasure-info">
          <div class="treasure-recommendation">
            <h4>Recommended Treasures:</h4>
            <ul class="treasure-list">
              <li v-for="treasure in getRecommendedTreasures()" :key="treasure.id" class="treasure-item">
                <span class="treasure-icon">{{ treasure.icon }}</span>
                <span class="treasure-name">{{ treasure.name }}</span>
              </li>
            </ul>
          </div>
        </div>
        
        <div class="bottleneck-actions">
          <slot name="actions"></slot>
        </div>
      </div>
    </div>
  </div>
  <div v-else-if="disciple" class="no-bottleneck">
    <div class="status-message">
      <span class="status-icon">✓</span>
      <span>No cultivation bottlenecks detected</span>
    </div>
  </div>
</template>

<script>
export default {
  name: 'BottleneckVisualizer',
  props: {
    disciple: {
      type: Object,
      required: true
    }
  },
  methods: {
    calculateInsightPercentage() {
      if (!this.disciple || this.disciple.bottleneck !== 'minor' || !this.disciple.insights_required) {
        return 0;
      }
      return Math.round((this.disciple.bottleneck_insights / this.disciple.insights_required) * 100);
    },
    
    getInsightSteps() {
      if (!this.disciple || !this.disciple.insights_required) {
        return [];
      }
      
      const totalSteps = this.disciple.insights_required;
      const steps = [];
      
      for (let i = 0; i <= totalSteps; i++) {
        const position = (i / totalSteps) * 100;
        steps.push({
          position,
          label: i === 0 ? 'Start' : i === totalSteps ? 'Breakthrough' : `${i}`,
          active: i <= this.disciple.bottleneck_insights
        });
      }
      
      return steps;
    },
    
    getBottleneckDescription() {
      if (!this.disciple) return '';
      
      const realmName = this.disciple.realm_name;
      const stageName = this.disciple.stage_name;
      
      if (this.disciple.bottleneck === 'minor') {
        return `Your cultivation has reached a minor bottleneck at ${stageName} stage of ${realmName} realm. Through meditation and gaining insights, you can overcome this obstacle and continue your advancement.`;
      } else if (this.disciple.bottleneck === 'major') {
        return `You've encountered a major bottleneck at ${stageName} stage of ${realmName} realm. This requires special treasures or external assistance to overcome. Your foundation is solid, but you need a catalyst to break through.`;
      }
      
      return '';
    },
    
    getRecommendedTreasures() {
      if (!this.disciple || this.disciple.bottleneck !== 'major') {
        return [];
      }
      
      // Map realm to recommended treasures
      const treasuresByRealm = {
        'Mortal': [
          { id: 'spirit_pill', name: 'Spirit Pill', icon: '💊' }
        ],
        'Qi Condensation': [
          { id: 'spirit_pill', name: 'Spirit Pill', icon: '💊' },
          { id: 'dao_comprehension_stone', name: 'Dao Comprehension Stone', icon: '🔮' }
        ],
        'Foundation Establishment': [
          { id: 'dao_comprehension_stone', name: 'Dao Comprehension Stone', icon: '🔮' },
          { id: 'heaven_and_earth_spirit_fruit', name: 'Heaven and Earth Spirit Fruit', icon: '🍑' }
        ],
        'Core Formation': [
          { id: 'heaven_and_earth_spirit_fruit', name: 'Heaven and Earth Spirit Fruit', icon: '🍑' },
          { id: 'nine_transformation_pill', name: 'Nine Transformation Pill', icon: '💊' }
        ],
        'Nascent Soul': [
          { id: 'nine_transformation_pill', name: 'Nine Transformation Pill', icon: '💊' }
        ],
        'Spirit Severing': [
          { id: 'nine_transformation_pill', name: 'Nine Transformation Pill', icon: '💊' },
          { id: 'immortal_ascension_stone', name: 'Immortal Ascension Stone', icon: '💎' }
        ],
        'Dao Seeking': [
          { id: 'immortal_ascension_stone', name: 'Immortal Ascension Stone', icon: '💎' }
        ],
        'Immortal Ascension': [
          { id: 'immortal_ascension_stone', name: 'Immortal Ascension Stone', icon: '💎' }
        ]
      };
      
      return treasuresByRealm[this.disciple.realm_name] || [];
    }
  }
};
</script>

<style scoped>
.bottleneck-visualizer {
  margin: 15px 0;
}

.bottleneck-container {
  display: flex;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  background-color: #fff;
  transition: all 0.3s ease;
}

.bottleneck-container.minor {
  border-left: 4px solid #f39c12;
}

.bottleneck-container.major {
  border-left: 4px solid #e74c3c;
}

.bottleneck-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  font-size: 2.5rem;
}

.bottleneck-content {
  flex: 1;
  padding: 15px;
}

.bottleneck-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 10px;
}

.bottleneck-title {
  margin: 0;
  color: #333;
  font-size: 1.2rem;
}

.bottleneck-realm {
  font-size: 0.9rem;
  color: #666;
  font-style: italic;
}

.bottleneck-description {
  margin-bottom: 15px;
  font-size: 0.95rem;
  color: #555;
  line-height: 1.5;
}

.insight-progress {
  margin: 15px 0;
}

.progress-label {
  display: flex;
  justify-content: space-between;
  margin-bottom: 5px;
  font-size: 0.9rem;
  color: #555;
}

.percentage {
  font-weight: bold;
}

.progress-bar {
  height: 10px;
  background-color: #f0f0f0;
  border-radius: 5px;
  overflow: hidden;
  position: relative;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #f39c12, #f1c40f);
  transition: width 0.5s ease;
}

.progress-steps {
  position: relative;
  height: 30px;
  margin-top: 5px;
}

.step {
  position: absolute;
  transform: translateX(-50%);
}

.step-marker {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background-color: #ddd;
  margin: 0 auto;
}

.step.active .step-marker {
  background-color: #f39c12;
}

.step-label {
  font-size: 0.8rem;
  color: #777;
  text-align: center;
  margin-top: 3px;
}

.treasure-info {
  margin: 15px 0;
}

.treasure-recommendation h4 {
  margin: 0 0 10px 0;
  font-size: 1rem;
  color: #333;
}

.treasure-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.treasure-item {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
  padding: 8px;
  background-color: #f9f9f9;
  border-radius: 4px;
}

.treasure-icon {
  font-size: 1.2rem;
  margin-right: 10px;
}

.treasure-name {
  font-size: 0.9rem;
  color: #333;
}

.bottleneck-actions {
  margin-top: 15px;
}

.no-bottleneck {
  margin: 15px 0;
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #2ecc71;
}

.status-message {
  display: flex;
  align-items: center;
  color: #2ecc71;
  font-weight: 500;
}

.status-icon {
  font-size: 1.2rem;
  margin-right: 10px;
}
</style>
