from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from models import Calendar, Event

class GoogleCalendarClient():
    """Google Calendar Client.
    
    Based on given credentials in credentials.json downloaded from google site
    Allows to download events information based on calendars names.
    
    The event model transform the time types and add values like event duration.
    """
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
    
    def __init__(self):
        self.SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
        credentials = self._get_or_create_credentials()
        self.SERVICE = build('calendar', 'v3', credentials=credentials)
        self.CALENDARS = self._get_calendars()
    
    def get_calendar_events(self, calendar_name: str):
        """Get calendar events.
        
        List of Event with the information that you need to make analisis.
        This function acept on
        """
        
        calendar = self._get_calendar_by_name(calendar_name)
        crud_events = self.SERVICE.events().list(
            calendarId=calendar.id, 
            orderBy='startTime',
            singleEvents=True,
        ).execute()
        events = self._get_cleaned_events(crud_events['items'], calendar_name)
        return events
    
    def _get_cleaned_events(self, crud_events: list, calendar_name: str):
        """Celaned events
        
        Get the raw events from the calendar and transform into a class with the 
        values that we need
        """
        events = []
        for event in crud_events:
            events.append(
                Event(
                    calendar=calendar_name,
                    summary=event['summary'],
                    start_date=event['start']['dateTime'],
                    end_date=event['end']['dateTime'],
                    creator=event['creator']['email'],
                )
            )
        return events
        
    def _get_calendar_by_name(self, name: str):
        for calendar in self.CALENDARS:
            if calendar.name == name:
                return calendar
        return f"No calendar with '{name}' name" 
    
    def _get_calendars(self):
        """Get teh calendars for the account
        
        Use the account to get a list of Calendars
        """
        calendars = []
        page_token = None
        while True:
            calendar_list = self.SERVICE.calendarList().list(pageToken=page_token).execute()
            for calendar_list_entry in calendar_list['items']:
                calendars.append(
                    Calendar(
                        id=calendar_list_entry['id'],
                        name=calendar_list_entry['summary'],
                        color=calendar_list_entry['backgroundColor']
                    )
                )
                page_token = calendar_list.get('nextPageToken')
            if not page_token:
                break     
        return calendars
        
    def _get_or_create_credentials(self):
        """Create credentiasl to login.
        The file token.pickle stores the user's acces and refresh tokens, and is
        created automatically when the authorization flow complets for the first
        time
        """
        credentials = None
        
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                credentials = pickle.load(token)
                
        # If there are no (valid) credentials available, let the user log in.
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                credentials = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(credentials, token)
        
        return credentials

