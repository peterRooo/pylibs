import json
import logging

g_config = {}
g_config_path = ''

def init(config_path):
    logging.info(f'Config path: {config_path}')
    global g_config_path
    g_config_path = config_path
    global g_config
    with open(config_path, 'r', encoding='utf-8') as f:
        g_config = json.load(f)
    logging.info(f'Config: {g_config}')
    
def get(*keys, default=None):
    """
    Retrieve a value from a nested dictionary using variable arguments for keys.

    :param config: The configuration dictionary to search.
    :param keys: Variable arguments representing the path to the desired value.
    :param default: The default value to return if the keys path is not found.
    :return: The value from the config if the keys path is found, otherwise default.
    """
    current_level = g_config
    for key in keys:
        if isinstance(current_level, dict) and key in current_level:
            current_level = current_level[key]
        else:
            return default
    return current_level

def save():
    global g_config_path
    logging.info(f'Save config to {g_config_path}')
    with open(g_config_path, 'w', encoding='utf-8') as f:
        json.dump(g_config, f, ensure_ascii=False, indent=4)

def set(*keys, value):
    """
    Set a value in a nested dictionary using variable arguments for keys.

    :param config: The configuration dictionary to modify.
    :param keys: Variable arguments representing the path to the desired value.
    :param value: The value to set at the specified keys path.
    """
    current_level = g_config
    for key in keys[:-1]:  # Iterate over keys except the last one
        if key not in current_level or not isinstance(current_level[key], dict):
            current_level[key] = {}  # Create a new dictionary if key doesn't exist or is not a dictionary
        current_level = current_level[key]
    current_level[keys[-1]] = value  # Set the value for the last key

    save()
