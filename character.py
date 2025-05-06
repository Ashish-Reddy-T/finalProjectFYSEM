"""
Character classes for 'The Line: A Border Journey'

This module defines the character classes used in the game,
including the base Character class and specialized character types.
"""

import random


class Character:
    """Base character class for all game characters."""
    
    def __init__(self, name, description, health=100):
        """Initialize a character with basic attributes.
        
        Args:
            name (str): Character's name
            description (str): Brief description of the character
            health (int): Character's health points (default: 100)
        """
        self.name = name
        self.description = description
        self.health = health
        self.inventory = []
        self.location = None
        self.story_flags = {}
        self.traits = []  # Character personality traits for more depth
        
    def describe(self):
        """Return a description of the character."""
        base_desc = f"{self.name}: {self.description}"
        if self.traits:
            base_desc += f"\nTraits: {', '.join(self.traits)}"
        return base_desc
    
    def add_to_inventory(self, item):
        """Add an item to the character's inventory."""
        self.inventory.append(item)
        return f"{self.name} acquired {item}."
    
    def remove_from_inventory(self, item):
        """Remove an item from the character's inventory if present."""
        if item in self.inventory:
            self.inventory.remove(item)
            return f"{self.name} no longer has {item}."
        return f"{self.name} doesn't have {item}."
    
    def set_flag(self, flag_name, value):
        """Set a story flag for this character."""
        self.story_flags[flag_name] = value
    
    def has_flag(self, flag_name):
        """Check if a story flag exists and is True."""
        return self.story_flags.get(flag_name, False)
    
    def add_trait(self, trait):
        """Add a personality trait to the character."""
        if trait not in self.traits:
            self.traits.append(trait)
            return f"{self.name} now has the trait: {trait}"
        return f"{self.name} already has the trait: {trait}"
    
    def has_trait(self, trait):
        """Check if the character has a specific trait."""
        return trait in self.traits


class Migrant(Character):
    """Class representing a migrant character."""
    
    def __init__(self, name, description, origin, motivation, health=100):
        """Initialize a migrant character.
        
        Args:
            name (str): Character's name
            description (str): Brief description of the character
            origin (str): Character's place of origin
            motivation (str): Reason for migration
            health (int): Character's health points (default: 100)
        """
        super().__init__(name, description, health)
        self.origin = origin
        self.motivation = motivation
        self.water = 100  # Water level (0-100)
        self.food = 100   # Food level (0-100)
        self.hope = 100   # Hope level (0-100)
        self.money = 100  # Starting money
        self.family_ties = []  # List of family members
        self.survival_skills = 0  # Grows with experience (0-100)
        self.trauma = 0  # Trauma accumulation (0-100)
        
    def describe(self):
        """Return a detailed description of the migrant."""
        base_desc = super().describe()
        detailed_desc = f"{base_desc}\nOrigin: {self.origin}\nMotivation: {self.motivation}"
        
        # Add family ties if present
        if self.family_ties:
            family_desc = "Family: " + ", ".join([f"{tie['name']} ({tie['relationship']})" for tie in self.family_ties])
            detailed_desc += f"\n{family_desc}"
            
        return detailed_desc
    
    def consume_resources(self, water_amount=5, food_amount=5):
        """Consume water and food resources.
        
        Args:
            water_amount (int): Amount of water to consume
            food_amount (int): Amount of food to consume
            
        Returns:
            str: Description of resource consumption effects
        """
        # Apply survival skills to reduce consumption (if applicable)
        if self.survival_skills > 0:
            skill_factor = 1.0 - (self.survival_skills / 200)  # Max 50% reduction at 100 skill
            water_amount = max(1, int(water_amount * skill_factor))
            food_amount = max(1, int(food_amount * skill_factor))
        
        # Consume resources
        self.water = max(0, self.water - water_amount)
        self.food = max(0, self.food - food_amount)
        
        # Health effects
        health_loss = 0
        effects = []
        
        # Water effects
        if self.water <= 0:
            health_loss += 20  # Severe dehydration
            effects.append("severe dehydration")
        elif self.water < 20:
            health_loss += 5   # Moderate dehydration
            effects.append("dehydration")
            
        # Food effects
        if self.food <= 0:
            health_loss += 8   # Starvation
            effects.append("starvation")
        elif self.food < 20:
            health_loss += 3   # Hunger
            effects.append("hunger")
            
        # Hope effects on health
        if self.hope < 30:
            health_loss += 2   # Low morale affects physical health
            effects.append("despair")
            
        # Apply health loss
        if health_loss > 0:
            self.health = max(0, self.health - health_loss)
            
        # Generate status message
        if not effects:
            return f"{self.name} is doing well."
        
        if health_loss > 15:
            return f"{self.name} is severely weakened by {' and '.join(effects)}."
        elif health_loss > 0:
            return f"{self.name} is suffering from {' and '.join(effects)}."
        else:
            return f"{self.name} is experiencing {' and '.join(effects)}."
    
    def change_hope(self, amount):
        """Change the character's hope level.
        
        Args:
            amount (int): Amount to change hope by (positive or negative)
            
        Returns:
            str: Description of hope change effect
        """
        old_hope = self.hope
        self.hope = max(0, min(100, self.hope + amount))
        change = self.hope - old_hope
        
        # Hope affects trauma recovery
        if amount > 0 and self.trauma > 0:
            trauma_recovery = min(self.trauma, amount // 3)
            self.trauma = max(0, self.trauma - trauma_recovery)
        
        # Hope messages based on direction and magnitude
        if change > 20:
            return f"{self.name} feels a powerful surge of hope."
        elif change > 10:
            return f"{self.name} feels significantly more hopeful."
        elif change > 0:
            return f"{self.name} feels a bit more hopeful."
        elif change < -20:
            return f"{self.name} feels overwhelmed by despair."
        elif change < -10:
            return f"{self.name}'s hope diminishes significantly."
        elif change < 0:
            return f"{self.name} feels slightly less hopeful."
        else:
            return f"{self.name}'s hope remains unchanged."
    
    def add_family_tie(self, name, relationship):
        """Add a family member with their relationship.
        
        Args:
            name (str): Name of family member
            relationship (str): Relationship to character
            
        Returns:
            str: Description of added family tie
        """
        self.family_ties.append({"name": name, "relationship": relationship})
        return f"{self.name} thinks of {name}, their {relationship}."
    
    def improve_skill(self, amount=1):
        """Improve survival skills from experience.
        
        Args:
            amount (int): Amount to increase skill by
            
        Returns:
            str: Description of skill improvement
        """
        old_skill = self.survival_skills
        self.survival_skills = min(100, self.survival_skills + amount)
        
        if self.survival_skills > old_skill:
            return f"{self.name} learns from experience, improving their survival skills."
        return f"{self.name}'s survival instincts are already well-developed."
    
    def experience_trauma(self, amount=10, event_description=None):
        """Experience a traumatic event that affects mental state.
        
        Args:
            amount (int): Trauma amount
            event_description (str): Description of traumatic event
            
        Returns:
            str: Description of trauma effect
        """
        self.trauma = min(100, self.trauma + amount)
        
        # Trauma affects hope
        hope_loss = amount // 2
        self.hope = max(0, self.hope - hope_loss)
        
        if event_description:
            return f"{self.name} is deeply affected by {event_description}. The trauma weighs heavily."
        return f"{self.name} experiences trauma that affects their mental state."


class BorderPatrol(Character):
    """Class representing a border patrol agent."""
    
    def __init__(self, name, description, years_of_service=0, health=100):
        """Initialize a border patrol agent character.
        
        Args:
            name (str): Character's name
            description (str): Brief description of the character
            years_of_service (int): Years served in border patrol
            health (int): Character's health points (default: 100)
        """
        super().__init__(name, description, health)
        self.years_of_service = years_of_service
        self.moral_compass = 50  # Scale from 0 (corrupt) to 100 (strictly moral)
        self.stress = 0  # Stress level from 0 to 100
        self.encounters = 0  # Number of migrant encounters
        self.money = 200 # Border patrol money
        self.water = 100
        self.food = 100
        self.experience = years_of_service * 10  # Experience level (0-100)
        self.department_standing = 50  # Standing within the organization (0-100)
        
    def describe(self):
        """Return a detailed description of the agent."""
        base_desc = super().describe()
        detailed_desc = f"{base_desc}\nYears of Service: {self.years_of_service}"
        
        # Add reputation description
        if self.department_standing >= 80:
            detailed_desc += "\nYou're highly respected within the department."
        elif self.department_standing >= 60:
            detailed_desc += "\nYou have a good reputation among your colleagues."
        elif self.department_standing >= 40:
            detailed_desc += "\nYour standing in the department is average."
        elif self.department_standing >= 20:
            detailed_desc += "\nSome colleagues question your commitment to the job."
        else:
            detailed_desc += "\nYour reputation within the department has suffered."
            
        return detailed_desc
    
    def encounter_migrant(self, migrant, action="detain"):
        """Handle an encounter with a migrant.
        
        Args:
            migrant (Migrant): The migrant character encountered
            action (str): The action taken ("detain", "help", "ignore")
            
        Returns:
            str: Description of what happened
        """
        self.encounters += 1
        
        # Stress increase depends on experience
        base_stress = random.randint(1, 10)
        experience_factor = max(0.2, 1.0 - (self.experience / 120))  # Experience reduces stress
        stress_increase = int(base_stress * experience_factor)
        self.stress = min(100, self.stress + stress_increase)
        
        # Different actions affect moral compass and department standing
        result = ""
        
        if action == "detain":
            # Standard procedure, effects depend on migrant condition
            if migrant.health < 30 or hasattr(migrant, 'water') and migrant.water < 20:
                self.moral_compass -= 5
                result = f"{self.name} detained {migrant.name}, who was in poor condition. This weighs on {self.name}'s conscience."
            else:
                self.department_standing = min(100, self.department_standing + 5)
                result = f"{self.name} detained {migrant.name} according to protocol."
            
        elif action == "help":
            # Helping improves moral compass but may affect department standing
            self.moral_compass += 10
            if random.random() < 0.3:  # 30% chance someone notices
                self.department_standing = max(0, self.department_standing - 5)
                result = f"{self.name} chose to help {migrant.name}, providing water and medical attention. A colleague noticed this deviation from protocol."
            else:
                result = f"{self.name} chose to help {migrant.name}, providing water and medical attention before processing."
            
        elif action == "ignore":
            # Ignoring duty decreases moral compass and risks department standing
            self.moral_compass -= 15
            if random.random() < 0.2:  # 20% chance of being caught
                self.department_standing = max(0, self.department_standing - 15)
                result = f"{self.name} chose to look the other way, allowing {migrant.name} to continue undetained. This violation of duty was reported."
            else:
                result = f"{self.name} chose to look the other way, allowing {migrant.name} to continue undetained."
            
        return result if result else f"{self.name} encountered {migrant.name}."
    
    def process_stress(self):
        """Process the effects of accumulated stress.
        
        Returns:
            str: Description of stress effects
        """
        effects = []
        
        # Determine stress effects
        if self.stress > 80:
            self.health -= 5
            effects.append("severe burnout")
        elif self.stress > 60:
            self.health -= 2
            effects.append("trouble sleeping")
        elif self.stress > 40:
            effects.append("preoccupation with work")
            
        # Stress recovery if below threshold
        if self.stress < 30:
            self.stress = max(0, self.stress - 5)
            return f"{self.name} is managing work stress well."
            
        # Generate status message
        if not effects:
            return f"{self.name} is coping with the job's demands."
            
        return f"{self.name} is experiencing {' and '.join(effects)} due to job stress."
    
    def consume_resources(self, water_amount=3, food_amount=3):
        """Consume water and food resources (slower than migrants).
        
        Args:
            water_amount (int): Amount of water to consume
            food_amount (int): Amount of food to consume
            
        Returns:
            str: Description of resource consumption effects
        """
        # Experience helps with resource management
        if self.experience > 0:
            experience_factor = 1.0 - (self.experience / 200)  # Max 50% reduction
            water_amount = max(1, int(water_amount * experience_factor))
            food_amount = max(1, int(food_amount * experience_factor))
        
        # Consume resources
        self.water = max(0, self.water - water_amount)
        self.food = max(0, self.food - food_amount)
        
        # Health effects
        health_loss = 0
        effects = []
        
        # Water effects
        if self.water <= 0:
            health_loss += 5  # Less severe than migrants
            effects.append("severe dehydration")
        elif self.water < 20:
            health_loss += 2
            effects.append("thirst")
            
        # Food effects
        if self.food <= 0:
            health_loss += 4
            effects.append("hunger")
        elif self.food < 20:
            health_loss += 1
            effects.append("mild hunger")
            
        # Stress effects on health
        if self.stress > 70:
            health_loss += 2
            effects.append("stress")
            
        # Apply health loss
        if health_loss > 0:
            self.health = max(0, self.health - health_loss)
            
        # Generate status message
        if not effects:
            return f"{self.name} is doing well."
        
        if health_loss > 10:
            return f"{self.name} is significantly affected by {' and '.join(effects)}."
        elif health_loss > 0:
            return f"{self.name} is dealing with {' and '.join(effects)}."
        else:
            return f"{self.name} is experiencing {' and '.join(effects)}."
    
    def modify_standing(self, amount):
        """Modify department standing.
        
        Args:
            amount (int): Amount to change standing by
            
        Returns:
            str: Description of standing change
        """
        old_standing = self.department_standing
        self.department_standing = max(0, min(100, self.department_standing + amount))
        change = self.department_standing - old_standing
        
        if change > 15:
            return f"{self.name}'s actions have significantly improved their standing in the department."
        elif change > 0:
            return f"{self.name}'s reputation in the department has slightly improved."
        elif change < -15:
            return f"{self.name}'s actions have seriously damaged their reputation in the department."
        elif change < 0:
            return f"{self.name}'s standing in the department has slightly suffered."
        else:
            return f"{self.name}'s departmental standing remains unchanged."