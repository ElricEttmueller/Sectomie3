#!/usr/bin/env python3
"""
Flask API for the Sectomie Cultivation System - Single Sect Focus
"""

from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
import json
import random
import uuid
from datetime import datetime
import os
import sys
import traceback

# Import game state manager
from game_state import GameState

# Add the parent directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from member import Member
from sect import Sect
from data_manager import DataManager

app = Flask(__name__)

# Configure CORS more explicitly
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

# Add error handler to ensure CORS headers are set even on errors
@app.errorhandler(500)
def handle_500_error(e):
    response = jsonify({'error': 'Internal server error', 'details': str(e)})
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    return response, 500

# Initialize data manager
data_manager = DataManager()

# Add global OPTIONS method handling for all API routes
@app.route('/api/<path:path>', methods=['OPTIONS'])
def handle_api_options(path):
    response = make_response()
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    return response

# Global variables to store sects and members
sects = []
members = []

# Player sect ID (the main sect being managed)
player_sect_id = 0  # Default to the first sect

# Initialize game state
game_state = GameState()
game_state.sect_id = player_sect_id

# Try to load existing data
try:
    sects, members = data_manager.load_data("example_data.json")
except:
    # If no data exists, create some example data
    azure_peak = Sect("Azure Peak Sect", "Sword Dao", 3, 
                      "A prestigious sword cultivation sect located on Azure Peak Mountain")
    mystic_cloud = Sect("Mystic Cloud Sect", "Alchemy Dao", 5, 
                        "Ancient sect renowned for its alchemy and medicine cultivation")
    
    # Add some spirit veins to the sects
    azure_peak.add_territory("Azure Peak Mountain", 4)
    mystic_cloud.add_territory("Cloud Valley", 6)
    
    # Add some techniques to the sects
    azure_peak.techniques = ["Azure Sword Art", "Flowing Water Sword Technique", "Mountain Cleaving Sword"]
    mystic_cloud.techniques = ["Five Elements Pill Refinement", "Cloud Gathering Formation", "Spiritual Essence Extraction"]
    
    # Create disciples
    li_mei = Member("Li Mei", 20, "Sword", 85, 65, 75)
    li_mei.techniques = ["Azure Sword Art"]
    
    zhang_wei = Member("Zhang Wei", 35, "Alchemy", 60, 90, 80)
    zhang_wei.techniques = ["Five Elements Pill Refinement"]
    zhang_wei.realm = 2  # Foundation Establishment
    zhang_wei.realm_stage = 3  # Late stage
    zhang_wei.max_qi = 400
    zhang_wei.qi = 350
    zhang_wei.elixirs_refined = 27
    
    # Add disciples to sects
    azure_peak.add_member(li_mei)
    mystic_cloud.add_member(zhang_wei)
    
    sects = [azure_peak, mystic_cloud]
    members = [li_mei, zhang_wei]
    
    # Save the example data
    data_manager.save_data(sects, members, "example_data.json")

# API Routes

@app.route('/api/player-sect', methods=['GET'])
def get_player_sect():
    """Get the player's sect (the main sect being managed)"""
    if player_sect_id < 0 or player_sect_id >= len(sects):
        return jsonify({'error': 'Player sect not found'}), 404
    
    sect = sects[player_sect_id]
    return jsonify({
        'id': player_sect_id,
        'name': sect.name,
        'dao_heritage': sect.dao_heritage,
        'tier': sect.tier,
        'description': sect.description,
        'spirit_stones': sect.spirit_stones,
        'spirit_veins': sect.spirit_veins,
        'spirit_vein_quality': sect.spirit_vein_quality,
        'elixir_fields': sect.elixir_fields,
        'sect_influence': sect.sect_influence,
        'reputation': sect.reputation,
        'territories': sect.territories,
        'formation_strength': sect.formation_strength,
        'disciples_count': len(sect.members),
        'techniques_count': len(sect.techniques),
        'secret_manuals_count': len(sect.secret_manuals)
    })

@app.route('/api/player-sect/disciples', methods=['GET'])
def get_player_sect_disciples():
    """Get all disciples in the player's sect"""
    if player_sect_id < 0 or player_sect_id >= len(sects):
        return jsonify({'error': 'Player sect not found'}), 404
    
    sect = sects[player_sect_id]
    return jsonify([{
        'id': members.index(member),
        'name': member.name,
        'age': member.age,
        'path': member.path,
        'realm': member.get_realm_name(),
        'stage': member.get_stage_name(),
        'combat_power': member.get_combat_power()
    } for member in sect.members])

@app.route('/api/player-sect/resources', methods=['GET'])
def get_player_sect_resources():
    """Get detailed resources for the player's sect"""
    if player_sect_id < 0 or player_sect_id >= len(sects):
        return jsonify({'error': 'Player sect not found'}), 404
    
    sect = sects[player_sect_id]
    
    # Calculate monthly income
    monthly_income = sum(vein["output"] for vein in sect.spirit_veins)
    
    return jsonify({
        'spirit_stones': sect.spirit_stones,
        'spirit_veins': sect.spirit_veins,
        'elixir_fields': sect.elixir_fields,
        'monthly_income': monthly_income,
        'territories': sect.territories
    })

@app.route('/api/player-sect/knowledge', methods=['GET'])
def get_player_sect_knowledge():
    """Get knowledge assets for the player's sect"""
    if player_sect_id < 0 or player_sect_id >= len(sects):
        return jsonify({'error': 'Player sect not found'}), 404
    
    sect = sects[player_sect_id]
    return jsonify({
        'techniques': sect.techniques,
        'secret_manuals': sect.secret_manuals,
        'alchemy_recipes': sect.alchemy_recipes,
        'formation_diagrams': sect.formation_diagrams,
        'artifact_blueprints': sect.artifact_blueprints
    })

@app.route('/api/player-sect/collect-resources', methods=['POST'])
def collect_player_sect_resources():
    """Collect resources from spirit veins for the player's sect"""
    if player_sect_id < 0 or player_sect_id >= len(sects):
        return jsonify({'error': 'Player sect not found'}), 404
    
    sect = sects[player_sect_id]
    initial_stones = sect.spirit_stones
    monthly_income = sum(vein["output"] for vein in sect.spirit_veins)
    sect.spirit_stones += monthly_income
    
    # Save the updated data
    data_manager.save_data(sects, members, "example_data.json")
    
    return jsonify({
        'initial_stones': initial_stones,
        'income': monthly_income,
        'current_stones': sect.spirit_stones
    })

@app.route('/api/sects', methods=['GET'])
def get_sects():
    """Get all sects"""
    return jsonify([{
        'id': i,
        'name': sect.name,
        'dao_heritage': sect.dao_heritage,
        'tier': sect.tier,
        'description': sect.description,
        'disciples_count': len(sect.members),
        'spirit_stones': sect.spirit_stones
    } for i, sect in enumerate(sects)])

@app.route('/api/sects/<int:sect_id>', methods=['GET'])
def get_sect(sect_id):
    """Get details for a specific sect"""
    if sect_id < 0 or sect_id >= len(sects):
        return jsonify({'error': 'Sect not found'}), 404
    
    sect = sects[sect_id]
    return jsonify({
        'id': sect_id,
        'name': sect.name,
        'dao_heritage': sect.dao_heritage,
        'tier': sect.tier,
        'description': sect.description,
        'spirit_stones': sect.spirit_stones,
        'spirit_veins': sect.spirit_veins,
        'spirit_vein_quality': sect.spirit_vein_quality,
        'elixir_fields': sect.elixir_fields,
        'sect_influence': sect.sect_influence,
        'reputation': sect.reputation,
        'territories': sect.territories,
        'formation_strength': sect.formation_strength,
        'disciples': [{
            'id': members.index(member),
            'name': member.name
        } for member in sect.members],
        'techniques': sect.techniques,
        'secret_manuals': sect.secret_manuals,
        'alchemy_recipes': sect.alchemy_recipes,
        'formation_diagrams': sect.formation_diagrams,
        'artifact_blueprints': sect.artifact_blueprints
    })

@app.route('/api/disciples', methods=['GET'])
def get_disciples():
    """Get all disciples"""
    return jsonify([{
        'id': i,
        'name': member.name,
        'age': member.age,
        'path': member.path,
        'realm': member.get_realm_name(),
        'stage': member.get_stage_name(),
        'sect': member.sect.name if member.sect else None
    } for i, member in enumerate(members)])

@app.route('/api/disciples/<int:disciple_id>', methods=['GET'])
def get_disciple(disciple_id):
    """Get details for a specific disciple"""
    if disciple_id < 0 or disciple_id >= len(members):
        return jsonify({'error': 'Disciple not found'}), 404
    
    member = members[disciple_id]
    return jsonify({
        'id': disciple_id,
        'name': member.name,
        'age': member.age,
        'path': member.path,
        'physical': member.physical,
        'spiritual': member.spiritual,
        'comprehension': member.comprehension,
        'realm': member.realm,
        'realm_name': member.get_realm_name(),
        'realm_stage': member.realm_stage,
        'stage_name': member.get_stage_name(),
        'qi': member.qi,
        'max_qi': member.max_qi,
        'techniques': member.techniques,
        'spirit_stones': member.spirit_stones,
        'breakthrough_chance': member.breakthrough_chance,
        'sect': member.sect.name if member.sect else None,
        'combat_power': member.get_combat_power()
    })

@app.route('/api/disciples/<int:disciple_id>/cultivate', methods=['POST'])
def cultivate(disciple_id):
    """Cultivate for a disciple using the legacy hour-based method"""
    if disciple_id < 0 or disciple_id >= len(members):
        return jsonify({'error': 'Disciple not found'}), 404
    
    data = request.get_json()
    hours = data.get('hours', 1)
    
    member = members[disciple_id]
    qi_gained = member.cultivate(hours)
    
    # Save the updated data
    data_manager.save_data(sects, members, "example_data.json")
    
    return jsonify({
        'qi_gained': qi_gained,
        'current_qi': member.qi,
        'max_qi': member.max_qi,
        'breakthrough_chance': member.breakthrough_chance
    })

@app.route('/api/disciples/<int:disciple_id>/cultivate-method', methods=['POST'])
def cultivate_with_method(disciple_id):
    """Cultivate for a disciple using a specific cultivation method"""
    try:
        # Ensure CORS headers are set in the response
        response = make_response()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        
        if disciple_id < 0 or disciple_id >= len(members):
            response.status_code = 404
            response.data = json.dumps({'error': 'Disciple not found', 'success': False})
            return response
        
        # Parse request data
        data = request.get_json()
        if data is None:
            data = {}
        method = data.get('method', 'qi_circulation')
        
        # Get the player sect
        sect = sects[game_state.sect_id]
        member = members[disciple_id]
        
        # Check if sect has enough resources
        method_costs = {
            'qi_circulation': {'spirit_stones': 50},
            'essence_refinement': {'spirit_stones': 200},
            'dao_heart_tempering': {'spirit_stones': 400, 'spirit_herbs': 1},
            'heavenly_tribulation': {'spirit_stones': 800, 'dao_crystals': 1}
        }
        
        # Get the cost for the selected method
        cost = method_costs.get(method, {'spirit_stones': 50})
        
        # Initialize resources if they don't exist
        if not hasattr(sect, 'spirit_herbs'):
            sect.spirit_herbs = 0
        
        if not hasattr(sect, 'dao_crystals'):
            sect.dao_crystals = 0
        
        # Check spirit stones
        if sect.spirit_stones < cost.get('spirit_stones', 0):
            result = {
                'success': False,
                'error': 'Not enough spirit stones',
                'required': cost.get('spirit_stones', 0),
                'available': sect.spirit_stones
            }
            response.status_code = 400
            response.data = json.dumps(result)
            return response
        
        # Check special resources
        if 'spirit_herbs' in cost and sect.spirit_herbs < cost['spirit_herbs']:
            result = {
                'success': False,
                'error': 'Not enough spirit herbs',
                'required': cost['spirit_herbs'],
                'available': sect.spirit_herbs
            }
            response.status_code = 400
            response.data = json.dumps(result)
            return response
        
        if 'dao_crystals' in cost and sect.dao_crystals < cost['dao_crystals']:
            result = {
                'success': False,
                'error': 'Not enough dao crystals',
                'required': cost['dao_crystals'],
                'available': sect.dao_crystals
            }
            response.status_code = 400
            response.data = json.dumps(result)
            return response
        
        # Deduct resources
        sect.spirit_stones -= cost.get('spirit_stones', 0)
        if 'spirit_herbs' in cost:
            sect.spirit_herbs -= cost['spirit_herbs']
        if 'dao_crystals' in cost:
            sect.dao_crystals -= cost['dao_crystals']
        
        # Debug print before calling cultivation method
        print(f"About to call cultivate_with_method with method: {method}")
        print(f"Member: {member.name}, Sect: {sect.name}")
        
        # Apply cultivation effects
        results = member.cultivate_with_method(method, sect)
        
        # Debug print after calling cultivation method
        print(f"Cultivation results: {results}")
        
        # Add resource info to results
        results['resources'] = {
            'spirit_stones': sect.spirit_stones,
            'spirit_herbs': getattr(sect, 'spirit_herbs', 0),
            'dao_crystals': getattr(sect, 'dao_crystals', 0)
        }
        
        # Add disciple current stats to results
        results['disciple'] = {
            'qi': member.qi,
            'max_qi': member.max_qi,
            'breakthrough_chance': member.breakthrough_chance,
            'physical': member.physical,
            'spiritual': member.spiritual,
            'comprehension': member.comprehension
        }
        
        # Save the updated data
        data_manager.save_data(sects, members, "example_data.json")
        
        # Return successful response
        response.status_code = 200
        response.data = json.dumps(results)
        return response
        
    except Exception as e:
        # Log the error
        print(f"Error in cultivation method: {str(e)}")
        print(traceback.format_exc())
        
        # Return error response with CORS headers
        response = make_response()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.status_code = 500
        response.data = json.dumps({
            'success': False,
            'error': 'Internal server error',
            'details': str(e)
        })
        return response

@app.route('/api/disciples/<int:disciple_id>/breakthrough', methods=['POST'])
def breakthrough(disciple_id):
    """Attempt breakthrough for a disciple"""
    if disciple_id < 0 or disciple_id >= len(members):
        return jsonify({'error': 'Disciple not found'}), 404
    
    member = members[disciple_id]
    success, new_realm, new_stage = member.attempt_breakthrough()
    
    # Save the updated data
    data_manager.save_data(sects, members, "example_data.json")
    
    return jsonify({
        'success': success,
        'realm': member.get_realm_name(),
        'stage': member.get_stage_name(),
        'qi': member.qi,
        'max_qi': member.max_qi,
        'breakthrough_chance': member.breakthrough_chance
    })

# Keep the original endpoint for backward compatibility
@app.route('/api/sects/<int:sect_id>/collect-resources', methods=['POST'])
def collect_resources(sect_id):
    """Collect resources from spirit veins for a sect"""
    if sect_id < 0 or sect_id >= len(sects):
        return jsonify({'error': 'Sect not found'}), 404
    
    sect = sects[sect_id]
    initial_stones = sect.spirit_stones
    monthly_income = sum(vein["output"] for vein in sect.spirit_veins)
    sect.spirit_stones += monthly_income
    
    # Save the updated data
    data_manager.save_data(sects, members, "example_data.json")
    
    return jsonify({
        'initial_stones': initial_stones,
        'income': monthly_income,
        'current_stones': sect.spirit_stones
    })

# Recruitment system endpoints
@app.route('/api/recruitment/candidates', methods=['GET'])
def get_recruitment_candidates():
    """Generate random disciples for recruitment"""
    # Generate 3 random disciples as recruitment candidates
    candidates = []
    
    # Define possible paths and their attributes tendencies
    paths = {
        "Sword": {"physical": (70, 95), "spiritual": (50, 80), "comprehension": (50, 80)},
        "Fire": {"physical": (60, 85), "spiritual": (70, 90), "comprehension": (50, 75)},
        "Water": {"physical": (50, 75), "spiritual": (70, 90), "comprehension": (60, 85)},
        "Earth": {"physical": (75, 95), "spiritual": (50, 70), "comprehension": (60, 80)},
        "Wind": {"physical": (60, 80), "spiritual": (65, 85), "comprehension": (65, 85)},
        "Lightning": {"physical": (65, 90), "spiritual": (65, 90), "comprehension": (50, 75)},
        "Alchemy": {"physical": (40, 70), "spiritual": (75, 95), "comprehension": (70, 90)},
        "Formation": {"physical": (50, 70), "spiritual": (70, 90), "comprehension": (75, 95)},
    }
    
    # Chinese-inspired first and last names
    first_names = ["Wei", "Li", "Zhang", "Liu", "Chen", "Yang", "Huang", "Zhao", "Wu", "Zhou", 
                  "Sun", "Xu", "Feng", "Hu", "Gao", "Zhu", "Mei", "Jin", "Ye", "Bai"]
    last_names = ["Xiao", "Ming", "Feng", "Yu", "Hui", "Jie", "Ling", "Cheng", "Yun", "Hao",
                 "Jian", "Qing", "Tao", "Kai", "Jun", "Yi", "Xue", "Wen", "Rui", "Ping"]
    
    for _ in range(3):
        # Generate a unique ID for the candidate
        candidate_id = str(uuid.uuid4())
        
        # Generate a random name
        name = f"{random.choice(last_names)} {random.choice(first_names)}"
        
        # Generate a random age (16-25 for new disciples)
        age = random.randint(16, 25)
        
        # Select a random path
        path = random.choice(list(paths.keys()))
        path_attributes = paths[path]
        
        # Generate attributes based on the path's tendencies
        physical = random.randint(path_attributes["physical"][0], path_attributes["physical"][1])
        spiritual = random.randint(path_attributes["spiritual"][0], path_attributes["spiritual"][1])
        dao_comprehension = random.randint(path_attributes["comprehension"][0], path_attributes["comprehension"][1])
        
        # All new recruits start at Mortal realm
        realm = 0  # Mortal
        realm_stage = random.randint(0, 3)  # Random stage within Mortal realm
        
        # Calculate a basic combat power
        combat_power = int((physical + spiritual + dao_comprehension) / 3)
        
        candidates.append({
            "id": candidate_id,
            "name": name,
            "age": age,
            "path": path,
            "physical_foundation": physical,
            "spiritual_sensitivity": spiritual,
            "dao_comprehension": dao_comprehension,
            "realm": "Mortal",
            "stage": ["Early", "Middle", "Late", "Peak"][realm_stage],
            "combat_power": combat_power
        })
    
    return jsonify(candidates)

@app.route('/api/recruitment/select', methods=['POST'])
def select_recruit():
    """Add a selected recruit to the player's sect"""
    if player_sect_id < 0 or player_sect_id >= len(sects):
        return jsonify({'error': 'Player sect not found'}), 404
    
    data = request.get_json()
    candidate_id = data.get('candidate_id')
    
    if not candidate_id:
        return jsonify({'error': 'No candidate selected'}), 400
    
    # In a real implementation, we would validate the candidate ID against a temporary storage
    # For simplicity, we'll create a new disciple based on the ID (assuming it's valid)
    
    # Cost for recruitment
    recruitment_cost = 500
    
    sect = sects[player_sect_id]
    
    # Check if the sect has enough spirit stones
    if sect.spirit_stones < recruitment_cost:
        return jsonify({'error': 'Insufficient spirit stones'}), 400
    
    # Deduct the cost
    sect.spirit_stones -= recruitment_cost
    
    # Create a new disciple with random but reasonable stats
    # In a real implementation, we would retrieve the actual candidate data
    # For now, we'll generate a new disciple with random stats
    
    # Chinese-inspired first and last names
    first_names = ["Wei", "Li", "Zhang", "Liu", "Chen", "Yang", "Huang", "Zhao", "Wu", "Zhou"]
    last_names = ["Xiao", "Ming", "Feng", "Yu", "Hui", "Jie", "Ling", "Cheng", "Yun", "Hao"]
    
    name = f"{random.choice(last_names)} {random.choice(first_names)}"
    age = random.randint(16, 25)
    path = random.choice(["Sword", "Fire", "Water", "Earth", "Wind", "Lightning", "Alchemy", "Formation"])
    physical = random.randint(50, 90)
    spiritual = random.randint(50, 90)
    comprehension = random.randint(50, 90)
    
    new_disciple = Member(name, age, path, physical, spiritual, comprehension)
    
    # Add the new disciple to the sect and global members list
    sect.add_member(new_disciple)
    members.append(new_disciple)
    
    # Save the updated data
    data_manager.save_data(sects, members, "example_data.json")
    
    # Return the new disciple's information
    return jsonify({
        'success': True,
        'disciple': {
            'id': len(members) - 1,  # Index of the new disciple
            'name': new_disciple.name,
            'age': new_disciple.age,
            'path': new_disciple.path,
            'realm': new_disciple.get_realm_name(),
            'stage': new_disciple.get_stage_name(),
            'combat_power': new_disciple.get_combat_power()
        },
        'cost': recruitment_cost,
        'remaining_spirit_stones': sect.spirit_stones
    })

# Turn-based system endpoints
@app.route('/api/game-state', methods=['GET'])
def get_game_state():
    """Get the current game state"""
    return jsonify({
        'current_turn': game_state.current_turn,
        'game_date': game_state.get_game_date_string(),
        'sect_id': game_state.sect_id,
        'spirit_stones': sects[game_state.sect_id].spirit_stones if game_state.sect_id < len(sects) else 0
    })

@app.route('/api/end-turn', methods=['POST'])
def end_turn():
    """End the current turn and process all turn-end events"""
    # Process turn end
    results = game_state.process_turn_end(sects, members)
    
    # Advance to next turn
    new_turn = game_state.advance_turn()
    
    # Save the updated data
    data_manager.save_data(sects, members, "example_data.json")
    
    # Return the results
    return jsonify({
        'new_turn': new_turn,
        'game_date': game_state.get_game_date_string(),
        'results': results
    })

if __name__ == '__main__':
    app.run(debug=True)
