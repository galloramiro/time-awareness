"""Clendars model."""

class Calendar:
    """Calendar model.

    Store main properties of the calendar
    """
    
    def __init__(self, id:str, name: str, color:str):
        self.id = id
        self.name = name
        self.color = color
    
    def __str__(self):
        return f"Calendar: {self.name}"
    
    def __repr__(self):
        return f"Calendar: {self.name}"
