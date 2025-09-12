import os
import subprocess
import sys  # Import sys to use sys.executable
import logging

##################################################### Logger ##################################################### 
# Set up logger
log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs.txt')

logging.basicConfig(
    level=logging.DEBUG,  # Minimum level of messages to log
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Output to console
        logging.FileHandler(log_file)  # Output to file
    ]
)

logger = logging.getLogger(__name__)

##################################################### requirements ##################################################### 
# Get the directory where this script is located
base_dir = os.path.dirname(os.path.abspath(__file__))

# Install requirements
requirements_path = os.path.join(base_dir, 'requirements.txt')
if os.path.exists(requirements_path):
    try:
        logger.info("Installing requirements...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', requirements_path])
        logger.info("Installing requirements Successfull")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error installing requirements: {e}")
        sys.exit(1)
else:
    logger.warning("No requirements.txt file found.")

##################################################### run script ##################################################### 
# List of Python files to run
scripts_to_run = [
    'FPL_Dashboard.py']

# Run each script
for script_name in scripts_to_run:
    script_path = os.path.join(base_dir, script_name)
    if os.path.exists(script_path):
        logger.info(f"Running {script_name}...")
        subprocess.run(['python', script_path])
    else:
        logger.warning(f"{script_name} not found.")

logger.info("Run Successfull")

