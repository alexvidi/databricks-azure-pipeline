import os
import yaml
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def load_config():
    """Load configuration from YAML file."""
    config_path = os.path.join(os.path.dirname(__file__), "../config/config.yaml")
    
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
    
    # Replace placeholders with environment variables
    for key, value in config["azure"].items():
        if isinstance(value, str) and value.startswith("${"):
            env_var = value.strip("${}")
            config["azure"][key] = os.getenv(env_var, "")
    
    return config["azure"]
