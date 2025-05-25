"""
Game State Manager for Sectomie Cultivation System
Handles turn-based mechanics and global game state
"""

import random

class GameState:
    def __init__(self):
        self.current_turn = 1
        self.turn_length = 30  # 30 days per turn
        self.game_date = {
            "year": 1,
            "month": 1,
            "day": 1
        }
        self.events = []
        self.available_missions = []
        self.sect_id = 0  # Player's sect ID
        
    def advance_turn(self):
        """Advance the game by one turn"""
        self.current_turn += 1
        
        # Advance game date
        self.game_date["month"] += 1
        if self.game_date["month"] > 12:
            self.game_date["month"] = 1
            self.game_date["year"] += 1
            
        return self.current_turn
    
    def process_turn_end(self, sects, members):
        """Process all end-of-turn events and calculations"""
        results = {
            "resource_income": {},
            "cultivation_progress": {},
            "events": [],
            "new_missions": [],
            "cultivation_deviations": [],
            "attribute_increases": []
        }
        
        # Get player sect
        if self.sect_id < 0 or self.sect_id >= len(sects):
            return {"error": "Invalid sect ID"}
        
        player_sect = sects[self.sect_id]
        
        # Calculate resource income
        spirit_stone_income = sum(vein["output"] for vein in player_sect.spirit_veins)
        player_sect.spirit_stones += spirit_stone_income
        results["resource_income"]["spirit_stones"] = spirit_stone_income
        
        # Generate spirit herbs from elixir fields
        if player_sect.elixir_fields > 0:
            # Each elixir field has a chance to produce 0-2 spirit herbs
            herb_income = 0
            for _ in range(player_sect.elixir_fields):
                herb_income += random.randint(0, 2)
                
            # Initialize spirit_herbs if it doesn't exist
            if not hasattr(player_sect, 'spirit_herbs'):
                player_sect.spirit_herbs = 0
                
            player_sect.spirit_herbs += herb_income
            results["resource_income"]["spirit_herbs"] = herb_income
        
        # Process automatic cultivation for disciples
        for member in player_sect.members:
            # Skip disciples that are not active or are in seclusion
            if hasattr(member, 'status') and member.status not in ['active', None]:
                continue
                
            # Get assigned cultivation method (default to qi_circulation if none assigned)
            assigned_method = getattr(member, 'assigned_cultivation_method', 'qi_circulation')
            
            # Calculate facility bonus based on sect buildings
            facility_bonus = 1.0
            if hasattr(player_sect, 'cultivation_chambers') and player_sect.cultivation_chambers > 0:
                facility_bonus += player_sect.cultivation_chambers * 0.05  # 5% bonus per chamber
                
            # Calculate manual bonus based on sect technique manuals
            manual_bonus = 1.0
            if hasattr(player_sect, 'technique_manuals') and player_sect.technique_manuals:
                # Check if there's a manual for this specific method
                for manual in player_sect.technique_manuals:
                    if manual.get('method') == assigned_method:
                        manual_bonus += manual.get('bonus', 0.1)  # Default 10% bonus per manual
            
            # Calculate resource bonus based on allocated resources
            resource_bonus = 1.0
            if hasattr(member, 'allocated_resources'):
                resource_bonus += member.allocated_resources * 0.1  # 10% bonus per resource point
            
            # Apply monthly cultivation with all bonuses
            cultivation_result = member.calculate_monthly_cultivation(
                assigned_method=assigned_method,
                facility_bonus=facility_bonus,
                manual_bonus=manual_bonus,
                resource_bonus=resource_bonus
            )
            
            # Record cultivation progress
            results["cultivation_progress"][members.index(member)] = {
                "name": member.name,
                "qi_gained": cultivation_result["qi_gained"],
                "current_qi": member.qi,
                "max_qi": member.max_qi,
                "breakthrough_chance": member.breakthrough_chance,
                "method_used": assigned_method,
                "method_description": cultivation_result.get("method_description", "")
            }
            
            # Record cultivation deviations
            if cultivation_result["cultivation_deviation"]:
                results["cultivation_deviations"].append({
                    "disciple_id": members.index(member),
                    "name": member.name,
                    "message": cultivation_result["message"]
                })
                
            # Record attribute increases
            if cultivation_result["attribute_increase"]:
                results["attribute_increases"].append({
                    "disciple_id": members.index(member),
                    "name": member.name,
                    "attribute": cultivation_result["attribute_increase"],
                    "value": cultivation_result["attribute_value"]
                })
                
            # Check for automatic breakthrough attempts
            if member.qi >= member.max_qi and member.bottleneck == "none":
                # 10% chance to automatically attempt breakthrough when qi is full
                if random.random() < 0.1:
                    breakthrough_result = member.attempt_breakthrough()
                    if breakthrough_result["success"]:
                        results["events"].append({
                            "type": "breakthrough",
                            "disciple_id": members.index(member),
                            "name": member.name,
                            "message": breakthrough_result["message"],
                            "new_realm": member.realm,
                            "new_stage": member.stage
                        })
        
        # Generate new missions/opportunities (placeholder)
        # TODO: Implement mission generation
        
        return results
    
    def get_game_date_string(self):
        """Return formatted game date string"""
        return f"Year {self.game_date['year']}, Month {self.game_date['month']}"
    
    def get_state_summary(self):
        """Return a summary of the current game state"""
        return {
            "current_turn": self.current_turn,
            "game_date": self.get_game_date_string(),
            "events_count": len(self.events),
            "available_missions": len(self.available_missions)
        }
