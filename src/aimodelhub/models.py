import requests

from paths import HEADERS


def get_models():
    """
    Retrieves a list of available models from the IONOS AI Model Hub API.
    Returns:
        list: A list of models with their names and descriptions.
    """
    try:
        # Define the API endpoint
        endpoint = 'https://openai.inference.de-txl.ionos.com/v1/models'
        # Make the API call (GET request)
        response = requests.get(endpoint, headers=HEADERS)
        # Check the response status code
        if response.status_code == 200:
            # If successful, process and return the models
            models = response.json()['data']
            # Return the models as a simple list
            return models
        else:
            # If there was an error, print the status code and error message
            print(f'Error: {response.status_code}')
            print('Message:', response.text)
            raise Exception('Error retrieving models')
    except Exception as e:
        print(f'An error occurred: {e}')


def print_models(models):
    """
    Prints a list of models with their names and descriptions.
    Args:
        models (list): A list of models with their names and descriptions.
    """
    for model in models:
        print(f"  - {model['id']}")


if __name__ == "__main__":
    models = get_models()
    print_models(models)
