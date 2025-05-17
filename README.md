# The Line: A Border Journey

## Project Overview

*The Line: A Border Journey* is a text-based narrative game inspired by Francisco Cantú's memoir "The Line Becomes a River." This game explores the human stories, moral complexities, and harsh realities faced by those who cross the US-Mexico border and those who patrol it.

This immersive experience invites players to engage with the border not as an abstract political concept, but as a complex human reality that transforms all who encounter it. Through authentic mechanics and narrative choices, players witness firsthand the physical, emotional, and moral dimensions of border experiences.

This project is created as part of NYU's FY-SEM course taught by Prof. Huddleston, as a creative project to explore and interpret Cantú's powerful book.

---

## Installation

### Requirements:

* Python 3.7+ installed
* Required Python libraries:
    ```bash
    pip3 install -r requirements.txt
    ```

### Optional AI Feature:
For enhanced natural language processing, you can use:
* Ollama with the `mxbai-embed-large` model running locally (usually at `http://localhost:11434`)
* If Ollama isn't available, the game will gracefully fall back to standard text commands

#### Installing Ollama CLI

__macOS & Linux__
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

__Windows__
1. Download the Windows installer from the [Ollama download page](https://ollama.com/download).
2. Run the downloaded `.exe` and follow the prompts.

#### Pull the embedding model

```bash
ollama pull mxbai-embed-large # [OR]
ollama pull nomic-embed-text # Suitable for a smaller and faster model
```

#### Start the Ollama API server

```bash
ollama serve # By default, Ollama listens on `http://localhost:11434`.
```

### Running the Game:

1. Clone or download this repository
2. Navigate to the game directory in your terminal
3. Run the main script:
   
   ```bash
   python3 main.py
   ```

### Command Line Options:
```
python3 main.py --help        # Show available options
python3 main.py --debug       # Enable debug mode
python3 main.py --skip-intro  # Skip introduction sequence
```
---

## Gameplay Features

### Dual Perspectives:
Experience the border from two distinct viewpoints:
* **Migrant**: Journey northward seeking safety and opportunity, managing resources and hope. Starting in Nogales, Mexico, you'll need to gather resources, face the challenge of crossing the border wall, and navigate life in the United States.
* **Border Patrol**: Enforce policies within US territory while navigating the moral complexities of your role. Starting in Nogales, USA, you patrol the American side of the border, apprehending those who cross illegally while confronting difficult ethical dilemmas.

### Core Mechanics:
* **Resource Management**: Monitor and manage water, food, health, and other vital resources
* **Border Crossing Challenges**: As a migrant, choose from multiple realistic crossing methods, each with different risks, requirements, and success rates
* **Jurisdictional Realism**: Border Patrol operations realistically confined to US territory
* **Moral Choices**: Make difficult decisions that impact your character's journey and others' lives
* **Narrative Events**: Encounter a variety of situations drawn from the realities of border life
* **Environmental Challenges**: Face the harsh desert conditions, patrol encounters, and human interactions
* **Character Development**: Your decisions shape your character's mental and physical wellbeing
* **Trauma System**: Experience the psychological impact of border experiences, reflective of Cantú's own accounts

### Immersive Storytelling:
* Rich environmental descriptions based on actual border locations
* Dialogue inspired by Cantú's work and real border testimonies
* Detailed border crossing mechanics that reflect genuine methods described in Cantú's book
* Weather and time-of-day systems that affect gameplay
* Trauma and psychological aspects of border experiences

---

## Game World

### Locations:
* **Nogales (Mexico)**: Starting point for migrants, offering basic services and supplies for the journey ahead
* **Sonoran Desert**: Harsh terrain with extreme conditions and scarce resources, where survival is constantly tested
* **Border Wall**: Heavily patrolled barrier with surveillance systems, representing the central challenge for migrants
* **Nogales (USA)**: American side with different challenges and opportunities, the starting point for Border Patrol agents
* **Detention Center**: Processing facility for apprehended migrants, representing one possible outcome of the journey
* **Tucson**: Final destination for migrants, representing success in the migration journey

### Narrative Elements:
* **Border Crossing Event**: Detailed challenges of crossing the physical barrier between nations
* **Trauma Events**: Psychological impacts of border experiences
* **Moral Dilemmas**: Difficult choices with no clear "right" answers
* **Encounter Events**: Interactions with other characters in the borderlands
* **Resource Events**: Finding or losing vital supplies
* **Weather Events**: Environmental challenges that affect gameplay

### Items & Equipment:
* **Essential Supplies**: Water bottles, food, blankets and other survival necessities
* **Border Crossing Tools**: Wire cutters and other equipment to facilitate crossing attempts
* **Communication Devices**: Radios and phones that connect characters across the border
* **Personal Items**: Family photos and mementos that impact hope and psychological wellbeing

---

## Thematic Connections to "The Line Becomes a River"

The game directly engages with key themes from Cantú's memoir:

* **Border as Transformer**: Like Cantú, characters are changed by their border experiences
* **Moral Ambiguity**: No clear heroes or villains, only people navigating complex systems
* **Psychological Cost**: Trauma mechanics reflect Cantú's nightmares and psychological struggles
* **Humanity Across Division**: Opportunities for compassion that transcend institutional roles
* **Policy vs. People**: The clash between abstract policy and flesh-and-blood reality

Specific game mechanics draw inspiration from Cantú's experiences:
* The border crossing methods reference actual crossing techniques described in the book
* Character dialogue incorporates themes and reflections from Cantú's writing
* The trauma system reflects Cantú's accounts of dreams and psychological impacts

---

## Educational Value

This game is designed not just for entertainment, but as an educational tool to foster empathy and understanding about:

* The humanitarian aspects of migration
* The ethical complexities of border enforcement
* The impact of policy decisions on human lives
* The psychological toll of the border on all who encounter it
* The physical challenges and dangers of border crossing
* The jurisdictional realities of border enforcement

By experiencing both sides of the border narrative, players gain insight into the complex human dimensions that often get lost in political discourse.

---

## Developer Notes

This project strives for authenticity while remaining respectful of the serious nature of its subject matter. Research beyond Cantú's book included:

* Testimonies from migrants and border patrol agents
* Geographic and environmental data about the border region
* Official border enforcement protocols and jurisdictional boundaries
* Humanitarian reports on migration challenges and border deaths

The game mechanics—particularly the border crossing system and jurisdictional limitations—are designed to reflect real-world conditions as accurately as possible within the constraints of a text-based narrative game.

---

## Credits

* Game Design & Writing: FY-SEM Creative Project
* Programming: Ashish Reddy Tummuri
* Academic Professor: Prof. Robert Huddleston
* Literary Inspiration: Francisco Cantú, "The Line Becomes a River"

Additional inspiration from:
* Humanitarian organizations working at the border

---

## License

This project is created for educational purposes. All rights therefore reserved.

---

## Disclaimer

This game portrays situations based on real border experiences but is a work of fiction. It is not intended to make political statements but rather to inspire reflection on the human aspects of migration and enforcement.

---

_Made with __LOVE___ 💖