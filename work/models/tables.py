"""Table models.

This file will contains the diferent models to analyze de data.
"""

# Models
from .events import Event


class Summary:
    """summary model.
    
    Generate a Summary with the following properties:
        - issue
        - repository
        - description
        - help
    """
    
    def __init__(self, summary):
        self.issue = self._get_issue(summary)
        self.repository = self._get_repository(summary)
        self.description = self._get_description(summary)
        self.help = self._get_help(summary)
        
    def _get_issue(self, summary):
        start_index = summary.find("[") + 1
        end_index = summary.find("]")
        return summary[start_index:end_index]
        
    def _get_repository(self, summary):
        start_index = summary.find("]") + 2
        end_index = summary.find("-")
        return summary[start_index:end_index]
        
    def _get_description(self, summary):
        start_index = summary.find("-") + 2
        end_index = summary.find("|")
        return summary[start_index:end_index]
        
    def _get_help(self, summary):
        start_index = summary.find("|")+2
        return summary[start_index:]
    

class GoogleCalendarTable:
    """Google Calendar Table
    
    This model will get the events from google calendar and
    will put it on a structure that pandas can handle.
    """
    
    def __init__(self):
        self.calendar = list()
        self.issue = list()
        self.repository = list()
        self.description = list()
        self.start_date = list()
        self.end_date = list()
        self.start_time = list()
        self.end_time = list()
        self.event_duration_seconds = list()
        self.creator = list()
        self.help = list()
        
    
    def events_to_table(self, events: list):
        for event in events:
            summary = Summary(event.summary)
            self._generate_row(event, summary)
        return self
        
    def _generate_row(self, event: Event, summary):
        self.calendar.append(event.calendar)
        self.issue.append(summary.issue)
        self.repository.append(summary.repository)
        self.description.append(summary.description)
        self.start_date.append(event.start_date)
        self.end_date.append(event.end_date)
        self.start_time.append(event.start_time)
        self.end_time.append(event.end_time)
        self.event_duration_seconds.append(event.event_duration_seconds)
        self.creator.append(event.creator)
        self.help.append(summary.help)



