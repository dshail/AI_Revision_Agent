# Technology Stack

## Language & Runtime
- **Python** - Primary development language
- Command-line interface for user interaction

## Architecture Pattern
- **Agent-based modular system** with specialized components:
  - Planner Agent: Breaks down revision tasks
  - Summarizer Agent: Generates content summaries
  - CLI Interface: Handles user interaction
  - Utils: Shared helper functions

## Common Commands

### Running the Application
```bash
python cli_interface.py
```

### Development Guidelines
- Each agent should have a single, well-defined responsibility
- Use modular design to allow easy extension of new agent types
- Maintain clear separation between planning and content generation
- Include comprehensive comments explaining agent roles and functions

## Code Style
- Use descriptive comments at the top of each file explaining the component's purpose
- Follow Python naming conventions
- Keep agent logic modular and testable