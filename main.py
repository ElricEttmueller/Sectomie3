#!/usr/bin/env python3
"""
Sectomie - A Chinese Cultivation Sect Management System
"""

from member import Member
from sect import Sect
from data_manager import DataManager

def main():
    """Main entry point for the Sectomie cultivation system"""
    data_manager = DataManager()
    
    # Example usage
    print("=== SECTOMIE CULTIVATION SECT MANAGEMENT SYSTEM ===")
    print("\n1. Create a new cultivation sect")
    print("2. Create a new disciple")
    print("3. Add disciple to sect")
    print("4. View sect details")
    print("5. View disciple details")
    print("6. Cultivate")
    print("7. Attempt breakthrough")
    print("8. Manage sect resources")
    print("9. Save data")
    print("10. Load data")
    print("11. Exit")
    
    # In a real application, we would implement a proper menu system
    # and user interaction here
    
    # Example of creating sects and disciples
    azure_peak = Sect("Azure Peak Sect", "Sword Dao", 3, "A prestigious sword cultivation sect located on Azure Peak Mountain")
    mystic_cloud = Sect("Mystic Cloud Sect", "Alchemy Dao", 5, "Ancient sect renowned for its alchemy and medicine cultivation")
    
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
    
    print("\nExample Sects:")
    print(azure_peak)
    print(mystic_cloud)
    
    print("\nExample Disciples:")
    print(li_mei)
    print(zhang_wei)
    
    # Example of cultivation and breakthrough
    print("\nCultivation Example:")
    print(f"{li_mei.name} begins cultivation...")
    qi_gained = li_mei.cultivate(24)  # Cultivate for 24 hours
    print(f"Gained {int(qi_gained)} qi points from cultivation")
    print(f"Current qi: {int(li_mei.qi)}/{li_mei.max_qi}")
    
    print("\nBreakthrough Attempt:")
    # Fill qi to maximum for demonstration
    li_mei.qi = li_mei.max_qi
    success, new_realm, new_stage = li_mei.attempt_breakthrough()
    if success:
        print(f"{li_mei.name} successfully advanced to {li_mei.get_stage_name()} stage of {li_mei.get_realm_name()}!")
    else:
        print(f"{li_mei.name} failed to breakthrough. Current realm: {li_mei.get_stage_name()} {li_mei.get_realm_name()}")  
    
    # Example of sect resource management
    print("\nSect Resource Management:")
    initial_stones = azure_peak.spirit_stones
    monthly_income = sum(vein["output"] for vein in azure_peak.spirit_veins)
    azure_peak.spirit_stones += monthly_income
    print(f"{azure_peak.name} collected {monthly_income} spirit stones from spirit veins")
    print(f"Spirit stones: {initial_stones} → {azure_peak.spirit_stones}")
    
    # Save example data
    data_manager.save_data([azure_peak, mystic_cloud], [li_mei, zhang_wei], "example_data.json")
    print("\nData saved to example_data.json")

if __name__ == "__main__":
    main()
