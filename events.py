"""
Events for 'The Line: A Border Journey'

This module defines the narrative events that can occur during gameplay,
representing key moments and challenges from 'The Line Becomes a River'.
"""

import random


class Event:
    """Base class for all game events."""
    
    def __init__(self, name, description, location_types=None, required_flags=None, 
                 excluded_flags=None, time_of_day=None):
        """
        Initialize an event.
        
        Args:
            name (str): Name of the event
            description (str): Description of the event
            location_types (list): Types of locations where this event can occur
            required_flags (dict): Flags that must be set for this event to occur
            excluded_flags (dict): Flags that prevent this event from occurring
            time_of_day (list): Times of day when this event can occur (dawn, day, dusk, night)
        """
        self.name = name
        self.description = description
        self.location_types = location_types or []
        self.required_flags = required_flags or {}
        self.excluded_flags = excluded_flags or {}
        self.time_of_day = time_of_day or ["dawn", "day", "dusk", "night"]
        
    def can_occur(self, location):
        """Check if this event can occur at the given location.
        
        Args:
            location: The location to check
            
        Returns:
            bool: True if event can occur at location, False otherwise
        """
        # Check location type
        if self.location_types and not any(isinstance(location, t) for t in self.location_types):
            return False
            
        # Check time of day if location has time attribute
        if hasattr(location, 'time_of_day') and location.time_of_day not in self.time_of_day:
            return False
            
        return True
    
    def check_flags(self, character):
        """Check if a character meets the flag requirements for this event.
        
        Args:
            character: The character to check
            
        Returns:
            bool: True if character meets requirements, False otherwise
        """
        # Check required flags
        for flag, value in self.required_flags.items():
            if not hasattr(character, 'story_flags') or character.story_flags.get(flag) != value:
                return False
                
        # Check excluded flags
        for flag, value in self.excluded_flags.items():
            if hasattr(character, 'story_flags') and character.story_flags.get(flag) == value:
                return False
                
        return True
    
    def execute(self, game, character):
        """Execute the event for the given character.
        
        Args:
            game: The game instance
            character: The character experiencing the event
            
        Returns:
            str: Description of what happened
        """
        # Check if character meets flag requirements
        if not self.check_flags(character):
            return None
            
        return self.description


class EncounterEvent(Event):
    """An event where the character encounters someone or something."""
    
    def __init__(self, name, description, encounter_type, location_types=None, 
                 required_flags=None, excluded_flags=None, time_of_day=None,
                 dialogue=None, choices=None):
        """
        Initialize an encounter event.
        
        Args:
            name (str): Name of the event
            description (str): Description of the event
            encounter_type (str): Type of encounter ('migrant', 'patrol', 'local', 'wildlife')
            location_types (list): Types of locations where this event can occur
            required_flags (dict): Flags that must be set for this event to occur
            excluded_flags (dict): Flags that prevent this event from occurring
            time_of_day (list): Times of day when this event can occur
            dialogue (list): Possible dialogue lines for the encounter
            choices (dict): Possible player choices and their consequences
        """
        super().__init__(name, description, location_types, required_flags, excluded_flags, time_of_day)
        self.encounter_type = encounter_type
        self.dialogue = dialogue or []
        self.choices = choices or {}
        
    def execute(self, game, character):
        """Execute the encounter event.
        
        Args:
            game: The game instance
            character: The character experiencing the event
            
        Returns:
            str: Description of what happened
        """
        # Check if character meets flag requirements
        if not self.check_flags(character):
            return None
            
        base_result = f"{self.description}"
        
        # Add dialogue if available
        if self.dialogue:
            base_result += f"\n\n\"{random.choice(self.dialogue)}\""
        
        # Present choices if available
        if self.choices and len(self.choices) > 0:
            # Display choices
            choice_text = "\nChoices:\n"
            choice_options = list(self.choices.keys())
            
            for i, choice in enumerate(choice_options, 1):
                choice_text += f"{i}. {choice}\n"
                
            print(f"\n{base_result}")
            print(choice_text)
            
            # Get player's choice
            valid_choice = False
            choice_index = 0
            
            while not valid_choice:
                try:
                    choice_input = input(f"Enter your choice (1-{len(choice_options)}): ")
                    choice_index = int(choice_input) - 1
                    if 0 <= choice_index < len(choice_options):
                        valid_choice = True
                    else:
                        print(f"Please enter a number between 1 and {len(choice_options)}.")
                except ValueError:
                    print("Please enter a valid number.")
                    
            chosen_option = choice_options[choice_index]
            consequence = self.choices[chosen_option]

            # Update stats - ADD THESE LINES
            game.story.update_journey_stats("moral_choices_made")
            game.story.update_journey_stats("lives_impacted")
            
            # Apply the consequence effects
            result = f"You chose: {chosen_option}\n{consequence['description']}"
            
            # Apply impacts if defined
            if 'impacts' in consequence:
                for stat, value in consequence['impacts'].items():
                    if stat == 'hope' and hasattr(character, 'hope'):
                        character.hope = max(0, min(100, character.hope + value))
                    elif stat == 'health' and hasattr(character, 'health'):
                        character.health = max(0, min(100, character.health + value))
                    elif stat == 'water' and hasattr(character, 'water'):
                        character.water = max(0, min(100, character.water + value))
                    elif stat == 'food' and hasattr(character, 'food'):
                        character.food = max(0, min(100, character.food + value))
                    elif stat == 'moral_compass' and hasattr(character, 'moral_compass'):
                        character.moral_compass = max(0, min(100, character.moral_compass + value))
                    elif stat == 'stress' and hasattr(character, 'stress'):
                        character.stress = max(0, min(100, character.stress + value))
                        
            # Set any flags from the consequence
            if 'flags' in consequence:
                for flag, value in consequence['flags'].items():
                    character.set_flag(flag, value)
                    
            return result
        
        # Different outcomes based on encounter type if no choices
        if self.encounter_type == 'patrol' and hasattr(character, 'hope'):
            # Migrants lose hope when encountering patrol
            character.hope = max(0, character.hope - 20)
            return f"{base_result}\n{character.name}'s hope diminishes."
            
        elif self.encounter_type == 'migrant' and hasattr(character, 'stress'):
            # Border patrol agents gain stress when encountering migrants
            character.stress = min(100, character.stress + 10)
            return f"{base_result}\n{character.name}'s stress increases."
            
        elif self.encounter_type == 'local' and hasattr(character, 'hope'):
            # Migrants gain hope when encountering helpful locals
            character.hope = min(100, character.hope + 10)
            return f"{base_result}\n{character.name} feels more hopeful."
            
        elif self.encounter_type == 'wildlife':
            # Wildlife encounters can be dangerous
            if random.random() < 0.3:  # 30% chance of danger
                character.health = max(0, character.health - 10)
                return f"{base_result}\nThe wildlife encounter costs {character.name} some health."
            else:
                # Not dangerous, possibly beneficial for Border Patrol morale
                if hasattr(character, 'moral_compass'):
                    character.moral_compass = min(100, character.moral_compass + 5)
                    return f"{base_result}\nThe wildlife encounter reminds {character.name} of the beauty in this harsh land."
            
        return base_result


class ResourceEvent(Event):
    """An event related to finding or losing resources."""
    
    def __init__(self, name, description, resource_type, amount, location_types=None, 
                 required_flags=None, excluded_flags=None, time_of_day=None, difficulty=None):
        """
        Initialize a resource event.
        
        Args:
            name (str): Name of the event
            description (str): Description of the event
            resource_type (str): Type of resource ('water', 'food', 'health', 'item', 'money')
            amount (int): Amount gained (positive) or lost (negative)
            location_types (list): Types of locations where this event can occur
            required_flags (dict): Flags that must be set for this event to occur
            excluded_flags (dict): Flags that prevent this event from occurring
            time_of_day (list): Times of day when this event can occur
            difficulty (int): Difficulty level to overcome (0-100, None for automatic)
        """
        super().__init__(name, description, location_types, required_flags, excluded_flags, time_of_day)
        self.resource_type = resource_type
        self.amount = amount
        self.difficulty = difficulty
        
    def execute(self, game, character):
        """Execute the resource event.
        
        Args:
            game: The game instance
            character: The character experiencing the event
            
        Returns:
            str: Description of what happened
        """
        # Check if character meets flag requirements
        if not self.check_flags(character):
            return None
            
        base_result = f"{self.description}"
        
        # If there's a difficulty check, see if character succeeds
        success = True
        if self.difficulty is not None:
            # Success based on character skills if available
            if hasattr(character, 'survival_skills'):
                success_chance = min(90, max(10, character.survival_skills - self.difficulty + 50))
            else:
                success_chance = min(90, max(10, 100 - self.difficulty))
                
            success = random.randint(1, 100) <= success_chance
        
        # Apply resource effects based on success
        if success:
            if self.resource_type == 'water' and hasattr(character, 'water'):
                old_water = character.water
                character.water = max(0, min(100, character.water + self.amount))
                change = character.water - old_water
                
                if self.amount > 0:
                    return f"{base_result}\n{character.name} found water (+{change} water)."
                else:
                    return f"{base_result}\n{character.name} lost water ({change} water)."
                    
            elif self.resource_type == 'food' and hasattr(character, 'food'):
                old_food = character.food
                character.food = max(0, min(100, character.food + self.amount))
                change = character.food - old_food
                
                if self.amount > 0:
                    return f"{base_result}\n{character.name} found food (+{change} food)."
                else:
                    return f"{base_result}\n{character.name} lost food ({change} food)."
                    
            elif self.resource_type == 'health':
                old_health = character.health
                character.health = max(0, min(100, character.health + self.amount))
                change = character.health - old_health
                
                if self.amount > 0:
                    return f"{base_result}\n{character.name}'s health improved (+{change} health)."
                else:
                    return f"{base_result}\n{character.name}'s health worsened ({change} health)."
                    
            elif self.resource_type == 'money' and hasattr(character, 'money'):
                old_money = character.money
                character.money += self.amount
                change = character.money - old_money
                
                if self.amount > 0:
                    return f"{base_result}\n{character.name} found ${change}."
                else:
                    return f"{base_result}\n{character.name} lost ${-change}."
                    
            elif self.resource_type == 'item':
                if self.amount > 0 and hasattr(game, 'items') and game.items:
                    # Add a random item from game's item pool
                    item = random.choice(game.items)
                    character.add_to_inventory(item)
                    return f"{base_result}\n{character.name} found {item}."
                elif self.amount < 0 and character.inventory:
                    # Remove a random item from inventory
                    item = random.choice(character.inventory)
                    character.remove_from_inventory(item)
                    return f"{base_result}\n{character.name} lost {item}."
        else:
            # Failed to find/protect resource
            if self.amount > 0:
                return f"{base_result}\nDespite efforts, {character.name} failed to acquire the resource."
            else:
                # Still lose resources on failure to protect
                if self.resource_type == 'water' and hasattr(character, 'water'):
                    old_water = character.water
                    character.water = max(0, character.water + self.amount)
                    change = character.water - old_water
                    return f"{base_result}\nDespite efforts to protect supplies, {character.name} lost {-change} water."
                elif self.resource_type == 'food' and hasattr(character, 'food'):
                    old_food = character.food
                    character.food = max(0, character.food + self.amount)
                    change = character.food - old_food
                    return f"{base_result}\nDespite efforts to protect supplies, {character.name} lost {-change} food."
                elif self.resource_type == 'health':
                    old_health = character.health
                    character.health = max(0, character.health + self.amount)
                    change = character.health - old_health
                    return f"{base_result}\n{character.name} was injured, losing {-change} health."
                elif self.resource_type == 'item' and character.inventory:
                    item = random.choice(character.inventory)
                    character.remove_from_inventory(item)
                    return f"{base_result}\n{character.name} lost {item} despite attempts to protect it."
        
        return base_result
    
class BorderCrossingEvent(Event):
    """An event specifically for crossing the border wall."""
    
    def __init__(self, name, description, location_types=None, 
                 required_flags=None, excluded_flags=None, time_of_day=None):
        """Initialize a border crossing event."""
        # Make sure this only happens at Border locations
        from location import Border
        super().__init__(name, description, location_types=[Border], 
                        required_flags=required_flags, excluded_flags=excluded_flags, 
                        time_of_day=time_of_day)
        
        # Define different crossing methods with varying risks
        self.crossing_methods = [
            {
                "name": "Climb over with makeshift ladder",
                "description": "Use a homemade ladder to scale the wall in a less monitored section.",
                "success_chance": 40,
                "health_risk": 15,
                "requires": None,
                "outcome_success": "You carefully set up the ladder against the wall during a patrol gap. Climbing is harder than expected, especially while carrying your belongings. At the top, you must drop down 20 feet to the other side. The impact jars through your body, but you've made it across.",
                "outcome_failure": "The ladder shifts unexpectedly as you climb. You fall hard onto Mexican soil, painfully injuring yourself. Border Patrol spotlights sweep nearby, forcing you to retreat quickly."
            },
            {
                "name": "Pay a guide (coyote) for tunnel access",
                "description": "Pay $50 to use a hidden tunnel that runs beneath the border wall.",
                "success_chance": 70,
                "health_risk": 10,
                "requires": {"money": 50},
                "outcome_success": "The guide leads you to an unmarked location half a mile from the wall. You squeeze into a narrow tunnel, crawling through darkness for what feels like hours. Emerging on the US side, you're disoriented but safely across.",
                "outcome_failure": "The tunnel entrance seems suspicious, and indeed, you spot signs of recent patrol activity. Your guide abandons you when border patrol vehicles approach, keeping your payment while you're forced to retreat."
            },
            {
                "name": "Find a gap in the fence",
                "description": "Search for damaged sections where you might slip through.",
                "success_chance": 30,
                "health_risk": 5,
                "requires": None,
                "outcome_success": "After hours of careful scouting, you find a section where erosion has created a small gap beneath the wall. It's a tight squeeze that tears your clothing and scrapes your skin, but you wriggle through to the other side.",
                "outcome_failure": "You find what appears to be a gap, but while attempting to squeeze through, you become temporarily stuck. By the time you extract yourself, you've been spotted by a patrol drone and must flee back into Mexican territory."
            },
            {
                "name": "Wait for nightfall and use wire cutters",
                "description": "Use wire cutters to create an opening in a less monitored section at night.",
                "success_chance": 50,
                "health_risk": 10,
                "requires": {"item": "Wire Cutters"},
                "outcome_success": "Under cover of darkness, you approach a section between camera posts. The sound of metal cutting through metal seems deafening in the night silence. You create just enough space to squeeze through, leaving behind a gap that will likely be discovered by morning patrols.",
                "outcome_failure": "As you begin cutting, bright floodlights suddenly illuminate your position. The Border Patrol has night vision technology, and your attempt has been discovered. You run back toward Nogales to avoid capture."
            },
            {
                "name": "Join a larger group crossing",
                "description": "Safety in numbers - join 15-20 others attempting a coordinated crossing.",
                "success_chance": 60,
                "health_risk": 20,
                "requires": {"money": 30},
                "outcome_success": "You join a large group led by experienced guides. When you reach the wall, the group splits into smaller units. While Border Patrol intercepts some groups, yours slips through during the chaos. The sprint across open terrain is exhausting, but you make it to the pickup point.",
                "outcome_failure": "The large group attracts immediate attention. Patrol vehicles, helicopters, and agents converge quickly. In the ensuing chaos, some make it across, but you're forced back into Mexico as agents close in."
            }
        ]
    
    def execute(self, game, character):
        """Execute the border crossing event for the given character.
        
        Args:
            game: The game instance
            character: The character experiencing the event
            
        Returns:
            str: Description of what happened
        """
        # Only relevant for migrants
        from character import Migrant
        if not isinstance(character, Migrant):
            return "This event is only relevant for migrants."
            
        # Check if character meets flag requirements
        if not self.check_flags(character):
            return None
            
        # Present the crossing options
        print(f"\n-----BORDER CROSSING CHALLENGE-----")
        print(self.description)
        print("\nYou must find a way past the heavily guarded border wall. Each method has risks and requirements.")
        
        # Show available options
        valid_options = []
        for i, method in enumerate(self.crossing_methods, 1):
            # Check if player meets requirements
            can_use = True
            req_text = ""
            
            if method["requires"]:
                if "money" in method["requires"] and hasattr(character, 'money'):
                    if character.money < method["requires"]["money"]:
                        can_use = False
                        req_text = f" (Requires ${method['requires']['money']} - you only have ${character.money})"
                    else:
                        req_text = f" (Costs ${method['requires']['money']})"
                        
                if "item" in method["requires"] and method["requires"]["item"] not in character.inventory:
                    can_use = False
                    req_text = f" (Requires {method['requires']['item']} - not in your inventory)"
            
            if can_use:
                valid_options.append(i-1)  # Store index of valid option
                
            # Format text differently based on availability
            if can_use:
                print(f"{i}. {method['name']}: {method['description']}{req_text}")
            else:
                print(f"{i}. {method['name']}: {method['description']}{req_text} [NOT AVAILABLE]")
        
        if not valid_options:
            return "You don't have the resources needed for any crossing method. You'll need to gather more supplies or money."
            
        # Get player's choice
        valid_choice = False
        choice_index = 0
        
        while not valid_choice:
            try:
                choice_input = input(f"\nChoose your crossing method (1-{len(self.crossing_methods)}): ")
                choice_index = int(choice_input) - 1
                if 0 <= choice_index < len(self.crossing_methods):
                    if choice_index in valid_options:
                        valid_choice = True
                    else:
                        print("You don't meet the requirements for that method. Choose another.")
                else:
                    print(f"Please enter a number between 1 and {len(self.crossing_methods)}.")
            except ValueError:
                print("Please enter a valid number.")
                
        chosen_method = self.crossing_methods[choice_index]
        
        # Apply resource costs
        if chosen_method["requires"] and "money" in chosen_method["requires"]:
            character.money -= chosen_method["requires"]["money"]
        
        # Determine success based on chance
        success_roll = random.randint(1, 100)
        success = success_roll <= chosen_method["success_chance"]
        
        # Apply health impact
        health_impact = chosen_method["health_risk"]
        if not success:
            health_impact = int(health_impact * 1.5)  # Higher impact on failure
            
        old_health = character.health
        character.health = max(0, character.health - health_impact)
        health_change = character.health - old_health
        
        # Build result narrative
        result = f"You attempt to cross using the '{chosen_method['name']}' method.\n\n"
        
        # Handle success or failure
        if success:
            result += chosen_method["outcome_success"]
            result += f"\n\nThe crossing takes a physical toll ({health_change} health)."
            
            # Move character to US side if currently at border
            if game.current_location.name == "Border Wall":
                # Remove from current location
                game.current_location.remove_character(character)
                # Move to US side
                game.current_location = game.world["nogales_us"]
                game.current_location.add_character(character)
                game.current_location.visited = True
                
                # Update journey stats
                game.story.update_journey_stats("key_events", f"Successfully crossed border using {chosen_method['name']}")
                
                # Add some hope for successful crossing
                if hasattr(character, 'hope'):
                    character.hope = min(100, character.hope + 15)
                    result += " Despite the difficulties, your spirits rise as you set foot on US soil."
            
        else:
            result += chosen_method["outcome_failure"]
            result += f"\n\nThe failed attempt is costly to your health ({health_change} health)."
            
            # Reduce hope for failed crossing
            if hasattr(character, 'hope'):
                character.hope = max(0, character.hope - 10)
                result += " Your failed attempt weighs heavily on your spirit."
                
            # Update journey stats
            game.story.update_journey_stats("key_events", f"Failed border crossing attempt using {chosen_method['name']}")
        
        # Add trauma from the experience
        if hasattr(character, 'trauma'):
            trauma_increase = 5 if success else 10
            character.trauma = min(100, character.trauma + trauma_increase)
            
        # Apply the turn count
        game.turn_count += 1
            
        return result

class MoralEvent(Event):
    """An event that presents a moral choice to the character."""
    
    def __init__(self, name, description, choices, consequences, location_types=None, 
                 required_flags=None, excluded_flags=None, time_of_day=None, event_type="moral"):
        """
        Initialize a moral event.
        
        Args:
            name (str): Name of the event
            description (str): Description of the event
            choices (list): List of possible choices
            consequences (list): List of consequences for each choice
            location_types (list): Types of locations where this event can occur
            required_flags (dict): Flags that must be set for this event to occur
            excluded_flags (dict): Flags that prevent this event from occurring
            time_of_day (list): Times of day when this event can occur
            event_type (str): Type of moral event ("moral", "survival", "loyalty")
        """
        super().__init__(name, description, location_types, required_flags, excluded_flags, time_of_day)
        self.choices = choices
        self.consequences = consequences
        self.event_type = event_type
        
    def execute(self, game, character):
        """Execute the moral event.
        
        Args:
            game: The game instance
            character: The character experiencing the event
            
        Returns:
            str: Description of what happened
        """
        # Check if character meets flag requirements
        if not self.check_flags(character):
            return None
        
        # Print the event description FIRST
        print(f"\n{self.description}")

        # Present choices to the player
        choice_text = "\nChoices:\n"
        for i, choice in enumerate(self.choices):
            choice_text += f"{i+1}. {choice}\n"
        print(choice_text)

        # Get player input for the choice
        while True:
            try:
                choice_input = input(f"Enter choice (1-{len(self.choices)}): ")
                choice_index = int(choice_input) - 1
                if 0 <= choice_index < len(self.choices):
                    break
                else:
                    print("Invalid choice. Please enter a number from the list.")
            except ValueError:
                print("Invalid input. Please enter a number.")
                
        consequence = self.consequences[choice_index]
        
        # Apply the consequences based on character type and event type
        if hasattr(character, 'moral_compass'):
            # Border patrol moral compass adjustment
            moral_impact = consequence.get('moral_impact', 0)
            old_moral = character.moral_compass
            character.moral_compass = max(0, min(100, character.moral_compass + moral_impact))
            moral_change = character.moral_compass - old_moral
            
            # Also affects stress
            if hasattr(character, 'stress'):
                stress_impact = consequence.get('stress_impact', 0)
                old_stress = character.stress
                character.stress = max(0, min(100, character.stress + stress_impact))
                stress_change = character.stress - old_stress
                
        if hasattr(character, 'hope'):
            # Migrant hope adjustment
            hope_impact = consequence.get('hope_impact', 0)
            old_hope = character.hope
            character.hope = max(0, min(100, character.hope + hope_impact))
            hope_change = character.hope - old_hope
            
            # Traumatic moral choices also affect trauma
            if self.event_type in ["survival", "loyalty"] and hasattr(character, 'trauma'):
                trauma_impact = consequence.get('trauma_impact', max(0, -hope_impact // 2))
                old_trauma = character.trauma
                character.trauma = max(0, min(100, character.trauma + trauma_impact))
                trauma_change = character.trauma - old_trauma
                
        # Health impacts if specified
        if 'health_impact' in consequence and hasattr(character, 'health'):
            health_impact = consequence.get('health_impact', 0)
            old_health = character.health
            character.health = max(0, min(100, character.health + health_impact))
            health_change = character.health - old_health
            
        # Set any story flags from the consequence
        for flag, value in consequence.get('flags', {}).items():
            character.set_flag(flag, value)
            
        # Track moral choice in game stats if available
        if hasattr(game, 'story') and hasattr(game.story, 'update_journey_stats'):
            game.story.update_journey_stats("moral_choices_made")
            # Also track impact on others if specified
            if consequence.get('impact_others', False):
                game.story.update_journey_stats("lives_impacted")
            
        # Build result description with stat changes if significant
        result_description = consequence.get('description', '')
        stat_changes = []
        
        locals_dict = locals()
        for stat in ['hope_change', 'moral_change', 'stress_change', 'trauma_change', 'health_change']:
            if stat in locals_dict and locals_dict[stat] != 0:
                change = locals_dict[stat]
                stat_name = stat.split('_')[0]
                symbol = "+" if change > 0 else ""
                stat_changes.append(f"{stat_name}: {symbol}{change}")
                
        if stat_changes:
            result_description += f"\n[{', '.join(stat_changes)}]"
            
        return f"You chose: {self.choices[choice_index]}\n{result_description}"


class WeatherEvent(Event):
    """An event that changes the weather conditions."""
    
    def __init__(self, name, description, weather_type, effects, location_types=None, 
                 required_flags=None, excluded_flags=None, time_of_day=None, duration=3):
        """Initialize a weather event.
        
        Args:
            name (str): Name of the event
            description (str): Description of the event
            weather_type (str): Type of weather (rain, heat, cold, etc.)
            effects (dict): Effects on gameplay (water_drain, health_drain, etc.)
            location_types (list): Types of locations where this event can occur
            required_flags (dict): Flags that must be set for this event to occur
            excluded_flags (dict): Flags that prevent this event from occurring
            time_of_day (list): Times of day when this event can occur
            duration (int): Number of turns the weather lasts
        """
        super().__init__(name, description, location_types, required_flags, excluded_flags, time_of_day)
        self.weather_type = weather_type
        self.effects = effects
        self.duration = duration
        
    def execute(self, game, character):
        """Execute the weather event.
        
        Args:
            game: The game instance
            character: The character experiencing the event
            
        Returns:
            str: Description of what happened
        """
        # Check if character meets flag requirements
        if not self.check_flags(character):
            return None
            
        # Set the weather in the game if possible
        if hasattr(game, 'current_weather'):
            game.current_weather = {
                'name': self.name,
                'description': self.description,
                'effect': self.effects,
                'duration': self.duration
            }
            
        # Apply immediate effects if any
        impact_text = ""
        
        if 'immediate_water' in self.effects and hasattr(character, 'water'):
            water_change = self.effects['immediate_water']
            old_water = character.water
            character.water = max(0, min(100, character.water + water_change))
            water_diff = character.water - old_water
            
            if water_diff != 0:
                impact_text += f"\nWater: {'+' if water_diff > 0 else ''}{water_diff}"
                
        if 'immediate_health' in self.effects and hasattr(character, 'health'):
            health_change = self.effects['immediate_health']
            old_health = character.health
            character.health = max(0, min(100, character.health + health_change))
            health_diff = character.health - old_health
            
            if health_diff != 0:
                impact_text += f"\nHealth: {'+' if health_diff > 0 else ''}{health_diff}"
                
        # Apply environment changes to location if possible
        if game.current_location and hasattr(game.current_location, 'set_environment'):
            if 'visibility' in self.effects:
                game.current_location.set_environment('visibility', self.effects['visibility'])
            if 'terrain' in self.effects:
                game.current_location.set_environment('terrain', self.effects['terrain'])
            if 'temperature' in self.effects:
                game.current_location.set_environment('temperature', self.effects['temperature'])
                
        return f"{self.description}{impact_text}"


class TraumaEvent(Event):
    """An event that causes psychological trauma to the character."""
    
    def __init__(self, name, description, trauma_level, location_types=None, 
                 required_flags=None, excluded_flags=None, impact=None):
        """
        Initialize a trauma event.
        
        Args:
            name (str): Name of the event
            description (str): Description of the event
            trauma_level (int): Severity of trauma (1-10)
            location_types (list): Types of locations where this event can occur
            required_flags (dict): Flags that must be set for this event to occur
            excluded_flags (dict): Flags that prevent this event from occurring
            impact (dict): Additional impact on other stats
        """
        super().__init__(name, description, location_types, required_flags, excluded_flags)
        self.trauma_level = trauma_level
        self.impact = impact or {}
        
    def execute(self, game, character):
        """Execute the trauma event.
        
        Args:
            game: The game instance
            character: The character experiencing the event
            
        Returns:
            str: Description of what happened
        """
        # Check if character meets flag requirements
        if not self.check_flags(character):
            return None
            
        # Calculate final trauma based on character's current state
        final_trauma = self.trauma_level
        
        # Characters with high hope/moral compass resist trauma better
        if hasattr(character, 'hope') and character.hope > 70:
            final_trauma = max(1, final_trauma - 2)
        if hasattr(character, 'moral_compass') and character.moral_compass > 70:
            final_trauma = max(1, final_trauma - 1)
            
        # Apply trauma effects
        impact_text = ""
        
        # Primary impact on trauma stat if it exists
        if hasattr(character, 'trauma'):
            old_trauma = character.trauma
            trauma_increase = final_trauma * 5  # Scale 1-10 to 5-50
            character.trauma = min(100, character.trauma + trauma_increase)
            trauma_diff = character.trauma - old_trauma
            
            impact_text += f"\nTrauma: +{trauma_diff}"
            
        # Secondary impact on hope
        if hasattr(character, 'hope'):
            old_hope = character.hope
            hope_loss = final_trauma * 3  # Scale to 3-30
            character.hope = max(0, character.hope - hope_loss)
            hope_diff = character.hope - old_hope
            
            impact_text += f"\nHope: {hope_diff}"
            
        # Apply any custom impacts
        for stat, value in self.impact.items():
            if stat == 'health' and hasattr(character, 'health'):
                old_health = character.health
                character.health = max(0, min(100, character.health + value))
                health_diff = character.health - old_health
                
                if health_diff != 0:
                    impact_text += f"\nHealth: {'+' if health_diff > 0 else ''}{health_diff}"
                    
            elif stat == 'stress' and hasattr(character, 'stress'):
                old_stress = character.stress
                character.stress = max(0, min(100, character.stress + value))
                stress_diff = character.stress - old_stress
                
                if stress_diff != 0:
                    impact_text += f"\nStress: {'+' if stress_diff > 0 else ''}{stress_diff}"
        
        # Set trauma flag for story tracking
        character.set_flag(f"experienced_{self.name.lower().replace(' ', '_')}", True)
        
        # Track in game stats if available
        if hasattr(game, 'story') and hasattr(game.story, 'update_journey_stats'):
            game.story.update_journey_stats("trauma_experienced")
            
        # Provide a reflection on the trauma
        reflections = [
            "Some memories can never be fully processed.",
            "The border changes all who cross it, in ways both visible and invisible.",
            "Trauma accumulates like layers of sediment, eventually hardening into something unrecognizable.",
            "What the eyes see, the heart carries forever.",
            "To witness suffering is to bear a fragment of it within yourself."
        ]
        
        return f"{self.description}{impact_text}\n\n{random.choice(reflections)}"


# Define a comprehensive set of events for use in the game
def create_common_events():
    """Create a list of common events with rich narrative content.
    
    Returns:
        list: List of Event objects
    """
    from location import Desert, Border, Settlement  # Import here to avoid circular dependency

    events = []
    
    # ===== ENCOUNTER EVENTS =====
    
    # Migrant encounters
    migrant_family_encounter = EncounterEvent(
        "Migrant Family",
        "You encounter a family with small children attempting to cross the border.",
        "migrant",
        location_types=[Desert, Border],
        dialogue=[
            "Please, can you help us? Our children haven't had water since yesterday.",
            "Do you know how much further to the nearest town? The coyotes abandoned us.",
            "We've been walking for days. Is there a safer crossing point ahead?"
        ],
        choices={
            "Offer to share your supplies": {
                "description": "You share what you can spare. The gratitude in their eyes is evident.",
                "impacts": {"water": -10, "food": -10, "hope": 15},
                "flags": {"helped_migrants": True}
            },
            "Give them directions and continue alone": {
                "description": "You provide what information you have but explain you must continue alone.",
                "impacts": {"hope": -5},
                "flags": {"abandoned_migrants": True}
            },
            "Travel together for safety": {
                "description": "You decide to join forces. There's safety in numbers, but also more mouths to feed.",
                "impacts": {"hope": 10, "water": -15, "food": -15},
                "flags": {"traveling_with_others": True}
            }
        }
    )
    events.append(migrant_family_encounter)
    
    injured_migrant_encounter = EncounterEvent(
        "Injured Migrant",
        "You find a migrant with an injured leg, unable to walk properly.",
        "migrant",
        location_types=[Desert, Border],
        dialogue=[
            "I twisted my ankle yesterday. The group I was with... they left me behind.",
            "I can't go back. If you leave me here, I'll die in this desert.",
            "Please, I have family waiting for me. I can't give up now."
        ],
        choices={
            "Help them walk, slowing your progress": {
                "description": "You support their weight, but your pace is significantly reduced.",
                "impacts": {"health": -10, "hope": 10},
                "flags": {"helping_injured": True}
            },
            "Fashion a makeshift splint and leave": {
                "description": "You do what you can to treat the injury, but continue on your own path.",
                "impacts": {"hope": -10},
                "flags": {"abandoned_injured": True}
            },
            "Carry their belongings to lighten their load": {
                "description": "You take their backpack, allowing them to focus on walking. It's a heavy additional burden.",
                "impacts": {"health": -5, "hope": 5},
                "flags": {"carried_belongings": True}
            }
        }
    )
    events.append(injured_migrant_encounter)
    
    # Border Patrol encounters
    border_patrol_vehicle = EncounterEvent(
        "Border Patrol Vehicle",
        "A Border Patrol vehicle appears on the horizon, moving in your direction.",
        "patrol",
        location_types=[Desert, Border],
        dialogue=[
            "This is United States Border Patrol. Stay where you are.",
            "We've been tracking movement in this sector. Identify yourself.",
            "Multiple subjects detected. Remain in place for processing."
        ],
        choices={
            "Hide and hope they pass by": {
                "description": "You quickly find cover and stay absolutely still as the vehicle approaches.",
                "impacts": {"hope": -10, "health": -5},
                "flags": {"evaded_patrol": True}
            },
            "Run in the opposite direction": {
                "description": "You make a break for it, pushing your body to its limits.",
                "impacts": {"health": -15, "water": -15},
                "flags": {"fled_patrol": True}
            },
            "Surrender peacefully": {
                "description": "You stand with your hands visible, accepting that your journey may end here.",
                "impacts": {"hope": -20},
                "flags": {"surrendered_to_patrol": True}
            }
        }
    )
    events.append(border_patrol_vehicle)
    
    patrol_on_foot = EncounterEvent(
        "Border Patrol Agent",
        "You come face to face with a Border Patrol agent on foot patrol.",
        "patrol",
        location_types=[Desert, Border],
        dialogue=[
            "Stop right there. Let me see your hands.",
            "I need to see identification. Are you carrying any weapons?",
            "This area is under surveillance. How did you get here?"
        ],
        choices={
            "Try to explain your situation": {
                "description": "You attempt to communicate your circumstances, hoping for empathy.",
                "impacts": {"hope": -5},
                "flags": {"explained_to_patrol": True}
            },
            "Make a run for it": {
                "description": "You bolt suddenly, hoping to lose them in the rough terrain.",
                "impacts": {"health": -20, "water": -10},
                "flags": {"fled_patrol": True}
            },
            "Offer a bribe": {
                "description": "You discreetly suggest a financial arrangement, risking a more severe response.",
                "impacts": {"hope": -10},
                "flags": {"attempted_bribe": True}
            }
        }
    )
    events.append(patrol_on_foot)
    
    # Local encounters
    sympathetic_local = EncounterEvent(
        "Sympathetic Local",
        "You meet a local resident who seems to understand the plight of migrants.",
        "local",
        location_types=[Settlement],
        dialogue=[
            "My grandparents crossed this same desert. History repeats itself.",
            "I leave water caches out there when I can. It's not much, but it's something.",
            "The politics change, but the human suffering stays the same."
        ],
        choices={
            "Ask for assistance": {
                "description": "You cautiously explain your situation and ask for help.",
                "impacts": {"hope": 15, "water": 20, "food": 15},
                "flags": {"received_local_help": True}
            },
            "Ask for information about patrols": {
                "description": "You inquire about Border Patrol patterns and safe routes.",
                "impacts": {"hope": 10},
                "flags": {"received_patrol_info": True}
            },
            "Thank them and move on quickly": {
                "description": "You appreciate their kindness but minimize contact to reduce risk.",
                "impacts": {"hope": 5},
                "flags": {"minimized_contact": True}
            }
        }
    )
    events.append(sympathetic_local)
    
    hostile_locals = EncounterEvent(
        "Hostile Locals",
        "You encounter locals who clearly resent migrant presence in their community.",
        "local",
        location_types=[Settlement],
        dialogue=[
            "We don't want your kind here. Go back where you came from.",
            "I've already called Border Patrol. They'll be here soon.",
            "You people are ruining this town. We're watching you."
        ],
        choices={
            "Try to defuse the situation": {
                "description": "You speak calmly and respectfully, trying to reduce tensions.",
                "impacts": {"hope": -5},
                "flags": {"defused_tension": True}
            },
            "Leave the area immediately": {
                "description": "You turn and walk away quickly without engaging.",
                "impacts": {"hope": -10},
                "flags": {"fled_hostility": True}
            },
            "Stand your ground": {
                "description": "You refuse to be intimidated, asserting your human dignity.",
                "impacts": {"hope": -15, "health": -10},
                "flags": {"stood_ground": True}
            }
        }
    )
    events.append(hostile_locals)
    
    # Wildlife encounters
    snake_encounter = EncounterEvent(
        "Rattlesnake",
        "A rattlesnake appears suddenly in your path, coiled and rattling.",
        "wildlife",
        location_types=[Desert],
        time_of_day=["dawn", "dusk", "night"],
        choices={
            "Freeze and slowly back away": {
                "description": "You remain perfectly still, then carefully create distance between you and the snake.",
                "impacts": {"hope": -5},
                "flags": {"avoided_snake": True}
            },
            "Find a stick and try to move it": {
                "description": "You attempt to gently prod the snake away from your path.",
                "impacts": {"health": -15, "hope": -5},
                "flags": {"confronted_snake": True}
            },
            "Take a wide detour around it": {
                "description": "You choose a much longer route to avoid any risk from the snake.",
                "impacts": {"water": -15, "food": -10},
                "flags": {"took_detour": True}
            }
        }
    )
    events.append(snake_encounter)
    
    coyote_pack = EncounterEvent(
        "Coyote Pack",
        "As night falls, you hear the howls of coyotes drawing closer to your position.",
        "wildlife",
        location_types=[Desert],
        time_of_day=["dusk", "night"],
        choices={
            "Climb to higher ground": {
                "description": "You scramble up a rocky outcrop to get away from ground level.",
                "impacts": {"health": -5},
                "flags": {"climbed_for_safety": True}
            },
            "Light a small fire": {
                "description": "You gather what brush you can find and create a small fire to keep the animals at bay.",
                "impacts": {"hope": 5, "health": -5},
                "flags": {"used_fire": True}
            },
            "Make loud noises to scare them off": {
                "description": "You shout and bang objects together, hoping to intimidate the pack.",
                "impacts": {"hope": -5},
                "flags": {"scared_wildlife": True}
            }
        }
    )
    events.append(coyote_pack)
    
    # ===== RESOURCE EVENTS =====
    
    water_cache = ResourceEvent(
        "Water Cache",
        "You discover jugs of water left by humanitarian aid workers.",
        "water",
        30,
        location_types=[Desert],
        difficulty=20
    )
    events.append(water_cache)
    
    food_cache = ResourceEvent(
        "Food Stash",
        "You find a small stash of non-perishable food items hidden under rocks.",
        "food",
        25,
        location_types=[Desert, Border],
        difficulty=30
    )
    events.append(food_cache)
    
    lost_supplies = ResourceEvent(
        "Lost Supplies",
        "Your backpack tears open, spilling some of your vital supplies.",
        "item",
        -1,
        location_types=[Desert, Border],
        difficulty=40
    )
    events.append(lost_supplies)
    
    found_money = ResourceEvent(
        "Found Money",
        "You discover a weathered wallet containing some cash.",
        "money",
        50,
        location_types=[Settlement, Border],
        difficulty=25
    )
    events.append(found_money)
    
    dehydration = ResourceEvent(
        "Severe Dehydration",
        "The relentless sun and dry air rapidly drain your water reserves.",
        "water",
        -25,
        location_types=[Desert],
        time_of_day=["day"]
    )
    events.append(dehydration)
    
    border_wall_injury = ResourceEvent(
        "Fence Injury",
        "While climbing over a section of border wall, you slip and fall.",
        "health",
        -20,
        location_types=[Border],
        difficulty=50
    )
    events.append(border_wall_injury)
    
    # ===== MORAL EVENTS =====
    
    abandoned_child = MoralEvent(
        "Abandoned Child",
        "You find a young child alone, crying, apparently separated from their group.",
        [
            "Take the child with you, accepting the additional burden",
            "Leave them for Border Patrol to find, as they'll have better resources",
            "Search the area for the child's family, delaying your journey"
        ],
        [
            {"description": "The child clings to you, both a responsibility and a reminder of why this journey matters.", 
             "hope_impact": -5, "moral_impact": 15, "health_impact": -10, "flags": {"has_child": True}},
            {"description": "You cannot risk the extra burden. The image of the child's tear-streaked face haunts you as you walk away.", 
             "hope_impact": -20, "moral_impact": -20, "flags": {"abandoned_child": True}},
            {"description": "You spend precious time searching. Eventually, you find the parents, their gratitude overwhelming.", 
             "hope_impact": 15, "moral_impact": 10, "water_impact": -15, "food_impact": -15, "flags": {"reunited_family": True}}
        ],
        location_types=[Border, Desert],
        event_type="moral"
    )
    events.append(abandoned_child)
    
    dying_migrant = MoralEvent(
        "Dying Migrant",
        "You encounter a migrant clearly in their final hours, suffering from severe dehydration and heat stroke.",
        [
            "Stay with them so they don't die alone, using precious time and resources",
            "Mercy kill them to end their suffering quickly",
            "Say a brief prayer or kind word and continue your journey"
        ],
        [
            {"description": "You sit beside them as their breathing grows shallow. They clutch your hand and whisper thanks.", 
             "hope_impact": -15, "moral_impact": 20, "water_impact": -20, "food_impact": -20, 
             "flags": {"stayed_with_dying": True}, "trauma_impact": 20},
            {"description": "You make the hardest choice possible, ending their suffering quickly and humanely.", 
             "hope_impact": -25, "moral_impact": -10, "flags": {"performed_mercy_kill": True}, "trauma_impact": 30},
            {"description": "You offer what comfort you can with words, knowing you must prioritize your own survival.", 
             "hope_impact": -20, "moral_impact": -5, "flags": {"left_dying_behind": True}, "trauma_impact": 15}
        ],
        location_types=[Desert],
        event_type="survival"
    )
    events.append(dying_migrant)
    
    border_patrol_dilemma = MoralEvent(
        "Border Patrol Dilemma",
        "As a Border Patrol agent, you encounter a young mother and child crossing illegally. You know deportation would return them to extreme danger.",
        [
            "Follow protocol and process them for deportation",
            "Look the other way this once, against regulations",
            "Process them but flag their case for asylum consideration"
        ],
        [
            {"description": "You follow procedure. The system exists for a reason, however imperfect.", 
             "moral_impact": -15, "stress_impact": 20, "flags": {"followed_protocol": True}},
            {"description": "You pretend you didn't see them. A small mercy in a merciless system.", 
             "moral_impact": 10, "stress_impact": 25, "flags": {"broke_rules": True}},
            {"description": "You process them but add notes to their file emphasizing asylum eligibility.", 
             "moral_impact": 5, "stress_impact": 10, "flags": {"bent_rules": True}}
        ],
        location_types=[Border],
        required_flags={"is_border_patrol": True},
        event_type="loyalty"
    )
    events.append(border_patrol_dilemma)
    
    # ===== WEATHER EVENTS =====
    
    dust_storm = WeatherEvent(
        "Dust Storm",
        "A wall of dust approaches rapidly, visibility dropping to near zero.",
        "dust_storm",
        {"visibility": 0.2, "immediate_health": -10, "water_drain": 1.5},
        location_types=[Desert],
        duration=2
    )
    events.append(dust_storm)
    
    flash_flood = WeatherEvent(
        "Flash Flood",
        "Sudden rainfall in the distance sends a wall of water rushing through the dry wash you're following.",
        "flash_flood",
        {"terrain": "flooded", "immediate_health": -15, "immediate_water": 15},
        location_types=[Desert],
        duration=1
    )
    events.append(flash_flood)
    
    extreme_heat = WeatherEvent(
        "Extreme Heat Wave",
        "The temperature soars to dangerous levels, the air shimmering with heat.",
        "heat_wave",
        {"temperature": "extreme", "immediate_water": -20, "water_drain": 2.0},
        location_types=[Desert, Border],
        time_of_day=["day"],
        duration=3
    )
    events.append(extreme_heat)
    
    freezing_night = WeatherEvent(
        "Freezing Desert Night",
        "The temperature plummets after sunset, the desert cold penetrating to the bone.",
        "freezing",
        {"temperature": "freezing", "immediate_health": -10},
        location_types=[Desert],
        time_of_day=["night"],
        duration=1
    )
    events.append(freezing_night)
    
    # ===== TRAUMA EVENTS =====
    
    discovered_remains = TraumaEvent(
        "Human Remains",
        "You discover human remains partially buried in the sand - a grim reminder of the journey's dangers.",
        8,
        location_types=[Desert],
        impact={"health": -5}
    )
    events.append(discovered_remains)
    
    witnessed_violence = TraumaEvent(
        "Cartel Violence",
        "You witness cartel members brutally punishing migrants who couldn't pay their crossing fees.",
        9,
        location_types=[Border],
        impact={"health": -10, "stress": 25}
    )
    events.append(witnessed_violence)
    
    separation_trauma = TraumaEvent(
        "Family Separation",
        "You witness Border Patrol separating a family during processing, the children's cries echoing across the facility.",
        7,
        location_types=[Border, Settlement],
        impact={"stress": 20}
    )
    events.append(separation_trauma)
    
    desert_hallucination = TraumaEvent(
        "Desert Hallucination",
        "Dehydration and heat cause you to experience vivid hallucinations that blur the line between reality and delusion.",
        6,
        location_types=[Desert],
        required_flags={"water_critical": True},
        impact={"health": -15}
    )
    events.append(desert_hallucination)
    
    return events