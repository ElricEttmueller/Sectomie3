#!/usr/bin/env python3
"""
Data Manager for the Sectomie system
"""

import json
import os
from member import Member
from sect import Sect


class DataManager:
    """
    Handles data persistence for the Sectomie system
    """
    
    def save_data(self, sects, members, filename):
        """
        Save sects and members data to a JSON file
        
        Args:
            sects (list): List of Sect objects
            members (list): List of Member objects
            filename (str): Path to save the data
        """
        data = {
            "sects": [sect.to_dict() for sect in sects],
            "members": [member.to_dict() for member in members]
        }
        
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
    
    def load_data(self, filename):
        """
        Load sects and members data from a JSON file
        
        Args:
            filename (str): Path to the data file
            
        Returns:
            tuple: (sects, members) lists of loaded objects
        """
        if not os.path.exists(filename):
            return [], []
        
        with open(filename, 'r') as file:
            data = json.load(file)
        
        # First pass: Create all members and sects without relationships
        members = []
        for member_data in data.get("members", []):
            member = Member.from_dict(member_data)
            members.append(member)
        
        sects = []
        for sect_data in data.get("sects", []):
            sect = Sect.from_dict(sect_data)
            sects.append(sect)
        
        # Second pass: Establish relationships
        for i, member_data in enumerate(data.get("members", [])):
            if member_data.get("sect"):
                for sect in sects:
                    if sect.name == member_data["sect"]:
                        sect.add_member(members[i])
                        break
        
        # Handle sect alliances and rivalries
        for i, sect_data in enumerate(data.get("sects", [])):
            for alliance_name in sect_data.get("alliances", []):
                for other_sect in sects:
                    if other_sect.name == alliance_name and other_sect != sects[i]:
                        if other_sect not in sects[i].alliances:
                            sects[i].alliances.append(other_sect)
            
            for rival_name in sect_data.get("rivals", []):
                for other_sect in sects:
                    if other_sect.name == rival_name and other_sect != sects[i]:
                        if other_sect not in sects[i].rivals:
                            sects[i].rivals.append(other_sect)
        
        return sects, members
