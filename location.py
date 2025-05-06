"""
Location classes for 'The Line: A Border Journey'

This module defines the locations and environments that characters
can navigate through in the game world.
"""

import random
from character import Migrant, BorderPatrol

class Location:
    """Base class for all game locations."""
    
    def __init__(self, name, description, danger_level=0):
        """Initialize a location.
        
        Args:
            name (str): Name of the location
            description (str): Description of the location
            danger_level (int): How dangerous the location is (0-10)
        """
        self.name = name
        self.description = description
        self.danger_level = danger_level
        self.characters = []  # Characters present at this location
        self.items = []       # Items available at this location
        self.connections = {} # Connected locations {direction: location}
        self.visited = False  # Whether player has visited this location
        self.events = []      # Possible events at this location
        self.environment = {} # Environmental factors (visibility, terrain, etc.)
        self.time_of_day = "day" # Current time of day
        
    def describe(self, detailed=False):
        """Return a description of the location.
        
        Args:
            detailed (bool): Whether to include detailed information
            
        Returns:
            str: Location description
        """
        base_desc = f"{self.name}: {self.description}"
        
        if not detailed:
            return base_desc
            
        # Add details about danger
        danger_desc = "\nDanger Level: "
        if self.danger_level <= 2:
            danger_desc += "Low - Relatively safe area."
        elif self.danger_level <= 5:
            danger_desc += "Medium - Exercise caution."
        elif self.danger_level <= 8:
            danger_desc += "High - Very dangerous area."
        else:
            danger_desc += "Extreme - Life-threatening conditions."
            
        # Add details about connections
        connections_desc = "\nPaths: "
        if self.connections:
            connections_desc += ", ".join([f"{direction} to {location.name}" 
                                         for direction, location in self.connections.items()])
        else:
            connections_desc += "No obvious paths from here."
            
        # Add details about characters present (excluding player)
        non_player_characters = [c for c in self.characters if not hasattr(c, 'is_player') or not c.is_player]
        characters_desc = "\nPresent: "
        if non_player_characters:
            characters_desc += ", ".join([character.name for character in non_player_characters])
        else:
            characters_desc += "No one else is here."
            
        # Add details about items
        items_desc = "\nItems: "
        if self.items:
            items_desc += ", ".join(self.items)
        else:
            items_desc += "Nothing useful found here."
            
        # Add environmental details if present
        environment_desc = ""
        if self.environment:
            environment_desc = "\nConditions: "
            conditions = []
            if "visibility" in self.environment:
                visibility = self.environment["visibility"]
                if visibility < 0.3:
                    conditions.append("extremely poor visibility")
                elif visibility < 0.7:
                    conditions.append("limited visibility")
                else:
                    conditions.append("clear visibility")
            
            if "terrain" in self.environment:
                conditions.append(f"{self.environment['terrain']} terrain")
                
            if "temperature" in self.environment:
                conditions.append(f"{self.environment['temperature']} temperature")
                
            environment_desc += ", ".join(conditions)
            
        return base_desc + danger_desc + connections_desc + characters_desc + items_desc + environment_desc
    
    def add_connection(self, direction, location):
        """Connect this location to another in the specified direction.
        
        Args:
            direction (str): Direction of connection
            location: Location to connect to
        """
        self.connections[direction] = location
        
    def add_character(self, character):
        """Add a character to this location.
        
        Args:
            character: Character to add
        """
        self.characters.append(character)
        character.location = self
        
    def remove_character(self, character):
        """Remove a character from this location.
        
        Args:
            character: Character to remove
            
        Returns:
            bool: True if character was removed, False otherwise
        """
        if character in self.characters:
            self.characters.remove(character)
            if character.location == self:
                character.location = None
            return True
        return False
                
    def add_item(self, item):
        """Add an item to this location.
        
        Args:
            item (str): Item to add
        """
        self.items.append(item)
        
    def remove_item(self, item):
        """Remove an item from this location if present.
        
        Args:
            item (str): Item to remove
            
        Returns:
            bool: True if item was removed, False otherwise
        """
        if item in self.items:
            self.items.remove(item)
            return True
        return False
    
    def add_event(self, event):
        """Add a possible event to this location.
        
        Args:
            event: Event to add
        """
        self.events.append(event)
        
    def get_random_event(self):
        """Return a random event from this location, or None if no events.
        
        Returns:
            Event or None: Random event or None if no events
        """
        if not self.events:
            return None
        return random.choice(self.events)
    
    def set_environment(self, key, value):
        """Set an environmental factor for this location.
        
        Args:
            key (str): Environmental factor
            value: Value of the factor
        """
        self.environment[key] = value
    
    def apply_effects(self, character):
        """Apply location-specific effects to a character.
        
        Args:
            character: Character to apply effects to
            
        Returns:
            str: Description of effects
        """
        # Base location has no special effects
        return None
    
    def set_time_of_day(self, time_str):
        """Set the time of day for this location.
        
        Args:
            time_str (str): Time of day (dawn, day, dusk, night)
        """
        self.time_of_day = time_str
        
        # Adjust environmental factors based on time
        if time_str == "night":
            self.set_environment("visibility", 0.4)
            self.set_environment("temperature", "cold")
        elif time_str == "dawn" or time_str == "dusk":
            self.set_environment("visibility", 0.7)
        else:  # day
            self.set_environment("visibility", 1.0)
            self.set_environment("temperature", "hot")


class Desert(Location):
    """A desert location with extreme conditions."""
    
    def __init__(self, name, description, water_scarcity=8, danger_level=7):
        """Initialize a desert location.
        
        Args:
            name (str): Name of the location
            description (str): Description of the location
            water_scarcity (int): How scarce water is (0-10)
            danger_level (int): How dangerous the location is (0-10)
        """
        super().__init__(name, description, danger_level)
        self.water_scarcity = water_scarcity
        self.set_environment("terrain", "sandy")
        self.set_environment("temperature", "extremely hot")
        
        # Randomly add desert items
        desert_items = ["Cactus Fruit", "Empty Water Bottle", "Sun-Bleached Bone", 
                       "Abandoned Backpack", "Discarded Clothing"]
        if random.random() < 0.3:  # 30% chance of having an item
            self.add_item(random.choice(desert_items))
        
    def describe(self, detailed=False):
        """Return a description of the desert location.
        
        Args:
            detailed (bool): Whether to include detailed information
            
        Returns:
            str: Desert description
        """
        base_desc = super().describe(detailed)
        
        if detailed:
            water_desc = "\nWater: "
            if self.water_scarcity >= 8:
                water_desc += "Critically scarce - No water sources visible."
            elif self.water_scarcity >= 5:
                water_desc += "Very limited - Might find small amounts if lucky."
            else:
                water_desc += "Limited - Some water sources may be found."
                
            # Add time-specific descriptions
            time_desc = "\nTime: "
            if self.time_of_day == "dawn":
                time_desc += "Dawn brings brief respite from the heat, but the day's furnace is awakening."
            elif self.time_of_day == "day":
                time_desc += "The sun is merciless, baking the sand and everything upon it."
            elif self.time_of_day == "dusk":
                time_desc += "The setting sun paints the dunes in gold and crimson as the air begins to cool."
            else:  # night
                time_desc += "Desert night brings bitter cold, a cruel contrast to the day's heat."
                
            return base_desc + water_desc + time_desc
            
        return base_desc
    
    def apply_effects(self, character):
        """Apply desert-specific effects to a character.
        
        Args:
            character: Character to apply effects to
            
        Returns:
            str: Description of effects
        """
        effects = []
        impact_messages = []
        
        # Base effects applicable to all character types
        # Water depletion effects
        if hasattr(character, 'water'):
            # Time of day affects water consumption
            if self.time_of_day == "day":
                water_impact = 2  # Higher consumption during day
            else:
                water_impact = 1  # Lower consumption at night/dawn/dusk
                
            # Character water level affects messaging
            if character.water < 30:
                effects.append("severely dehydrated")
                impact_messages.append("Your throat burns with thirst")
            elif character.water < 50:
                effects.append("thirsty")
                impact_messages.append("Your lips crack from dryness")

        # Desert danger affects health
        if self.danger_level > 5 and hasattr(character, 'health') and character.health < 50:
            effects.append("weakened by the harsh conditions")
            impact_messages.append("The relentless sun saps your strength")
        elif self.danger_level > 7:
            effects.append("struggling against the extreme heat")
            impact_messages.append("Waves of heat distort your vision")

        # Character-specific effects
        if isinstance(character, Migrant):
            # Migrants are more affected by desert conditions
            if hasattr(character, 'hope'):
                # Desert at night offers some hope
                if self.time_of_day == "night" and character.hope < 90:
                    character.hope += 5
                    impact_messages.append("The star-filled desert night brings a moment of beauty amidst hardship")
                # Harsh day diminishes hope
                elif self.time_of_day == "day" and character.hope > 10:
                    character.hope -= 2
                    impact_messages.append("The endless expanse of sand challenges your resolve")
                    
            # Those with survival skills fare better
            if hasattr(character, 'survival_skills') and character.survival_skills > 50:
                impact_messages.append("Your experience helps you navigate the desert's challenges")
        
        # Border Patrol stress increases in desert
        elif isinstance(character, BorderPatrol) and hasattr(character, 'stress'):
            if self.time_of_day == "day":
                character.stress = min(100, character.stress + 5)
                effects.append("stressed from desert heat")
            else:
                character.stress = min(100, character.stress + 2)
                effects.append("fatigued from desert patrol")

        # Build final message based on effects and impacts
        if effects or impact_messages:
            # Combine effects into a character state description
            character_state = f"{character.name} is " + (" and ".join(effects)) if effects else ""
            
            # Combine impact messages into an environmental effect description
            environment_impact = ". ".join(impact_messages) if impact_messages else ""
            
            # Combine both parts, avoiding empty strings
            components = [s for s in [character_state, environment_impact] if s]
            return ". ".join(components) + "."
            
        return f"{character.name} endures the challenging desert conditions."


class Border(Location):
    """A border location with patrol presence."""
    
    def __init__(self, name, description, patrol_intensity=5, danger_level=6):
        """Initialize a border location.
        
        Args:
            name (str): Name of the location
            description (str): Description of the location
            patrol_intensity (int): Level of border patrol presence (0-10)
            danger_level (int): How dangerous the location is (0-10)
        """
        super().__init__(name, description, danger_level)
        self.patrol_intensity = patrol_intensity
        self.surveillance_level = patrol_intensity * 10  # Chance of being detected
        
        # Set environmental factors
        self.set_environment("terrain", "varied")
        
        # Randomly add border items
        border_items = ["Discarded Water Bottle", "Border Crossing Map", "Lost ID Card", 
                      "Surveillance Camera Parts", "Torn Clothing"]
        if random.random() < 0.3:  # 30% chance of having an item
            self.add_item(random.choice(border_items))
        
    def describe(self, detailed=False):
        """Return a description of the border location.
        
        Args:
            detailed (bool): Whether to include detailed information
            
        Returns:
            str: Border description
        """
        base_desc = super().describe(detailed)
        
        if detailed:
            patrol_desc = "\nPatrol: "
            if self.patrol_intensity >= 8:
                patrol_desc += "Heavy presence - Constant surveillance and patrols."
            elif self.patrol_intensity >= 5:
                patrol_desc += "Moderate presence - Regular patrols pass through."
            else:
                patrol_desc += "Light presence - Occasional patrols in the area."
                
            # Add time-specific border descriptions
            time_desc = "\nTime: "
            if self.time_of_day == "dawn":
                time_desc += "Dawn shift change brings fresh patrols and renewed vigilance."
            elif self.time_of_day == "day":
                time_desc += "Daylight makes crossing more visible, but patrols more predictable."
            elif self.time_of_day == "dusk":
                time_desc += "Dusk brings increased crossing attempts as visibility decreases."
            else:  # night
                time_desc += "Night operations use thermal imaging and night vision to detect movement."
                
            # Add surveillance description
            surveillance_desc = "\nSurveillance: "
            if self.surveillance_level >= 80:
                surveillance_desc += "Multiple cameras, sensors, and drones monitor the area constantly."
            elif self.surveillance_level >= 50:
                surveillance_desc += "Periodic drone flights and stationary cameras cover key crossing points."
            else:
                surveillance_desc += "Basic surveillance with occasional monitoring."
                
            return base_desc + patrol_desc + time_desc + surveillance_desc
            
        return base_desc
    
    def encounter_chance(self):
        """Return the chance (0-100) of encountering border patrol.
        
        Returns:
            int: Chance of patrol encounter (0-100)
        """
        # Base chance from patrol intensity
        chance = self.patrol_intensity * 10
        
        # Adjust based on time of day
        if self.time_of_day == "day":
            chance = int(chance * 0.8)  # Lower chance during day (more visible)
        elif self.time_of_day == "dawn" or self.time_of_day == "dusk":
            chance = int(chance * 1.0)  # Normal chance during transition periods
        else:  # night
            chance = int(chance * 1.2)  # Higher chance at night (more patrols)
            
        return max(0, min(100, chance))  # Ensure within 0-100 range
    
    def apply_effects(self, character):
        """Apply border-specific effects to a character.
        
        Args:
            character: Character to apply effects to
            
        Returns:
            str: Description of effects
        """
        effects = []
        impact_messages = []
        
        # Check for patrol encounter for migrants
        if isinstance(character, Migrant):
            encounter_roll = random.randint(1, 100)
            
            # Adjust encounter threshold based on character attributes
            threshold = self.encounter_chance()
            if hasattr(character, 'survival_skills'):
                # Higher skills reduce encounter chance
                threshold -= character.survival_skills // 5
                
            if encounter_roll <= threshold:
                # Patrol spotted, apply stress effects
                if hasattr(character, 'hope'):
                    character.hope = max(0, character.hope - 10)
                    effects.append("anxious about patrol presence")
                    impact_messages.append("You spot a Border Patrol vehicle in the distance")
                    
                # Possible trauma from near-capture
                if hasattr(character, 'trauma'):
                    character.trauma = min(100, character.trauma + 5)
                    
            elif encounter_roll <= threshold + 10:
                # Close call
                effects.append("on edge")
                impact_messages.append("The sound of a patrol vehicle passes nearby")
        
        # Border Patrol agents feel different effects
        elif isinstance(character, BorderPatrol):
            # On duty at border increases stress but improves job standing
            if hasattr(character, 'stress'):
                character.stress = min(100, character.stress + 3)
                effects.append("alert and vigilant")
                
            if hasattr(character, 'department_standing') and random.random() < 0.2:
                character.department_standing = min(100, character.department_standing + 2)
                impact_messages.append("Your presence at the border is noted by supervisors")
        
        # Build final message
        if effects or impact_messages:
            character_state = f"{character.name} is " + (" and ".join(effects)) if effects else ""
            environment_impact = ". ".join(impact_messages) if impact_messages else ""
            
            components = [s for s in [character_state, environment_impact] if s]
            return ". ".join(components) + "."
            
        return f"{character.name} remains watchful at the border."


class Settlement(Location):
    """A settlement location with people and resources."""
    
    def __init__(self, name, description, population=0, danger_level=3):
        """Initialize a settlement location.
        
        Args:
            name (str): Name of the location
            description (str): Description of the location
            population (int): Approximate population of the settlement
            danger_level (int): How dangerous the location is (0-10)
        """
        super().__init__(name, description, danger_level)
        self.population = population
        self.services = []  # Available services ("food", "shelter", "medical")
        self.attitude = random.choice(["friendly", "neutral", "wary", "hostile"])  # Local attitude
        
        # Set environmental factors
        self.set_environment("terrain", "urban")
        
        # Randomly add settlement items
        settlement_items = ["Local Newspaper", "Food Voucher", "Maps", "Used Clothing", "Medicine"]
        if random.random() < 0.4:  # 40% chance of having an item
            self.add_item(random.choice(settlement_items))
        
    def describe(self, detailed=False):
        """Return a description of the settlement location.
        
        Args:
            detailed (bool): Whether to include detailed information
            
        Returns:
            str: Settlement description
        """
        base_desc = super().describe(detailed)
        
        if detailed:
            pop_desc = "\nPopulation: "
            if self.population > 100000:
                pop_desc += "Major urban center"
            elif self.population > 10000:
                pop_desc += "Large community"
            elif self.population > 1000:
                pop_desc += "Medium-sized community"
            elif self.population > 100:
                pop_desc += "Small community"
            else:
                pop_desc += "Tiny settlement"
                
            services_desc = "\nServices: "
            if self.services:
                services_desc += ", ".join(self.services)
            else:
                services_desc += "No services available"
                
            # Add attitude description
            attitude_desc = "\nLocal Attitude: "
            if self.attitude == "friendly":
                attitude_desc += "Residents seem welcoming and helpful."
            elif self.attitude == "neutral":
                attitude_desc += "People mind their own business, neither helpful nor hostile."
            elif self.attitude == "wary":
                attitude_desc += "Locals watch strangers with suspicion and keep their distance."
            else:  # hostile
                attitude_desc += "There's a palpable tension in the air. It's best to keep a low profile."
                
            # Add time-specific descriptions
            time_desc = "\nTime: "
            if self.time_of_day == "dawn":
                time_desc += "The settlement stirs to life as the first light breaks."
            elif self.time_of_day == "day":
                time_desc += "Daily activities are in full swing, streets busy with locals."
            elif self.time_of_day == "dusk":
                time_desc += "People return home as businesses begin to close for the evening."
            else:  # night
                time_desc += "Streets are mostly empty, with only a few late-night establishments active."
                
            return base_desc + pop_desc + services_desc + attitude_desc + time_desc
            
        return base_desc
    
    def add_service(self, service):
        """Add an available service to this settlement.
        
        Args:
            service (str): Service to add
        """
        if service not in self.services:
            self.services.append(service)
            
    def has_service(self, service):
        """Check if a specific service is available.
        
        Args:
            service (str): Service to check
            
        Returns:
            bool: True if service is available, False otherwise
        """
        return service in self.services

    def provide_shelter(self, service_name, character):
        """Provide a service to a character.
        
        Args:
            service_name (str): Service to provide
            character: Character to provide service to
            
        Returns:
            str: Description of service provided
        """
        if service_name not in self.services:
            return f"No {service_name} service available here."

        # Different costs based on service
        service_costs = {
            "food": 20,
            "shelter": 30,
            "medical": 50
        }

        # Adjust costs based on settlement attitude
        attitude_multipliers = {
            "friendly": 0.7,
            "neutral": 1.0,
            "wary": 1.3,
            "hostile": 1.8
        }
        
        base_cost = service_costs.get(service_name.lower(), 0)
        cost = int(base_cost * attitude_multipliers.get(self.attitude, 1.0))
        
        # Check if character can afford the service
        if not hasattr(character, 'money') or character.money < cost:
            return f"You don't have enough money for {service_name} service (needs ${cost})."

        # Apply service effects
        service_message = ""
        if service_name.lower() == "food":
            if hasattr(character, 'food'):
                old_food = character.food
                character.food = min(100, character.food + 40)
                character.money -= cost
                
                gain = character.food - old_food
                service_message = f"{character.name} pays ${cost} and receives a meal, restoring {gain} food."
                
                # Possible extra effect based on settlement size
                if self.population > 5000 and random.random() < 0.3:
                    # Information from other travelers in large settlements
                    tips = [
                        "You overhear other travelers discussing safer crossing points.",
                        "A local mentions increased patrol activity to the west.",
                        "Someone shares the location of a water cache in the desert."
                    ]
                    service_message += f" {random.choice(tips)}"
                    
        elif service_name.lower() == "shelter":
            if hasattr(character, 'health'):
                old_health = character.health
                character.health = min(100, character.health + 20)
                character.money -= cost
                
                gain = character.health - old_health
                service_message = f"{character.name} pays ${cost} for shelter and rests safely, recovering {gain} health."
                
                # Rest also reduces stress for Border Patrol
                if isinstance(character, BorderPatrol) and hasattr(character, 'stress'):
                    old_stress = character.stress
                    character.stress = max(0, character.stress - 15)
                    reduction = old_stress - character.stress
                    service_message += f" The rest also reduces stress by {reduction} points."
                    
                # Rest improves hope for Migrants
                if isinstance(character, Migrant) and hasattr(character, 'hope'):
                    old_hope = character.hope
                    character.hope = min(100, character.hope + 10)
                    gain = character.hope - old_hope
                    service_message += f" The safe environment improves hope by {gain} points."
                    
        elif service_name.lower() == "medical":
            if hasattr(character, "health"):
                old_health = character.health
                character.health = min(100, character.health + 35)
                character.money -= cost
                
                gain = character.health - old_health
                service_message = f"{character.name} pays ${cost} and receives medical care, healing {gain} health."
                
                # Medical care also helps with trauma
                if hasattr(character, 'trauma') and character.trauma > 0:
                    old_trauma = character.trauma
                    character.trauma = max(0, character.trauma - 10)
                    reduction = old_trauma - character.trauma
                    if reduction > 0:
                        service_message += f" The professional care helps process some trauma (-{reduction} trauma)."
        
        return service_message if service_message else f"Used {service_name} service for ${cost}."
    
    def apply_effects(self, character):
        """Apply settlement-specific effects to a character.
        
        Args:
            character: Character to apply effects to
            
        Returns:
            str: Description of effects
        """
        effects = []
        impact_messages = []
        
        # Effects based on settlement attitude
        if self.attitude == "friendly":
            # Friendly settlements improve hope/morale
            if hasattr(character, 'hope') and character.hope < 95:
                character.hope += 5
                impact_messages.append("The welcoming atmosphere lifts your spirits")
                
            # May find resources
            if random.random() < 0.1 and not "Water Bottle" in self.items:
                self.add_item("Water Bottle")
                impact_messages.append("A local resident left water for travelers")
                
        elif self.attitude == "hostile":
            # Hostile settlements increase stress/reduce hope
            if isinstance(character, Migrant):
                if hasattr(character, 'hope'):
                    character.hope = max(0, character.hope - 5)
                    effects.append("unwelcome")
                    
                # Increased risk of being reported
                if random.random() < 0.15:
                    impact_messages.append("You notice someone watching you with suspicion")
                    
            elif isinstance(character, BorderPatrol):
                if hasattr(character, 'stress'):
                    character.stress = min(100, character.stress + 5)
                    effects.append("tense")
                    impact_messages.append("The locals seem uncooperative with authorities")
        
        # Services provide passive benefits just from being available
        if "food" in self.services:
            # Food availability reduces anxiety about resources
            if hasattr(character, 'food') and character.food < 30:
                impact_messages.append("The availability of food services provides some relief")
                
        if "medical" in self.services:
            # Medical presence gives security
            if hasattr(character, 'health') and character.health < 40:
                impact_messages.append("Knowing medical help is available eases your concern")
        
        # Build final message
        if effects or impact_messages:
            character_state = f"{character.name} feels " + (" and ".join(effects)) if effects else ""
            environment_impact = ". ".join(impact_messages) if impact_messages else ""
            
            components = [s for s in [character_state, environment_impact] if s]
            return ". ".join(components) + "."
            
        return None