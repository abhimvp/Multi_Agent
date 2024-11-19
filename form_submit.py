# write the function that will update the data for us
from datetime import datetime
from db import personal_data_collection,notes_collection
def update_personal_info(existing,update_type,**kwargs):
    """
    - **kwargs - a dictionary containing all of the key value pairs
    Idea is to make this a general function that will allow us to update any of the fields in the database
    - existing: the existing data that we have in the database
    - update_type: the type of update that we want to make
    - **kwargs: the fields that we want to update
    - so we're going to update one of the fields at a time in database
    """

    if update_type == "goals":
        existing["goals"] = kwargs.get("goals", []) # if it's not passed it's going to be an empty llist
        update_field = {"goals": existing["goals"]}
    else:
        existing[update_type]=kwargs
        update_field = {update_type:existing[update_type]}
        
    personal_data_collection.update_one(
        {"_id": existing["_id"]}, # entry we want to update
        {"$set": update_field}
    )
        
def add_note(note,profile_id):
    new_note = {
        "user_id": profile_id,
        "text": note,
        "$vectorize":note, # when we do this , we can pass the type of content that we want to be vectorized in our vector database
        # what will happen is that in datastax astradb this will automatically convert this note into a vector be vectorized and stored in our vector database
        # and we can then use this to find similar notes
        "metadata": {"injested":datetime.now()} # Inorder for this to work we do need to pass a metadata field as well
    }
    
    result = notes_collection.insert_one(new_note) 
    new_note["_id"] = result.inserted_id
    return new_note

def delete_note(_id):
    notes_collection.delete_one({"_id":_id})



# earlier where we would need to kind of generate our own embedding model, use the embedding model
# create the vector , it'll just automatically be handled for us because we set that up in the astrdb database

