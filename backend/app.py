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

@app.route('/api/disciples/<int:disciple_id>/force-peak', methods=['POST'])
def force_peak(disciple_id):
    """Force a disciple to Peak stage for testing realm advancement"""
    if disciple_id < 0 or disciple_id >= len(members):
        return jsonify({'error': 'Disciple not found'}), 404
    
    member = members[disciple_id]
    member.realm_stage = 4  # Set to Peak stage
    member.qi = member.max_qi  # Fill qi to maximum
    member.breakthrough_chance = 100  # Ensure breakthrough success
    
    # Save the updated data
    data_manager.save_data(sects, members, "example_data.json")
    
    return jsonify({
        'message': f'Disciple {member.name} has been forced to Peak stage',
        'realm': member.get_realm_name(),
        'stage': member.get_stage_name(),
        'realm_stage': member.realm_stage
    })

@app.route('/api/disciples/<int:disciple_id>/clear-bottleneck', methods=['POST'])
def clear_bottleneck(disciple_id):
    """Clear any bottlenecks for a disciple"""
    if disciple_id < 0 or disciple_id >= len(members):
        return jsonify({'error': 'Disciple not found'}), 404
    
    member = members[disciple_id]
    
    # Print current bottleneck status
    print(f"\nCLEARING BOTTLENECK FOR {member.name}:")
    print(f"Before: Bottleneck = {member.bottleneck}, Insights = {member.bottleneck_insights}/{member.insights_required}")
    
    # Clear bottleneck
    old_bottleneck = member.bottleneck
    member.bottleneck = "none"
    member.bottleneck_insights = 0
    member.insights_required = 0
    
    # Save the updated data
    data_manager.save_data(sects, members, "example_data.json")
    
    return jsonify({
        'message': f'Bottleneck cleared for {member.name}',
        'previous_bottleneck': old_bottleneck,
        'current_bottleneck': member.bottleneck
    })

@app.route('/api/disciples/<int:disciple_id>/breakthrough', methods=['POST'])
def breakthrough(disciple_id):
    """Attempt breakthrough for a disciple"""
    if disciple_id < 0 or disciple_id >= len(members):
        return jsonify({'error': 'Disciple not found'}), 404
    
    member = members[disciple_id]
    
    # Print debug info before breakthrough
    print(f"\nBREAKTHROUGH ATTEMPT FOR {member.name}:")
    print(f"Before: Realm {member.realm} ({member.get_realm_name()}), Stage {member.realm_stage} ({member.get_stage_name()})")
    print(f"Qi: {member.qi}/{member.max_qi}, Breakthrough chance: {member.breakthrough_chance}")
    
    # Attempt breakthrough
    results = member.attempt_breakthrough()
    
    # Print debug info after breakthrough
    print(f"After: Realm {member.realm} ({member.get_realm_name()}), Stage {member.realm_stage} ({member.get_stage_name()})")
    print(f"Success: {results['success']}, Message: {results['message']}\n")
    
    # Save the updated data
    data_manager.save_data(sects, members, "example_data.json")
    
    return jsonify(results)

@app.route('/api/disciples/<int:disciple_id>/meditate', methods=['POST'])
def meditate_for_insight(disciple_id):
    """Meditate to gain insights for overcoming minor bottlenecks"""
    if disciple_id < 0 or disciple_id >= len(members):
        return jsonify({'error': 'Disciple not found'}), 404
    
    member = members[disciple_id]
    results = member.meditate_for_insight()
    
    # Add disciple current stats to results
    results['disciple'] = {
        'bottleneck': member.bottleneck,
        'bottleneck_insights': member.bottleneck_insights,
        'insights_required': member.insights_required,
        'breakthrough_chance': member.breakthrough_chance
    }
    
    # Save the updated data
    data_manager.save_data(sects, members, "example_data.json")
    
    return jsonify(results)

@app.route('/api/add-treasure', methods=['POST'])
def add_treasure():
    """Add a treasure to the sect for testing purposes"""
    data = request.get_json()
    if data is None:
        data = {}
    
    treasure_type = data.get('treasure_type', '')
    quantity = data.get('quantity', 1)
    
    # Valid treasure types
    valid_treasures = [
        "spirit_pill", 
        "dao_comprehension_stone", 
        "heaven_and_earth_spirit_fruit",
        "nine_transformation_pill",
        "immortal_ascension_stone"
    ]
    
    if treasure_type not in valid_treasures:
        return jsonify({
            'success': False,
            'message': f'Invalid treasure type. Valid types are: {", ".join(valid_treasures)}'
        }), 400
    
    # Get the player sect
    sect = sects[game_state.sect_id]
    
    # Initialize treasures if needed
    if not hasattr(sect, 'treasures'):
        sect.treasures = {}
    
    # Add the treasure
    if treasure_type not in sect.treasures:
        sect.treasures[treasure_type] = 0
    
    sect.treasures[treasure_type] += quantity
    
    # Save the updated data
    data_manager.save_data(sects, members, "example_data.json")
    
    return jsonify({
        'success': True,
        'message': f'Added {quantity} {treasure_type.replace("_", " ")} to your sect.',
        'treasures': sect.treasures
    })

@app.route('/api/disciples/<int:disciple_id>/use-treasure', methods=['POST'])
def use_treasure(disciple_id):
    """Use a treasure to overcome a major bottleneck"""
    if disciple_id < 0 or disciple_id >= len(members):
        return jsonify({'error': 'Disciple not found'}), 404
    
    data = request.get_json()
    if data is None:
        data = {}
    treasure_type = data.get('treasure_type', '')
    
    # Get the player sect
    sect = sects[game_state.sect_id]
    member = members[disciple_id]
    
    # Check if sect has the treasure
    if not hasattr(sect, 'treasures'):
        sect.treasures = {}
    
    if treasure_type not in sect.treasures or sect.treasures.get(treasure_type, 0) <= 0:
        return jsonify({
            'success': False,
            'message': f'Your sect does not possess any {treasure_type.replace("_", " ")}.',
        }), 400
    
    # Use the treasure
    results = member.use_treasure_for_bottleneck(treasure_type)
    
    # If successful, consume the treasure
    if results['success']:
        sect.treasures[treasure_type] -= 1
    
    # Add disciple current stats to results
    results['disciple'] = {
        'bottleneck': member.bottleneck,
        'breakthrough_chance': member.breakthrough_chance
    }
    
    # Add sect treasures to results
    results['treasures'] = sect.treasures
    
    # Save the updated data
    data_manager.save_data(sects, members, "example_data.json")
    
    return jsonify(results)

@app.route('/api/disciples/<int:disciple_id>/update-attributes', methods=['POST'])
def update_disciple_attributes(disciple_id):
    """Update attributes for a specific disciple"""
    # Find the disciple
    if disciple_id < 0 or disciple_id >= len(members):
        return jsonify({'error': 'Disciple not found'}), 404
    
    disciple = members[disciple_id]
    data = request.get_json()
    
    # Update attributes with validation
    if 'physical' in data:
        disciple.physical = disciple._validate_stat(data['physical'])
    
    if 'spiritual' in data:
        disciple.spiritual = disciple._validate_stat(data['spiritual'])
    
    if 'comprehension' in data:
        disciple.comprehension = disciple._validate_stat(data['comprehension'])
    
    if 'qi' in data:
        disciple.qi = max(0, min(disciple.max_qi, data['qi']))
    
    if 'max_qi' in data:
        disciple.max_qi = max(100, data['max_qi'])
        # Ensure qi doesn't exceed max_qi
        disciple.qi = min(disciple.qi, disciple.max_qi)
    
    if 'breakthrough_chance' in data:
        disciple.breakthrough_chance = max(0, min(100, data['breakthrough_chance']))
    
    # Save the updated data
    data_manager.save_data(sects, members, "example_data.json")
    
    # Return the updated disciple
    return jsonify(disciple.to_dict())

@app.route('/api/disciples/<int:disciple_id>/create-bottleneck', methods=['POST'])
def create_bottleneck(disciple_id):
    """Create a bottleneck for a specific disciple (for testing)"""
    # Find the disciple
    if disciple_id < 0 or disciple_id >= len(members):
        return jsonify({'error': 'Disciple not found'}), 404
    
    disciple = members[disciple_id]
    data = request.get_json()
    
    # Get bottleneck type from request (default to minor)
    bottleneck_type = data.get('type', 'minor')
    
    # Validate bottleneck type
    if bottleneck_type not in ['minor', 'major']:
        return jsonify({'error': 'Invalid bottleneck type. Must be "minor" or "major"'}), 400
    
    # Create the bottleneck
    disciple.bottleneck = bottleneck_type
    
    # For minor bottlenecks, set random insights required
    if bottleneck_type == 'minor':
        disciple.insights_required = random.randint(3, 7)
        disciple.bottleneck_insights = 0
    
    # Save the updated data
    data_manager.save_data(sects, members, "example_data.json")
    
    # Return the updated disciple
    return jsonify({
        'success': True,
        'message': f'Created {bottleneck_type} bottleneck for {disciple.name}',
        'disciple': disciple.to_dict()
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

# Cultivation system overhaul endpoints
@app.route('/api/disciples/<int:disciple_id>/assign-cultivation-method', methods=['POST'])
def assign_cultivation_method(disciple_id):
    """Assign a cultivation method to a disciple"""
    try:
        data = request.get_json()
        method = data.get('method')
        resource_allocation = data.get('resource_allocation', 0)
        
        # Validate input
        if not method:
            return jsonify({
                "success": False,
                "message": "Method is required"
            }), 400
            
        # Find the disciple
        if disciple_id < 0 or disciple_id >= len(members):
            return jsonify({
                "success": False,
                "message": "Invalid disciple ID"
            }), 400
            
        disciple = members[disciple_id]
        
        # Get available methods to validate the requested method
        try:
            available_methods = disciple.get_cultivation_methods()
        except Exception as method_error:
            print(f"Error getting cultivation methods: {str(method_error)}")
            import traceback
            traceback.print_exc()
            # Provide a default set of methods if there's an error
            available_methods = {
                "qi_circulation": {
                    "name": "Qi Circulation",
                    "description": "A balanced method focusing on steady qi accumulation",
                    "effectiveness": 3,
                    "recommended_for": "beginners"
                }
            }
        
        if method not in available_methods:
            return jsonify({
                "success": False,
                "message": f"Method '{method}' is not available for this disciple"
            }), 400
            
        # Check if we have enough resources for allocation
        if resource_allocation > 0:
            player_sect = sects[player_sect_id]
            if player_sect.spirit_stones < resource_allocation:
                return jsonify({
                    "success": False,
                    "message": f"Not enough spirit stones for resource allocation. Required: {resource_allocation}, Available: {player_sect.spirit_stones}"
                }), 400
                
            # Deduct the resources
            player_sect.spirit_stones -= resource_allocation
            
        # Assign the method
        disciple.assigned_cultivation_method = method
        disciple.allocated_resources = resource_allocation
        
        method_details = available_methods[method]
        
        return jsonify({
            "success": True,
            "message": f"Assigned {method_details['name']} cultivation method to {disciple.name}",
            "disciple": {
                "id": disciple_id,
                "name": disciple.name,
                "assigned_method": method,
                "method_name": method_details['name'],
                "method_description": method_details['description'],
                "effectiveness": method_details['effectiveness'],
                "resource_allocation": resource_allocation
            }
        })
        
    except Exception as e:
        print(f"Error assigning cultivation method: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"Error: {str(e)}"
        }), 500

@app.route('/api/disciples/<int:disciple_id>/cultivation-methods', methods=['GET'])
def get_cultivation_methods(disciple_id):
    """Get available cultivation methods for a disciple with effectiveness ratings"""
    try:
        # Find the disciple
        if disciple_id < 0 or disciple_id >= len(members):
            return jsonify({
                "success": False,
                "message": "Invalid disciple ID"
            }), 400
            
        disciple = members[disciple_id]
        
        # Get available methods with effectiveness ratings
        try:
            methods = disciple.get_cultivation_methods()
        except Exception as method_error:
            print(f"Error in get_cultivation_methods: {str(method_error)}")
            import traceback
            traceback.print_exc()
            # Provide a default set of methods if there's an error
            methods = {
                "qi_circulation": {
                    "name": "Qi Circulation",
                    "description": "A balanced method focusing on steady qi accumulation",
                    "effectiveness": 3,
                    "recommended_for": "beginners"
                }
            }
        
        # Get currently assigned method if any
        assigned_method = getattr(disciple, 'assigned_cultivation_method', None)
        resource_allocation = getattr(disciple, 'allocated_resources', 0)
        
        return jsonify({
            "success": True,
            "disciple": {
                "id": disciple_id,
                "name": disciple.name,
                "assigned_method": assigned_method,
                "resource_allocation": resource_allocation
            },
            "methods": methods
        })
        
    except Exception as e:
        print(f"Error getting cultivation methods: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "success": False,
            "message": f"Error: {str(e)}"
        }), 500

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
    try:
        # Get the player sect for reference
        player_sect = sects[game_state.sect_id]
        
        # Store initial state for comparison
        initial_state = {
            'spirit_stones': player_sect.spirit_stones,
            'disciples': [{
                'id': i,
                'name': member.name,
                'qi': member.qi,
                'max_qi': member.max_qi,
                'breakthrough_chance': member.breakthrough_chance,
                'realm': member.realm,
                'realm_name': member.get_realm_name(),
                'realm_stage': member.realm_stage,
                'stage_name': member.get_stage_name()
            } for i, member in enumerate(members) if member.sect and member.sect.name == player_sect.name]
        }
        
        # Process turn end
        results = game_state.process_turn_end(sects, members)
        
        # Advance to next turn
        new_turn = game_state.advance_turn()
        
        # Compare with new state to identify changes
        changes = {
            'spirit_stones': player_sect.spirit_stones - initial_state['spirit_stones'],
            'disciples': []
        }
        
        # Track disciple changes
        for initial_disciple in initial_state['disciples']:
            disciple_id = initial_disciple['id']
            if disciple_id < len(members):
                current_disciple = members[disciple_id]
                disciple_changes = {
                    'id': disciple_id,
                    'name': current_disciple.name,
                    'qi_change': current_disciple.qi - initial_disciple['qi'],
                    'breakthrough_chance_change': current_disciple.breakthrough_chance - initial_disciple['breakthrough_chance'],
                    'realm_changed': current_disciple.realm != initial_disciple['realm'] or current_disciple.realm_stage != initial_disciple['realm_stage'],
                    'new_realm_name': current_disciple.get_realm_name(),
                    'new_stage_name': current_disciple.get_stage_name()
                }
                if any(value != 0 for key, value in disciple_changes.items() if key not in ['id', 'name', 'new_realm_name', 'new_stage_name', 'realm_changed']):
                    changes['disciples'].append(disciple_changes)
        
        # Add changes to results
        results['changes'] = changes
        
        # Add current game state to results
        results['game_state'] = {
            'current_turn': game_state.current_turn,
            'game_date': game_state.get_game_date_string(),
            'sect_spirit_stones': player_sect.spirit_stones
        }
        
        # Save the updated data
        data_manager.save_data(sects, members, "example_data.json")
        
        # Return the results
        return jsonify({
            'new_turn': new_turn,
            'game_date': game_state.get_game_date_string(),
            'results': results
        })
        
    except Exception as e:
        # Log the error
        print(f"Error in end_turn: {str(e)}")
        import traceback
        traceback.print_exc()
        
        # Return error response
        return jsonify({
            'error': 'An error occurred while processing the turn end',
            'details': str(e)
        }), 500

@app.route('/api/events', methods=['GET'])
def get_events():
    """Get current events for the player's sect"""
    try:
        # Get the player sect
        player_sect = sects[game_state.sect_id]
        
        # In a real implementation, events would be stored in the game state or a dedicated events system
        # For now, we'll generate some placeholder events based on the current game state
        
        active_events = []
        upcoming_events = []
        history_events = []
        
        # Generate active events based on sect state
        
        # 1. Resource-related events
        if player_sect.spirit_stones < 500:
            active_events.append({
                'id': 1,
                'title': 'Spirit Stone Shortage',
                'type': 'Challenge',
                'description': 'Your sect is running low on spirit stones, which may affect cultivation efficiency.',
                'timeRemaining': '3 days',
                'location': 'Sect Treasury',
                'urgency': 'Medium',
                'requiresDecision': False,
                'canAssignDisciples': True
            })
        
        # 2. Disciple-related events
        for i, member in enumerate(members):
            if member.sect and member.sect.name == player_sect.name:
                # Check for disciples close to breakthrough
                if member.qi >= member.max_qi * 0.9 and member.breakthrough_chance >= 70:
                    active_events.append({
                        'id': 100 + i,
                        'title': f'{member.name} Approaching Breakthrough',
                        'type': 'Opportunity',
                        'description': f'{member.name} is close to breaking through to the next stage. Consider providing resources to assist.',
                        'timeRemaining': '5 days',
                        'location': 'Cultivation Chamber',
                        'urgency': 'Medium',
                        'requiresDecision': False,
                        'canAssignDisciples': False
                    })
                
                # Check for disciples with bottlenecks
                if hasattr(member, 'bottleneck') and member.bottleneck != 'none':
                    active_events.append({
                        'id': 200 + i,
                        'title': f'{member.name} Cultivation Bottleneck',
                        'type': 'Challenge',
                        'description': f'{member.name} has encountered a {member.bottleneck} bottleneck in their cultivation.',
                        'timeRemaining': '7 days',
                        'location': 'Meditation Chamber',
                        'urgency': 'High',
                        'requiresDecision': True,
                        'canAssignDisciples': False
                    })
        
        # 3. Sect development opportunities
        if not hasattr(player_sect, 'cultivation_chambers') or player_sect.cultivation_chambers < 3:
            upcoming_events.append({
                'id': 300,
                'title': 'Cultivation Chamber Construction',
                'type': 'Opportunity',
                'description': 'An opportunity to construct or upgrade cultivation chambers to improve disciples\'  cultivation efficiency.',
                'startsIn': '10 days',
                'duration': '30 days',
                'location': 'Sect Grounds'
            })
        
        # 4. External events (tournaments, etc.)
        upcoming_events.append({
            'id': 400,
            'title': 'Immortal Ascension Conference',
            'type': 'Tournament',
            'description': 'A grand gathering of sects where disciples can compete and exchange cultivation experiences.',
            'startsIn': '15 days',
            'duration': '7 days',
            'location': 'Central Plains'
        })
        
        # 5. Generate some history events based on the current turn
        if game_state.current_turn > 1:
            history_events.append({
                'id': 500,
                'title': 'Sect Founding',
                'type': 'Sect',
                'description': 'The establishment of your sect, marking the beginning of your journey.',
                'completedDate': 'Year 1, Month 1',
                'location': 'Azure Peak',
                'outcome': 'Success',
                'results': [
                    {'icon': 'fa-mountain', 'description': 'Established sect territory'},
                    {'icon': 'fa-user-plus', 'description': 'Recruited initial disciples'}
                ]
            })
            
            # Add more history events based on game progression
            if game_state.current_turn > 3:
                history_events.append({
                    'id': 501,
                    'title': 'Spirit Vein Discovery',
                    'type': 'Opportunity',
                    'description': 'Discovery of a spirit stone vein in your territory.',
                    'completedDate': 'Year 1, Month 2',
                    'location': 'Eastern Territory',
                    'outcome': 'Success',
                    'results': [
                        {'icon': 'fa-gem', 'description': '+100 Spirit Stones per month'},
                        {'icon': 'fa-chart-line', 'description': 'Increased sect resources'}
                    ]
                })
        
        return jsonify({
            'active_events': active_events,
            'upcoming_events': upcoming_events,
            'history_events': history_events
        })
        
    except Exception as e:
        # Log the error
        print(f"Error in get_events: {str(e)}")
        import traceback
        traceback.print_exc()
        
        # Return error response
        return jsonify({
            'error': 'An error occurred while fetching events',
            'details': str(e)
        }), 500

@app.route('/api/logs', methods=['GET'])
def get_logs():
    """Get logs for the player's sect"""
    try:
        # In a real implementation, logs would be stored in the game state or a dedicated logging system
        # For now, we'll generate some placeholder logs based on the current game state
        
        # Parse the current game date
        import re
        game_date = game_state.get_game_date_string()
        year_match = re.search(r'Year (\d+), Month (\d+)', game_date)
        current_year = int(year_match.group(1)) if year_match else 1
        current_month = int(year_match.group(2)) if year_match else 1
        
        logs = []
        notable_events = []
        
        # Generate logs for year 1
        year1 = {
            'year': 1,
            'summary': 'Founding of the sect and initial development',
            'months': []
        }
        
        # Month 1: Sect founding
        month1 = {
            'month': 1,
            'summary': 'Establishment of the sect and recruitment of first disciples',
            'entries': [
                {
                    'day': 1,
                    'title': 'Sect Founding',
                    'category': 'Sect',
                    'description': 'Your sect was officially established.',
                    'details': [
                        {'icon': 'fa-mountain', 'text': 'Sect territory claimed'},
                        {'icon': 'fa-user-plus', 'text': 'Initial disciples joined'}
                    ]
                }
            ]
        }
        year1['months'].append(month1)
        
        # Add more months if we're past month 1
        if current_year >= 1 and current_month >= 2:
            month2 = {
                'month': 2,
                'summary': 'Resource development and cultivation progress',
                'entries': [
                    {
                        'day': 5,
                        'title': 'Spirit Vein Discovery',
                        'category': 'Sect',
                        'description': 'A spirit vein was discovered in your territory.',
                        'details': [
                            {'icon': 'fa-gem', 'text': '+100 Spirit Stones per month'},
                            {'icon': 'fa-chart-line', 'text': 'Increased sect resources'}
                        ]
                    }
                ]
            }
            year1['months'].append(month2)
        
        logs.append(year1)
        
        # Add more years if we're past year 1
        if current_year >= 2:
            year2 = {
                'year': 2,
                'summary': 'Expansion and growth of the sect',
                'months': []
            }
            logs.append(year2)
        
        # Add notable events
        notable_events.append({
            'year': 1,
            'month': 1,
            'title': 'Sect Founding',
            'description': 'The establishment of your sect, marking the beginning of your journey.'
        })
        
        if current_year >= 1 and current_month >= 2:
            notable_events.append({
                'year': 1,
                'month': 2,
                'title': 'Spirit Vein Discovery',
                'description': 'Discovery of a spirit stone vein, significantly boosting the sect\'s resources.'
            })
        
        return jsonify({
            'logs': logs,
            'notable_events': notable_events,
            'total_entries': sum(len(month['entries']) for year in logs for month in year['months']),
            'current_year': current_year,
            'sect_age': current_year
        })
        
    except Exception as e:
        # Log the error
        print(f"Error in get_logs: {str(e)}")
        import traceback
        traceback.print_exc()
        
        # Return error response
        return jsonify({
            'error': 'An error occurred while fetching logs',
            'details': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
