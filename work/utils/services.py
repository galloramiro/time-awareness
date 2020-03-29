# Models
from models import GoogleCalendarTable

# Utils
from datetime import datetime
from os import getcwd, listdir
import pandas as pd
from pathlib import PurePosixPath
from .clients import GoogleCalendarClient


class CsvGeneratorService:
    
    def __init__(self, client=GoogleCalendarClient()):
        self.CLIENT = client
        self.DATA_PATH = f"{getcwd()}/data/"
        
    def generate_crud_csv_file(self, calendars_names: list):
        """Generate crud csv files based on a list of calendars names"""
        
        for calendar_name in calendars_names:
            calendar_events = self.CLIENT.get_calendar_events(calendar_name)
            gc_table = GoogleCalendarTable().events_to_table(calendar_events)
            df = pd.DataFrame(gc_table.__dict__)
            self._save_file(df, 'crud', calendar_name)
    
    def get_available_files_names(self):
        """Get the names of the files saved."""
        files = [file for file in listdir(self.DATA_PATH) if PurePosixPath(file).suffix == '.csv']
        print("Your available files are:")
        for file in files:
            print(f"  - '{file}'")
    
    def _file_to_data_frame(self, file_name: str):
        """Read de csv file and optimize the data"""
        
        file_path = f"{self.DATA_PATH}{file_name}"
        df = pd.read_csv(file_path)
        
        # Data optimization
        df["calendar"] = df["calendar"].astype("category")
        df["issue"] = df["issue"].astype("category")
        df["repository"] = df["repository"].astype("category")
        df["start_date"] = pd.to_datetime(df["start_date"])
        df["end_date"] = pd.to_datetime(df["end_date"])
        df["creator"] = df["creator"].astype("category")
        df["help"] = df["help"].astype("category")
        
        return df
    
    def _total_seconds_to_hours(self, total_seconds):
        """Transform the total_secods to hours and minutes"""
        hours = int(total_seconds//3600)
        minutes = int((total_seconds%3600) // 60)
        return f"{hours:02}:{minutes:02}"
    
    def _save_file(self, df, prefix, calendar_name):
        today = str(datetime.now().date())
        file_name = f"{prefix}_{today}_{calendar_name}.csv"
        df.to_csv(f"{self.DATA_PATH}{file_name}", index=False)
        print(f"The CSV was saved under the name: {file_name}")


class CsvByMonthService(CsvGeneratorService):
    
    def issues_and_total_hours_by_month(self, file_name: str):
        """Issues & total hours by month
        
        To improve:
          - add hours average by issue
        """
        df_base = self._file_to_data_frame(file_name)
        calendar_name = df_base["calendar"].iloc[0]
        df_issues_duration_by_month = self._issues_and_total_hours_by_month_df(df_base)
        
        self._save_file(df_issues_duration_by_month, 'by_month_and_total_hours', calendar_name)
    
    
    def issues_and_total_hours_by_repository_and_month(self, file_name: str):
        df_base = self._file_to_data_frame(file_name)
        calendar_name = df_base["calendar"].iloc[0]
        repositories = df_base['repository'].cat.categories
        df_final = pd.DataFrame()

        for repo in repositories:
            df_temp = df_base[df_base['repository'] == repo]
            df_temp = self._issues_and_total_hours_by_month_df(df_temp)
            df_temp['repository'] = repo
            df_final = df_final.append(df_temp, ignore_index=True)
        df_final.sort_values(by=['start_date', 'repository'], ascending=False, inplace=True)
        
        self._save_file(df_final, 'by_month_and_total_hours_by_repo_and_month', calendar_name)

    def _issues_and_total_hours_by_month_df(self, df_base):
        df_base.index = df_base["start_date"]
        df_base = df_base.groupby(pd.Grouper(freq='M'))

        series_issue = df_base["issue"].nunique()
        series_event_duration = df_base["event_duration_seconds"].sum()
        series_event_duration = series_event_duration.apply(self._total_seconds_to_hours)

        df_issues_and_duration_by_month = pd.concat(
                [series_issue, series_event_duration], 
                axis=1
            )
        df_issues_and_duration_by_month.rename(
                columns=dict(
                    issue="total_issues",
                    event_duration_seconds="total_hours"
                ),
                inplace=True
            )
        df_issues_and_duration_by_month.reset_index(
                level=None, 
                drop=False, 
                inplace=True,
            )
        return df_issues_and_duration_by_month

    