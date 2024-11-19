# setting up saving the user's information entered in forms
from db import personal_data_collection, notes_collection


def get_values(_id):
    """
    - Returns a sample version of what we're gonna be storing in our personal data collection
    - when we don't have any data in the database we will start with this initially
    - so that we kind of have schema already created and later for every request we can update the values

    """
    return {
        "_id": _id,
        "general": {
            "name": "",
            "age": 30,
            "weight": 60,
            "height": 165,
            "activity_level": "Moderately Active",
            "gender": "Male",
        },
        "goals": ["Muscle Gain"],
        "nutrition": {
            "calories": 2000,
            "protein": 140,
            "fat": 20,
            "carbs": 100,
        },
    }


def create_profile(_id):
    profile_values = get_values(_id)
    result = personal_data_collection.insert_one(profile_values) #returns a InsertOneResult
    # if we don't already have an entry in our database , we're just going to create that in the database
    # we're going to grab the id of that entry and return it
    return result.inserted_id, result


# this way on the frontend we get access to them and then we can update our form


def get_profile(_id):
    # if we already have an entry in our database , we're just going to grab that entry and return it
    # we're going to grab the id of that entry and return it
    profile_values = personal_data_collection.find_one(
        {"_id": {"$eq": _id}}
    )  # this is available in datastax documentation
    return profile_values

def get_notes(_id):
    """Get the Notes associated with that profile"""
    return list(notes_collection.find({"user_id":{"$eq":_id}}))