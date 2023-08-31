from datetime import date
import json
from classes_ems import * 

# function to list attendees based off of an event no.
def list_attendees(event_no):
    event = events.get(event_no)
    if event: # if statement checking if event is in records
        attendees_found = False 
        for attendee_no, attendee in attendees.items(): # for loop to iterate through dictionary 
            if attendee.event_no == event.event_no:
                print(f"\nAttendees for Event {event_no}:")
                print("------------------------------------")
                print(f"Attendee No. {attendee_no}: {attendee.name}")  
                attendees_found = True
        if not attendees_found:
            print("\nNo attendees found for event.")

# function listing all events using for loop to iterate through relevant dictionary
def list_all_events():
    if not events:
        print("\nNo events found.")
    else:
        for event_no, event in events.items():
            print('------------------------------------------------------------------------------------------------------------------------')
            print(f"Event No. {event_no}: {event.event_name}, Venue Name: {event.event_venue[0]}, Capacity: {event.event_venue[1]}, Location: {event.event_venue[2]},  Date: {event.event_date}")

# function listing a singular event
def list_event():
    user_input = input("\nEnter Event No. to list: ")    
    event_no = user_input
    event = events.get(event_no)
    if event:
        print("------------------------------------------------------------------------------------------------------------------------")
        print(f"Event {event_no}: {event.event_name}, Venue Name: {event.event_venue[0]}, Capacity: {event.event_venue[1]}, Location: {event.event_venue[2]},  Date: {event.event_date}")
    else:
        print("\nEvent not found.")  

# function that loads data from events and attendees files
def load_data_from_files():
    try:   # try / except block displaying error message if no file was found and starting with an empty dictionary.
        with open("events_data.json", "r") as events_file:
            events_data = json.load(events_file)
            global events
            events = {event_no: Event.from_dict(event_data) for event_no, event_data in events_data.items()}
    except FileNotFoundError:
        print("Events data file not found. Starting with empty events dictionary.")
        events = {event_no: Event.from_dict(event_data) for event_no, event_data in events.items()}

    try:  # try / except block displaying error message if no file was found and starting with an empty dictionary.
        with open("attendees_data.json", "r") as attendees_file:
            attendees_data = json.load(attendees_file)
            global attendees
            attendees = {attendee_no: Attendee.from_dict(attendee_data) for attendee_no, attendee_data in attendees_data.items()}
    except FileNotFoundError:
        print("\nAttendees data file not found. Starting with empty attendees dictionary.")
        attendees = {attendee_no: Attendee.from_dict(attendee_data) for attendee_no, attendee_data in attendees.items()}

# function saving the data to their appropriate files. 
def save_data_to_files():
    with open("events_data.json", "w") as events_file:
        json.dump(events, events_file, indent=4, default=serialize_event)
    
    with open("attendees_data.json", "w") as attendees_file:
        json.dump(attendees, attendees_file, indent=4, default=serialize_attendee)

# function that handles the data to be inputted in the correct format for the attendees JSON file 
def serialize_attendee(obj):
    if isinstance(obj, Attendee):
        return {
            "attendee_no": obj.attendee_no,
            "event_no": obj.event_no,
            "name": obj.name,
            "phone": obj.phone,
            "email": obj.email
        }
    raise TypeError("Object of type Attendee is not JSON serializable")

# function that handles the data to be inputted in the correct format for the events JSON file 
def serialize_event(obj):
    if isinstance(obj, Event):
        return {
            "event_no": obj.event_no,
            "event_name": obj.event_name,
            "date": obj.event_date.strftime("%Y-%m-%d") if isinstance(obj.event_date, date) else obj.event_date, 
            "event_venue": obj.event_venue,
            "attendees": obj.attendees
        }
    raise TypeError("Object of type Event is not JSON serializable")

# main function for the entire system
def main():
    while True: # while loop ensuring the program keeps running till user exits the system
        print("\n---------------------------\n| Event Management System |\n---------------------------")
        print("\nPlease select one of the following options: \n[1] List Events \n[2] List Attendees \n[3] Customize Events \n[4] Customize Atteendees \n[5] Exit")
        user_input = input("\n")

        # if / elif statements based on user input 
        if user_input == '5' or user_input.lower() == 'exit':
            print("\nGoodbye!")
            break

        elif user_input == '1':
            load_data_from_files() # calling load data function 
            while True: 
                event_listing = input("\nSelect an option: \n[1] All Events  \n[2] Event\n")
                if event_listing.lower() == 'all' or event_listing.lower() == 'all events' or event_listing == '1':
                    list_all_events() # calling list all events function 
                    break
                elif event_listing.lower() == 'event' or event_listing == '2':
                    list_event() # calling list event function 
                    break
                else:
                    print("\nInvalid choice. ")

        elif user_input == '2':
            load_data_from_files() # load data function
            list_all_events() # calling list all events function so user knows event numbers 
            while True:
                event_no = input("\nEnter Event no. to list attendees: ")
                if event_no in events:
                    list_attendees(event_no) # list attendees function with event no. as argument 
                    break 
                else:
                    print("\nEvent not found.")
                    break
                                   
        elif user_input == '3':
            load_data_from_files() # calling load data function 
            while True:
                user_choice = input("\nSelect an option: \n[1] Create an event \n[2] Edit an event \n[3] Delete an event\n")
                if user_choice.lower() == 'create' or user_choice == '1':
                    try: # try / except block for value error for the num_events prompt
                        num_events = int(input("\nEnter the number of events to create: ")) # user input to create a number of events 
                        for x in range(num_events):  # for loop to create number of events based off of user input 
                            Event.create(Event)      # calling create event method 
                            save_data_to_files()     # calling save data function 
                        break
                    except ValueError:
                        print("Invalid input. Please provide valid inputs for event creation.")
                elif user_choice.lower() == 'edit' or user_choice == '2':
                            event_no = input("\nEnter Event No. to edit: ")
                            event = events.get(event_no)
                            if not event:
                                print("\nEvent not found.")
                            else:
                                event.edit()
                                save_data_to_files() # calling save data function 
                                break
                elif user_choice.lower() == 'delete' or user_choice == '3':
                    event_no = input("\nEnter Event No. to delete: ")
                    event = events.get(event_no)
                    if event:
                        event.delete(event_no) # calling event delete method
                        save_data_to_files() # calling save data function 
                        break  
                    else:
                        print("\nEvent not found.")
                else:
                    print("Invalid choice.")

        elif user_input == '4':
            load_data_from_files() # load data function 
            user_edit = input("\nSelect an option: \n[1] Add an attendee  \n[2] Delete an attendee \n[3] Edit an attendee\n")
            if user_edit.lower() == 'add' or user_edit == '1':
                list_all_events()  # call list all events function so user knows which events are available
                while True:
                    event_no = input("\nEnter Event No. to add attendee: ")
                    if event_no not in events:
                        print("\nEvent not found.")
                    else:
                        while True:
                            try: # try / except block for value error on num_attendees
                                num_attendees = int(input("\nEnter the number of attendees to create: ")) # user input to create a number of attendees
                                break
                            except ValueError:
                                print("Invalid number. Please enter a valid number.")
                        for x in range(num_attendees):  # for loop to create a number of attendees based of user input 
                            Attendee.create(event_no)  # create attendee method with event no. as argument 
                            save_data_to_files() # save data function 
                        break
            elif user_edit.lower() == 'delete' or user_edit == '2': 
                attendee_no = input("\nEnter Attendee No. you wish to delete: ")
                attendee = attendees.get(attendee_no) # getting attendee no. from attendee dictionary 
                if attendee:
                    attendee.delete() # calling delete attendee method 
                    save_data_to_files() # save data function 
                else:
                    print("\nAttendee not found.")            
            elif user_edit.lower() == 'edit' or user_edit == '3':
                attendee_no = input("\nEnter Attendee No. you wish to edit: ")
                attendee = attendees.get(attendee_no) # getting attendee no. from attendee dictionary 
                if attendee:
                    attendee.edit() # edit attendee method 
                    save_data_to_files() # save data function 
                else:
                    print("\nAttendee not found.")
            
        else:
            print("\nInvalid choice.")

if __name__ == "__main__":  # calling main function 
    main()