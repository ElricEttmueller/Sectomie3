#!/usr/bin/env python3
"""
Cultivator class for the Sectomie cultivation system
"""

import random

class Member:
    """
    Represents a cultivator in the sect with cultivation attributes
    """
    
    def __init__(self, name, age, path, physical, spiritual, comprehension):
        """
        Initialize a new Cultivator
        
        Args:
            name (str): Name of the cultivator
            age (int): Age of the cultivator
            path (str): Cultivation path (e.g., "Sword", "Alchemy", "Formation")
            physical (int): Physical foundation attribute (0-100)
            spiritual (int): Spiritual sensitivity attribute (0-100)
            comprehension (int): Dao comprehension attribute (0-100)
        """
        self.name = name
        self.age = age
        self.path = path
        self.physical = self._validate_stat(physical)
        self.spiritual = self._validate_stat(spiritual)
        self.comprehension = self._validate_stat(comprehension)
        self.sect = None  # The sect this cultivator belongs to
        
        # Cultivation attributes
        self.realm = 0     # Cultivation realm (0: Mortal, 1: Qi Condensation, 2: Foundation Establishment, etc.)
        self.realm_stage = 1  # Stage within current realm (Early, Middle, Late, Peak)
        self.qi = 100     # Current qi level
        self.max_qi = 100  # Maximum qi capacity
        self.techniques = []  # Known cultivation techniques
        self.spirit_stones = 0  # Currency/resources
        self.breakthrough_chance = 50  # Base chance for successful breakthrough
        self.elixirs_refined = 0  # For alchemists
        self.formations_mastered = 0  # For formation masters
        self.weapons_forged = 0  # For weapon refiners
        
    def _validate_stat(self, value):
        """Ensure stats are within the valid range (0-100)"""
        return max(0, min(100, value))
        
    def cultivate(self, hours):
        """
        Legacy method for hour-based cultivation
        
        Args:
            hours (int): Hours spent cultivating
        """
        # Base qi gain depends on spiritual attribute and current realm
        qi_gain = hours * (self.spiritual / 10) * (1 + self.realm * 0.5)
        self.qi = min(self.qi + qi_gain, self.max_qi)
        
        # Improve breakthrough chance slightly
        self.breakthrough_chance = min(self.breakthrough_chance + (hours * 0.1), 99)
        
        # Return qi gained
        return qi_gain
        
    def cultivate_with_method(self, method, sect=None):
        """
        Cultivate using a specific method
        
        Args:
            method (str): Cultivation method to use
            sect (Sect, optional): The sect object for resource verification
            
        Returns:
            dict: Results of the cultivation session
        """
        results = {
            "qi_gained": 0,
            "breakthrough_increase": 0,
            "attribute_increase": None,
            "attribute_value": 0,
            "cultivation_deviation": False,
            "success": True,
            "message": ""
        }
        
        # Define base effects for different methods
        method_effects = {
            "qi_circulation": {
                "qi_multiplier": 1.0,
                "breakthrough_increase": 1.0,
                "attribute_chance": 0,
                "deviation_chance": 0
            },
            "essence_refinement": {
                "qi_multiplier": 2.0,
                "breakthrough_increase": 2.0,
                "attribute_chance": 0,
                "deviation_chance": 0
            },
            "dao_heart_tempering": {
                "qi_multiplier": 3.0,
                "breakthrough_increase": 4.0,
                "attribute_chance": 0.15,  # 15% chance to improve comprehension
                "attribute": "comprehension",
                "attribute_increase": 1,
                "deviation_chance": 0.02  # 2% chance of deviation
            },
            "heavenly_tribulation": {
                "qi_multiplier": 1.5,
                "breakthrough_increase": 10.0,
                "attribute_chance": 0,
                "deviation_chance": 0.1  # 10% chance of deviation
            }
        }
        
        # Check if method exists
        if method not in method_effects:
            results["success"] = False
            results["message"] = "Unknown cultivation method"
            return results
            
        effects = method_effects[method]
        
        # Calculate qi gain based on method
        base_qi_gain = (self.spiritual / 10) * (1 + self.realm * 0.5) * 24  # Base is 24 hours
        qi_gain = base_qi_gain * effects["qi_multiplier"]
        self.qi = min(self.qi + qi_gain, self.max_qi)
        results["qi_gained"] = qi_gain
        
        # Calculate breakthrough chance increase
        breakthrough_increase = effects["breakthrough_increase"]
        self.breakthrough_chance = min(self.breakthrough_chance + breakthrough_increase, 99)
        results["breakthrough_increase"] = breakthrough_increase
        
        # Check for attribute increase
        if "attribute" in effects and random.random() < effects["attribute_chance"]:
            attribute = effects["attribute"]
            increase = effects["attribute_increase"]
            
            if attribute == "physical":
                self.physical = min(self.physical + increase, 100)
                results["attribute_increase"] = "physical"
                results["attribute_value"] = self.physical
            elif attribute == "spiritual":
                self.spiritual = min(self.spiritual + increase, 100)
                results["attribute_increase"] = "spiritual"
                results["attribute_value"] = self.spiritual
            elif attribute == "comprehension":
                self.comprehension = min(self.comprehension + increase, 100)
                results["attribute_increase"] = "comprehension"
                results["attribute_value"] = self.comprehension
                
        # Check for cultivation deviation
        if random.random() < effects["deviation_chance"]:
            # Higher comprehension reduces deviation chance
            if random.random() * 100 > self.comprehension:
                results["cultivation_deviation"] = True
                # Reduce qi by 20%
                qi_loss = self.qi * 0.2
                self.qi -= qi_loss
                results["message"] = "Cultivation deviation occurred! Lost some qi progress."
        
        return results
    
    def attempt_breakthrough(self):
        """
        Attempt to break through to the next cultivation stage or realm
        
        Returns:
            tuple: (success, new_realm, new_stage)
        """
        # Check if qi is at maximum capacity
        if self.qi < self.max_qi * 0.9:
            return False, self.realm, self.realm_stage
        
        # Calculate success chance based on attributes and current qi
        chance = self.breakthrough_chance + (self.comprehension / 5)
        success = (chance > 50)  # Simple check for now
        
        if success:
            # Consume qi for breakthrough
            self.qi = self.max_qi * 0.3
            
            # Advance stage or realm
            if self.realm_stage < 4:  # Early, Middle, Late, Peak
                self.realm_stage += 1
            else:  # Advance to next realm
                self.realm += 1
                self.realm_stage = 1
                self.max_qi *= 2  # Double qi capacity with new realm
            
            # Reset breakthrough chance
            self.breakthrough_chance = 30 + (self.comprehension / 5)
            
        return success, self.realm, self.realm_stage
        
    def complete_mission(self, difficulty=1):
        """
        Complete a sect mission and gain resources
        
        Args:
            difficulty (int): Difficulty level of the mission (1-5)
        """
        # Gain spirit stones and potential technique insights
        stones_gained = difficulty * 50 * (1 + self.realm * 0.5)
        self.spirit_stones += stones_gained
        
        # Chance to learn new technique
        technique_chance = difficulty * 5 * (self.comprehension / 100)
        learned_technique = (technique_chance > 30)  # Simple check
        
        # Track mission completion
        if hasattr(self, 'missions_completed'):
            self.missions_completed += 1
        else:
            self.missions_completed = 1
            
        return stones_gained, learned_technique
    
    def get_combat_power(self):
        """Calculate the overall combat power of the cultivator"""
        # Base power from attributes
        attr_power = (self.physical + self.spiritual + self.comprehension) / 3
        
        # Realm and stage multipliers
        realm_multiplier = 10 ** self.realm  # Exponential growth between realms
        stage_multiplier = self.realm_stage
        
        # Techniques contribute to power
        technique_bonus = len(self.techniques) * 50
        
        # Current qi level affects combat power
        qi_factor = self.qi / self.max_qi
        
        return int((attr_power * realm_multiplier * stage_multiplier + technique_bonus) * qi_factor)
    
    def to_dict(self):
        """Convert cultivator data to dictionary for serialization"""
        return {
            "name": self.name,
            "age": self.age,
            "path": self.path,
            "physical": self.physical,
            "spiritual": self.spiritual,
            "comprehension": self.comprehension,
            "realm": self.realm,
            "realm_stage": self.realm_stage,
            "qi": self.qi,
            "max_qi": self.max_qi,
            "techniques": self.techniques,
            "spirit_stones": self.spirit_stones,
            "breakthrough_chance": self.breakthrough_chance,
            "elixirs_refined": self.elixirs_refined,
            "formations_mastered": self.formations_mastered,
            "weapons_forged": self.weapons_forged,
            "missions_completed": getattr(self, 'missions_completed', 0),
            "sect": self.sect.name if self.sect else None
        }
    
    @classmethod
    def from_dict(cls, data, sects=None):
        """Create a Member instance from dictionary data"""
        member = cls(
            data["name"],
            data["age"],
            data["path"],
            data["physical"],
            data["spiritual"],
            data["comprehension"]
        )
        member.realm = data["realm"]
        member.realm_stage = data["realm_stage"]
        member.qi = data["qi"]
        member.max_qi = data["max_qi"]
        member.techniques = data["techniques"]
        member.spirit_stones = data["spirit_stones"]
        member.breakthrough_chance = data["breakthrough_chance"]
        member.elixirs_refined = data["elixirs_refined"]
        member.formations_mastered = data["formations_mastered"]
        member.weapons_forged = data["weapons_forged"]
        member.missions_completed = data["missions_completed"]
        
        # Handle sect reference if sects are provided
        if sects and data["sect"]:
            for sect in sects:
                if sect.name == data["sect"]:
                    member.sect = sect
                    break
        
        return member
    
    def get_realm_name(self):
        """Get the name of the current cultivation realm"""
        realms = [
            "Mortal",
            "Qi Condensation",
            "Foundation Establishment",
            "Core Formation",
            "Nascent Soul",
            "Spirit Severing",
            "Dao Seeking",
            "Immortal Ascension"
        ]
        if self.realm < len(realms):
            return realms[self.realm]
        return "Transcendent"
    
    def get_stage_name(self):
        """Get the name of the current cultivation stage"""
        stages = ["Early", "Middle", "Late", "Peak"]
        if 1 <= self.realm_stage <= 4:
            return stages[self.realm_stage - 1]
        return "Unknown"
    
    def __str__(self):
        """String representation of the cultivator"""
        sect_info = f"Disciple of {self.sect.name}" if self.sect else "Rogue Cultivator"
        realm_info = f"{self.get_stage_name()} {self.get_realm_name()}"
        
        return (f"{self.name} ({realm_info} - {self.path} Path)\n"
                f"  Physical: {self.physical} | Spiritual: {self.spiritual} | "
                f"Comprehension: {self.comprehension}\n"
                f"  Qi: {int(self.qi)}/{self.max_qi} | Combat Power: {self.get_combat_power()}\n"
                f"  {sect_info} | Techniques: {len(self.techniques)} | Spirit Stones: {self.spirit_stones}")
