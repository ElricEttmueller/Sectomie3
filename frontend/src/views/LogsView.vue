<template>
  <div class="logs-view">
    <div class="page-header">
      <h1>Sect Chronicles</h1>
      <p>View the history and records of your sect's journey</p>
    </div>
    
    <div class="logs-content">
      <div class="logs-stats">
        <div class="stat-card">
          <div class="stat-title">Total Entries</div>
          <div class="stat-value">{{ totalEntries }}</div>
        </div>
        <div class="stat-card">
          <div class="stat-title">Current Year</div>
          <div class="stat-value">Year {{ currentYear }}</div>
        </div>
        <div class="stat-card">
          <div class="stat-title">Notable Events</div>
          <div class="stat-value">{{ notableEvents }}</div>
        </div>
        <div class="stat-card">
          <div class="stat-title">Sect Age</div>
          <div class="stat-value">{{ sectAge }} Years</div>
        </div>
      </div>
      
      <div class="logs-filters">
        <div class="filter-group">
          <label>Category:</label>
          <select v-model="filter.category">
            <option value="all">All Categories</option>
            <option value="disciples">Disciples</option>
            <option value="cultivation">Cultivation</option>
            <option value="sect">Sect Development</option>
            <option value="events">Events</option>
            <option value="battles">Battles</option>
          </select>
        </div>
        <div class="filter-group">
          <label>Time Period:</label>
          <select v-model="filter.period">
            <option value="all">All Time</option>
            <option value="current-year">Current Year</option>
            <option value="current-month">Current Month</option>
            <option value="last-10">Last 10 Turns</option>
          </select>
        </div>
        <div class="filter-group">
          <label>Search:</label>
          <div class="search-container">
            <input type="text" v-model="filter.search" placeholder="Search logs..." class="search-input">
            <i class="fa fa-search search-icon"></i>
          </div>
        </div>
      </div>
      
      <div class="logs-timeline">
        <div v-for="(year, yearIndex) in filteredLogs" :key="yearIndex" class="timeline-year">
          <div class="year-header">
            <h2>Year {{ year.year }}</h2>
            <div class="year-summary">{{ year.summary }}</div>
          </div>
          
          <div v-for="(month, monthIndex) in year.months" :key="monthIndex" class="timeline-month">
            <div class="month-header">
              <h3>Month {{ month.month }}</h3>
              <div class="month-summary">{{ month.summary }}</div>
            </div>
            
            <div class="log-entries">
              <div v-for="(entry, entryIndex) in month.entries" :key="entryIndex" 
                   class="log-entry" :class="entry.category.toLowerCase()">
                <div class="entry-date">Day {{ entry.day }}</div>
                <div class="entry-content">
                  <div class="entry-header">
                    <div class="entry-title">{{ entry.title }}</div>
                    <div class="entry-category">{{ entry.category }}</div>
                  </div>
                  <div class="entry-description">{{ entry.description }}</div>
                  <div v-if="entry.details" class="entry-details">
                    <div v-for="(detail, detailIndex) in entry.details" :key="detailIndex" class="detail-item">
                      <i :class="`fa ${detail.icon}`"></i>
                      <span>{{ detail.text }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div v-if="filteredLogs.length === 0" class="no-logs">
          <i class="fa fa-scroll"></i>
          <div>No log entries match your filters</div>
        </div>
      </div>
      
      <div class="notable-events">
        <h2>Notable Events</h2>
        <div class="events-grid">
          <div v-for="(event, eventIndex) in notableEventsList" :key="eventIndex" class="notable-event">
            <div class="event-date">Year {{ event.year }}, Month {{ event.month }}</div>
            <div class="event-title">{{ event.title }}</div>
            <div class="event-description">{{ event.description }}</div>
            <button class="view-details-button">
              <i class="fa fa-search"></i>
              View Details
            </button>
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
  name: 'LogsView',
  data() {
    return {
      currentYear: 1,
      sectAge: 1,
      notableEvents: 0,
      gameState: {
        current_turn: 1,
        game_date: 'Year 1, Month 1'
      },
      filter: {
        category: 'all',
        period: 'all',
        search: ''
      },
      logs: [
        {
          year: 1,
          summary: 'Founding of the Azure Peak Sect and initial development',
          months: [
            {
              month: 1,
              summary: 'Establishment of the sect and recruitment of first disciples',
              entries: [
                {
                  day: 1,
                  title: 'Sect Founding',
                  category: 'Sect',
                  description: 'The Azure Peak Sect was officially established by Grandmaster Feng.',
                  details: [
                    { icon: 'fa-mountain', text: 'Azure Peak claimed as sect territory' },
                    { icon: 'fa-user-plus', text: 'First 3 disciples recruited' }
                  ]
                },
                {
                  day: 5,
                  title: 'Spirit Vein Discovery',
                  category: 'Sect',
                  description: 'A medium-grade spirit vein was discovered beneath the main peak.',
                  details: [
                    { icon: 'fa-gem', text: '+50 Spirit Stones added to sect treasury' },
                    { icon: 'fa-chart-line', text: 'Cultivation speed increased by 10%' }
                  ]
                },
                {
                  day: 15,
                  title: 'Li Mei Joins the Sect',
                  category: 'Disciples',
                  description: 'A talented young cultivator named Li Mei joined the sect after demonstrating exceptional spiritual aptitude.',
                  details: [
                    { icon: 'fa-fire', text: 'Shows strong fire affinity' },
                    { icon: 'fa-star', text: 'Spiritual: 45, Physical: 30, Comprehension: 38' }
                  ]
                }
              ]
            },
            {
              month: 2,
              summary: 'First cultivation breakthroughs and territory expansion',
              entries: [
                {
                  day: 8,
                  title: 'Zhang Wei Breakthrough',
                  category: 'Cultivation',
                  description: 'Disciple Zhang Wei successfully broke through to Qi Condensation Stage 2.',
                  details: [
                    { icon: 'fa-arrow-up', text: 'Qi Condensation Early → Qi Condensation Middle' },
                    { icon: 'fa-tint', text: 'Water affinity strengthened' }
                  ]
                },
                {
                  day: 12,
                  title: 'Verdant Valley Exploration',
                  category: 'Events',
                  description: 'A small team explored the nearby Verdant Valley and claimed it for the sect.',
                  details: [
                    { icon: 'fa-leaf', text: 'Rich herb resources discovered' },
                    { icon: 'fa-map-marked', text: 'Territory expanded by 30%' }
                  ]
                },
                {
                  day: 25,
                  title: 'Minor Sect Conflict',
                  category: 'Battles',
                  description: 'A dispute with the Iron Fist Sect over territory boundaries was resolved through negotiation.',
                  details: [
                    { icon: 'fa-handshake', text: 'Peaceful resolution achieved' },
                    { icon: 'fa-gem', text: '100 Spirit Stones paid as compensation' }
                  ]
                }
              ]
            },
            {
              month: 3,
              summary: 'Development of sect facilities and cultivation methods',
              entries: [
                {
                  day: 3,
                  title: 'Main Hall Construction',
                  category: 'Sect',
                  description: 'The sect\'s main hall was completed, providing a central gathering place for disciples.',
                  details: [
                    { icon: 'fa-building', text: 'Main Hall Level 1 constructed' },
                    { icon: 'fa-users', text: 'Disciple capacity increased to 10' }
                  ]
                },
                {
                  day: 17,
                  title: 'Azure Flame Method Acquisition',
                  category: 'Cultivation',
                  description: 'The sect acquired the Azure Flame Refinement cultivation method from a wandering cultivator.',
                  details: [
                    { icon: 'fa-book', text: 'Fire-based cultivation method added to sect library' },
                    { icon: 'fa-fire', text: 'Especially suitable for disciples with fire affinity' }
                  ]
                },
                {
                  day: 22,
                  title: 'Hui Wu Joins the Sect',
                  category: 'Disciples',
                  description: 'A physically strong cultivator named Hui Wu joined the sect after impressing with his endurance.',
                  details: [
                    { icon: 'fa-dumbbell', text: 'Exceptional physical attributes' },
                    { icon: 'fa-mountain', text: 'Shows strong earth affinity' }
                  ]
                }
              ]
            }
          ]
        }
      ],
      notableEventsList: [
        {
          year: 1,
          month: 1,
          title: 'Sect Founding',
          description: 'The establishment of the Azure Peak Sect by Grandmaster Feng, marking the beginning of our journey.'
        },
        {
          year: 1,
          month: 2,
          title: 'First Territory Expansion',
          description: 'The successful exploration and claiming of Verdant Valley, significantly expanding the sect\'s influence.'
        },
        {
          year: 1,
          month: 3,
          title: 'Azure Flame Method Acquisition',
          description: 'Acquisition of our first high-quality cultivation method, setting the foundation for our disciples\' growth.'
        }
      ]
    }
  },
  computed: {
    totalEntries() {
      let count = 0;
      this.logs.forEach(year => {
        year.months.forEach(month => {
          count += month.entries.length;
        });
      });
      return count;
    },
    filteredLogs() {
      if (this.filter.category === 'all' && this.filter.period === 'all' && !this.filter.search) {
        return this.logs;
      }
      
      // Deep clone the logs to avoid modifying the original data
      let filtered = JSON.parse(JSON.stringify(this.logs));
      
      // Filter by period
      if (this.filter.period !== 'all') {
        // This would be implemented with actual date logic
        // For now, we'll just return the data as is
      }
      
      // Filter entries by category and search
      filtered = filtered.map(year => {
        const filteredMonths = year.months.map(month => {
          const filteredEntries = month.entries.filter(entry => {
            const categoryMatch = this.filter.category === 'all' || entry.category.toLowerCase() === this.filter.category;
            
            const searchMatch = !this.filter.search || 
                               entry.title.toLowerCase().includes(this.filter.search.toLowerCase()) ||
                               entry.description.toLowerCase().includes(this.filter.search.toLowerCase());
            
            return categoryMatch && searchMatch;
          });
          
          return {
            ...month,
            entries: filteredEntries
          };
        }).filter(month => month.entries.length > 0);
        
        return {
          ...year,
          months: filteredMonths
        };
      }).filter(year => year.months.length > 0);
      
      return filtered;
    }
  },
  methods: {
    async fetchGameState() {
      try {
        const response = await axios.get('http://localhost:5000/api/game-state');
        if (response.data) {
          this.gameState = response.data;
          
          // Parse the game date to extract year
          const yearMatch = response.data.game_date.match(/Year (\d+)/);
          if (yearMatch && yearMatch[1]) {
            this.currentYear = parseInt(yearMatch[1]);
            this.sectAge = this.currentYear; // Assuming the sect was founded in year 1
          }
        }
      } catch (error) {
        console.error('Error fetching game state:', error);
      }
    },
    
    async fetchLogs() {
      try {
        const response = await axios.get('http://localhost:5000/api/logs');
        if (response.data) {
          // Replace placeholder data with real data from the API
          this.logs = response.data.logs || [];
          this.notableEventsList = response.data.notable_events || [];
          this.notableEvents = this.notableEventsList.length;
          this.currentYear = response.data.current_year || 1;
          this.sectAge = response.data.sect_age || 1;
        }
      } catch (error) {
        console.error('Error fetching logs:', error);
      }
    },
    
    async recordEndTurnResults(results) {
      // This method would be called after an end-turn to record the results in the logs
      if (!results) return;
      
      // Parse the current game date
      const yearMatch = this.gameState.game_date.match(/Year (\d+), Month (\d+)/);
      if (!yearMatch || yearMatch.length < 3) return;
      
      const year = parseInt(yearMatch[1]);
      const month = parseInt(yearMatch[2]);
      
      // Find or create the year entry
      let yearEntry = this.logs.find(y => y.year === year);
      if (!yearEntry) {
        yearEntry = {
          year: year,
          summary: `Year ${year} of the sect's development`,
          months: []
        };
        this.logs.push(yearEntry);
      }
      
      // Find or create the month entry
      let monthEntry = yearEntry.months.find(m => m.month === month);
      if (!monthEntry) {
        monthEntry = {
          month: month,
          summary: `Month ${month} activities and events`,
          entries: []
        };
        yearEntry.months.push(monthEntry);
      }
      
      // Add entries for significant events
      const day = 1; // Default to day 1 since we don't track specific days
      
      // Record resource income
      if (results.resource_income) {
        const resourceDetails = [];
        for (const [resource, amount] of Object.entries(results.resource_income)) {
          if (amount > 0) {
            const resourceName = resource.replace('_', ' ');
            resourceDetails.push({
              icon: resource === 'spirit_stones' ? 'fa-gem' : 'fa-leaf',
              text: `+${amount} ${resourceName}`
            });
          }
        }
        
        if (resourceDetails.length > 0) {
          monthEntry.entries.push({
            day: day,
            title: 'Resource Collection',
            category: 'Sect',
            description: 'Monthly resources were collected from sect territories.',
            details: resourceDetails
          });
        }
      }
      
      // Record cultivation progress
      if (results.cultivation_progress) {
        for (const [discipleId, progress] of Object.entries(results.cultivation_progress)) {
          // Only record significant progress
          if (progress.qi_gained > 0) {
            monthEntry.entries.push({
              day: day,
              title: `${progress.name} Cultivation`,
              category: 'Cultivation',
              description: `${progress.name} made progress in cultivation using ${progress.method_used}.`,
              details: [
                { icon: 'fa-tint', text: `+${Math.floor(progress.qi_gained)} Qi gained` },
                { icon: 'fa-percentage', text: `${progress.breakthrough_chance}% breakthrough chance` }
              ]
            });
          }
        }
      }
      
      // Record breakthroughs and other events
      if (results.events && results.events.length > 0) {
        for (const event of results.events) {
          if (event.type === 'breakthrough') {
            monthEntry.entries.push({
              day: day + 1, // Offset by a day to show sequence
              title: `${event.name} Breakthrough`,
              category: 'Cultivation',
              description: event.message,
              details: [
                { icon: 'fa-arrow-up', text: `Advanced to ${event.new_realm} Realm` }
              ]
            });
            
            // Add to notable events if it's a significant breakthrough
            if (event.new_realm && event.new_realm !== 'Qi Condensation') {
              this.notableEventsList.push({
                year: year,
                month: month,
                title: `${event.name} Breakthrough to ${event.new_realm}`,
                description: `${event.name} successfully advanced to the ${event.new_realm} Realm, a significant milestone for the sect.`
              });
              this.notableEvents = this.notableEventsList.length;
            }
          }
        }
      }
      
      // Record cultivation deviations
      if (results.cultivation_deviations && results.cultivation_deviations.length > 0) {
        for (const deviation of results.cultivation_deviations) {
          monthEntry.entries.push({
            day: day + 1,
            title: `${deviation.name} Cultivation Deviation`,
            category: 'Disaster',
            description: deviation.message,
            details: [
              { icon: 'fa-exclamation-triangle', text: 'Requires immediate attention' }
            ]
          });
        }
      }
      
      // Record attribute increases
      if (results.attribute_increases && results.attribute_increases.length > 0) {
        for (const increase of results.attribute_increases) {
          monthEntry.entries.push({
            day: day + 2,
            title: `${increase.name} Attribute Improvement`,
            category: 'Disciples',
            description: `${increase.name}'s ${increase.attribute} attribute has improved through cultivation.`,
            details: [
              { icon: 'fa-chart-line', text: `${increase.attribute}: ${increase.value}` }
            ]
          });
        }
      }
    }
  },
  mounted() {
    this.fetchGameState();
    this.fetchLogs();
    
    // Listen for turn-ended events from other components
    EventBus.$on('turn-ended', (data) => {
      console.log('Turn ended event received in LogsView:', data);
      this.gameState.current_turn = data.turnNumber;
      this.gameState.game_date = data.gameDate;
      this.currentYear = parseInt(data.gameDate.match(/Year (\d+)/)[1]) || 1;
      this.sectAge = this.currentYear;
      
      // Record the turn results in the logs
      this.recordEndTurnResults(data.results);
    });
  },
  
  beforeDestroy() {
    // Clean up event listeners when component is destroyed
    EventBus.$off('turn-ended');
  }
}
</script>

<style scoped>
.logs-view {
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

.logs-content {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.logs-stats {
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

.logs-filters {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  background-color: rgba(0, 0, 0, 0.5);
  border: 1px solid rgba(212, 175, 55, 0.3);
  border-radius: 0.5rem;
  padding: 1rem;
  align-items: center;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.filter-group label {
  color: #a0a0a0;
  font-size: 0.9rem;
}

.filter-group select {
  background-color: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(212, 175, 55, 0.3);
  color: #e0e0e0;
  padding: 0.5rem;
  border-radius: 0.25rem;
}

.search-container {
  position: relative;
}

.search-input {
  background-color: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(212, 175, 55, 0.3);
  color: #e0e0e0;
  padding: 0.5rem 1rem 0.5rem 2.5rem;
  border-radius: 0.25rem;
  width: 250px;
}

.search-icon {
  position: absolute;
  left: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  color: #a0a0a0;
}

.logs-timeline {
  background-color: rgba(0, 0, 0, 0.5);
  border: 1px solid rgba(212, 175, 55, 0.3);
  border-radius: 0.5rem;
  padding: 1.5rem;
}

.timeline-year {
  margin-bottom: 2.5rem;
}

.timeline-year:last-child {
  margin-bottom: 0;
}

.year-header {
  margin-bottom: 1.5rem;
}

.year-header h2 {
  color: #d4af37;
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid rgba(212, 175, 55, 0.3);
}

.year-summary {
  color: #e0e0e0;
  font-style: italic;
}

.timeline-month {
  margin-left: 1.5rem;
  margin-bottom: 2rem;
  position: relative;
}

.timeline-month:before {
  content: '';
  position: absolute;
  left: -1.5rem;
  top: 0;
  bottom: 0;
  width: 2px;
  background-color: rgba(212, 175, 55, 0.3);
}

.timeline-month:last-child {
  margin-bottom: 0;
}

.month-header {
  margin-bottom: 1rem;
  position: relative;
}

.month-header:before {
  content: '';
  position: absolute;
  left: -1.5rem;
  top: 0.75rem;
  width: 1rem;
  height: 1px;
  background-color: rgba(212, 175, 55, 0.3);
}

.month-header h3 {
  color: #d4af37;
  font-size: 1.2rem;
  margin-bottom: 0.5rem;
}

.month-summary {
  color: #e0e0e0;
  font-size: 0.9rem;
  font-style: italic;
}

.log-entries {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.log-entry {
  display: flex;
  gap: 1rem;
  background-color: rgba(0, 0, 0, 0.3);
  border-radius: 0.5rem;
  padding: 1rem;
  position: relative;
}

.log-entry:before {
  content: '';
  position: absolute;
  left: -1.5rem;
  top: 50%;
  width: 1rem;
  height: 1px;
  background-color: rgba(212, 175, 55, 0.3);
}

.log-entry.disciples {
  border-left: 3px solid #4a90e2;
}

.log-entry.cultivation {
  border-left: 3px solid #9c27b0;
}

.log-entry.sect {
  border-left: 3px solid #4caf50;
}

.log-entry.events {
  border-left: 3px solid #ff9800;
}

.log-entry.battles {
  border-left: 3px solid #f44336;
}

.entry-date {
  background-color: rgba(0, 0, 0, 0.3);
  color: #a0a0a0;
  padding: 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.9rem;
  height: fit-content;
  min-width: 70px;
  text-align: center;
}

.entry-content {
  flex: 1;
}

.entry-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.entry-title {
  color: #d4af37;
  font-weight: bold;
}

.entry-category {
  font-size: 0.8rem;
  color: #a0a0a0;
  padding: 0.25rem 0.5rem;
  background-color: rgba(0, 0, 0, 0.3);
  border-radius: 0.25rem;
}

.entry-description {
  color: #e0e0e0;
  margin-bottom: 0.5rem;
}

.entry-details {
  background-color: rgba(0, 0, 0, 0.2);
  border-radius: 0.25rem;
  padding: 0.75rem;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #a0a0a0;
  font-size: 0.9rem;
  margin-bottom: 0.25rem;
}

.detail-item:last-child {
  margin-bottom: 0;
}

.no-logs {
  text-align: center;
  padding: 3rem 0;
  color: #a0a0a0;
}

.no-logs i {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.notable-events {
  background-color: rgba(0, 0, 0, 0.5);
  border: 1px solid rgba(212, 175, 55, 0.3);
  border-radius: 0.5rem;
  padding: 1.5rem;
}

.notable-events h2 {
  color: #d4af37;
  margin-bottom: 1.5rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid rgba(212, 175, 55, 0.3);
}

.events-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.notable-event {
  background-color: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(212, 175, 55, 0.3);
  border-radius: 0.5rem;
  padding: 1.5rem;
  transition: all 0.2s ease;
}

.notable-event:hover {
  transform: translateY(-2px);
  border-color: rgba(212, 175, 55, 0.6);
}

.event-date {
  color: #a0a0a0;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}

.event-title {
  color: #d4af37;
  font-weight: bold;
  font-size: 1.1rem;
  margin-bottom: 0.75rem;
}

.event-description {
  color: #e0e0e0;
  margin-bottom: 1rem;
  line-height: 1.6;
}

.view-details-button {
  background-color: rgba(212, 175, 55, 0.2);
  border: 1px solid rgba(212, 175, 55, 0.5);
  color: #d4af37;
  padding: 0.5rem 1rem;
  border-radius: 0.25rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  transition: all 0.2s ease;
}

.view-details-button:hover {
  background-color: rgba(212, 175, 55, 0.3);
}

@media (max-width: 992px) {
  .events-grid {
    grid-template-columns: 1fr 1fr;
  }
}

@media (max-width: 768px) {
  .logs-filters {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .filter-group {
    width: 100%;
  }
  
  .filter-group select,
  .search-input {
    width: 100%;
  }
  
  .log-entry {
    flex-direction: column;
  }
  
  .entry-date {
    align-self: flex-start;
  }
  
  .entry-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
  
  .events-grid {
    grid-template-columns: 1fr;
  }
}
</style>
