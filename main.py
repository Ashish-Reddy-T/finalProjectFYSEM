"""
The Line: A Border Journey
A text-based narrative game inspired by Francisco Cantú's 'The Line Becomes a River'

This game explores the human stories and moral complexities of border migration
and enforcement through interactive storytelling.
"""

import time
import random
import os
import sys
import argparse
from character import Character, Migrant, BorderPatrol
from location import Location, Desert, Border, Settlement
from game_engine import GameEngine
from story import Story


def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else "clear")


def print_slow(text, delay=0.03, end='\n'):
    """Print text with a typing effect for immersion.
    
    Args:
        text (str): Text to print
        delay (float): Delay between characters
        end (str): End character for print
    """
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print(end=end)


def display_title():
    """Display the game title with artistic ASCII border."""
    title = """
    ╔════════════════════════════════════════════════════════════╗
    ║                                                            ║
    ║                      THE LINE                              ║
    ║                  A Border Journey                          ║
    ║                                                            ║
    ║          Inspired by 'The Line Becomes a River'            ║
    ║                  by Francisco Cantú                        ║
    ║                                                            ║
    ╚════════════════════════════════════════════════════════════╝
    """
    print_slow(title, 0.005)


def display_credits():
    """Display game credits and acknowledgments."""
    credits = """
    ╔════════════════════════════════════════════════════════════╗
    ║                      CREDITS                               ║
    ╚════════════════════════════════════════════════════════════╝
    
    Game Design & Writing: FY-SEM CREATIVE PROJECT
    Programming: Ashish Reddy Tummuri
    Academic Adviser: Prof. Robert Huddleston
    
    Special Thanks:
    - Francisco Cantú for the powerful book that inspired this project
    - The countless real people whose lives are affected by border policies
    
    This game is a work of interactive fiction designed to promote
    empathy and understanding of the complex human realities at the
    US-Mexico border.
    
    Therfore, no political stance is intended - only a commitment to 
    recognizing our shared humanity across borders.
    """
    
    clear_screen()
    print_slow(credits, 0.02)
    input("\nPress Enter to return to the main menu...")


def save_game(game):
    """Rudimentary save game functionality.
    
    Args:
        game: The active GameEngine instance
    """
    print("\nSaving game is not yet implemented in this version.")
    print("This feature would allow you to continue your journey later.")
    input("\nPress Enter to continue...")


def intro_page():
    """Display the introductory page with game description."""
    clear_screen()
    display_title()

    intro_text = """
    Welcome to 'The Line: A Border Journey'
    
    This narrative game explores the human stories and moral complexities 
    of border migration through interactive storytelling, inspired by 
    Francisco Cantú's memoir 'The Line Becomes a River'.
    
    You will experience the border region from one of two perspectives:
    
    - As a migrant seeking a better life across the border
    - As a Border Patrol agent enforcing policies at the line
    
    Your choices will shape your journey and reveal the profound impact
    the border has on all who encounter it.
    
    This is not a game about politics, but about people.
    """
    
    print_slow(intro_text)
    print('\nPress Enter to continue ', end='')
    print_slow("... ", delay=0.6, end='')
    input()


def main_menu():
    """Display the main menu and handle user selection.
    
    Returns:
        str: User's menu choice
    """
    clear_screen()
    display_title()
    
    menu_text = """
    MAIN MENU
    =========
    
    1. Start New Journey
    2. About This Game
    3. Credits
    4. Exit
    """
    
    print(menu_text)
    
    while True:
        choice = input("\nEnter your choice (1-4): ")
        if choice in ["1", "2", "3", "4"]:
            return choice
        print("Invalid choice. Please enter a number from 1 to 4.")


def about_game():
    """Display information about the game and its themes."""
    about_text = """
    ╔════════════════════════════════════════════════════════════╗
    ║                  ABOUT THIS GAME                           ║
    ╚════════════════════════════════════════════════════════════╝
    
    'The Line: A Border Journey' is an interactive narrative experience
    that explores the complex human stories on both sides of the US-Mexico
    border, inspired by Francisco Cantú's memoir 'The Line Becomes a River'.
    
    The game examines themes of:
    
    • Humanity across borders
    • The personal cost of migration
    • The moral complexity of enforcement
    • Trauma and healing
    • Identity and belonging
    
    Through your choices, you'll experience the physical, emotional, and
    ethical challenges faced by those who cross the border and those who
    patrol it.
    
    Game Mechanics:
    
    • Resource Management: Manage water, food, and health
    • Moral Choices: Make difficult decisions that affect your character
    • Environmental Challenges: Navigate the dangers of the border region
    • Character Development: Your choices shape your character's journey
    
    The journey is designed to be played multiple times, exploring different
    perspectives and choices to better understand the multifaceted reality
    of the borderlands.
    """
    
    clear_screen()
    print_slow(about_text, 0.02)
    input("\nPress Enter to return to the main menu...")


def parse_arguments():
    """Parse command line arguments.
    
    Returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(description='The Line: A Border Journey')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode with additional outputs')
    parser.add_argument('--skip-intro', action='store_true', help='Skip introduction and go straight to character creation')
    return parser.parse_args()


def main():
    """Main function to run the game."""
    # Parse command line arguments
    args = parse_arguments()
    
    # Show introduction unless skipped
    if not args.skip_intro:
        intro_page()
    
    # Main menu loop
    while True:
        choice = main_menu()
        
        if choice == "1":  # Start New Journey
            # Initialize game components
            story = Story()
            game = GameEngine(story)
            
            # Enable debug mode if specified
            if args.debug:
                print("[DEBUG MODE ENABLED]")
                game.debug_mode = True
            
            # Start the game
            try:
                game.start()
            except KeyboardInterrupt:
                print("\n\nGame interrupted. Returning to main menu...")
                time.sleep(2)
            except Exception as e:
                if args.debug:
                    print(f"\nERROR: {e}")
                    print("Returning to main menu...")
                    time.sleep(3)
                else:
                    print("\nAn error occurred. Returning to main menu...")
                    time.sleep(2)
                    
        elif choice == "2":  # About This Game
            about_game()
            
        elif choice == "3":  # Credits
            display_credits()
            
        elif choice == "4":  # Exit
            clear_screen()
            print_slow("Thank you for exploring 'The Line: A Border Journey'.")
            print_slow("May we all find more humanity across borders.")
            sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear_screen()
        print("\nGame exited.")
        sys.exit(0)