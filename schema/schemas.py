def indivial_serializer(todo) -> dict:
    print(dir(todo))
    return {
        "id": str(todo["_id"]),
        "name": todo["name"],
        "description": todo["description"],
        "complete": todo["complete"],

    }

def list_serial(todos) -> list:
    return [indivial_serializer(todo) for todo in todos]