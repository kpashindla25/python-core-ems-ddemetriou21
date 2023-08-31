from datetime import date
import json

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
