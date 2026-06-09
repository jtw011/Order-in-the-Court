
# Store lists in a list of lists, where each inner list represents a round
all_lists = [[]]  # Start with one empty list for initial names

# The logic for where the PO enters the round information
def po():
    name = input("Enter the P.O's name: ")
    round_name = input("Enter the round name: ")
    room_number = input("Enter the room number: ")
    
    while True:
        person = input("Enter names (type quit to end): ")
        if person.lower() == 'quit':
            print(f"\nInfo has been added. Thank you!")
            break
        else:
            all_lists[0].insert(0, person)

    return name, round_name, room_number

# The logic for viewers information
def viewer(name, round_name, room_number):
    print("------------------------------------")
    print(f"\nViewer Information")
    print(f"P.O: {name}")
    print(f"Round Name: {round_name}")
    print(f"Room Number: {room_number}")
    
    # Print all non-empty lists
    for list_num, current_list in enumerate(all_lists):
        if current_list:  # Only print non-empty lists
            print(f"\nList {list_num}: ")
            for index, item in enumerate(current_list):
                print(f"{index}: {item}")
    print("------------------------------------")
    print()

# Logic for moving people over to the next list
def move_to_next_list(source_list_index, person_index):
    if 0 <= source_list_index < len(all_lists) and 0 <= person_index < len(all_lists[source_list_index]):
        # If we're moving from the last available list, create a new one
        if source_list_index == len(all_lists) - 1:
            all_lists.append([])
            
        # Move the person
        person = all_lists[source_list_index][person_index]
        all_lists[source_list_index + 1].append(person)
        del all_lists[source_list_index][person_index]
        
        # Remove empty lists (except the first one)
        for i in range(len(all_lists) - 1, 0, -1):  # Start from the end, go backwards
            if not all_lists[i]:
                del all_lists[i]
        
        return True
    return False

# Where the magic happens!
def main():
    print()
    print("Welcome to the Recency Tracker!")
    po_name = po_round = po_room = None
    
    while True:
        print()
        print("Please pick an option: ")
        print("1. P.O Area")
        print("2. Viewer Area")
        print("3. Move Person Forward")
        print("4. Quit")
        user = input("> ").strip()
        print()
        
        if user == "1":
            po_name, po_round, po_room = po()
        
        elif user == "2":
            if po_name and po_round and po_room:
                viewer(po_name, po_round, po_room)
            else:
                print("Please enter P.O info first.")    
        
        elif user == "3":
            if not po_name:
                print("Please enter P.O info first.")
                continue
                
            viewer(po_name, po_round, po_room)
            try:
                list_num = int(input("Enter the list number to move from: "))
                if 0 <= list_num < len(all_lists):
                    person_index = int(input("Enter the index of the person to move: "))
                    if move_to_next_list(list_num, person_index):
                        print("Person moved successfully.")
                        # Show updated lists
                        viewer(po_name, po_round, po_room)
                    else:
                        print("Invalid person index.")
                else:
                    print("Invalid list number.")
            except ValueError:
                print("Please enter valid numbers.")

        elif user == "4":
            print("Goodbye!")
            break
        else:
            print("Not an option. Try again")

if __name__ == "__main__":
    main()