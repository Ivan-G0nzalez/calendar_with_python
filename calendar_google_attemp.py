from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import datetime



class GoogleAuthentification:
    def __init__(self, credentials_path="client_secret_google.json", token_path="token.json", SCOPE=["https://www.googleapis.com/auth/calendar"]):
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.scope = SCOPE

    def get_credentials(self):
        flow = InstalledAppFlow.from_client_secrets_file(
        self.credentials_path, 
        self.scope
    )
        creds = flow.run_local_server(port=0)
        return creds
    

class GoogleCalendar:
    def __init__(self, credentials):
        self.credentials = credentials
        self.service = self.build_services()


    def build_services(self):  
        return build("calendar", "v3", credentials=self.credentials)
    
    def create_event(self, summary, start_time, end_time, location=None):
        durantion = end_time - start_time
        max_duration = datetime.timedelta(minutes=40)

        if durantion > max_duration:
            print(f'La duración del evento excede el límite permitido de {max_duration}.')
            return
        
        event = {
            'summary': summary,
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': 'UTC',
            },
            'end': {
                'dateTime': end_time.isoformat(),
                'timeZone': 'UTC',
            },
            'location': location,
        }

        event = self.service.events().insert(calendarId='primary', body=event).execute()
        print(f'Event created: {event["htmlLink"]}')

    def delete_event(self, event_id):
        self.service.events().delete(calendarId='primary', eventId=event_id).execute()
        print(f'Event deleted: {event_id}')

    def get_events(self):
        now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
        print("Getting the upcoming 10 events")
        try:
            events_result = (
                self.service.events()
                .list(
                    calendarId="primary",
                    timeMin=now,
                    maxResults=10,
                    singleEvents=True,
                    orderBy="startTime",
                )
                .execute()
            )
            events = events_result.get("items", [])

            if not events:
                print("No upcoming events found.")
                return []

            # Return a list of dictionaries containing event information
            upcoming_events = []
            for event in events:
                start = event["start"].get("dateTime", event["start"].get("date"))
                upcoming_events.append({
                    "start": start,
                    "summary": event["summary"]
                })

            return upcoming_events

        except HttpError as error:
            print(f"An error occurred: {error}")
            return []

if __name__ == '__main__':
    authenticator = GoogleAuthentification()
    credentials = authenticator.get_credentials()

    calendar = GoogleCalendar(credentials)

    next_events = calendar.get_events()

    for event in next_events:
        print(event)

    # now = datetime.datetime.now()
    # next_tuesday = now + datetime.timedelta((1 - now.weekday() + 7) % 7)
    # start_time = datetime.datetime(next_tuesday.year, next_tuesday.month, next_tuesday.day, 10, 0, 0)
    # end_time = start_time + datetime.timedelta(minutes=40)

    # try:
    #     calendar.create_event(summary="Cita peluquería", start_time=start_time, end_time=end_time)
    # except ValueError as e:
    #     print(f'Error al crear evento: {e}')