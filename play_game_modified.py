import json, time



def main():
    # TODO: allow them to choose from multiple JSON files?
    games = ["spooky_mansion.json","adventuregamerish.json"]
    index = choose_from_list("Which game do you want to play?", games)
    if index < 0:
        print("Ok, bye!")
        return
   
    with open(games[index]) as fp:
        game = json.load(fp)
    print_instructions()
    print("You are about to play '{}'! Good luck!".format(game['__metadata__']['title']))
    print("")
    play(game)

def choose_from_list(qtext, opts):
    print(qtext)
    # the (+4) challenge here is the available list.
    available = []
    # I did show enumerate on the quiz, which might be better.
    for i in range(len(opts)):
        num = str(i+1)
        available.append(num)
        print("  ", num, ". ", opts[i], sep="")
    # slightly more clever than they achieve:
    return available.index(input("> "))
    # OK for the 8 points
    return int(input("> ")) + 1

def play(rooms):
    # Where are we? Look in __metadata__ for the room we should start in first.
    current_place = rooms['__metadata__']['start']
    # The things the player has collected.
    stuff = ['Cell Phone;']

    while True:
        # Figure out what room we're in -- current_place is a name.
        here = rooms[current_place]
        # Print the description.
        
        print(here["description"])
        if len(here['items'])>= 1:
            print("In the room there is", here['items'])
        else:
            print("")
            

        # TODO: print any available items in the room...
        # e.g., There is a Mansion Key.

        # Is this a game-over?
        if here.get("ends_game", False):
            break

        # Allow the user to choose an exit:
        usable_exits = find_visable_exits(here)
        # Print out numbers for them to choose:
        for i, exit in enumerate(usable_exits):
           print("  {}. {}".format(i+1, exit['description']))

        # See what they typed:
        action = input("> ").lower().strip()

        # If they type any variant of quit; exit the game.
        if action in ["quit", "escape", "exit", "q"]:
            print("You quit.")
            break
        if action == "help":
             print_instructions();
             continue
        if action == "stuff":
            if len(stuff)== 0:
                print("you have no stuff")
            else:
                print("here are your items",stuff)
            continue
       
       
        if action == "take":
            for i in (here['items']):
                stuff.append(i)
            here['items'].clear()
    
            continue
        if action == "drop":
            index = choose_from_list("What would you like to drop?", stuff);
            here['items'].append(stuff[index - 1])
            stuff.remove(stuff[index - 1]);
            continue
        if action == "search":
           dog = find_hidden_exits(here)
           for exit in dog:
               usable_exits.append(exit)
           print(usable_exits)
            
           continue
           
             
            
            
        
        
        
                
      
            
                     
                     
                   
            
            
                
         
            
            
      
            
            

        # TODO: if they type "stuff", print any items they have (check the stuff list!)
        # TODO: if they type "take", grab any items in the room.
        # TODO: if they type "search", or "find", look through any exits in the room that might be hidden, and make them not hidden anymore!
        
        # Try to turn their action into an exit, by number.
        try:
            num = int(action) - 1
            selected = usable_exits[num]
            if "required_key" in selected:
                if selected["required_key"] in stuff:
                    current_place = selected['destination']
                else:    
                    print("You don't have the items to do this!")
            else:
                current_place = selected['destination']
            
            print("...")
        
        except:
            print("I don't understand '{}'...".format(action))
        
        
    print("")
    print("")
    print("=== GAME OVER ===")


   

def find_visable_exits(room):
    """
    Given a room, and the player's stuff, find a list of exits that they can use right now.
   That means the exits must not be hidden, and if they require a key, the player has it.

   RETURNS
    - a list of exits that are visible (not hidden) and don't require a key!
"""
    usable = []
    for exit in room['exits']:
        if exit.get('hidden',False):
            continue
        usable.append(exit)
    return usable

          
def find_hidden_exits(room):
    hidden = []
    for exit in room['exits']:
        if exit.get('hidden',False):
        
            hidden.append(exit)
    return hidden
    

def print_instructions():
    print("=== Instructions ===")
    print(" - Type a number to select an exit.")
    print(" - Type 'stuff' to see what you're carrying.")
    print(" - Type 'take' to pick up an item.")
    print(" - Type 'quit' to exit the game.")
    print(" - Type 'search' to take a deeper look at a room.")
    print(" - Type 'help' to read instructions.")
    print("=== Instructions ===")
    print("")

if __name__ == '__main__':
    start_time = time.time() 
    main()
print("You eascaped in " , (time.time() - start_time), "seconds")

