<template>
  <div class="events-view">
    <div class="page-header">
      <h1>Events</h1>
      <p>Manage and respond to events in the cultivation world</p>
      <div class="turn-controls">
        <div class="game-date">{{ gameState.game_date }}</div>
        <button @click="endTurn" class="end-turn-button">
          <i class="fa fa-calendar-alt"></i>
          End Turn
        </button>
      </div>
    </div>
    
    <div class="events-content">
      <div class="events-stats">
        <div class="stat-card">
          <div class="stat-title">Active Events</div>
          <div class="stat-value">{{ activeEvents.length }}</div>
        </div>
        <div class="stat-card">
          <div class="stat-title">Pending Decisions</div>
          <div class="stat-value">{{ pendingDecisions.length }}</div>
        </div>
        <div class="stat-card">
          <div class="stat-title">Opportunities</div>
          <div class="stat-value">{{ opportunities.length }}</div>
        </div>
        <div class="stat-card">
          <div class="stat-title">Threats</div>
          <div class="stat-value">{{ threats.length }}</div>
        </div>
      </div>
      
      <div class="events-tabs">
        <div class="tab" :class="{ active: activeTab === 'current' }" @click="activeTab = 'current'">
          <i class="fa fa-bell"></i>
          Current Events
        </div>
        <div class="tab" :class="{ active: activeTab === 'upcoming' }" @click="activeTab = 'upcoming'">
          <i class="fa fa-calendar"></i>
          Upcoming Events
        </div>
        <div class="tab" :class="{ active: activeTab === 'history' }" @click="activeTab = 'history'">
          <i class="fa fa-history"></i>
          Event History
        </div>
      </div>
      
      <!-- Current Events Tab -->
      <div v-if="activeTab === 'current'" class="tab-content">
        <div class="events-list">
          <div v-for="event in activeEvents" :key="event.id" class="event-card" :class="event.type.toLowerCase()">
            <div class="event-header">
              <div class="event-title">{{ event.title }}</div>
              <div class="event-type">{{ event.type }}</div>
            </div>
            
            <div class="event-description">{{ event.description }}</div>
            
            <div class="event-details">
              <div class="detail">
                <i class="fa fa-clock"></i>
                <span>{{ event.timeRemaining }} remaining</span>
              </div>
              <div class="detail">
                <i class="fa fa-map-marker-alt"></i>
                <span>{{ event.location }}</span>
              </div>
              <div class="detail">
                <i class="fa fa-exclamation-circle"></i>
                <span>{{ event.urgency }} Priority</span>
              </div>
            </div>
            
            <div class="event-actions">
              <button v-if="event.requiresDecision" class="decision-button">
                <i class="fa fa-gavel"></i>
                Make Decision
              </button>
              <button v-if="event.canAssignDisciples" class="assign-button">
                <i class="fa fa-user-plus"></i>
                Assign Disciples
              </button>
              <button class="details-button">
                <i class="fa fa-info-circle"></i>
                View Details
              </button>
            </div>
          </div>
          
          <div v-if="activeEvents.length === 0" class="no-events">
            <i class="fa fa-check-circle"></i>
            <div>No active events at this time</div>
          </div>
        </div>
      </div>
      
      <!-- Upcoming Events Tab -->
      <div v-if="activeTab === 'upcoming'" class="tab-content">
        <div class="events-list">
          <div v-for="event in upcomingEvents" :key="event.id" class="event-card upcoming">
            <div class="event-header">
              <div class="event-title">{{ event.title }}</div>
              <div class="event-type">{{ event.type }}</div>
            </div>
            
            <div class="event-description">{{ event.description }}</div>
            
            <div class="event-details">
              <div class="detail">
                <i class="fa fa-calendar-alt"></i>
                <span>Begins in {{ event.startsIn }}</span>
              </div>
              <div class="detail">
                <i class="fa fa-hourglass-half"></i>
                <span>Duration: {{ event.duration }}</span>
              </div>
              <div class="detail">
                <i class="fa fa-map-marker-alt"></i>
                <span>{{ event.location }}</span>
              </div>
            </div>
            
            <div class="event-actions">
              <button class="prepare-button">
                <i class="fa fa-tasks"></i>
                Prepare
              </button>
              <button class="details-button">
                <i class="fa fa-info-circle"></i>
                View Details
              </button>
            </div>
          </div>
          
          <div v-if="upcomingEvents.length === 0" class="no-events">
            <i class="fa fa-calendar-times"></i>
            <div>No upcoming events scheduled</div>
          </div>
        </div>
      </div>
      
      <!-- Event History Tab -->
      <div v-if="activeTab === 'history'" class="tab-content">
        <div class="history-filters">
          <div class="filter-group">
            <label>Event Type:</label>
            <select v-model="historyFilter.type">
              <option value="all">All Types</option>
              <option value="opportunity">Opportunities</option>
              <option value="challenge">Challenges</option>
              <option value="disaster">Disasters</option>
              <option value="tournament">Tournaments</option>
              <option value="encounter">Encounters</option>
            </select>
          </div>
          <div class="filter-group">
            <label>Outcome:</label>
            <select v-model="historyFilter.outcome">
              <option value="all">All Outcomes</option>
              <option value="success">Success</option>
              <option value="failure">Failure</option>
              <option value="neutral">Neutral</option>
            </select>
          </div>
          <div class="filter-group">
            <label>Time Period:</label>
            <select v-model="historyFilter.period">
              <option value="all">All Time</option>
              <option value="recent">Recent (Last 10 Turns)</option>
              <option value="month">This Month</option>
              <option value="year">This Year</option>
            </select>
          </div>
        </div>
        
        <div class="events-list history-list">
          <div v-for="event in filteredHistoryEvents" :key="event.id" class="event-card history" :class="event.outcome.toLowerCase()">
            <div class="event-header">
              <div class="event-title">{{ event.title }}</div>
              <div class="event-outcome">{{ event.outcome }}</div>
            </div>
            
            <div class="event-description">{{ event.description }}</div>
            
            <div class="event-details">
              <div class="detail">
                <i class="fa fa-calendar-check"></i>
                <span>{{ event.completedDate }}</span>
              </div>
              <div class="detail">
                <i class="fa fa-map-marker-alt"></i>
                <span>{{ event.location }}</span>
              </div>
            </div>
            
            <div class="event-results">
              <div class="result" v-for="(result, resultIndex) in event.results" :key="resultIndex">
                <i :class="`fa ${result.icon}`"></i>
                <span>{{ result.description }}</span>
              </div>
            </div>
          </div>
          
          <div v-if="filteredHistoryEvents.length === 0" class="no-events">
            <i class="fa fa-history"></i>
            <div>No event history matching your filters</div>
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
  name: 'EventsView',
  data() {
    return {
      activeTab: 'current',
      historyFilter: {
        type: 'all',
        outcome: 'all',
        period: 'all'
      },
      gameState: {
        current_turn: 1,
        game_date: 'Year 1, Month 1'
      },
      activeEvents: [
        {
          id: 1,
          title: 'Spirit Stone Vein Dispute',
          type: 'Challenge',
          description: 'The neighboring Golden Sun Sect is disputing ownership of a newly discovered spirit stone vein in the border territory.',
          timeRemaining: '3 days',
          location: 'Eastern Border',
          urgency: 'High',
          requiresDecision: true,
          canAssignDisciples: true
        },
        {
          id: 2,
          title: 'Mysterious Herb Discovery',
          type: 'Opportunity',
          description: 'A rare herb with extraordinary properties has been discovered in your territory. It could greatly benefit your disciples\' cultivation.',
          timeRemaining: '5 days',
          location: 'Verdant Valley',
          urgency: 'Medium',
          requiresDecision: false,
          canAssignDisciples: true
        },
        {
          id: 3,
          title: 'Demonic Beast Incursion',
          type: 'Disaster',
          description: 'A group of demonic beasts has entered your territory and is threatening the safety of your disciples and resources.',
          timeRemaining: '2 days',
          location: 'Southern Mountains',
          urgency: 'Critical',
          requiresDecision: true,
          canAssignDisciples: true
        }
      ],
      upcomingEvents: [
        {
          id: 4,
          title: 'Immortal Ascension Conference',
          type: 'Tournament',
          description: 'A grand gathering of sects where disciples can compete and exchange cultivation experiences.',
          startsIn: '15 days',
          duration: '7 days',
          location: 'Central Plains'
        },
        {
          id: 5,
          title: 'Heavenly Tribulation',
          type: 'Challenge',
          description: 'Your senior disciple Li Mei is approaching a breakthrough that will trigger a heavenly tribulation.',
          startsIn: '10 days',
          duration: '1 day',
          location: 'Azure Peak'
        }
      ],
      historyEvents: [
        {
          id: 6,
          title: 'Rogue Cultivator Encounter',
          type: 'Encounter',
          description: 'A powerful rogue cultivator sought refuge in your sect.',
          completedDate: 'Year 1, Month 3',
          location: 'Sect Entrance',
          outcome: 'Success',
          results: [
            { icon: 'fa-user-plus', description: 'Gained a new elite disciple' },
            { icon: 'fa-book', description: 'Acquired new cultivation technique' }
          ]
        },
        {
          id: 7,
          title: 'Minor Sect Conflict',
          type: 'Challenge',
          description: 'A conflict with the Iron Fist Sect over a misunderstanding.',
          completedDate: 'Year 1, Month 2',
          location: 'Trading Town',
          outcome: 'Neutral',
          results: [
            { icon: 'fa-handshake', description: 'Resolved peacefully through negotiation' },
            { icon: 'fa-gem', description: 'Lost 100 spirit stones in compensation' }
          ]
        },
        {
          id: 8,
          title: 'Spirit Beast Hunt',
          type: 'Opportunity',
          description: 'Organized a hunt for a rare spirit beast in the mountains.',
          completedDate: 'Year 1, Month 1',
          location: 'Northern Mountains',
          outcome: 'Failure',
          results: [
            { icon: 'fa-user-injured', description: 'Two disciples injured' },
            { icon: 'fa-running', description: 'Spirit beast escaped' }
          ]
        }
      ]
    }
  },
  computed: {
    pendingDecisions() {
      return this.activeEvents.filter(event => event.requiresDecision);
    },
    opportunities() {
      return this.activeEvents.filter(event => event.type === 'Opportunity');
    },
    threats() {
      return this.activeEvents.filter(event => event.type === 'Challenge' || event.type === 'Disaster');
    },
    filteredHistoryEvents() {
      return this.historyEvents.filter(event => {
        let matchesType = this.historyFilter.type === 'all' || event.type.toLowerCase() === this.historyFilter.type;
        let matchesOutcome = this.historyFilter.outcome === 'all' || event.outcome.toLowerCase() === this.historyFilter.outcome;
        // Period filtering would be implemented with actual date logic
        let matchesPeriod = true;
        
        return matchesType && matchesOutcome && matchesPeriod;
      });
    }
  },
  methods: {
    async fetchGameState() {
      try {
        const response = await axios.get('http://localhost:5000/api/game-state');
        if (response.data) {
          this.gameState = response.data;
        }
      } catch (error) {
        console.error('Error fetching game state:', error);
      }
    },
    
    async fetchEvents() {
      try {
        const response = await axios.get('http://localhost:5000/api/events');
        if (response.data) {
          // Replace placeholder data with real data from the API
          this.activeEvents = response.data.active_events || [];
          this.upcomingEvents = response.data.upcoming_events || [];
          this.historyEvents = response.data.history_events || [];
        }
      } catch (error) {
        console.error('Error fetching events:', error);
      }
    },
    
    async endTurn() {
      try {
        // Show loading indicator or disable button here if needed
        
        const response = await axios.post('http://localhost:5000/api/end-turn');
        if (response.data) {
          // Update game state with the new turn information
          this.gameState.current_turn = response.data.new_turn;
          this.gameState.game_date = response.data.game_date;
          
          // Process turn results
          const results = response.data.results;
          
          // Create notifications for important events
          if (results.cultivation_progress) {
            for (const [discipleId, progress] of Object.entries(results.cultivation_progress)) {
              // Add to active events if significant progress was made
              if (progress.qi_gained > progress.max_qi * 0.1) { // More than 10% of max qi gained
                this.activeEvents.push({
                  id: Date.now() + parseInt(discipleId), // Generate a unique ID
                  title: `${progress.name} Cultivation Progress`,
                  type: 'Cultivation',
                  description: `${progress.name} made significant progress in cultivation using ${progress.method_used}.`,
                  timeRemaining: '7 days',
                  location: 'Sect',
                  urgency: 'Low',
                  requiresDecision: false,
                  canAssignDisciples: false
                });
              }
            }
          }
          
          // Process cultivation deviations
          if (results.cultivation_deviations && results.cultivation_deviations.length > 0) {
            for (const deviation of results.cultivation_deviations) {
              this.activeEvents.push({
                id: Date.now() + 1000 + parseInt(deviation.disciple_id),
                title: `${deviation.name} Cultivation Deviation`,
                type: 'Disaster',
                description: deviation.message,
                timeRemaining: '3 days',
                location: 'Cultivation Chamber',
                urgency: 'High',
                requiresDecision: true,
                canAssignDisciples: false
              });
            }
          }
          
          // Process attribute increases
          if (results.attribute_increases && results.attribute_increases.length > 0) {
            // These could be added to the history events instead of active events
          }
          
          // Process any events from the results
          if (results.events && results.events.length > 0) {
            for (const event of results.events) {
              this.activeEvents.push({
                id: Date.now() + 2000 + parseInt(event.disciple_id || 0),
                title: event.type === 'breakthrough' ? `${event.name} Breakthrough` : event.type,
                type: 'Event',
                description: event.message,
                timeRemaining: '5 days',
                location: 'Sect',
                urgency: 'Medium',
                requiresDecision: false,
                canAssignDisciples: false
              });
            }
          }
          
          // Refresh data after turn end
          this.fetchEvents();
          
          // Emit an event so other components can react to the turn end
          EventBus.$emit('turn-ended', {
            turnNumber: this.gameState.current_turn,
            gameDate: this.gameState.game_date,
            results: results
          });
          
          // Return the results for potential use by the caller
          return results;
        }
      } catch (error) {
        console.error('Error ending turn:', error);
        return null;
      }
    }
  },
  mounted() {
    this.fetchGameState();
    this.fetchEvents();
  }
}
</script>

<style scoped>
.events-view {
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

.events-content {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.events-stats {
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

.events-tabs {
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

.events-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.event-card {
  background-color: rgba(0, 0, 0, 0.3);
  border-left: 4px solid #808080;
  border-radius: 0.5rem;
  padding: 1.5rem;
  transition: all 0.2s ease;
}

.event-card:hover {
  transform: translateY(-2px);
}

.event-card.opportunity {
  border-left-color: #4caf50;
}

.event-card.challenge {
  border-left-color: #ff9800;
}

.event-card.disaster {
  border-left-color: #f44336;
}

.event-card.tournament {
  border-left-color: #9c27b0;
}

.event-card.encounter {
  border-left-color: #2196f3;
}

.event-card.upcoming {
  border-left-color: #03a9f4;
}

.event-card.success {
  border-left-color: #4caf50;
}

.event-card.failure {
  border-left-color: #f44336;
}

.event-card.neutral {
  border-left-color: #9e9e9e;
}

.event-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.event-title {
  color: #d4af37;
  font-weight: bold;
  font-size: 1.1rem;
}

.event-type, .event-outcome {
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.8rem;
  background-color: rgba(0, 0, 0, 0.3);
}

.event-type {
  color: #e0e0e0;
}

.event-outcome {
  color: #e0e0e0;
}

.event-description {
  color: #e0e0e0;
  margin-bottom: 1.5rem;
  line-height: 1.6;
}

.event-details {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.detail {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #a0a0a0;
  font-size: 0.9rem;
}

.event-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.decision-button, .assign-button, .details-button, .prepare-button {
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

.decision-button:hover, .assign-button:hover, .details-button:hover, .prepare-button:hover {
  background-color: rgba(212, 175, 55, 0.3);
}

.decision-button {
  background-color: rgba(255, 152, 0, 0.2);
  border-color: rgba(255, 152, 0, 0.5);
  color: #ff9800;
}

.decision-button:hover {
  background-color: rgba(255, 152, 0, 0.3);
}

.no-events {
  text-align: center;
  padding: 3rem 0;
  color: #a0a0a0;
}

.no-events i {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.event-results {
  background-color: rgba(0, 0, 0, 0.2);
  border-radius: 0.25rem;
  padding: 1rem;
}

.result {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
  color: #e0e0e0;
}

.result:last-child {
  margin-bottom: 0;
}

.history-filters {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 1.5rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid rgba(212, 175, 55, 0.3);
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

@media (max-width: 992px) {
  .events-tabs {
    flex-wrap: wrap;
  }
  
  .tab {
    flex: 1;
    justify-content: center;
  }
}

@media (max-width: 768px) {
  .event-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
  
  .event-actions {
    flex-direction: column;
    width: 100%;
  }
  
  .decision-button, .assign-button, .details-button, .prepare-button {
    width: 100%;
    justify-content: center;
  }
  
  .history-filters {
    flex-direction: column;
  }
  
  .filter-group {
    width: 100%;
  }
  
  .filter-group select {
    flex: 1;
  }
}
</style>
