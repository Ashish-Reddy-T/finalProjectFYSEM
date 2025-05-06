"""
Story module for 'The Line: A Border Journey'

This module handles the narrative elements, player interactions,
and storytelling aspects of the game, inspired by Francisco Cantú's
'The Line Becomes a River'.
"""

import time
import os
import sys
import random
from datetime import datetime


class Story:
    """Manages the narrative elements of the game."""
    
    def __init__(self):
        """Initialize the story."""
        # Core themes from Cantú's book
        self.themes = [
            "humanity across borders",          
            "moral complexity of enforcement",
            "personal cost of migration",
            "impact of policy on individual lives",
            "trauma and healing",
            "identity and belonging",
            "duty versus compassion",
            "memory and forgetting"
        ]
        
        # Philosophical quotes about borders and migration
        self.quotes = [
            "The border is a place characterized by flux and tension, a landscape of convergence where the realities of two nations meet.",
            "We are trapped in a system that has no regard for humanity.",
            "There are days when I feel I am becoming good at what I do. And then I wonder, what does it mean to be good at this?",
            "The border divides the past from the future, and we stand always in its present shadow.",
            "Each body recovered from the desert has a story, a dream that ended too soon.",
            "The border makes ghosts of us all - those who cross, those who guard, those who never return.",
            "In the end, we're all just people trying to do what we believe is right.",
            "Some wounds never heal; they just become part of who we are.",
            "The line on the map means nothing to the birds that fly above it, or the plants that grow across it, or the animals that wander over it.",
            "Policy becomes human when it meets flesh and bone in the borderlands.",
            "Dreams are the true currency of the border economy, more precious than dollars or pesos.",
            "The desert has no allegiance to either side of the line; it claims victims without discrimination."
        ]
        
        # Enhanced moral choices with deeper ethical dilemmas
        self.moral_choices = {
            # Migrant moral dilemmas
            "migrant": [
                {
                    "description": "A mother with two young children asks you to help her cross. She doesn't have enough water for all of you.",
                    "choices": [
                        "Share your limited water, putting yourself at greater risk",
                        "Advise her to wait for better prepared smugglers",
                        "Take only one of her children, promising to send help back"
                    ],
                    "consequences": [
                        {"hope_impact": 10, "health_impact": -15, "flag": "helped_family", "description": "You share your water. The gratitude in her eyes gives you strength, but the physical toll is significant."},
                        {"hope_impact": -10, "flag": "abandoned_family", "description": "You continue alone. Their faces haunt you as you walk away."},
                        {"hope_impact": -5, "flag": "split_family", "description": "You take the older child. The mother's tears burn into your memory, but you promise to send help when you can."}
                    ]
                },
                {
                    "description": "You encounter an injured man who can't walk. He begs you not to leave him to die in the desert.",
                    "choices": [
                        "Stay with him, delaying your journey significantly",
                        "Try to carry him, slowing your pace dramatically",
                        "Mark his location and promise to send help when you reach civilization"
                    ],
                    "consequences": [
                        {"hope_impact": 5, "health_impact": -5, "flag": "delayed_journey", "description": "You stay with the stranger. Hours pass as you share stories of the homes you both left behind."},
                        {"hope_impact": -5, "health_impact": -20, "flag": "helped_injured", "description": "The weight on your shoulders is immense, but so is the weight that would have been on your conscience."},
                        {"hope_impact": -15, "flag": "abandoned_injured", "description": "You mark his location and continue. His voice calling after you fades with distance, but not from memory."}
                    ]
                },
                {
                    "description": "A coyote offers to guide you through cartel territory - a shortcut that would save days but expose you to dangerous people.",
                    "choices": [
                        "Take the risky shortcut, trusting the coyote",
                        "Refuse and take the longer, safer route",
                        "Negotiate for more security guarantees before deciding"
                    ],
                    "consequences": [
                        {"hope_impact": -10, "health_impact": -10, "flag": "took_shortcut", "description": "The shortcut saves time but exposes you to dangers. You witness things that cannot be unseen."},
                        {"hope_impact": 5, "health_impact": -15, "flag": "took_long_route", "description": "The longer route tests your endurance but keeps you away from the cartel's eyes."},
                        {"hope_impact": 0, "health_impact": -5, "flag": "negotiated_with_coyote", "description": "Your caution serves you well. The coyote respects your questions, offering more details about the journey."}
                    ]
                },
                {
                    "description": "You find an abandoned backpack containing water, food, and a wallet with $200 and family photos.",
                    "choices": [
                        "Take only the water and food you need",
                        "Take everything - you need every advantage",
                        "Leave it undisturbed - its owner might return"
                    ],
                    "consequences": [
                        {"hope_impact": 5, "health_impact": 10, "flag": "took_necessities", "description": "You take only what you need to survive. The moral compromise weighs less than what you might have taken."},
                        {"hope_impact": -5, "health_impact": 15, "flag": "took_everything", "description": "The resources will help you survive, but the face in the family photo haunts your dreams."},
                        {"hope_impact": 10, "health_impact": -5, "flag": "left_backpack", "description": "You continue with empty hands but a full heart, hoping whoever lost these things finds them again."}
                    ]
                }
            ],
            
            # Border Patrol moral dilemmas
            "patrol": [
                {
                    "description": "You discover a group of migrants including children suffering from severe dehydration. Calling for medical transport will mean processing and likely deportation.",
                    "choices": [
                        "Follow protocol: call for medical assistance and process them",
                        "Give them water and medical aid, then let them go",
                        "Call medical assistance but 'lose' their paperwork in the system"
                    ],
                    "consequences": [
                        {"moral_impact": 0, "stress_impact": 10, "flag": "followed_protocol", "description": "You follow procedure. The children receive medical care, but their terrified eyes follow you as they're processed."},
                        {"moral_impact": 15, "stress_impact": 15, "flag": "broke_rules_for_compassion", "description": "You choose humanity over protocol. They disappear into the desert, their gratitude the only witness to your choice."},
                        {"moral_impact": 5, "stress_impact": 20, "flag": "bent_rules", "description": "You navigate the gray areas of the system. The paperwork is conveniently delayed, giving them time to recover before decisions must be made."}
                    ]
                },
                {
                    "description": "You witness a fellow agent using excessive force on a cooperative migrant. Your supervisor seems unconcerned when others have reported similar incidents.",
                    "choices": [
                        "Report the incident through official channels despite potential backlash",
                        "Confront the agent privately about their behavior",
                        "Stay silent to avoid making enemies within the department"
                    ],
                    "consequences": [
                        {"moral_impact": 20, "stress_impact": 25, "flag": "reported_misconduct", "description": "You file the report, knowing it may cost you professionally. Some colleagues avoid you in the break room."},
                        {"moral_impact": 10, "stress_impact": 15, "flag": "confronted_colleague", "description": "The conversation is tense, but you speak your truth. The relationship is strained, but perhaps a seed was planted."},
                        {"moral_impact": -15, "stress_impact": 5, "flag": "ignored_misconduct", "description": "You say nothing. Life continues as normal, except for the moments you catch your reflection and look away."}
                    ]
                },
                {
                    "description": "You find a severely injured migrant who crossed recently. He has information about a dangerous smuggling operation, but needs immediate medical care.",
                    "choices": [
                        "Focus on getting his smuggling information before seeking medical help",
                        "Prioritize medical care, potentially losing valuable intelligence",
                        "Radio for both medical assistance and backup simultaneously"
                    ],
                    "consequences": [
                        {"moral_impact": -20, "stress_impact": 15, "flag": "prioritized_intelligence", "description": "You get the information, but his condition worsens. The intelligence could save lives, but at what cost?"},
                        {"moral_impact": 15, "stress_impact": 5, "flag": "prioritized_care", "description": "You focus on saving his life. The smugglers may continue operating, but you sleep without this particular weight on your conscience."},
                        {"moral_impact": 5, "stress_impact": 10, "flag": "balanced_approach", "description": "You attempt to balance duty and humanity. The juggling act is imperfect, but you try your best in an impossible situation."}
                    ]
                },
                {
                    "description": "You're ordered to separate a young child from their parents due to documentation issues, following a new policy you personally disagree with.",
                    "choices": [
                        "Follow orders despite your moral objections",
                        "Refuse the order and face potential disciplinary action",
                        "Find a procedural loophole to keep the family together"
                    ],
                    "consequences": [
                        {"moral_impact": -25, "stress_impact": 30, "flag": "followed_immoral_orders", "description": "You follow orders. The child's screams as they're pulled from their mother's arms will echo in your mind for years."},
                        {"moral_impact": 25, "stress_impact": 20, "flag": "refused_orders", "description": "You stand your ground. Your supervisor is furious, but the family remains together - for now."},
                        {"moral_impact": 10, "stress_impact": 15, "flag": "found_loophole", "description": "You find a technicality in the processing forms. It won't work forever, but it buys the family time together."}
                    ]
                }
            ]
        }

        # Traumatic experiences that shape character development
        self.trauma_events = [
            {
                "description": "You discover human remains in the desert - a grim reminder of the journey's dangers.",
                "impact": {"hope": -15, "trauma": 20, "health": -5},
                "reflection": "Death becomes real here. Not an abstract concept, but sun-bleached bones and faded dreams."
            },
            {
                "description": "You witness cartel violence against migrants who couldn't pay their fees.",
                "impact": {"hope": -20, "trauma": 25, "health": -10},
                "reflection": "The border creates its own economy of desperation, where human life has a price tag."
            },
            {
                "description": "A child in your group falls ill with a high fever, crying through the night.",
                "impact": {"hope": -10, "trauma": 15, "health": -5},
                "reflection": "Innocence suffers most at the border. Children bear burdens they cannot understand."
            },
            {
                "description": "You suffer hallucinations from heat exposure, seeing water where there is only sand.",
                "impact": {"hope": -15, "trauma": 15, "health": -15},
                "reflection": "The desert plays cruel tricks on the mind, offering mirages of salvation."
            },
            {
                "description": "You're separated from your traveling companions during a patrol encounter.",
                "impact": {"hope": -15, "trauma": 15, "health": -5},
                "reflection": "In an instant, everything can change. People disappear into the machinery of enforcement."
            },
            {
                "description": "You help rescue a migrant trapped in a drainage tunnel during flash flooding.",
                "impact": {"hope": 5, "trauma": 15, "health": -10},
                "reflection": "Even in moments of crisis, humanity can bridge the divide between roles and rules."
            },
            {
                "description": "You encounter evidence of sexual assault at a known migrant rest area.",
                "impact": {"hope": -20, "trauma": 25, "health": -5},
                "reflection": "Vulnerability is exploited at every turn. The border strips away protections most take for granted."
            },
            {
                "description": "A migrant dies of dehydration despite your attempts to help them.",
                "impact": {"hope": -25, "trauma": 30, "health": -15},
                "reflection": "Some failures leave permanent marks on the soul. Some debts can never be repaid."
            }
        ]

        # Environmental events reflecting the harsh reality of the border region
        self.random_events = {
            "migrant": [
                {
                    "description": "A helicopter spotlight sweeps across your position, forcing you to hide.",
                    "impact": {"hope": -5, "health": -5},
                    "flavor": "The mechanical eye in the sky searches the desert. You press your body against the earth, becoming one with the shadow."
                },
                {
                    "description": "You find an abandoned backpack with supplies.",
                    "impact": {"hope": 10, "health": 10},
                    "flavor": "Someone else's journey ended here. Their loss becomes your salvation - a common tragedy of the border."
                },
                {
                    "description": "Distant gunshots echo through the canyon, raising everyone's anxiety.",
                    "impact": {"hope": -10, "health": 0},
                    "flavor": "The sound bounces between rock walls, impossible to locate. You freeze, calculating risks and routes."
                },
                {
                    "description": "You discover a hidden water cache left by humanitarian aid workers.",
                    "impact": {"hope": 15, "health": 15},
                    "flavor": "Plastic jugs of water, placed with intention. Small acts of compassion flourish even here, where policy fails."
                },
                {
                    "description": "A dust storm approaches from the horizon, forcing you to seek shelter.",
                    "impact": {"hope": -5, "health": -10},
                    "flavor": "The wall of dust devours the landscape. You cover your face and huddle against a rock, waiting for the world to return."
                },
                {
                    "description": "You spot border patrol vehicles in the distance, patrolling the area.",
                    "impact": {"hope": -10, "health": -5},
                    "flavor": "Green and white SUVs move along the ridge. You drop to the ground, counting seconds between their passes, mapping their pattern."
                },
                {
                    "description": "You find recent footprints heading north, suggesting others passed recently.",
                    "impact": {"hope": 5, "health": 0},
                    "flavor": "The footprints tell a story - a group, moving hurriedly but determined. You are not alone in this journey."
                },
                {
                    "description": "The howl of coyotes fills the night, their cries haunting and familiar.",
                    "impact": {"hope": 0, "health": -5},
                    "flavor": "Their voices rise like spirits from the darkness. Predators calling to each other, claiming territory."
                },
                {
                    "description": "Morning reveals beautiful desert flowers blooming after rare rainfall.",
                    "impact": {"hope": 10, "health": 5},
                    "flavor": "Impossibly vibrant colors burst from the harsh landscape. Life finds a way, even here."
                },
                {
                    "description": "You encounter an elderly indigenous man who offers silent guidance with a nod toward a hidden path.",
                    "impact": {"hope": 15, "health": 0},
                    "flavor": "No words pass between you. His eyes hold knowledge of this land that predates all borders."
                }
            ],
            "patrol": [
                {
                    "description": "You receive reports of cartel activity nearby, increasing tension in your unit.",
                    "impact": {"moral": 0, "stress": 15},
                    "flavor": "The radio crackles with coded warnings. Cartel scouts watching patrol patterns, waiting for opportunities."
                },
                {
                    "description": "Your radio crackles with reports of multiple crossings, stretching resources thin.",
                    "impact": {"moral": -5, "stress": 10},
                    "flavor": "Coordinates flood the channel. Too many locations, too few agents. The system strains under pressure."
                },
                {
                    "description": "You find evidence of human trafficking - discarded women's clothing and restraints.",
                    "impact": {"moral": 10, "stress": 20},
                    "flavor": "The items tell a story you don't want to read. The border economy trades in human cargo."
                },
                {
                    "description": "A migrant family surrenders to your unit, the children crying from exhaustion.",
                    "impact": {"moral": 5, "stress": 15},
                    "flavor": "They approach with hands raised. The father speaks clearly: 'Asylum. Please. We seek asylum.'"
                },
                {
                    "description": "You discover a sophisticated tunnel entrance hidden beneath an abandoned structure.",
                    "impact": {"moral": 0, "stress": 5},
                    "flavor": "The entrance is expertly concealed. Millions of dollars of engineering to bypass a multi-billion dollar wall."
                },
                {
                    "description": "Your thermal imaging detects movement ahead - a group moving through the night.",
                    "impact": {"moral": 0, "stress": 10},
                    "flavor": "Ghost-like heat signatures move across your screen. Nameless, faceless - until they aren't."
                },
                {
                    "description": "You find an abandoned vehicle with supplies and multiple fake IDs.",
                    "impact": {"moral": -5, "stress": 5},
                    "flavor": "The SUV is still warm, recently abandoned. The documents show different faces with the same eyes."
                },
                {
                    "description": "A fellow agent requests immediate backup after encountering armed smugglers.",
                    "impact": {"moral": 5, "stress": 25},
                    "flavor": "Their voice is controlled but tight with tension. Protocol and training take over as you respond."
                },
                {
                    "description": "Local ranchers report water tanks damaged by desperate migrants.",
                    "impact": {"moral": -5, "stress": 10},
                    "flavor": "The rancher's face is sunburned and angry. 'Those tanks were for my cattle. Now everything's dying.'"
                },
                {
                    "description": "You find a child's teddy bear dropped in the desert, a silent testimony to invisible journeys.",
                    "impact": {"moral": 10, "stress": 15},
                    "flavor": "Small, worn, carried from one life toward another. You place it in your vehicle. What else can you do?"
                }
            ]
        }

        # Journey statistics tracking for narrative development
        self.journey_stats = {
            "distance_traveled": 0,
            "lives_impacted": 0,
            "moral_choices_made": 0,
            "trauma_experienced": 0,
            "key_events": [],
            "water_consumed": 0,
            "health_lost": 0,
            "hope_changes": 0
        }

        # Weather conditions that affect gameplay experience
        self.weather_conditions = [
            {"name": "Scorching Heat", "effect": {"water_drain": 2.0, "health_drain": 1.5}, 
             "description": "The sun beats down mercilessly, creating heat mirages on the horizon."},
            {"name": "Dust Storm", "effect": {"visibility": 0.3, "health_drain": 1.3}, 
             "description": "Fine particles fill the air, reducing visibility and making each breath a struggle."},
            {"name": "Desert Night", "effect": {"temperature": "cold", "visibility": 0.5}, 
             "description": "Temperature drops dramatically after sunset, the cold seeping into your bones."},
            {"name": "Monsoon Rain", "effect": {"water_drain": 0.5, "terrain": "muddy"}, 
             "description": "Sudden downpours transform dry washes into raging torrents within minutes."},
            {"name": "Clear Skies", "effect": {"visibility": 1.0, "detection_risk": 1.2}, 
             "description": "Perfect visibility makes navigation easier, but also increases the risk of being spotted."}
        ]
        
        # The current weather condition (can change during gameplay)
        self.current_weather = random.choice(self.weather_conditions)
        
    def clear_screen(self):
        """Clear the terminal screen for better presentation."""
        os.system('cls' if os.name == 'nt' else "clear")
    
    def print_slow(self, text, delay=0.001):
        """Print text with a typing effect for dramatic presentation.
        
        Args:
            text (str): Text to print
            delay (float): Delay between characters in seconds
        """
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()
    
    def display_intro(self, starting_location):
        """Display the game introduction with context from Cantú's book.
        
        Args:
            starting_location (str): The name of the player's starting location
        """
        self.clear_screen()
        
        intro_text = """
        ╔════════════════════════════════════════════════════════════╗
        ║             THE LINE: A BORDER JOURNEY                     ║
        ╚════════════════════════════════════════════════════════════╝
        
        The border is not just a line on a map. It's a place where lives intersect,
        where dreams and desperation collide with policy and duty.
        
        In this narrative experience, you will walk in the footsteps of those who
        cross the border and those who patrol it. Your choices will shape your
        journey and reveal the complex human stories behind headlines.
        
        As Francisco Cantú writes in 'The Line Becomes a River', the border leaves
        its mark on all who encounter it - those who cross it, those who enforce it,
        and those who live in its shadow.
        
        Every choice you make will test your humanity, your resolve, and your moral compass.
        There are no easy answers here, only human stories unfolding in the borderlands.
        """
        
        self.print_slow(intro_text)
        print(f"\nYour journey begins in {starting_location}.")
        input("\nPress Enter to continue ... ")
        self.clear_screen()
    
    def get_player_info(self):
        """Get the player's character information with more contextual depth.
        
        Returns:
            tuple: (name, character_type, extra_info)
        """
        self.clear_screen()
        print("╔════════════════════════════════════════════════════════════╗")
        print("║                   CHARACTER CREATION                       ║")
        print("╚════════════════════════════════════════════════════════════╝\n")
        
        # Choose character type with contextual information
        print("Choose your role in this border narrative:")
        print("\n1. Migrant")
        print("   You seek a better life across the border, driven by necessity or hope.")
        print("   You'll face the physical dangers of the journey and the constant fear of capture.")
        print("   Your resources are limited, but your determination is strong.")
        print("\n2. Border Patrol")
        print("   You enforce the boundary between nations, balancing duty and compassion.")
        print("   You'll confront the moral complexities of a system that processes people.")
        print("   Your authority brings responsibility and difficult choices.")
        
        while True:
            choice = input("\nEnter your choice (1 or 2): ")
            if choice in ["1", "2"]:
                break
            print("Invalid choice. Please enter 1 or 2.")
        
        character_type = "migrant" if choice == "1" else "patrol"
        
        # Get character name
        name = input("\nEnter your character's name: ")
        while not name.strip():
            name = input("Name cannot be empty. Please enter a name: ")
        
        # Get additional info based on character type with deeper narrative context
        if character_type == "migrant":
            # For migrant characters, explore origin and motivation
            print("\nWhere are you from? Your origins will shape your journey.")
            origin_options = ["Central Mexico", "Southern Mexico", "Guatemala", "El Salvador", "Honduras", "Other"]
            for i, option in enumerate(origin_options, 1):
                print(f"{i}. {option}")
                
            origin_choice = 0
            while origin_choice < 1 or origin_choice > len(origin_options):
                try:
                    origin_choice = int(input("Choose your origin (1-6): "))
                except ValueError:
                    pass
                    
            origin = origin_options[origin_choice-1]
            if origin == "Other":
                origin = input("Specify your origin: ")
            
            print("\nWhat drives you to risk everything for this journey?")
            motivation_options = [
                "Economic opportunity - poverty and lack of work pushed you north",
                "Escaping violence - threats from gangs or cartels made staying impossible",
                "Family reunification - loved ones already crossed and wait for you",
                "Political persecution - your views or activism made you a target",
                "Natural disaster - your home was destroyed, leaving nothing to return to",
                "Other"
            ]
            
            for i, option in enumerate(motivation_options, 1):
                print(f"{i}. {option}")
                
            motivation_choice = 0
            while motivation_choice < 1 or motivation_choice > len(motivation_options):
                try:
                    motivation_choice = int(input("Choose your primary motivation (1-6): "))
                except ValueError:
                    pass
                    
            motivation = motivation_options[motivation_choice-1]
            if motivation == "Other":
                motivation = input("Specify your motivation: ")
            
            # Ask about family ties for deeper character development
            has_family = input("\nDo you have family members depending on your success? (y/n): ").lower().startswith('y')
            family_info = {}
            
            if has_family:
                family_members = []
                print("\nWho waits for you on the other side? (Add up to 3 family members)")
                for i in range(3):
                    if i > 0 and input("Add another family member? (y/n): ").lower() != 'y':
                        break
                    name = input("Name: ")
                    relation = input("Relationship to you: ")
                    family_members.append({"name": name, "relationship": relation})
                family_info["members"] = family_members
            
            return name, character_type, {"origin": origin, "motivation": motivation, "family_info": family_info}
        else:
            # For Border Patrol characters, explore background and ethics
            print("\nHow many years have you served in Border Patrol?")
            years_options = ["Less than 1 (Rookie)", "1-3 (Junior Agent)", "4-7 (Experienced)", "8-12 (Veteran)", "13+ (Senior Agent)"]
            for i, option in enumerate(years_options, 1):
                print(f"{i}. {option}")
                
            years_choice = 0
            while years_choice < 1 or years_choice > len(years_options):
                try:
                    years_choice = int(input("Choose your experience level (1-5): "))
                except ValueError:
                    pass
                    
            years_text = years_options[years_choice-1]
            years = 1 if years_choice == 1 else 2 if years_choice == 2 else 5 if years_choice == 3 else 10 if years_choice == 4 else 15
            
            print("\nWhat led you to join the Border Patrol?")
            background_options = [
                "Family tradition - following in the footsteps of relatives",
                "Sense of duty - believing in the importance of border security",
                "Career opportunity - stable government job with benefits",
                "Personal experience - affected by border issues growing up",
                "Seeking purpose - wanting to make a difference in a complex situation",
                "Other"
            ]
            
            for i, option in enumerate(background_options, 1):
                print(f"{i}. {option}")
                
            background_choice = 0
            while background_choice < 1 or background_choice > len(background_options):
                try:
                    background_choice = int(input("Choose your background (1-6): "))
                except ValueError:
                    pass
                    
            background = background_options[background_choice-1]
            if background == "Other":
                background = input("Specify your background: ")
            
            # Ask about ethical stance for deeper character development
            print("\nHow do you view your role at the border?")
            ethics_options = [
                "By-the-book enforcer - rules exist for a reason",
                "Compassionate guardian - balancing humanity and duty",
                "Conflicted servant - struggling with the system's contradictions",
                "Reformer from within - working to change policies you disagree with",
                "Pragmatic professional - focusing on doing the job effectively"
            ]
            
            for i, option in enumerate(ethics_options, 1):
                print(f"{i}. {option}")
                
            ethics_choice = 0
            while ethics_choice < 1 or ethics_choice > len(ethics_options):
                try:
                    ethics_choice = int(input("Choose your ethical stance (1-5): "))
                except ValueError:
                    pass
                    
            ethics = ethics_options[ethics_choice-1]
            
            # Adjust starting moral compass based on ethics choice
            moral_compass = 40 if ethics_choice == 1 else 60 if ethics_choice == 2 else 50 if ethics_choice == 3 else 70 if ethics_choice == 4 else 45
            
            return name, character_type, {
                "years_of_service": years, 
                "background": background, 
                "ethics": ethics,
                "starting_moral_compass": moral_compass
            }
    
    def display_ending(self, ending_type, player):
        """Display the game ending with deeper emotional resonance.
        
        Args:
            ending_type (str): Type of ending ('success', 'detained', 'death', 'timeout')
            player: The player character object
        """
        self.clear_screen()
        print("\t\t╔════════════════════════════════════════════════════════════╗")
        print("\t\t║                       EPILOGUE                             ║")
        print("\t\t╚════════════════════════════════════════════════════════════╝\n")
        
        # Get player-specific context for the epilogue
        player_type = "migrant" if hasattr(player, 'origin') else "patrol"
        player_name = player.name
        
        if ending_type == "success" and player_type == "migrant":
            epilogue = f"""
            {player_name} has reached Tucson, but the journey is far from over.
            
            Like many migrants who cross the border, a new struggle begins - finding work,
            avoiding detection, building a life in the shadows. Success is relative in a
            system designed to marginalize those without documentation.
            
            The physical crossing was just the beginning. The psychological border will
            remain for years - the division between new life and old, between
            belonging and existing on the periphery.
            
            As Cantú writes, "The border divides the past from the future," and {player_name}
            now lives in that divide, carrying memories of home while forging an uncertain future.
            """
        
        elif ending_type == "success" and player_type == "patrol":
            epilogue = f"""
            {player_name} completes another patrol rotation, returning to the station with
            a complicated mix of pride and doubt.
            
            The border remains as it always has been - a place where policy meets humanity,
            where abstract debates in distant capitals become flesh and blood realities.
            
            Today's successes will be forgotten in tomorrow's challenges. The desert
            will continue to claim lives, migrants will continue to cross, and agents
            like {player_name} will continue to navigate the impossible space between
            law and compassion.
            
            As Cantú observed during his time as an agent, border work changes those
            who undertake it, often in ways they never anticipated.
            """
        
        elif ending_type == "detained":
            epilogue = f"""
            In detention, {player_name} becomes one of thousands processed through
            America's immigration system - a complex bureaucracy of holding cells,
            paperwork, and uncertain waiting.
            
            Days blend into weeks as {player_name} is moved between facilities,
            each identical in their institutional sterility. Dreams of a new life
            are replaced by the immediate concern of navigating a system designed
            to process rather than understand.
            
            Whether deportation or asylum awaits depends on factors largely outside
            {player_name}'s control - the specific judge assigned, the capacity of
            detention facilities, the political climate, the availability of legal aid.
            
            As Cantú witnessed firsthand, the individual humanity of migrants is often
            lost in the machinery of enforcement and policy, where people become cases
            and statistics.
            """
        
        elif ending_type == "death":
            epilogue = f"""
            {player_name}'s journey ends in the borderlands, as it does for hundreds
            of migrants each year. The Sonoran Desert has claimed another life.
            
            Perhaps someday, remains will be discovered - bones bleached by the sun,
            personal items scattered by animals and the elements. Perhaps a cross
            will mark the spot, one of many dotting the landscape like stars in a
            constellation of loss.
            
            Or perhaps {player_name} will simply become one of the disappeared,
            another name on the lists of the missing that families circulate in
            shelters and migrant support centers.
            
            Cantú writes of finding such remains during his patrols - grim reminders
            of the human cost of border policies and the desperate circumstances that
            drive people to risk everything for the chance at a different life.
            """
        
        elif ending_type == "timeout":
            epilogue = f"""
            Resources depleted, strength gone, {player_name}'s journey cannot continue.
            
            Stranded in the borderlands, each option more impossible than the last,
            {player_name} must find some way forward with nothing left to give.
            
            The border region is unforgiving to those who miscalculate, who underestimate
            the distance, the heat, the time required. Small errors compound into
            life-threatening situations with frightening speed.
            
            As Cantú's book shows us, the border is a place of extremes, where small
            decisions can have life-altering consequences, and where the gap between
            survival and disaster is often measured in hours rather than days.
            """
        
        else:
            epilogue = f"""
            {player_name}'s journey along the border has ended, but the larger story continues.
            
            Every day, people cross the border seeking better lives. Every day, agents patrol
            the line between nations. The complex interplay of policy, duty, desperation, and hope
            continues to shape countless lives.
            
            The border is not just a geographical reality but a moral space where humanity
            confronts its divisions and contradictions. It exists not just between nations,
            but within each person who encounters it.
            
            As 'The Line Becomes a River' shows us, there are no simple answers to the questions
            the border raises, only human stories that deserve to be understood in all their complexity.
            """
        
        self.print_slow(epilogue)
        
        # Add some reflection on the player's specific journey
        print("\n---YOUR JOURNEY---")
        
        # For migrants, reflect on their hope and what they experienced
        if player_type == "migrant":
            if hasattr(player, 'hope') and player.hope > 70:
                print(f"Despite everything, {player_name} maintained hope throughout the journey.")
            elif hasattr(player, 'hope') and player.hope > 30:
                print(f"The journey took its toll on {player_name}'s spirit, but did not break it entirely.")
            elif hasattr(player, 'hope'):
                print(f"The border crossing destroyed much of what made {player_name} who they were.")
                
            if hasattr(player, 'trauma') and player.trauma > 70:
                print(f"The psychological scars of this journey will remain with {player_name} forever.")
            elif hasattr(player, 'trauma') and player.trauma > 30:
                print(f"{player_name} witnessed things no person should have to see.")
                
            # Check family-related flags
            if player.has_flag("helped_family"):
                print(f"{player_name}'s compassion toward others revealed true character in crisis.")
            if player.has_flag("abandoned_family") or player.has_flag("abandoned_injured"):
                print(f"The harsh choices {player_name} made in the desert will haunt memories for years to come.")
                
        # For patrol agents, reflect on moral compass and stress
        else:
            if hasattr(player, 'moral_compass') and player.moral_compass > 70:
                print(f"{player_name} maintained humanity while upholding the duties of the badge.")
            elif hasattr(player, 'moral_compass') and player.moral_compass > 40:
                print(f"The job forced {player_name} to make compromises, but not to surrender principles entirely.")
            elif hasattr(player, 'moral_compass'):
                print(f"The border changed {player_name} in profound and troubling ways.")
                
            if hasattr(player, 'stress') and player.stress > 70:
                print(f"The psychological burden of border enforcement has taken a severe toll on {player_name}.")
            elif hasattr(player, 'stress') and player.stress > 40:
                print(f"{player_name} carries the weight of difficult decisions made in impossible situations.")
                
            # Check enforcement-related flags
            if player.has_flag("broke_rules_for_compassion"):
                print(f"{player_name} chose humanity over protocol when it mattered most.")
            if player.has_flag("reported_misconduct"):
                print(f"{player_name} stood against corruption and abuse, regardless of personal cost.")
        
        # Final reflection
        print("\nReflection:")
        self.print_slow(random.choice(self.quotes))
        
        print("\nThank you for experiencing 'The Line: A Border Journey'.")
        print("This narrative was inspired by 'The Line Becomes a River' by Francisco Cantú.")
        print("Remember that real people make these journeys every day.")
        print()
        
        input("\nPress Enter to exit ... ")
    
    def get_character_dialogue(self, character, player):
        """Get contextual dialogue for a character based on their type and relationship to player.
        
        Args:
            character: The character speaking
            player: The player character
            
        Returns:
            list: Possible dialogue options
        """
        from character import Migrant, BorderPatrol
        
        # Check for any character traits that might influence dialogue
        has_trait = lambda trait: hasattr(character, 'traits') and trait in character.traits
        
        # Enhanced dialogue templates with more emotional depth and context
        if isinstance(character, Migrant):
            if isinstance(player, Migrant):
                # Migrant to migrant dialogue - shared experiences
                dialogue = [
                    f"We're all trying to find something better. I'm from {character.origin}. {character.motivation}",
                    "Each step north carries the weight of those we left behind. But we must keep moving.",
                    "I saw someone collapse from dehydration yesterday. The Border Patrol found them... I don't know if they survived.",
                    f"My {', '.join([tie['name'] for tie in character.family_ties]) if hasattr(character, 'family_ties') and character.family_ties else 'family'} back home... they're all I think about. Their faces keep me going.",
                    "Sometimes I wonder if we're just chasing shadows across the desert.",
                    "Did you hear about the group they caught near the canyon? Twenty people, including children. All sent back.",
                    "I had a good life before. Professional, respected. Now I'm just... another body moving north.",
                    "The coyotes charge more each year. They know desperation has no ceiling price.",
                    "My brother made this journey three years ago. He said it's harder now. More walls, more sensors, more eyes watching."
                ]
                
                # Add trait-specific dialogue if applicable
                if has_trait("religious"):
                    dialogue.append("God walks with us in this desert. He must, or none would survive.")
                if has_trait("educated"):
                    dialogue.append("I was a teacher back home. My students would hardly recognize me now. Strange how quickly identity dissolves.")
                if has_trait("former_military"):
                    dialogue.append("I served my country, and now I flee it. The ironies of life never cease.")
                    
                return dialogue
                
            else:  # Player is Border Patrol
                # Migrant to Border Patrol dialogue - tense, cautious
                dialogue = [
                    "Please... my children haven't eaten in days. We had no choice but to leave.",
                    "I know you're just doing your job. But can you look at me and see a human being, not just another case number?",
                    "Send me back if you must, but please, let me keep my dignity.",
                    "You wear that uniform, but I see the conflict in your eyes. You understand, don't you?",
                    "I've buried friends in this desert. How many more must die before something changes?",
                    "In my hometown, the cartels run everything now. Return means death. Do you understand that?",
                    "I would have come legally if there was a way. The waitlist is years long. My need is now.",
                    "What would you do if it was your family in danger? If your children were hungry?",
                    "We don't want to break laws. We want to work, to contribute, to build something."
                ]
                
                # Add trait-specific dialogue
                if has_trait("desperate"):
                    dialogue.append("Please... I'm begging you. I can't go back. I CAN'T.")
                if has_trait("defiant"):
                    dialogue.append("Your laws are just lines on paper. They don't erase my right to survive.")
                if has_trait("educated"):
                    dialogue.append("I've studied your country's history. A nation of immigrants that now fears immigration. The contradiction is... striking.")
                    
                return dialogue
        
        elif isinstance(character, BorderPatrol):
            if isinstance(player, BorderPatrol):
                # Border Patrol to Border Patrol - professional, sometimes confessional
                dialogue = [
                    f"Been doing this {character.years_of_service} years now. Each year, the weight gets heavier.",
                    "Found a child's backpack yesterday. Pink, with butterflies. Still had a family photo inside...",
                    "We're supposed to be protecting the border, but sometimes I wonder what we're really protecting.",
                    "The desert doesn't discriminate. It takes from both sides of the line.",
                    "Some nights, I still hear their voices. The ones we couldn't save.",
                    "New directive from headquarters. More paperwork, less practical support. Typical.",
                    "My family doesn't ask about work anymore. They know I can't bring that home.",
                    "We're the face of a policy we didn't create. Easy to criticize when you're not out here.",
                    "Rescued a group last week. Three dehydrated, one with heat stroke. Saved their lives, then processed them for deportation. This job..."
                ]
                
                # Add trait-specific dialogue
                if has_trait("veteran"):
                    dialogue.append("Served in Afghanistan before this. Different desert, same human suffering. Never gets easier.")
                if has_trait("bureaucrat"):
                    dialogue.append("Keep your paperwork clean. Only way to survive when the inquiries start coming.")
                if has_trait("compassionate"):
                    dialogue.append("I keep extra water in my vehicle. Against protocol, but I can't watch people suffer if I can prevent it.")
                    
                return dialogue
                
            else:  # Player is Migrant
                # Border Patrol to Migrant - complex mix of authority and humanity
                dialogue = [
                    "I've seen too many deaths in these borderlands. Please, don't make me witness another.",
                    "The law is clear, but the heart... the heart sometimes speaks louder.",
                    "I have water if you need it. At least let me do that much.",
                    "Every face I send back haunts me. But what choice do I have?",
                    f"My own {random.choice(['grandparents', 'parents', 'family'])} crossed this same desert. The irony isn't lost on me.",
                    "I'm required to take you in. That's the job. But I'll make sure you're treated humanely.",
                    "This isn't personal. This is policy. Someone else makes the rules, I just enforce them.",
                    "If you surrender now, it's safer. The desert shows no mercy to anyone.",
                    "I've found too many bodies out here. Families who will never know what happened to their loved ones."
                ]
                
                # Add trait-specific dialogue
                if has_trait("by_the_book"):
                    dialogue.append("I'm placing you under the custody of United States Border Patrol. You have the right to claim asylum if you fear return to your country.")
                if has_trait("conflicted"):
                    dialogue.append("Sometimes I wonder if I'm on the right side of history. But then, what are the alternatives?")
                if has_trait("hardened"):
                    dialogue.append("Save your story. I've heard every variation. The system will determine your case, not me.")
                    
                return dialogue
        
        else:  # Generic character with deeper perspective
            # Locals, coyotes, aid workers, etc.
            dialogue = [
                "The border draws a line on the map, but the real divisions run deeper.",
                "In the end, we're all just trying to survive this place.",
                "I've seen the best and worst of humanity in these borderlands.",
                "The stories here could fill a thousand books. Most will never be told.",
                "Some say the desert holds the spirits of those who never made it. Some nights, I believe them.",
                "Politics happens far away. Here, it's just people facing the reality those politics create.",
                "Everyone passes through. The desert remains, indifferent to our human dramas.",
                "When you've lived here long enough, you stop seeing sides. You just see people.",
                "The wall is just a symbol. The real barriers are in the laws, in the minds, in the hearts."
            ]
            
            # Add character-specific dialogue variations
            if character.name == "Manuel":  # The coyote
                dialogue.extend([
                    "I know every wash and ridge for fifty miles. Knowledge that costs money, friend.",
                    "Some call me predator, some call me savior. I'm just a businessman in the border economy.",
                    "I don't create the demand, friend. I just provide the service. Blame your politicians.",
                    "Half my family lives on that side, half on this side. The border runs through our blood."
                ])
            
            return dialogue
    
    def present_moral_choice(self, player_type, situation=None):
        """Present a complex moral choice scenario to the player.
        
        Args:
            player_type (str): "migrant" or "patrol"
            situation (dict): Optional specific situation to present
            
        Returns:
            dict: The complete choice situation or None
        """
        # Select the appropriate pool of moral dilemmas
        choices_pool = self.moral_choices.get(player_type, [])
        if not choices_pool:
            return None
        
        # Either use provided situation or select a random one
        if situation:
            choice_scenario = situation
        else:
            choice_scenario = random.choice(choices_pool)
        
        # Display the scenario with rich description
        self.print_slow(f"\n-----MORAL CHOICE-----")
        self.print_slow(choice_scenario["description"])
        
        # Present choices
        print("\nWhat will you do?")
        for i, choice_text in enumerate(choice_scenario["choices"], 1):
            print(f"{i}. {choice_text}")
        
        # Get player's choice
        valid_choice = False
        choice_index = 0
        
        while not valid_choice:
            try:
                choice_input = input(f"\nEnter your choice (1-{len(choice_scenario['choices'])}): ")
                choice_index = int(choice_input) - 1
                if 0 <= choice_index < len(choice_scenario["choices"]):
                    valid_choice = True
                else:
                    print(f"Please enter a number between 1 and {len(choice_scenario['choices'])}.")
            except ValueError:
                print("Please enter a valid number.")
                    
        # Display consequence
        chosen_option = choice_scenario["choices"][choice_index]
        consequence = choice_scenario["consequences"][choice_index]
        
        self.print_slow(f"\nYou chose: {chosen_option}")
        self.print_slow(consequence["description"])
        
        # Update journey stats
        self.update_journey_stats("moral_choices_made")
        self.update_journey_stats("key_events", f"Moral Choice: {chosen_option}")
        
        # Return the complete choice information for the game engine to apply effects
        return {
            "description": choice_scenario["description"],
            "choice": chosen_option,
            "consequence": consequence
        }
    
    def trigger_trauma_event(self):
        """Trigger a random traumatic event with narrative impact.
        
        Returns:
            dict: The trauma event details or None
        """
        if not self.trauma_events:
            return None
        
        # Select a random trauma event
        event = random.choice(self.trauma_events)
        
        # Display the event
        self.print_slow(f"\n-----TRAUMATIC EXPERIENCE-----")
        self.print_slow(event["description"])
        self.print_slow(event["reflection"])
        
        # Update journey stats
        self.update_journey_stats("trauma_experienced")
        self.update_journey_stats("key_events", event["description"])
        
        return event
    
    def get_location_description(self, location_type, name):
        """Get rich thematic description for a location type.
        
        Args:
            location_type: The type of location (Desert, Border, Settlement)
            name (str): The name of the location
            
        Returns:
            list: Thematic descriptions
        """
        from location import Desert, Border, Settlement
        
        if isinstance(location_type, Desert):
            return [
                "The desert stretches endlessly, a vast graveyard of dreams and desperation.",
                "The sun beats down like judgment from above, while the sand below holds countless untold stories.",
                "Between the saguaros, you glimpse remnants of others' journeys - a child's shoe, a tattered backpack, a rosary.",
                "The wind whispers names of those who never made it, their hopes scattered among sun-bleached bones.",
                "Even the cacti seem to weep here, their shadows stretching like mourners across the sand.",
                "Heat ripples distort the horizon, blurring the line between reality and mirage, between hope and delusion.",
                "The day's heat brands you, while the night's cold cuts to the bone. The desert demands respect.",
                "Time loses meaning here. Only the sun's arc measures the passing hours, indifferent to human suffering.",
                "Each step disturbs dust that may have settled on another traveler's final resting place."
            ]
        
        elif isinstance(location_type, Border):
            return [
                "The wall rises like an iron curtain, dividing not just land, but dreams, families, and futures.",
                "Surveillance cameras stare with unblinking eyes, while sensors pulse beneath the ground like a mechanical heartbeat.",
                "The air thrums with tension - helicopter rotors above, desperate prayers below.",
                "Here, policy meets humanity in a clash of steel and flesh, law and desperation.",
                "Every footprint in the dust tells a story of choice - to cross, to turn back, to enforce, to defy.",
                "The border wall casts long shadows, both physical and metaphorical, obscuring what lies on either side.",
                "Birds fly across freely, mocking the human obsession with lines drawn on maps.",
                "The barrier stands as a monument to fear - of difference, of change, of the other.",
                "Graffiti marks sections of the wall - names, prayers, political statements. The voiceless finding voice."
            ]
        
        elif isinstance(location_type, Settlement):
            return [
                "The community lives and breathes the border, its rhythms shaped by the ebb and flow of crossings.",
                "In every face you see the weight of choice - to help, to hinder, to look away.",
                "Children play in the shadow of the wall, their laughter a defiant song against the barrier's silence.",
                "The streets hold secrets: safe houses marked with subtle signs, routes whispered in hushed tones.",
                "Even the church bells sound different here, their toll a reminder of lives interrupted, journeys unfinished.",
                "Markets sell necessities for crossing - black water jugs, desert-colored clothing, blister kits.",
                "Aid workers and enforcement officers move through the same spaces, engaged in their parallel missions.",
                "Posters of the missing hang in public spaces - faces frozen in time, families searching for closure.",
                "The economy here revolves around the border - serving those who enforce it, those who cross it, those who study it."
            ]
        
        else:
            return [
                f"{name} pulses with the heartbeat of the borderlands, each moment pregnant with possibility and peril.",
                "The border's gravity pulls at everything here, bending lives like light through a prism.",
                "Time feels different in this place, stretched taut between before and after, between here and there.",
                "The air itself carries stories - of courage and fear, of mercy and indifference, of hope and despair.",
                "In every shadow lurks a choice, in every choice, a story waiting to be told.",
                "History accumulates in layers here - indigenous pathways, colonial boundaries, modern enforcement.",
                "The language of the borderlands is unique - Spanish and English blending into something entirely its own.",
                "There's a particular quality to the light here, harsh yet revealing, exposing what might remain hidden elsewhere.",
                "This place exists in the hyphen between nation-states, a reality unto itself with its own unwritten laws."
            ]
    
    def trigger_random_event(self, player_type):
        """Trigger a random environmental or narrative event.
        
        Args:
            player_type (str): "migrant" or "patrol"
            
        Returns:
            dict: The event details or None
        """
        # Get appropriate event pool
        events_pool = self.random_events.get(player_type, [])
        if not events_pool:
            return None
        
        # Select a random event
        event = random.choice(events_pool)
        
        # Display the event
        self.print_slow(f"\n-----EVENT-----")
        self.print_slow(event["description"])
        self.print_slow(event["flavor"])
        
        # Update journey stats
        self.update_journey_stats("key_events", event["description"])

        # Check if this event involves another character
        if "encounter" in event["description"].lower() or "man" in event["description"].lower() or "person" in event["description"].lower():
            self.update_journey_stats("lives_impacted")
        
        return event
    
    def update_journey_stats(self, stat_type, value=1):
        """Update journey statistics for narrative tracking.
        
        Args:
            stat_type (str): Type of statistic to update
            value: Value to add (default: 1)
        """
        if stat_type in self.journey_stats:
            if isinstance(self.journey_stats[stat_type], list):
                if isinstance(value, list):
                    self.journey_stats[stat_type].extend(value)
                else:
                    self.journey_stats[stat_type].append(value)
            else:
                self.journey_stats[stat_type] += value
    
    def display_journey_summary(self, player):
        """Display a rich summary of the player's journey.
        
        Args:
            player: The player character object
        """
        self.clear_screen()
        print("╔════════════════════════════════════════════════════════════╗")
        print("║                     JOURNEY SUMMARY                        ║")
        print("╚════════════════════════════════════════════════════════════╝\n")
        
        # Basic stats with visual representations
        distance = self.journey_stats['distance_traveled']
        print(f"Distance Traveled: {distance} miles")
        print(f"Physical Journey: {'=' * (distance // 20)}○")
        print()
        
        print(f"Lives Impacted: {self.journey_stats['lives_impacted']} individuals")
        print(f"Moral Choices Made: {self.journey_stats['moral_choices_made']} decisions")
        print(f"Traumatic Events Experienced: {self.journey_stats['trauma_experienced']} incidents")
        print()
        
        # Key moments from journey
        if self.journey_stats['key_events']:
            print("Defining Moments:")
            key_events = self.journey_stats['key_events'][-7:] if len(self.journey_stats['key_events']) > 7 else self.journey_stats['key_events']
            for event in key_events:
                print(f"- {event}")
            print()
        
        # Character-specific summary
        if hasattr(player, 'origin'):  # Migrant
            origin = player.origin
            # Format player motivation by removing option number if present
            motivation = player.motivation
            if ". " in motivation:
                motivation = motivation.split(". ", 1)[1]
                
            print(f"You began in {origin} driven by {motivation}.")
            
            if hasattr(player, 'hope'):
                hope = player.hope
                hope_bar = "█" * (hope // 10) + "░" * (10 - (hope // 10))
                print(f"Hope: [{hope_bar}] {hope}/100")
                
                if hope > 70:
                    print("Despite the hardships, your spirit remains unbroken.")
                elif hope > 30:
                    print("The journey has taken its toll, but you persist.")
                else:
                    print("The weight of the journey has left deep scars on your soul.")
            
            if hasattr(player, 'trauma') and player.trauma > 0:
                trauma = player.trauma
                trauma_bar = "█" * (trauma // 10) + "░" * (10 - (trauma // 10))
                print(f"Trauma: [{trauma_bar}] {trauma}/100")
                
                if trauma > 70:
                    print("Some wounds never heal. The borderlands have marked you forever.")
                elif trauma > 30:
                    print("What you've witnessed will stay with you, a shadow over future days.")
                else:
                    print("You carry the memories of the crossing, but they do not define you.")
                
        else:  # Border Patrol
            years = player.years_of_service
            print(f"After {years} years of service, the border has shaped your perspective.")
            
            if hasattr(player, 'moral_compass'):
                moral = player.moral_compass
                moral_bar = "█" * (moral // 10) + "░" * (10 - (moral // 10))
                print(f"Moral Compass: [{moral_bar}] {moral}/100")
                
                if moral > 70:
                    print("You've maintained your humanity while upholding the law.")
                elif moral > 40:
                    print("The job has forced you to make difficult compromises.")
                else:
                    print("The border has changed you in ways you never expected.")
            
            if hasattr(player, 'stress'):
                stress = player.stress
                stress_bar = "█" * (stress // 10) + "░" * (10 - (stress // 10))
                print(f"Stress Level: [{stress_bar}] {stress}/100")
                
                if stress > 70:
                    print("The psychological toll of enforcement has left you burned out.")
                elif stress > 40:
                    print("You cope with the stress through compartmentalization.")
                else:
                    print("You've managed to maintain your equilibrium despite the challenges.")
        
        # Thematic reflection
        print("\nReflection:")
        reflection = random.choice(self.quotes)
        self.print_slow(reflection)
        
        input("\nPress Enter to continue ... ")
    
    def graceful_exit(self, player):
        """Handle early exit from the game with journey summary.
        
        Args:
            player: The player character object
        """
        self.clear_screen()
        print("Preparing your journey summary...\n")
        time.sleep(1)
        
        # Show journey summary
        self.display_journey_summary(player)
        
        print("\nYour journey along the borderlands remains unfinished.")
        print("Like many stories of the border, it ends without clear resolution.")
        print("Thank you for experiencing 'The Line: A Border Journey'.")
        
        # Exit the game
        sys.exit(0)

    def change_weather(self):
        """Change the current weather condition randomly.
        
        Returns:
            dict: The new weather condition
        """
        self.current_weather = random.choice(self.weather_conditions)
        
        # Announce the weather change
        self.print_slow(f"\nThe weather changes: {self.current_weather['name']}")
        self.print_slow(self.current_weather['description'])
        
        return self.current_weather
    
    def get_weather_effects(self):
        """Get the gameplay effects of current weather.
        
        Returns:
            dict: Weather effects on gameplay
        """
        return self.current_weather.get('effect', {})
    
    def record_player_choice(self, choice_description, consequence):
        """Record a player choice for the journey narrative.
        
        Args:
            choice_description (str): Description of the choice
            consequence (str): Outcome of the choice
        """
        self.update_journey_stats("key_events", f"Choice: {choice_description} - {consequence}")
        
    def get_time_of_day(self, turn_count):
        """Get the current time of day based on turn count.
        
        Args:
            turn_count (int): Current turn count
            
        Returns:
            str: Time of day description
        """
        # Cycle through day and night
        cycle = turn_count % 6
        
        if cycle == 0:
            return "Dawn breaks over the desert, painting the landscape in gold and pink."
        elif cycle == 1:
            return "Morning sun climbs higher, promising heat as the day advances."
        elif cycle == 2:
            return "Midday sun beats down mercilessly from directly overhead."
        elif cycle == 3:
            return "Afternoon heat shimmers across the landscape as the sun begins its descent."
        elif cycle == 4:
            return "Sunset bathes the borderlands in red and orange as shadows lengthen."
        else:
            return "Night falls over the desert, bringing chill air and a canopy of stars."