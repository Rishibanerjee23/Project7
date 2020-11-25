import json, time

# This global dictionary stores the name of the room as the key and the dictionary describing the room as the value.
GAME = {
    '__metadata__': {
        'title': 'The forgetful farmer who doesnt know where the keys to Pig pen are',
        'start': 'Pig_pen'
    }
}



def create_room(name, description, ends_game=False, first_time=None):
    assert (name not in GAME)
    room = {'name': name,'description': description,'exits': [],'items': []}
    # Is there a special message for the first visit?
    if first_time:
        exit['first_time'] = first_time
    # Does this end the game?
    if ends_game:
        room['ends_game'] = ends_game

    # Stick it into our big dictionary of all the rooms.
    GAME[name] = room
    return room

def create_exit(source, destination, description, required_key=None, hidden=False):
    # Make sure source is our room!
    if isinstance(source, str):
        source = GAME[source]
    # Make sure destination is a room-name!
    if isinstance(destination, dict):
        destination = destination['name']
    # Create the "exit":
    exit = {
        'destination': destination,
        'description': description
    }
    # Is it locked?
    if required_key:
        exit['required_key'] = required_key
    # Do we need to search for this?
    if hidden:
        exit['hidden'] = hidden
    source['exits'].append(exit)
    return exit

car_keys = "car keys"
pig_pen_key = "pig pen key"
house_key = "crowbar"
phone = "phone"
    
Pig_pen = create_room("Pig_pen", """Awe shucks. The Pigs need feeding. Where are the keys? """)

Pig_pen["items"].append("phone")
create_exit(Pig_pen, "chicken_coop", "Search in the chicken coop.")
create_exit(Pig_pen, "outside_house", "Head towards the house ")
create_exit(Pig_pen, "outside_car", "Head towards the car")
create_exit(Pig_pen, "unlock_pig_pen", "Unlock the pig pen",required_key = pig_pen_key)

chicken_coop = create_room("chicken_coop", """You are in the chicken coop. Where are the keys ?""")
create_exit(chicken_coop, Pig_pen, "Go back to the pig pen.")
create_exit(chicken_coop, "shed", "Maybe I left them in the shed?" )

shed = create_room("shed", """You are in the shed.... There is lots of stuff in here.""")
shed["items"].append("crowbar")
shed["items"].append("shovel")
shed["items"].append("rake")


create_exit(shed, chicken_coop , "Go back to the chicken coop")
create_exit(shed, "outside_house", "Go the house")


outside_house = create_room("outside_house", """The door is locked and can't get in. Find some tools to break into the house.""")
create_exit(outside_house, shed, "Go back to the shed")
create_exit(outside_house, "house", "Enter House",required_key = house_key)


house = create_room("house", """You are now inside your house and it is the only place with cellular service . The pig pen keys aren't here.""")
house["items"].append("car keys")
create_exit(house, "outside_car", "go check your car", required_key = car_keys)
create_exit(house, "Call_jim", "Call your buddy Jim to help you out", required_key = phone )
create_exit(house, "Pig_pen", "Go Back to the pig pen")

create_room("Call_jim", """Jim has comeover and helped you out.....Still need to find your keys!""", ends_game=True)

outside_car = create_room("outside_car", """You are outside your car. You think you might've left the pig pen keys in here.""")
create_exit(outside_car, "inside_car", "Enter the car", required_key = car_keys)
create_exit(outside_car, house, "Go back inside the house.")

inside_car = create_room("inside_car", """You are inside your car. You have a feeling that that they are in here""")
create_exit(inside_car, "glovebox", "Search the glovebox")
create_exit(inside_car, "floor", "check the floor")
create_exit(inside_car, "dashboard", "Check the dashboard")

glovebox = create_room("glovebox", """Nothing in glovebox""")
create_exit(glovebox, "floor", "Search the floor")
create_exit(glovebox, "dashboard", "Search the dashboard")



floor = create_room("floor", """Look's like the keys are not on the floor, Check somewhere else.""")
create_exit(floor, "dashboard", "Check the dashboard")
create_exit(floor, "glovebox", "Check the glovebox.")

dashboard = create_room("dashboard", """You have found the keys!Make sure to take them to the pig pen""")

create_exit(dashboard, "Pig_pen", "go back to the pig pen")
dashboard["items"].append("pig pen key")
unlock_pig_pen = create_room("unlock_pig_pen", """You unlock the pig pen and feed your pigs.
""", ends_game=True)



##
# Save our text-adventure to a file:
##
with open('adventuregamerish.json', 'w') as out:
    json.dump(GAME, out, indent=2)