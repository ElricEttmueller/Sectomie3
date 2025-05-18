<template>
  <div class="app-container" :style="{ backgroundImage: `url(${currentBackground})` }">
    <div class="overlay">
      <header class="app-header">
        <h1 class="app-title">Sectomie</h1>
        <div class="cultivation-world">Cultivation Sect Management</div>
      </header>
      
      <nav class="main-nav">
        <router-link to="/" class="nav-item">
          <span class="nav-icon">🏠</span>
          <span class="nav-text">Home</span>
        </router-link>
        <router-link to="/dashboard" class="nav-item">
          <span class="nav-icon">⚡</span>
          <span class="nav-text">Sect Dashboard</span>
        </router-link>
      </nav>
      
      <main class="main-content">
        <router-view/>
      </main>
    </div>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      backgrounds: [
        '/assets/backgrounds/mountain.jpg',
        '/assets/backgrounds/temple.jpg',
        '/assets/backgrounds/cloud.jpg',
        require('@/assets/backgrounds/Landscape01.png')
      ],
      currentBackground: require('@/assets/backgrounds/Landscape01.png')
    }
  },
  mounted() {
    // Always use Landscape01.png as the background
    this.currentBackground = require('@/assets/backgrounds/Landscape01.png');
  }
}
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Ma+Shan+Zheng&family=Noto+Serif+SC:wght@400;700&display=swap');

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Noto Serif SC', serif;
  color: #333;
  line-height: 1.6;
}

.app-container {
  min-height: 100vh;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  position: relative;
}

.overlay {
  min-height: 100vh;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  flex-direction: column;
}

.app-header {
  padding: 2rem;
  text-align: center;
  color: #f8f8f8;
}

.app-title {
  font-family: 'Ma Shan Zheng', cursive;
  font-size: 3rem;
  margin-bottom: 0.5rem;
  text-shadow: 0 0 10px rgba(255, 215, 0, 0.7);
  color: #ffd700;
}

.cultivation-world {
  font-size: 1.2rem;
  color: #e0e0e0;
}

.main-nav {
  display: flex;
  justify-content: center;
  padding: 1rem;
  background-color: rgba(0, 0, 0, 0.7);
}

.nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 0.5rem 1.5rem;
  color: #d4af37;
  text-decoration: none;
  border-radius: 0.25rem;
  transition: all 0.3s ease;
}

.nav-item:hover {
  background-color: rgba(212, 175, 55, 0.2);
  transform: translateY(-2px);
}

.nav-icon {
  font-size: 1.5rem;
  margin-bottom: 0.25rem;
}

.nav-text {
  font-size: 0.8rem;
}

.main-content {
  flex: 1;
  padding: 2rem;
  display: flex;
  justify-content: center;
}

/* For router transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
