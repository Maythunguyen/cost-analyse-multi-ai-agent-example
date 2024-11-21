# Warning control
import warnings
warnings.filterwarnings('ignore')

# Load environment variables
from helper import load_env
load_env()

import os
import yaml
from crewai import Agent, Task, Crew
from crewai_tools import FileReadTool




# Initialize tools with `name` attributes
clinical_note_tool = FileReadTool(file_path='./data/clinical_note_sample.pdf')
clinical_note_tool.name = "clinical_note_tool"

bills_tool = FileReadTool(file_path='./data/bills_sample.pdf')
bills_tool.name = "bills_tool"

outcome_measure_tool = FileReadTool(file_path='./data/outcome_measures_sample.pdf')
outcome_measure_tool.name = "outcome_measure_tool"

# Define file paths for YAML configurations
files = {
    'agents': 'config/agents.yaml',
    'tasks': 'config/tasks.yaml'
}

# Load configurations from YAML files
configs = {}
for config_type, file_path in files.items():
    with open(file_path, 'r') as file:
        configs[config_type] = yaml.safe_load(file)

# Assign loaded configurations to specific variables
agents_config = configs['agents']
tasks_config = configs['tasks']

# Debugging output
print("Agents Config:", agents_config)
print("Tasks Config:", tasks_config)

# Initialize agents with the configuration and tools
data_extraction_agent = Agent(
    config=agents_config['agents']['data_extraction_agent'],
    tools=[clinical_note_tool, bills_tool, outcome_measure_tool]
)

cost_calculation_agent = Agent(
    config=agents_config['agents']['cost_calculation_agent']  # No tools passed here
)

insight_recommendation_agent = Agent(
    config=agents_config['agents']['insight_recommendation_agent']
)

reporting_agent = Agent(
    config=agents_config['agents']['reporting_agent']
)

chart_generation_agent = Agent(
    config=agents_config['agents']['chart_generation_agent'],
    allow_code_execution=True
)

# Define tasks, associating them with agents
data_extraction_task = Task(
    config=tasks_config['tasks']['data_extraction_task'],
    agent=data_extraction_agent
)

cost_calculation_task = Task(
    config=tasks_config['tasks']['cost_calculation_task'],
    agent=cost_calculation_agent
)

insight_recommendation_task = Task(
    config=tasks_config['tasks']['insight_recommendation_task'],
    agent=insight_recommendation_agent
)

report_compilation_task = Task(
    config=tasks_config['tasks']['report_compilation_task'],
    agent=reporting_agent,
    context=[data_extraction_task, cost_calculation_task, insight_recommendation_task]
)

chart_creation_task = Task(
    config=tasks_config['tasks']['chart_creation_task'],
    agent=chart_generation_agent,
    context=[report_compilation_task]
)

# Create the Crew instance to manage agents and tasks
cost_calculation_crew = Crew(
    agents=[
        data_extraction_agent,
        cost_calculation_agent,
        insight_recommendation_agent,
        reporting_agent,
        chart_generation_agent
    ],
    tasks=[
        data_extraction_task,
        cost_calculation_task,
        insight_recommendation_task,
        report_compilation_task,
        chart_creation_task
    ],
    verbose=True
)

# Test the crew setup
cost_calculation_crew.test(n_iterations=1, openai_model_name='gpt-4o')

# Train and kick off the crew
cost_calculation_crew.train(n_iterations=1, filename='training.pkl')
result = cost_calculation_crew.kickoff()

# Display the result
from IPython.display import display, Markdown
display(Markdown(result.raw))
