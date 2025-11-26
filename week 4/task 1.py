def sort_list_of_dicts_manual(data, key):
    """
    Sorts a list of dictionaries by a specified key using manual implementation.

    Args:
        data (list): List of dictionaries.
        key (str): The key to sort by.

    Returns:
        list: Sorted list of dictionaries.
    """
    # Using the sorted function with a lambda as the key
    sorted_data = sorted(data, key=lambda x: x[key])
    return sorted_data

# Example usage
data = [{"name": "Charlie", "age": 25}, {"name": "Alice", "age": 30}, {"name": "Bob", "age": 20}]
print(sort_list_of_dicts_manual(data, "name"))
# Output: [{'name': 'Alice', 'age': 30}, {'name': 'Bob', 'age': 20}, {'name': 'Charlie', 'age': 25}]