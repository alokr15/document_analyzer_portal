import yaml

def load_config(config_path: str = "config\config.yaml") -> dict:
    """
    Load configuration from a YAML file.

    :param config_path: Path to the YAML configuration file.
    :return: Dictionary containing the configuration.
    """
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        return config
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file '{config_path}' not found.")
    except yaml.YAMLError as e:
        raise ValueError(f"Error parsing YAML configuration: {e}")