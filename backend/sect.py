#!/usr/bin/env python3
"""
Sect class for the Sectomie cultivation system
"""

class Sect:
    """
    Represents a cultivation sect with appropriate attributes
    """
    
    def __init__(self, name, dao_heritage, tier=1, description=""):
        """
        Initialize a new Cultivation Sect
        
        Args:
            name (str): Name of the sect
            dao_heritage (str): Main cultivation heritage/focus of the sect
            tier (int): Sect tier/rank in the cultivation world (1-9)
            description (str): Brief description of the sect
        """
        self.name = name
        self.dao_heritage = dao_heritage
        self.tier = self._validate_tier(tier)
        self.description = description
        self.members = []
        
        # Sect resources
        self.spirit_stones = 10000 * tier  # Basic currency
        self.spirit_veins = []  # Spirit veins/mines owned by the sect
        self.spirit_vein_quality = tier  # Quality of the sect's main spirit vein
        self.elixir_fields = tier  # Number of herb/elixir fields
        self.spirit_herbs = 2 * tier  # Basic cultivation herbs
        self.dao_crystals = 0  # Rare dao energy crystals
        
        # Sect properties
        self.sect_influence = 10 * tier   # Influence in the cultivation world
        self.reputation = 50          # Neutral starting reputation (0-100)
        self.territories = []         # List of controlled territories
        self.formation_strength = tier * 10  # Protective formation strength
        
        # Sect relationships
        self.alliances = []           # List of allied sects
        self.rivals = []              # List of rival sects
        
        # Sect knowledge
        self.techniques = []          # Cultivation techniques owned by sect
        self.secret_manuals = []      # Secret cultivation manuals
        self.alchemy_recipes = []     # Elixir recipes
        self.formation_diagrams = []  # Formation diagrams
        self.artifact_blueprints = [] # Artifact crafting blueprints
        
    def _validate_tier(self, tier):
        """Ensure tier is within valid range (1-9)"""
        return max(1, min(9, tier))
    
    def add_member(self, member):
        """
        Add a cultivator to the sect
        
        Args:
            member: Member object to add
        """
        if member not in self.members:
            self.members.append(member)
            member.sect = self  # Update the cultivator's sect reference
    
    def remove_member(self, member):
        """
        Remove a member from the sect
        
        Args:
            member: Member object to remove
        """
        if member in self.members:
            self.members.remove(member)
            member.sect = None  # Clear the member's sect reference
    
    def get_total_power(self):
        """Calculate the total combat power of all members"""
        if not self.members:
            return 0
        return sum(member.get_combat_power() for member in self.members)
    
    def get_average_power(self):
        """Calculate the average combat power of members"""
        if not self.members:
            return 0
        return self.get_total_power() / len(self.members)
    
    def add_territory(self, territory_name, spirit_vein_quality=0):
        """Add a territory to the sect's control"""
        if territory_name not in self.territories:
            self.territories.append(territory_name)
            self.sect_influence += 5  # Gaining territory increases influence
            
            # If territory has spirit veins
            if spirit_vein_quality > 0:
                self.spirit_veins.append({
                    "location": territory_name,
                    "quality": spirit_vein_quality,
                    "output": spirit_vein_quality * 100  # Spirit stones per month
                })
    
    def form_alliance(self, other_sect):
        """Form an alliance with another sect"""
        if other_sect not in self.alliances and other_sect != self:
            self.alliances.append(other_sect)
            other_sect.alliances.append(self)
            
            # Exchange a random technique as a sign of goodwill
            if self.techniques and other_sect.techniques:
                if len(self.techniques) > 0 and len(other_sect.techniques) > 0:
                    # In a full implementation, we would exchange actual techniques
                    self.sect_influence += 2
                    other_sect.sect_influence += 2
    
    def declare_rivalry(self, other_sect):
        """Declare a rivalry with another sect"""
        if other_sect not in self.rivals and other_sect != self:
            self.rivals.append(other_sect)
            other_sect.rivals.append(self)
    
    def to_dict(self):
        """Convert sect data to dictionary for serialization"""
        return {
            "name": self.name,
            "dao_heritage": self.dao_heritage,
            "tier": self.tier,
            "description": self.description,
            "spirit_stones": self.spirit_stones,
            "spirit_veins": self.spirit_veins,
            "spirit_vein_quality": self.spirit_vein_quality,
            "elixir_fields": self.elixir_fields,
            "spirit_herbs": getattr(self, 'spirit_herbs', 0),
            "dao_crystals": getattr(self, 'dao_crystals', 0),
            "sect_influence": self.sect_influence,
            "reputation": self.reputation,
            "territories": self.territories,
            "formation_strength": self.formation_strength,
            "members": [member.name for member in self.members],
            "alliances": [sect.name for sect in self.alliances],
            "rivals": [sect.name for sect in self.rivals],
            "techniques": self.techniques,
            "secret_manuals": self.secret_manuals,
            "alchemy_recipes": self.alchemy_recipes,
            "formation_diagrams": self.formation_diagrams,
            "artifact_blueprints": self.artifact_blueprints
        }
    
    @classmethod
    def from_dict(cls, data, members=None, sects=None):
        """Create a Sect instance from dictionary data"""
        sect = cls(
            data["name"],
            data["dao_heritage"],
            data["tier"],
            data["description"]
        )
        sect.spirit_stones = data["spirit_stones"]
        sect.spirit_veins = data["spirit_veins"]
        sect.spirit_vein_quality = data["spirit_vein_quality"]
        sect.elixir_fields = data["elixir_fields"]
        sect.spirit_herbs = data.get("spirit_herbs", 2 * data["tier"])
        sect.dao_crystals = data.get("dao_crystals", 0)
        sect.sect_influence = data["sect_influence"]
        sect.reputation = data["reputation"]
        sect.territories = data["territories"]
        sect.formation_strength = data["formation_strength"]
        sect.techniques = data["techniques"]
        sect.secret_manuals = data["secret_manuals"]
        sect.alchemy_recipes = data["alchemy_recipes"]
        sect.formation_diagrams = data["formation_diagrams"]
        sect.artifact_blueprints = data["artifact_blueprints"]
        
        # Handle member references if members are provided
        if members:
            for member_name in data["members"]:
                for member in members:
                    if member.name == member_name:
                        sect.add_member(member)
                        break
        
        # Alliance and rival references need to be handled after all sects are created
        # This would typically be done in a second pass by the data manager
        
        return sect
    
    def get_tier_name(self):
        """Get the name of the sect tier"""
        tiers = [
            "Mortal",
            "Spirit Gathering",
            "Foundation",
            "Core",
            "Nascent",
            "Spirit",
            "Dao",
            "Immortal",
            "Celestial"
        ]
        if 1 <= self.tier <= len(tiers):
            return tiers[self.tier - 1]
        return "Transcendent"
    
    def __str__(self):
        """String representation of the sect"""
        return (f"{self.name} ({self.get_tier_name()} Tier {self.dao_heritage} Sect)\n"
                f"  Disciples: {len(self.members)} | Influence: {self.sect_influence} | "
                f"Spirit Stones: {self.spirit_stones}\n"
                f"  Territories: {len(self.territories)} | "
                f"Spirit Veins: {len(self.spirit_veins)} | "
                f"Formation Strength: {self.formation_strength}\n"
                f"  Techniques: {len(self.techniques)} | "
                f"Secret Manuals: {len(self.secret_manuals)} | "
                f"Elixir Fields: {self.elixir_fields}\n"
                f"  {self.description}")
