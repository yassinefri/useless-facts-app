import requests
def connect_to_api(url, params=None):
    """
    Connects to the specified API URL with optional parameters.
    
    Args:
        url (str): The API endpoint URL.
        params (dict, optional): A dictionary of query parameters to include in the request.
        
    Returns:
        dict: The JSON response from the API if successful, otherwise None.
    """
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()
    except requests.RequestException as e:
        print(f"Error connecting to API: {e}")
        return None