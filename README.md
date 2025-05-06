# The Line: A Border Journey

## Project Overview

*The Line: A Border Journey* is a text-based narrative game inspired by Francisco Cantú's memoir "The Line Becomes a River." This game explores the human stories, moral complexities, and harsh realities faced by those who cross the US-Mexico border and those who patrol it.

This project is created as part of NYU's FY-SEM course taught by Prof. Huddleston, as a creative project to Cantú's powerful book.

---

## Installation

### Requirements:

* Python 3.7+ installed
* Required Python libraries:
    ```bash
    pip install -r requirements.txt
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
    python main.py
    ```

### Command Line Options:
```
python main.py --help        # Show available options
python main.py --debug       # Enable debug mode
python main.py --skip-intro  # Skip introduction sequence
```
---

## Gameplay Features

### Dual Perspectives:
Experience the border from two distinct viewpoints:
* **Migrant**: Journey northward seeking safety and opportunity, managing resources and hope
* **Border Patrol**: Enforce policies while navigating the moral complexities of your role

### Core Mechanics:
* **Resource Management**: Monitor and manage water, food, health, and other vital resources
* **Moral Choices**: Make difficult decisions that impact your character's journey and others' lives
* **Narrative Events**: Encounter a variety of situations drawn from the realities of border life
* **Environmental Challenges**: Face the harsh desert conditions, patrol encounters, and human interactions
* **Character Development**: Your decisions shape your character's mental and physical wellbeing

### Immersive Storytelling:
* Rich environmental descriptions based on actual border locations
* Dialogue inspired by real experiences documented in Cantú's work
* Weather and time-of-day systems that affect gameplay
* Trauma and psychological aspects of border experiences

---

## Game World

### Locations:
* **Nogales (Mexico)**: Starting point for migrants, offering basic services
* **Sonoran Desert**: Harsh terrain with extreme conditions and scarce resources
* **Border Wall**: Heavily patrolled barrier with surveillance systems
* **Nogales (USA)**: American side with different challenges and opportunities
* **Detention Center**: Processing facility for apprehended migrants
* **Tucson**: Final destination for migrants, representing success

### Narrative Elements:
* **Trauma Events**: Psychological impacts of border experiences
* **Moral Dilemmas**: Difficult choices with no clear "right" answers
* **Encounter Events**: Interactions with other characters in the borderlands
* **Resource Events**: Finding or losing vital supplies
* **Weather Events**: Environmental challenges that affect gameplay

---

## Educational Value

This game is designed not just for entertainment, but as an educational tool to foster empathy and understanding about:

* The humanitarian aspects of migration
* The ethical complexities of border enforcement
* The impact of policy decisions on human lives
* The psychological toll of the border on all who encounter it

---

## Credits

* Game Design & Writing: FY-SEM Creative Project
* Programming: Ashish Reddy Tummuri
* Academic Adviser: Prof. Robert Huddleston
* Literary Inspiration: Francisco Cantú, "The Line Becomes a River"

---

## License

This project is created for educational purposes. All rights therefore reserved.

---

## Disclaimer

This game portrays situations based on real border experiences but is a work of fiction. It is not intended to make political statements but rather to inspire reflection on the human aspects of migration and enforcement.

---

_Made with __LOVE___ 💖