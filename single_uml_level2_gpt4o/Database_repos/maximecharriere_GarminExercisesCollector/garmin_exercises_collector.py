import requests
import pandas as pd
import pickle
from googleapiclient.discovery import build
from google.oauth2 import service_account

class GarminExercisesCollector:
    def __init__(self):
        self.locale = 'en'
        self.base_url = 'https://connect.garmin.com/'
        self.exercises_url = f'{self.base_url}exercise/exercises'
        self.yoga_url = f'{self.base_url}exercise/yoga'
        self.pilates_url = f'{self.base_url}exercise/pilates'
        self.mobility_url = f'{self.base_url}exercise/mobility'
        self.equipment_url = f'{self.base_url}exercise/equipment'
        self.translations_url = f'{self.base_url}exercise/translations'
        self.detailed_data_based_url = f'{self.base_url}exercise/details'
        self.detailed_page_based_url = f'{self.base_url}exercise/page'
        
        self.df_exercises = pd.DataFrame()
        self.df_yoga = pd.DataFrame()
        self.df_pilates = pd.DataFrame()
        self.df_mobility = pd.DataFrame()
        
        self.translations = {}
        self.all_muscles = set()
        self.all_equipment = set()

    def fetch_json(self, url):
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def fetch_translations(self):
        self.translations = self.fetch_json(self.translations_url)

    def get_exercise_name(self, category, name):
        return self.translations.get(category, {}).get(name, name)

    def process_exercises_data(self):
        data = self.fetch_json(self.exercises_url)
        self.df_exercises = pd.DataFrame(data)

    def process_yoga_data(self):
        data = self.fetch_json(self.yoga_url)
        self.df_yoga = pd.DataFrame(data)

    def process_pilates_data(self):
        data = self.fetch_json(self.pilates_url)
        self.df_pilates = pd.DataFrame(data)

    def process_mobility_data(self):
        data = self.fetch_json(self.mobility_url)
        self.df_mobility = pd.DataFrame(data)

    def process_equipment_data(self):
        data = self.fetch_json(self.equipment_url)
        self.all_equipment = set(data)

    def clean_spreadsheet(self, sheets_service, spreadsheet_id):
        sheets = sheets_service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute().get('sheets', [])
        for sheet in sheets:
            sheets_service.spreadsheets().batchUpdate(
                spreadsheetId=spreadsheet_id,
                body={
                    'requests': [
                        {'deleteSheet': {'sheetId': sheet['properties']['sheetId']}}
                    ]
                }
            ).execute()

    def update_sheet(self, sheets_service, spreadsheet_id, sheet_name, dataframe):
        sheets_service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body={
                'requests': [
                    {'addSheet': {'properties': {'title': sheet_name}}}
                ]
            }
        ).execute()
        values = [dataframe.columns.tolist()] + dataframe.values.tolist()
        sheets_service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=sheet_name,
            valueInputOption='RAW',
            body={'values': values}
        ).execute()

    def export_to_google_sheets(self):
        credentials = service_account.Credentials.from_service_account_file('path/to/credentials.json')
        sheets_service = build('sheets', 'v4', credentials=credentials)
        spreadsheet_id = self.get_spreadsheet_id(sheets_service)
        if not spreadsheet_id:
            spreadsheet = sheets_service.spreadsheets().create(body={
                'properties': {'title': 'Garmin Exercises Data'}
            }).execute()
            spreadsheet_id = spreadsheet['spreadsheetId']
            with open('spreadsheet_id.pkl', 'wb') as f:
                pickle.dump(spreadsheet_id, f)
        self.clean_spreadsheet(sheets_service, spreadsheet_id)
        self.update_sheet(sheets_service, spreadsheet_id, 'Exercises', self.df_exercises)
        self.update_sheet(sheets_service, spreadsheet_id, 'Yoga', self.df_yoga)
        self.update_sheet(sheets_service, spreadsheet_id, 'Pilates', self.df_pilates)
        self.update_sheet(sheets_service, spreadsheet_id, 'Mobility', self.df_mobility)

    def get_spreadsheet_id(self, drive_service):
        try:
            with open('spreadsheet_id.pkl', 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            return None

    def delete_spreadsheet(self, drive_service):
        spreadsheet_id = self.get_spreadsheet_id(drive_service)
        if spreadsheet_id:
            drive_service.files().delete(fileId=spreadsheet_id).execute()
            os.remove('spreadsheet_id.pkl')

    def compare_data(self, current_data, new_data):
        return current_data.equals(new_data)

    def run(self):
        self.fetch_translations()
        self.process_exercises_data()
        self.process_yoga_data()
        self.process_pilates_data()
        self.process_mobility_data()
        self.process_equipment_data()
        self.export_to_google_sheets()

collector = GarminExercisesCollector()
collector.run()