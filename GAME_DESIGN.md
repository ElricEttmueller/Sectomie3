# Sectomie3 Game Design Document

## Game Overview

Sectomie3 is a cultivation simulator based on the concepts of Chinese Xianxia/Wuxia novels. Players manage a cultivation sect and its disciples, guiding them through their cultivation journey from mortal to immortal realms. The game combines resource management, character development, and strategic decision-making in a rich fantasy setting.

## Current Game State

### Core Systems

1. **Cultivation System**
   - Hierarchical realm progression (Mortal → Qi Condensation → Foundation Establishment → Core Formation → etc.)
   - Each realm has 4 stages: Early, Middle, Late, and Peak
   - Bottleneck mechanics with two types: Minor (requiring meditation) and Major (requiring treasures)
   - Multiple cultivation methods with different effects (qi_circulation, essence_refinement, dao_heart_tempering)

2. **Disciple Management**
   - Disciples have three primary attributes: Physical, Spiritual, and Comprehension
   - Qi accumulation through cultivation activities
   - Breakthrough system with success chance based on attributes and preparation
   - Technique learning and mastery

3. **Sect Management**
   - Resource collection from spirit veins
   - Spirit stone economy
   - Treasure acquisition and usage
   - Recruitment system for new disciples

4. **Turn-Based Progression**
   - Game advances through turns representing months in the cultivation world
   - Each turn processes automatic cultivation for all disciples based on their assigned methods
   - Resource income is generated from spirit veins and other sources each turn
   - Events and opportunities may occur at turn transitions
   - Turn end results are comprehensively displayed and logged in the sect chronicles
   - Game date advances with years and months tracking the sect's development

5. **Backend-Frontend Integration**
   - Event bus system for cross-component communication
   - RESTful API endpoints for all game actions
   - Real-time data updates across all views when game state changes
   - Automatic logging of significant events in the sect chronicles
   - Comprehensive turn end processing with detailed results

### User Interface

1. **Main Layout Structure**
   - Header bar with sect emblem and resource dashboard
   - Main navigation with icon-based tabs for easy access
   - Context-sensitive sidebar that updates based on the current route
   - Status bar with notifications and quick action buttons

2. **Sect View**
   - Overview of sect status, facilities, and resources
   - Facility management and upgrades
   - Sect-wide actions and policies

3. **Disciples View**
   - Comprehensive disciple listing with filtering and sorting
   - Attribute visualization with custom progress bars
   - Quick actions for common disciple management tasks

4. **Cultivation View**
   - Tabbed interface for disciples, methods, and resource allocation
   - Method effectiveness visualization with star rating system
   - Resource allocation interface with real-time feedback
   - Automatic cultivation assignment system

5. **Territories View**
   - Interactive territory map with selection functionality
   - Resource node visualization and management
   - Territory expansion and development options

6. **Events View**
   - Event management with tabbed interface for current, upcoming, and historical events
   - Color-coded event cards based on event type
   - Decision interface for event resolution
   - End turn functionality with comprehensive results display

7. **Logs View (Sect Chronicles)**
   - Chronological timeline of sect history
   - Filtering system for log entries by category and time period
   - Notable events highlighting and detailed view
   - Automatic logging of significant sect events
   - Comprehensive API response logging
   - Bottleneck creation and resolution testing

### Visual Design

- Traditional Chinese aesthetic with fantasy elements
- Color scheme based on earthy tones with gold accents
- Responsive layout with scrollable content areas
- Intuitive progress indicators for cultivation and bottlenecks

## Distinguishing Features

1. **Bottleneck System**
   - Realistic representation of cultivation challenges
   - Two-tiered approach with minor and major obstacles
   - Visual progress tracking for insight accumulation
   - Realm-specific treasure recommendations

2. **Cultivation Methods**
   - Different approaches to advancement with unique benefits
   - Risk/reward balancing with cultivation deviation chance
   - Method effectiveness varies based on disciple attributes

3. **Realm Progression**
   - Exponential power scaling between realms
   - Increasing difficulty of advancement
   - New abilities unlocked at higher realms

## Design Philosophy

Sectomie3 aims to capture the essence of cultivation novels while providing engaging gameplay. The design focuses on:

1. **Immersion over Micromanagement**
   - Streamlined interfaces that focus on important decisions
   - Automated routine tasks where appropriate
   - Rich contextual information about the cultivation world

2. **Meaningful Choices**
   - Different cultivation paths with unique advantages
   - Resource allocation decisions with long-term consequences
   - Strategic breakthrough timing

3. **Progression Satisfaction**
   - Clear visualization of advancement
   - Rewarding breakthrough moments
   - Tangible power increases with realm advancement

## Current Development Focus

1. **Enhanced User Experience**
   - Intuitive bottleneck visualization
   - Comprehensive tooltips and help system
   - Mobile-responsive design

2. **Expanded Game Mechanics**
   - Treasure inventory management
   - Sect relationship system
   - Advanced disciple interaction

3. **Technical Improvements**
   - Optimized API endpoints
   - Comprehensive error handling
   - Automated testing scenarios

## Cultivation System Overhaul

The cultivation system has been overhauled to reduce micromanagement and improve strategic depth:

1. **Turn-Based Automatic Cultivation** ✓
   - Disciples automatically cultivate each month/turn
   - Base progression determined by attributes (spiritual, comprehension)
   - No need for manual cultivation sessions
   - Cultivation progress tracked and reported at turn end

2. **Strategic Planning** ✓
   - Players set cultivation methods at the beginning of a period
   - Assign resources (spirit stones) to boost cultivation
   - Resource allocation provides multiple benefits:
     - Increased cultivation speed
     - Improved breakthrough chance
     - Enhanced deviation resistance

3. **Modifiers System** ✓
   - **Technique Manuals**: Provide permanent or long-term boosts
   - **Cultivation Methods**: Different methods favor different attributes and realms
   - **Method Compatibility**: Methods have varying effectiveness based on disciple attributes
   - **Resource Allocation**: Spirit stones provide scaling bonuses to cultivation

4. **Monthly Calculation Formula** ✓
   ```
   Monthly Qi Gain = Base Rate × Spiritual Attribute × Method Multiplier × Facility Bonus × Resource Bonus
   ```

5. **Enhanced Cultivation UI** ✓
   - **Method Selection Cards**: Visual cards with effectiveness ratings
   - **Resource Allocation Slider**: Intuitive control for spirit stone allocation
   - **Cultivation Forecast**: Projected qi gain and months to breakthrough
   - **Method Compatibility System**: Visual indication of method suitability for each disciple
   - **Method Attributes Visualization**: Detailed breakdown of method strengths

## UI Structure Redesign

### Main Layout Structure ✓

The main layout structure has been implemented with the following components:

```
┌─────────────────────────────────────────────────────────────────────┐
│ ┌─────────────┐ ┌─────────────────────────────────────────────────┐ │
│ │   SECT      │ │                  HEADER BAR                     │ │
│ │   EMBLEM    │ │  [Game Date] [Turn #] [Spirit Stones] [Actions] │ │
│ └─────────────┘ └─────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────────────┤
│ ┌─────────────────────────────────────────────────────────────────┐ │
│ │                       MAIN NAVIGATION TABS                      │ │
│ │  [Home] [Sect] [Disciples] [Cultivation] [Territories] [Events] [Logs]   │ │
│ └─────────────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────────────┤
│ ┌─────────────┐ ┌─────────────────────────────────────────────────┐ │
│ │             │ │                                                 │ │
│ │  CONTEXT-   │ │                                                 │ │
│ │  SENSITIVE  │ │                                                 │ │
│ │  SIDEBAR    │ │                MAIN CONTENT AREA                │ │
│ │             │ │                                                 │ │
│ │  • Section 1│ │                                                 │ │
│ │  • Section 2│ │                                                 │ │
│ │  • Section 3│ │                                                 │ │
│ │             │ │                                                 │ │
│ └─────────────┘ └─────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────────────┤
│ ┌─────────────────────────────────────────────────────────────────┐ │
│ │                         STATUS BAR                              │ │
│ │  [Notifications] [Quick Actions] [End Turn Button]              │ │
│ └─────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

### Key Layout Features ✓

1. **Header Bar**
   - Sect emblem and name on the left
   - Game information (year, month, turn number) in the center
   - Resource dashboard (spirit stones, herbs, treasures) on the right

2. **Main Navigation**
   - Clear, icon-based navigation tabs
   - Visual indicators for active section
   - Consistent placement for easy access

3. **Context-Sensitive Sidebar**
   - Dynamic content that changes based on the active section
   - Organized into collapsible sections
   - Provides quick access to relevant information and actions

4. **Status Bar**
   - Notifications system for important events
   - Quick action buttons for common tasks
   - End Turn button for game progression

### Section View Components ✓

#### 1. Sect View
- **Sect Info Card**: Displays sect name, level, reputation, and key statistics
- **Sect Actions**: Quick access to common sect management actions
- **Facilities Grid**: Visual representation of sect facilities with levels and effects
- **Responsive Design**: Adapts to different screen sizes while maintaining usability

#### 2. Disciples View
- **Disciples Statistics**: Overview of disciple numbers, average cultivation, and recruitment capacity
- **Action Buttons**: Recruit, assign tasks, and manage disciples
- **Disciples List**: Sortable and filterable list of all disciples
- **Disciple Cards**: Displays name, cultivation realm, attributes, and status
- **Quick Actions**: Direct access to disciple details and cultivation assignment

#### 3. Cultivation View
- **Tabbed Interface**: Separate tabs for disciples, methods, and resource allocation
- **Method Cards**: Visual representation of cultivation methods with effectiveness ratings
- **Assignment Cards**: Current cultivation assignments for each disciple
- **Resource Allocation**: Overview of spirit stone distribution and efficiency
- **Method Attributes**: Visual ratings for qi generation, breakthrough chance, safety, and attribute growth

#### 4. Territories View
- **Territory Statistics**: Overview of territories, resource nodes, and income
- **Interactive Map**: Visual representation of sect territories
- **Territory Details**: In-depth information about selected territory
- **Resource Nodes**: List of resource-generating nodes in each territory
- **Structure Management**: Interface for building and upgrading territory structures

#### 5. Events View
- **Event Categories**: Current events, upcoming events, and event history
- **Event Cards**: Visual representation of events with type, urgency, and actions
- **Decision Interface**: Tools for responding to events and making decisions
- **Filtering System**: Tools to filter and sort different types of events

#### 6. Logs View
- **Chronicle Timeline**: Chronological record of sect history
- **Filtering System**: Filter logs by category, time period, and keywords
- **Notable Events**: Highlighted significant events in sect history
- **Detailed Entries**: Comprehensive information about each historical event

### Cultivation Assignment Interface ✓

The new cultivation assignment interface has been implemented with the following components:

```
┌─────────────────────────────────────────────────────────────────────┐
│                     CULTIVATION ASSIGNMENT                          │
├─────────────────────────────────────────────────────────────────────┤
│ ┌─────────────────────────────────────────────────────────────────┐ │
│ │                   CURRENT ASSIGNMENT BANNER                     │ │
│ │  [Method Name] with [Resource Allocation] spirit stones         │ │
│ └─────────────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────────────┤
│ ┌─────────────────────────────────────────────────────────────────┐ │
│ │                     METHOD SELECTION CARDS                      │ │
│ │ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐   │ │
│ │ │Method 1 │ │Method 2 │ │Method 3 │ │Method 4 │ │Method 5 │   │ │
│ │ │★★★☆☆    │ │★★★★☆    │ │★★☆☆☆    │ │★★★★★    │ │★☆☆☆☆    │   │ │
│ │ └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘   │ │
│ └─────────────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────────────┤
│ ┌─────────────────────────┐ ┌─────────────────────────────────────┐ │
│ │                         │ │                                     │ │
│ │   RESOURCE ALLOCATION   │ │      SELECTED METHOD DETAILS        │ │
│ │                         │ │                                     │ │
│ │  Spirit Stones: [Slider]│ │  Method Description                 │ │
│ │                         │ │  Method Attributes                  │ │
│ │  Monthly Benefits:      │ │  - Qi Generation       [====---]    │ │
│ │  - Cultivation Speed    │ │  - Breakthrough Bonus [===----]    │ │
│ │  - Breakthrough Chance  │ │  - Safety             [======-]    │ │
│ │  - Deviation Resistance │ │  - Attribute Growth   [==-----]    │ │
│ │                         │ │                                     │ │
│ │  Monthly Forecast:      │ │  Compatibility with Disciple:       │ │
│ │  - Est. Qi Gain         │ │  [====================] 85%         │ │
│ │  - Months to Breakthrough│ │  Excellent                         │ │
│ │  - Resource Efficiency   │ │                                     │ │
│ │                         │ │                                     │ │
│ └─────────────────────────┘ └─────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────────────┤
│ ┌─────────────────────────────────────────────────────────────────┐ │
│ │                      ACTION BUTTONS                            │ │
│ │        [Assign Cultivation Method]    [Cancel]                  │ │
│ └─────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

### Key UI Components

1. **Header Bar** ✓
   - Sect emblem and identification
   - Game date and turn counter
   - Key resources display
   - Action points available
   - Settings access

2. **Main Navigation Tabs** ✓
   - Sect: Overview of sect status and buildings
   - Disciples: Disciple management and cultivation
   - Territories: Spirit veins and resource collection
   - Treasures: Inventory management
   - Events: Current events and missions
   - Logs: History of important actions

3. **Context-Sensitive Sidebar** ✓
   - Changes based on selected main tab
   - Provides sub-navigation for each section
   - Quick filters and sorting options

4. **Main Content Area** ✓
   - Displays content for selected tab/sidebar item
   - Sortable lists with key information
   - Visual indicators for status and progress

5. **Enhanced Cultivation Interface** ✓
   - **Current Assignment Banner**: Shows active cultivation method and resource allocation
   - **Method Selection Cards**: Visual cards with effectiveness ratings (1-5 stars)
   - **Resource Allocation Controls**: Slider for spirit stone allocation with real-time feedback
   - **Method Details Panel**: Comprehensive information about selected cultivation method
   - **Method Attributes Visualization**: Visual ratings for qi generation, breakthrough, safety, and attributes
   - **Disciple Compatibility System**: Meter showing method suitability for the specific disciple
   - **Cultivation Forecast**: Projections for qi gain, breakthrough timeline, and resource efficiency

6. **Turn End Processing** ✓
   - **Automatic Cultivation**: Disciples cultivate automatically at turn end
   - **Progress Summary**: Detailed report of cultivation progress for all disciples
   - **Event Notifications**: Alerts for important events like breakthroughs and deviations
   - **Resource Updates**: Summary of resource changes during the turn
   - Group action capabilities

5. **Status Bar**
   - Notifications for important events
   - Quick actions for common tasks
   - Prominent End Turn button
   - Time control options

### Special Screens

1. **Disciple Detail Screen**
   - Tab system for different aspects (Overview, Cultivation, Equipment, etc.)
   - Detailed stats and progress tracking
   - Bottleneck visualization and management

2. **Cultivation Assignment Screen**
   - Batch assignment of cultivation methods
   - Resource allocation interface
   - Effectiveness ratings for different combinations

3. **Territory Management**
   - Visual map of sect territories
   - Resource overlays and building placement
   - Disciple assignment to locations

### Visual Design

- **Primary Theme**: Deep burgundy and gold
- **Secondary Elements**: Earth tones (browns, greens)
- **Accent Colors**: Blue for cultivation, green for positive outcomes, red for warnings
- **Mobile Adaptations**: Collapsible elements and prioritized information
