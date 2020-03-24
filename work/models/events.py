"""Event model."""

# Utils
from datetime import datetime


class Event:
    """Event model.
    
    Store main properties of the event.
    Manage to transform string to dates and calculate event duration in seconds.
    """
    
    def __init__(self, calendar:str, sumary:str, start_date: str, end_date: str, creator:str):
        _start_date = self._string_to_date_time(start_date)
        _end_date = self._string_to_date_time(end_date)
        
        self.calendar = calendar
        self.sumary = sumary
        self.start_date = _start_date.date()
        self.end_date = _end_date.date()
        self.start_time = _start_date.time()
        self.end_time = _end_date.time()
        self.event_duration_seconds = self._get_event_duation_in_seconds(_start_date, _end_date)
        self.creator = creator
    
    def _string_to_date_time(self, date):
        return datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z')
        
    def _get_event_duation_in_seconds(self, start_date, end_date):
        event_duration = end_date - start_date
        return event_duration.total_seconds()
        
    def __str__(self):
        return f"{self.calendar} - {self.sumary} - {self.start_date}"
    
    def __repr__(self):
        return f"{self.calendar} - {self.sumary} - {self.start_date}"