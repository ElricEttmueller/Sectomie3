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
        
        # Bottleneck system
        self.bottleneck = "none"  # Can be "none", "minor", or "major"
        self.bottleneck_insights = 0  # Accumulated insights for overcoming minor bottlenecks
        self.insights_required = 0  # Insights needed to overcome current bottleneck
        self.bottleneck_treasures = []  # Special items for overcoming major bottlenecks
        
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
    
    def calculate_monthly_cultivation(self, assigned_method=None, facility_bonus=1.0, manual_bonus=1.0, resource_bonus=1.0):
        """
        Calculate monthly automatic cultivation progress based on the assigned method and bonuses
        
        Args:
            assigned_method (str, optional): The cultivation method assigned to this disciple
            facility_bonus (float, optional): Bonus from sect facilities (1.0 = no bonus)
            manual_bonus (float, optional): Bonus from technique manuals (1.0 = no bonus)
            resource_bonus (float, optional): Bonus from allocated resources (1.0 = no bonus)
            
        Returns:
            dict: Results of the monthly cultivation progress
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
        
        # Default method if none assigned
        if not assigned_method:
            assigned_method = "qi_circulation"
        
        # Define base effects for different methods
        method_effects = {
            "qi_circulation": {
                "qi_multiplier": 1.0,
                "breakthrough_increase": 1.0,
                "attribute_chance": 0.05,  # 5% chance to improve physical
                "attribute": "physical",
                "attribute_increase": 1,
                "deviation_chance": 0.01,  # 1% chance of deviation
                "description": "A balanced method focusing on steady qi accumulation"
            },
            "essence_refinement": {
                "qi_multiplier": 1.5,
                "breakthrough_increase": 1.2,
                "attribute_chance": 0.08,  # 8% chance to improve spiritual
                "attribute": "spiritual",
                "attribute_increase": 1,
                "deviation_chance": 0.03,  # 3% chance of deviation
                "description": "Focuses on refining spiritual essence, increasing qi gain but with higher deviation risk"
            },
            "dao_heart_tempering": {
                "qi_multiplier": 0.8,
                "breakthrough_increase": 2.0,
                "attribute_chance": 0.15,  # 15% chance to improve comprehension
                "attribute": "comprehension",
                "attribute_increase": 1,
                "deviation_chance": 0.02,  # 2% chance of deviation
                "description": "Focuses on understanding the Dao, improving breakthrough chance and comprehension at the cost of slower qi accumulation"
            },
            "foundation_building": {
                "qi_multiplier": 0.7,
                "breakthrough_increase": 1.5,
                "attribute_chance": 0.1,  # 10% chance to improve all attributes slightly
                "attribute": "all",
                "attribute_increase": 0.5,
                "deviation_chance": 0.005,  # 0.5% chance of deviation
                "description": "A slow but safe method that builds a solid foundation and reduces deviation chance"
            },
            "heavenly_tribulation": {
                "qi_multiplier": 2.0,
                "breakthrough_increase": 3.0,
                "attribute_chance": 0.2,  # 20% chance to improve random attribute
                "attribute": "random",
                "attribute_increase": 2,
                "deviation_chance": 0.15,  # 15% chance of deviation
                "description": "A dangerous but powerful method that greatly accelerates cultivation at the risk of severe deviation"
            }
        }
        
        # Check if method exists
        if assigned_method not in method_effects:
            results["success"] = False
            results["message"] = "Unknown cultivation method"
            return results
            
        effects = method_effects[assigned_method]
        
        # Calculate monthly qi gain based on method and bonuses
        base_qi_gain = (self.spiritual / 10) * (1 + self.realm * 0.5) * 30  # Base for 30 days
        qi_gain = base_qi_gain * effects["qi_multiplier"] * facility_bonus * manual_bonus * resource_bonus
        
        # Apply the qi gain
        self.qi = min(self.qi + qi_gain, self.max_qi)
        results["qi_gained"] = qi_gain
        
        # Calculate breakthrough chance increase with bonuses
        breakthrough_increase = effects["breakthrough_increase"] * facility_bonus * manual_bonus
        self.breakthrough_chance = min(self.breakthrough_chance + breakthrough_increase, 99)
        results["breakthrough_increase"] = breakthrough_increase
        
        # Check for attribute increase
        if random.random() < effects["attribute_chance"]:
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
            elif attribute == "all":
                self.physical = min(self.physical + increase, 100)
                self.spiritual = min(self.spiritual + increase, 100)
                self.comprehension = min(self.comprehension + increase, 100)
                results["attribute_increase"] = "all"
            elif attribute == "random":
                # Choose a random attribute to increase
                random_attr = random.choice(["physical", "spiritual", "comprehension"])
                if random_attr == "physical":
                    self.physical = min(self.physical + increase, 100)
                    results["attribute_increase"] = "physical"
                    results["attribute_value"] = self.physical
                elif random_attr == "spiritual":
                    self.spiritual = min(self.spiritual + increase, 100)
                    results["attribute_increase"] = "spiritual"
                    results["attribute_value"] = self.spiritual
                elif random_attr == "comprehension":
                    self.comprehension = min(self.comprehension + increase, 100)
                    results["attribute_increase"] = "comprehension"
                    results["attribute_value"] = self.comprehension
                
        # Check for cultivation deviation (reduced by comprehension and manual_bonus)
        deviation_chance = effects["deviation_chance"] / manual_bonus  # Better manuals reduce deviation
        if random.random() < deviation_chance:
            # Higher comprehension reduces deviation chance
            if random.random() * 100 > self.comprehension:
                results["cultivation_deviation"] = True
                # Reduce qi by 10-30% based on severity
                severity = random.uniform(0.1, 0.3)
                qi_loss = self.qi * severity
                self.qi -= qi_loss
                results["message"] = f"Cultivation deviation occurred! Lost {int(severity * 100)}% of accumulated qi."
        
        # Add method description to results
        results["method_description"] = effects["description"]
        
        return results

    def get_cultivation_methods(self):
        """
        Get available cultivation methods for this disciple with effectiveness ratings
        
        Returns:
            dict: Dictionary of available methods with their effectiveness ratings
        """
        # Ensure attributes are initialized
        if not hasattr(self, 'physical') or not hasattr(self, 'spiritual') or not hasattr(self, 'comprehension'):
            # Set default values if attributes are missing
            if not hasattr(self, 'physical'):
                self.physical = 50
            if not hasattr(self, 'spiritual'):
                self.spiritual = 50
            if not hasattr(self, 'comprehension'):
                self.comprehension = 50
        
        # Ensure realm is initialized
        if not hasattr(self, 'realm'):
            self.realm = 0
        
        methods = {
            "qi_circulation": {
                "name": "Qi Circulation",
                "description": "A balanced method focusing on steady qi accumulation",
                "effectiveness": 3,  # 1-5 scale
                "recommended_for": "beginners"
            },
            "essence_refinement": {
                "name": "Essence Refinement",
                "description": "Focuses on refining spiritual essence, increasing qi gain but with higher deviation risk",
                "effectiveness": 3,  # Base effectiveness
                "recommended_for": "disciples with high spiritual attribute"
            },
            "dao_heart_tempering": {
                "name": "Dao Heart Tempering",
                "description": "Focuses on understanding the Dao, improving breakthrough chance and comprehension",
                "effectiveness": 3,  # Base effectiveness
                "recommended_for": "disciples approaching breakthrough"
            },
            "foundation_building": {
                "name": "Foundation Building",
                "description": "A slow but safe method that builds a solid foundation and reduces deviation chance",
                "effectiveness": 3,  # Base effectiveness
                "recommended_for": "disciples with balanced attributes"
            }
        }
        
        # Add heavenly tribulation method only for higher realms
        if self.realm >= 3:  # Core Formation or higher
            methods["heavenly_tribulation"] = {
                "name": "Heavenly Tribulation",
                "description": "A dangerous but powerful method that greatly accelerates cultivation at the risk of severe deviation",
                "effectiveness": 3,  # Base effectiveness
                "recommended_for": "advanced disciples with high comprehension"
            }
        
        # Adjust effectiveness based on disciple attributes
        for method_key, method_info in methods.items():
            if method_key == "qi_circulation":
                # Balanced method, effectiveness based on overall balance
                balance = 100 - (abs(self.physical - self.spiritual) + abs(self.spiritual - self.comprehension) + abs(self.comprehension - self.physical)) / 3
                methods[method_key]["effectiveness"] = min(5, max(1, int(balance / 20)))
                
            elif method_key == "essence_refinement":
                # Effectiveness based on spiritual attribute
                methods[method_key]["effectiveness"] = min(5, max(1, int(self.spiritual / 20)))
                
            elif method_key == "dao_heart_tempering":
                # Effectiveness based on comprehension attribute
                methods[method_key]["effectiveness"] = min(5, max(1, int(self.comprehension / 20)))
                
            elif method_key == "foundation_building":
                # Effectiveness based on lowest attribute
                lowest_attr = min(self.physical, self.spiritual, self.comprehension)
                methods[method_key]["effectiveness"] = min(5, max(1, int(lowest_attr / 20)))
                
            elif method_key == "heavenly_tribulation":
                # Effectiveness based on comprehension and current realm
                methods[method_key]["effectiveness"] = min(5, max(1, int((self.comprehension + self.realm * 10) / 25)))
        
        return methods
        
    def attempt_breakthrough(self):
        """
        Attempt to break through to the next cultivation stage or realm
        
        Returns:
            dict: Results of the breakthrough attempt including success status and realm information
        """
        results = {
            "success": False,
            "realm": self.realm,
            "stage": self.get_stage_name(),
            "realm_name": self.get_realm_name(),
            "bottleneck": "none",
            "message": "",
            "qi": self.qi,
            "max_qi": self.max_qi
        }
        
        # If already at a bottleneck, can't attempt breakthrough
        if self.bottleneck != "none":
            results["message"] = f"You are currently facing a {self.bottleneck} bottleneck. You must overcome it before advancing."
            return results
        
        # Check if qi is at maximum capacity
        if self.qi < self.max_qi * 0.9:
            results["message"] = "Insufficient qi. Reach at least 90% of maximum qi capacity before attempting breakthrough."
            return results
        
        # Calculate success chance based on attributes and current qi
        chance = self.breakthrough_chance + (self.comprehension / 5)
        
        # Determine if bottleneck will occur
        bottleneck_chance = 0
        
        # Higher chance of bottleneck at higher realms
        if self.realm >= 2:  # Foundation Establishment and above
            bottleneck_chance = 0.3 + (self.realm * 0.1)  # 30% base + 10% per realm
        
        # Higher chance of major bottleneck when advancing to a new realm
        major_bottleneck_chance = 0
        if self.realm_stage == 4:  # At Peak stage, about to advance realm
            # TEMPORARY FIX: Disable bottleneck chance for testing realm advancement
            # major_bottleneck_chance = 0.5 + (self.realm * 0.1)  # 50% base + 10% per realm
            major_bottleneck_chance = 0  # Force to 0 for testing
        
        # Check for bottlenecks first
        if random.random() < major_bottleneck_chance:
            # Encounter major bottleneck
            self.bottleneck = "major"
            self.insights_required = 5 + (self.realm * 2)  # More insights needed at higher realms
            
            # Consume qi partially
            self.qi = self.max_qi * 0.7
            
            # Reset breakthrough chance partially
            self.breakthrough_chance = self.breakthrough_chance * 0.5
            
            results["bottleneck"] = "major"
            results["message"] = f"You've encountered a major bottleneck! Your cultivation has reached a fundamental barrier. You need special treasures to overcome this and advance to the next realm."
            return results
        
        elif random.random() < bottleneck_chance:
            # Encounter minor bottleneck
            self.bottleneck = "minor"
            self.insights_required = 3 + self.realm  # More insights needed at higher realms
            
            # Consume qi partially
            self.qi = self.max_qi * 0.8
            
            # Reset breakthrough chance partially
            self.breakthrough_chance = self.breakthrough_chance * 0.7
            
            results["bottleneck"] = "minor"
            results["message"] = f"You've encountered a minor bottleneck! Your cultivation has stalled. You need to gain insights through meditation or studying techniques."
            return results
        
        success = (chance > 50)
        print(f"DEBUG: Force success = {success}")
        
        if success:
            print("Breakthrough successful!")
            # Consume qi for breakthrough
            self.qi = self.max_qi * 0.3
            
            # Advance stage or realm
            if self.realm_stage < 4:  # Not at Peak stage yet
                self.realm_stage += 1
            else:  # At Peak stage, advance to next realm
                self.realm += 1
                self.realm_stage = 1  # Reset to Early stage of new realm
                self.max_qi *= 2  # Double qi capacity for new realm
            
            # Reset breakthrough chance
            self.breakthrough_chance = 0
            
            results["success"] = True
            results["realm"] = self.realm
            results["stage"] = self.get_stage_name()
            results["realm_name"] = self.get_realm_name()
            results["message"] = f"Breakthrough successful! Advanced to {self.get_stage_name()} {self.get_realm_name()}."
            results["qi"] = self.qi
            results["max_qi"] = self.max_qi
            
            return results
        else:
            # Failed breakthrough attempt
            self.qi = self.max_qi * 0.5  # Lose some qi
            results["message"] = "Breakthrough failed. Your foundation is not solid enough yet."
            return results
    
    def meditate_for_insight(self):
        """
        Meditate to gain insights for overcoming minor bottlenecks
        
        Returns:
            dict: Results of the meditation session
        """
        results = {
            "success": False,
            "insights_gained": 0,
            "bottleneck_overcome": False,
            "message": ""
        }
        
        # Can only meditate if at a minor bottleneck
        if self.bottleneck != "minor":
            if self.bottleneck == "major":
                results["message"] = "You are facing a major bottleneck. Meditation alone cannot overcome it. You need special treasures."
            else:
                results["message"] = "You are not currently facing a bottleneck. Focus on cultivation instead."
            return results
        
        # Base insight chance based on comprehension
        insight_chance = self.comprehension / 100
        
        # Bonus from techniques known
        technique_bonus = min(len(self.techniques) * 0.05, 0.25)  # Up to 25% bonus
        
        # Calculate final chance
        final_chance = insight_chance + technique_bonus
        
        # Determine insights gained
        if random.random() < final_chance:
            insights_gained = 1
            if random.random() < (self.comprehension / 200):  # Chance for extra insight
                insights_gained += 1
                
            self.bottleneck_insights += insights_gained
            results["insights_gained"] = insights_gained
            results["success"] = True
            
            # Check if bottleneck is overcome
            if self.bottleneck_insights >= self.insights_required:
                self.bottleneck = "none"
                self.bottleneck_insights = 0
                self.insights_required = 0
                
                # Increase breakthrough chance as reward
                self.breakthrough_chance += 20
                
                results["bottleneck_overcome"] = True
                results["message"] = f"Enlightenment! You've gained {insights_gained} insight(s) and overcome your bottleneck. Your path to advancement is clear."
            else:
                results["message"] = f"You've gained {insights_gained} insight(s). ({self.bottleneck_insights}/{self.insights_required} required)"
        else:
            results["message"] = "Your meditation yielded no insights this time. Keep trying."
        
        return results
        
    def use_treasure_for_bottleneck(self, treasure_type):
        """
        Use a special treasure to overcome a major bottleneck
        
        Args:
            treasure_type (str): Type of treasure to use
            
        Returns:
            dict: Results of using the treasure
        """
        results = {
            "success": False,
            "bottleneck_overcome": False,
            "message": ""
        }
        
        # Can only use treasures if at a major bottleneck
        if self.bottleneck != "major":
            if self.bottleneck == "minor":
                results["message"] = "You are facing a minor bottleneck. Try meditation instead."
            else:
                results["message"] = "You are not currently facing a bottleneck."
            return results
        
        # Define treasure effectiveness for different realms
        treasure_effectiveness = {
            "spirit_pill": [0, 1, 2],  # Effective for realms 0-2 (Mortal to Foundation Establishment)
            "dao_comprehension_stone": [2, 3, 4],  # Effective for realms 2-4
            "heaven_and_earth_spirit_fruit": [3, 4, 5],  # Effective for realms 3-5
            "nine_transformation_pill": [4, 5, 6],  # Effective for realms 4-6
            "immortal_ascension_stone": [6, 7]  # Effective for realms 6-7
        }
        
        # Check if treasure is effective for current realm
        if treasure_type in treasure_effectiveness:
            effective_realms = treasure_effectiveness[treasure_type]
            
            if self.realm in effective_realms:
                # Treasure is effective, overcome bottleneck
                self.bottleneck = "none"
                
                # Increase breakthrough chance significantly
                self.breakthrough_chance += 40
                
                results["success"] = True
                results["bottleneck_overcome"] = True
                results["message"] = f"The {treasure_type.replace('_', ' ')} resonates with your cultivation base! The bottleneck has been overcome."
            else:
                # Treasure is not effective for current realm
                if self.realm < min(effective_realms):
                    results["message"] = f"This {treasure_type.replace('_', ' ')} is too powerful for your current cultivation level. It might harm your foundation."
                else:
                    results["message"] = f"This {treasure_type.replace('_', ' ')} is too weak for your current cultivation level. You need a more potent treasure."
        else:
            results["message"] = "This item cannot help overcome cultivation bottlenecks."
        
        return results
    
    def complete_mission(self, difficulty=1):
        """
        Complete a sect mission and gain resources
        
        Args:
            difficulty (int): Difficulty level of the mission (1-5)
        """
        # Base rewards
        spirit_stones = difficulty * 50 * (1 + self.realm * 0.5)
        
        # Chance for special rewards based on attributes
        special_reward_chance = (self.spiritual + self.comprehension) / 200
        
        # Chance to gain insights from mission (helpful for bottlenecks)
        insight_chance = difficulty * 0.1
        insights_gained = 0
        
        if self.bottleneck == "minor" and random.random() < insight_chance:
            insights_gained = 1
            self.bottleneck_insights += 1
            
            # Check if bottleneck is overcome
            if self.bottleneck_insights >= self.insights_required:
                self.bottleneck = "none"
                self.bottleneck_insights = 0
                self.insights_required = 0
        
        # Chance to find special treasures (helpful for major bottlenecks)
        treasure_chance = difficulty * 0.05
        treasure_found = None
        
        if random.random() < treasure_chance:
            # Determine treasure type based on realm
            if self.realm <= 2:
                treasure_found = "spirit_pill"
            elif self.realm <= 4:
                treasure_found = "dao_comprehension_stone"
            else:
                treasure_found = "heaven_and_earth_spirit_fruit"
        
        # Add mission completion count
        if not hasattr(self, 'missions_completed'):
            self.missions_completed = 0
        self.missions_completed += 1
        
        # Return rewards
        return {
            "spirit_stones": int(spirit_stones),
            "special_reward": random.random() < special_reward_chance,
            "insights_gained": insights_gained,
            "treasure_found": treasure_found
        }
        
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
            "sect": self.sect.name if self.sect else None,
            # Bottleneck system properties
            "bottleneck": self.bottleneck,
            "bottleneck_insights": self.bottleneck_insights,
            "insights_required": self.insights_required,
            "bottleneck_treasures": self.bottleneck_treasures
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
        member.missions_completed = data.get("missions_completed", 0)
        
        # Load bottleneck system properties
        member.bottleneck = data.get("bottleneck", "none")
        member.bottleneck_insights = data.get("bottleneck_insights", 0)
        member.insights_required = data.get("insights_required", 0)
        member.bottleneck_treasures = data.get("bottleneck_treasures", [])
        
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
