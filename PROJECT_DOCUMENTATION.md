# Sectomie3 - Cultivation Simulator Project Documentation

## Project Overview

Sectomie3 is a cultivation simulator game based on the concepts of Chinese Xianxia/Wuxia novels, where players manage a cultivation sect and its disciples. The game features a cultivation system with realms, stages, bottlenecks, and various cultivation methods.

## System Architecture

The project follows a client-server architecture:

- **Backend**: Python-based Flask API server
- **Frontend**: Vue.js-based web application

### Directory Structure

```
sectomie3/
├── backend/
│   ├── app.py              # Main Flask application and API endpoints
│   ├── data_manager.py     # Data persistence management
│   ├── game_state.py       # Game state management
│   ├── member.py           # Disciple/Cultivator class definition
│   ├── sect.py             # Sect class definition
│   └── example_data.json   # Game data storage
├── frontend/
│   ├── public/             # Static public assets
│   └── src/
│       ├── components/     # Vue components
│       │   └── CultivationAssignment.vue  # Cultivation assignment interface
│       ├── views/          # Vue page views
│       │   ├── SectView.vue              # Sect management view
│       │   ├── DisciplesView.vue         # Disciples management view
│       │   ├── CultivationView.vue       # Cultivation system view
│       │   ├── TerritoriesView.vue       # Territories management view
│       │   ├── EventsView.vue            # Events management view
│       │   └── LogsView.vue              # Sect chronicles view
│       ├── router/         # Vue router configuration
│       │   └── index.js    # Route definitions
│       ├── assets/         # Frontend assets
│       │   └── backgrounds/# Background images
│       ├── App.vue         # Main Vue application with layout structure
│       └── main.js         # Vue application entry point
├── GAME_DESIGN.md          # Game design document
└── PROJECT_DOCUMENTATION.md # This documentation file
```

## Frontend Architecture

### Main Layout Structure

The application uses a comprehensive layout structure defined in `App.vue` with the following components:

1. **Header Bar**
   - Contains sect emblem, game date/turn information, and resource dashboard
   - Implemented with flexbox for responsive alignment

2. **Main Navigation**
   - Icon-based navigation tabs using Font Awesome icons
   - Vue Router integration for seamless navigation
   - Active route highlighting with CSS transitions

3. **Context-Sensitive Sidebar**
   - Dynamic content that changes based on the current route
   - Implemented using Vue's reactive data system
   - Organized into collapsible sections for better information hierarchy

4. **Main Content Area**
   - Router view container for displaying different view components
   - Responsive design with scrollable content

5. **Status Bar**
   - Notifications system, quick actions, and end turn functionality
   - Fixed position at the bottom of the layout

### View Components

The application is organized into several main view components:

1. **SectView.vue**
   - Manages sect information, facilities, and sect-level actions
   - Uses CSS Grid for facility layout
   - Implements card-based UI for facilities with hover effects

2. **DisciplesView.vue**
   - Displays disciples list with filtering and sorting capabilities
   - Uses CSS Grid for responsive layout
   - Implements attribute visualization with custom progress bars

3. **CultivationView.vue**
   - Tabbed interface for disciples, methods, and resource allocation
   - Star rating system for method effectiveness visualization
   - Resource allocation interface with real-time feedback

4. **TerritoriesView.vue**
   - Interactive territory map with selection functionality
   - Resource node visualization
   - Territory management interface

5. **EventsView.vue**
   - Event management with tabbed interface for current, upcoming, and historical events
   - Color-coded event cards based on event type
   - Decision interface for event resolution

6. **LogsView.vue**
   - Chronological timeline of sect history
   - Filtering system for log entries
   - Notable events highlighting

### Styling Approach

1. **CSS Organization**
   - Component-scoped CSS using Vue's `<style scoped>` feature
   - Consistent color scheme based on cultivation theme
   - Responsive design with media queries

2. **Theme Elements**
   - Gold accents (#d4af37) for important UI elements
   - Semi-transparent dark backgrounds for content areas
   - Chinese-inspired fonts (Ma Shan Zheng for titles, Noto Serif SC for content)

3. **Responsive Design**
   - Mobile-first approach with breakpoints at 768px, 992px, and 1200px
   - Flexbox and CSS Grid for layout
   - Collapsible elements for smaller screens

## Core Game Mechanics

### Cultivation System

1. **Realms and Stages**:
   - Realms: Mortal, Qi Condensation, Foundation Establishment, Core Formation, Nascent Soul, etc.
   - Each realm has 4 stages: Early, Middle, Late, and Peak

2. **Attributes**:
   - Physical: Affects combat power and physical techniques
   - Spiritual: Affects qi gain and spiritual techniques
   - Comprehension: Affects breakthrough chance and technique mastery

3. **Qi and Cultivation**:
   - Disciples accumulate qi through cultivation
   - Turn-based automatic cultivation system
   - Resource allocation affects cultivation speed and effectiveness

### Cultivation Methods

1. **Method Types**:
   - Different elemental affinities (Fire, Water, Earth, Wind, Lightning)
   - Balanced methods for general cultivation
   - Specialized methods for specific attributes or realms

2. **Method Attributes**:
   - Qi Generation: Rate of qi accumulation
   - Breakthrough Bonus: Increased chance of successful breakthrough
   - Safety: Resistance to cultivation deviation
   - Attribute Growth: Effect on disciple attribute development

3. **Compatibility System**:
   - Methods have varying effectiveness based on disciple attributes
   - Visual compatibility rating system
   - Personalized recommendations for each disciple
   - Multiple cultivation methods available (qi_circulation, essence_refinement, dao_heart_tempering)
   - Each method has different effects on qi gain, breakthrough chance, and attributes

4. **Breakthrough System**:
   - Disciples can attempt breakthrough when qi is at least 90% of maximum
   - Success chance based on breakthrough_chance attribute
   - Successful breakthrough advances to next stage or realm

5. **Bottleneck System**:
   - Minor Bottlenecks: Require meditation for insights
   - Major Bottlenecks: Require special treasures
   - Different treasures effective for different realm ranges

### Sect Management

1. **Resources**:
   - Spirit Stones: Main currency
   - Spirit Herbs: For alchemy
   - Dao Crystals: Advanced resource
   - Treasures: Special items for overcoming bottlenecks

2. **Sect Features**:
   - Spirit Veins: Generate resources
   - Territories: Expand sect influence
   - Techniques: Can be taught to disciples

## Backend-Frontend Integration

### Event Bus System

The application uses an event bus system to facilitate communication between components:

- Implemented in `frontend/src/services/eventBus.js`
- Uses Vue's event emitter pattern for cross-component communication
- Primary use cases:
  - Turn end notification across components
  - Game state updates propagation
  - Log entry creation from events

### Data Flow Architecture

1. **Turn End Process**:
   - User clicks "End Turn" button in EventsView
   - Frontend sends POST request to `/api/end-turn`
   - Backend processes turn end and returns comprehensive results
   - EventsView emits `turn-ended` event via EventBus
   - All connected components (CultivationView, LogsView, DiscipleDetail, DisciplesView) receive the event and update their data

2. **Disciple Management Process**:
   - DisciplesView fetches disciples list from `/api/disciples`
   - DiscipleDetail fetches detailed disciple information from `/api/disciples/:id`
   - Both components listen for `turn-ended` events to refresh their data
   - User can navigate between views by clicking on a disciple in the DisciplesView
   - Backend processes all end-of-turn events (resource income, cultivation progress, etc.)
   - Backend returns comprehensive results of turn processing
   - EventsView emits turn-ended event via EventBus
   - Other components (LogsView, CultivationView) listen for turn-ended event and update accordingly
   - LogsView records turn results in the sect chronicles

2. **Cultivation Assignment**:
   - User assigns cultivation method to disciple
   - Frontend sends POST request to `/api/disciples/:id/cultivate-method`
   - Backend validates resources and applies method
   - Results are returned to frontend and displayed

3. **Event System Integration**:
   - Events are fetched from the backend via `/api/events`
   - End-turn processing generates new events
   - Events are categorized as active, upcoming, or historical
   - Events can trigger log entries through the event bus

## API Endpoints

### Disciple Management

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/disciples` | GET | Get all disciples |
| `/api/disciples/{id}` | GET | Get specific disciple |
| `/api/disciples/{id}/cultivate-method` | POST | Cultivate using specific method |
| `/api/disciples/{id}/breakthrough` | POST | Attempt breakthrough |
| `/api/disciples/{id}/meditate` | POST | Meditate for insight (minor bottlenecks) |
| `/api/disciples/{id}/use-treasure` | POST | Use treasure (major bottlenecks) |
| `/api/disciples/{id}/clear-bottleneck` | POST | Clear bottleneck (testing) |
| `/api/disciples/{id}/force-peak` | POST | Force to peak stage (testing) |

### Sect Management

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/sects` | GET | Get all sects |
| `/api/player-sect` | GET | Get player's sect |
| `/api/player-sect/disciples` | GET | Get disciples in player's sect |
| `/api/add-treasure` | POST | Add treasure to sect (testing) |

### Game State

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/game-state` | GET | Get current game state |
| `/api/end-turn` | POST | Process turn end and advance game state |

### Events and Logs

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/events` | GET | Get active, upcoming, and historical events |
| `/api/logs` | GET | Get sect chronicles and notable events |

## Current Implementation Status

### Implemented Features

1. **Backend**:
   - Core cultivation mechanics
   - Realm and stage progression
   - Bottleneck system (both minor and major)
   - Treasure system for major bottlenecks
   - Meditation system for minor bottlenecks
   - Data persistence

2. **Frontend**:
   - Basic UI for disciple management
   - Cultivation interface
   - Breakthrough interface
   - Advanced bottleneck visualization system
   - Comprehensive testing dashboard with API response logging

### Missing Components and Limitations

1. **Frontend Limitations**:
   - Missing comprehensive tutorial or help system
   - Limited visual feedback for cultivation progress in main game interface
   - No mobile-responsive design

2. **Backend Limitations**:
   - Limited testing endpoints
   - No comprehensive error handling
   - Limited logging system

3. **Workflow Issues**:
   - Manual API testing required
   - No integrated testing tools in the frontend
   - Limited debugging information

## Recommended Improvements

### Frontend Enhancements

1. **Bottleneck Management UI**: ✅
   - ✅ Add a dedicated bottleneck management component
   - ✅ Create visual indicators for bottleneck types
   - ✅ Implement progress bars for insight accumulation
   - ✅ Add treasure recommendations based on realm
   - Add treasure inventory management

2. **Testing Tools**: ✅
   - ✅ Create a developer panel with testing functions
   - ✅ Add buttons to trigger specific game states
   - ✅ Implement a logging console for API responses
   - Add automated test scenarios

3. **User Experience**:
   - Add tooltips explaining game mechanics
   - Create a tutorial system
   - Improve visual feedback for actions

### Backend Enhancements

1. **Testing Endpoints**:
   - Create a comprehensive testing API
   - Add endpoints to manipulate game state
   - Implement debug logging

2. **Error Handling**:
   - Improve error messages
   - Add validation for all inputs
   - Create a consistent error response format

3. **Performance**:
   - Optimize data storage
   - Implement caching for frequently accessed data

## Development Workflow Recommendations

1. **Testing Strategy**: ✅
   - ✅ Create a testing dashboard in the frontend
   - ✅ Implement a two-column layout with fixed API response log
   - Implement automated tests for core mechanics
   - Add a debug mode with additional logging

2. **Development Tools**:
   - Add a command-line interface for common tasks
   - Create scripts for data manipulation
   - Implement a development configuration

3. **Documentation**:
   - Document all API endpoints
   - Create user guides for game mechanics
   - Add inline code documentation

## Conclusion

Sectomie3 has made significant progress with core game mechanics fully implemented and several key UI improvements completed. The bottleneck visualization system now provides clear, intuitive feedback to players, making this complex game mechanic much easier to understand. The comprehensive testing dashboard with its two-column layout and fixed API response log greatly improves the development workflow.

The project has successfully addressed two major development needs:
1. **Enhanced Bottleneck Visualization**: Players can now easily understand bottleneck status, progress, and requirements through visual indicators, progress tracking, and contextual information.
2. **Streamlined Testing Workflow**: Developers can efficiently test, debug, and implement features through the dedicated testing dashboard with real-time API response monitoring.

Moving forward, focus should be on implementing the remaining improvements, particularly around user experience, mobile responsiveness, and automated testing scenarios. With these enhancements, Sectomie3 will provide an even more engaging and intuitive experience for players while maintaining an efficient development workflow.
