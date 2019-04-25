from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from task import Task
from datetime import timedelta 


TOMATO = 'YouTube'
FLAMINGO = ''
BANANA = ''
TANGERINE = ''
SAGE = 'My Apps'
BASIL = 'App'
PEACOCK = 'Exercise'
BLUEBERRY = ''
LAVENDER = ''
GRAPE = 'Work'
GRAPHITE = 'School'

EVENTS_TO_LOOK_THROUGH = 60

color_activity = {
		0 : LAVENDER,
		1 : BLUEBERRY,
		2 : PEACOCK,
		3 : SAGE,
		4 : BASIL,
		5 : TANGERINE,
        6 : BANANA,
        7 : FLAMINGO,
        8 : TOMATO,
        9 : GRAPE,
        10 : GRAPHITE,
	}

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    start_day = datetime.datetime.utcnow()
    now = (datetime.datetime.utcnow()- timedelta(start_day.weekday())).isoformat() + 'Z' # 'Z' indicates UTC time
    week_end_time = str(datetime.datetime.utcnow() + timedelta(days=7)) + 'Z'
    print('Getting the upcoming 10 events')
    print('**************************************************************\n')
    events_result = service.events().list(calendarId='primary', timeMin=now, 
                                        maxResults=EVENTS_TO_LOOK_THROUGH, singleEvents=True,
                                        orderBy='startTime').execute()
    colors = service.colors().get(fields='event').execute()
    events = events_result.get('items', [])
    tasks = []

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        if start > week_end_time:
            GREATER = True
        else:
            array_of_start_time = start.split("T")
            date = array_of_start_time[0]
            total_start_times = array_of_start_time[(len(array_of_start_time))-1]
            start_time = total_start_times.split(":")[0] + ":" + total_start_times.split(":")[(len(array_of_start_time))-1]
        
            array_of_end_time = end.split("T")
            total_end_times = array_of_end_time[(len(array_of_end_time))-1]
            end_time = total_end_times.split(":")[0] + ":" + total_end_times.split(":")[(len(array_of_end_time))-1]

            name = event['summary']
            try: 
                color = colors['event'][event['colorId']]['background']
                if color == "#a4bdfc":
                    color=0
                if color == "#5484ed":
                    color=1
                if color == "#46d6db":
                    color=2
                if color == "#7ae7bf":
                    color=3
                if color == "#51b749":
                    color=4
                if color == "#ffb878":
                    color=5
                if color == "#fbd75b":
                    color=6
                if color == "#ff887c":
                    color=7
                if color == "#dc2127":
                    color = 8
                if color == "#dbadff":
                    color =9
                if color == "#e1e1e1":
                    color = 10
            except Exception as e:
                color = 2
            task = Task(name, start_time, end_time, color)
            task.date = date
            task.get_time_of_task()
            tasks.append(task)
    
    total_tasks = []
    for i in range(0,11):
        if len(color_activity[i]) > 1: 
            new_task = Task(color_activity[i], 0, 0, i )
            for task in tasks:
                if task.color == i:
                    new_task.total_time += task.total_time
            text = "For " + new_task.name + " you have planned to spend:"
            number_of_spaces = 15
            number_of_spaces -= len(new_task.name)
            string_length=len(text)+number_of_spaces    # will be adding 10 extra spaces
            string_revised=text.ljust(string_length)
            print("\n-----------------------------------------------------------------")
            print(string_revised + str(new_task.total_time) + "hrs this week")
    print("\n-----------------------------------------------------------------\n")
    print("\n********************************************************\n")
                




if __name__ == '__main__':
    main()

            # if color == "#a4bdfc":
            #     color='LAVENDER'
            # if color == "#5484ed":
            #     color='BLUEBERRY'
            # if color == "#46d6db":
            #     color='PEACOCK'
            # if color == "#7ae7bf":
            #     color='SAGE'
            # if color == "#51b749":
            #     color='BASIL'
            # if color == "#ffb878":
            #     color'TANGERINE'
            # if color == "#fbd75b":
            #     color='BANANA'
            # if color == "#ff887c":
            #     color='FLAMINGO'
            # if color == "#dc2127":
            #     color = 'TOMATO'

            # if color == "#dbadff":
            #     color ='GRAPE'
            # if color == "#e1e1e1":
            #     color = 'GRAPHITE'