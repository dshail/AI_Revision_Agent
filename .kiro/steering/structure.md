# Project Structure

## Root Level Files
- `README.md` - Basic project description and run instructions
- `1_Project_Overview.md` - Detailed project purpose and scope
- `2_Architecture_Diagram.png` - Visual system architecture
- `6_Reflection.md` - Development insights and lessons learned
- `7_Advanced_Features.md` - Future feature specifications

## Core Directories

### `3_Agent_Code/`
Contains the main application logic with modular agent components:
- `cli_interface.py` - Entry point and user interaction handler
- `planner_agent.py` - Task breakdown and planning logic
- `summarizer_agent.py` - Content generation and summarization
- `utils.py` - Shared utility functions across agents

### `4_Sample_Run_Logs/`
Example execution logs showing expected input/output behavior:
- `run_example_1.txt` - Deep Learning revision example
- `run_example_2.txt` - Agent AI recap example

### `5_Test_Cases/`
Test specifications and expected behaviors:
- `sample_tests.md` - Test case definitions with input/output pairs

## Organization Principles
- **Numbered prefixes** indicate logical flow and importance
- **Agent code centralized** in dedicated directory for modularity
- **Documentation-driven** with examples and test cases
- **Clear separation** between implementation, testing, and documentation