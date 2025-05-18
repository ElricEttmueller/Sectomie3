<template>
  <div class="events-page">
    <div class="page-header">
      <h1 class="page-title">Sect Events</h1>
    </div>
    
    <div class="events-container">
      <div class="events-calendar">
        <div class="calendar-header">
          <h2 class="calendar-title">Upcoming Events</h2>
        </div>
        <div class="calendar-content">
          <div class="placeholder-message">
            <div class="placeholder-icon">📅</div>
            <div class="placeholder-text">
              <p>Event system coming soon!</p>
              <p>Track sect activities, missions, and important dates.</p>
            </div>
          </div>
        </div>
      </div>
      
      <div class="events-missions">
        <div class="missions-header">
          <h2 class="missions-title">Available Missions</h2>
        </div>
        <div class="missions-content">
          <div class="placeholder-message">
            <div class="placeholder-icon">📜</div>
            <div class="placeholder-text">
              <p>Mission system coming soon!</p>
              <p>Send disciples on missions to gain resources and experience.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'EventsPage'
}
</script>

<style scoped>
.events-page {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.page-header {
  margin-bottom: 1.5rem;
}

.page-title {
  color: #f8f8f8;
  font-size: 1.8rem;
  margin: 0;
  text-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
}

.events-container {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.5rem;
  flex: 1;
  overflow-y: auto;
}

.events-calendar, .events-missions {
  background-color: rgba(255, 248, 220, 0.9);
  border: 1px solid #d4af37;
  border-radius: 0.5rem;
  overflow: hidden;
}

.calendar-header, .missions-header {
  background-color: rgba(42, 107, 93, 0.8);
  padding: 0.75rem 1rem;
}

.calendar-title, .missions-title {
  color: #f8f8f8;
  font-size: 1.2rem;
  margin: 0;
  font-weight: normal;
}

.calendar-content, .missions-content {
  padding: 2rem;
  min-height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.placeholder-message {
  text-align: center;
  color: #666;
}

.placeholder-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
  color: #d4af37;
}

.placeholder-text p {
  margin: 0.5rem 0;
}

@media (min-width: 768px) {
  .events-container {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
