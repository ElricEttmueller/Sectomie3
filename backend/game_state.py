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
            "new_missions": []
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
            # Basic passive cultivation (20% of normal cultivation)
            # We'll use the cultivate method but only apply 20% of the effect
            original_qi = member.qi
            original_breakthrough = member.breakthrough_chance
            
            # Temporarily store values
            member.cultivate(hours=24 * 0.2 * self.turn_length)
            
            # Calculate how much was gained
            qi_gained = member.qi - original_qi
            
            # Reset breakthrough chance to avoid double-counting
            member.breakthrough_chance = original_breakthrough + ((member.breakthrough_chance - original_breakthrough) * 0.2)
                
            # Update breakthrough chance
            if member.qi >= member.max_qi:
                member.breakthrough_chance += 5  # Small passive increase in breakthrough chance
                
            results["cultivation_progress"][members.index(member)] = {
                "name": member.name,
                "qi_gained": qi_gained,
                "current_qi": member.qi,
                "max_qi": member.max_qi,
                "breakthrough_chance": member.breakthrough_chance
            }
        
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
