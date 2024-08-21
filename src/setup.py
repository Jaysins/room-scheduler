def ensure_default_room():
    """ Ensure that there is at least one room in the database. """
    from .models import db, Room
    try:
        # Check if there are any rooms in the database
        if not db.session.query(Room).first():
            # If no rooms exist, add a default room
            default_room = Room(name="Default Room", capacity=1, number=1, type='suite')
            db.session.add(default_room)
            db.session.commit()
            print("Default room added to the database.")
        else:
            print("Rooms already exist in the database.")
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred: {e}")
