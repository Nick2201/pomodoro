

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from pydub import AudioSegment
import io

# Authenticate with Google Drive
creds = Credentials.from_authorized_user_file("path/to/credentials.json")
service = build("drive", "v3", credentials=creds)

# Fetch the MP3 file from Google Drive
file_id = "0B6AV35TIZFRcNDZ5dlgwb1RzY0E"
file = service.files().get(fileId=file_id, fields="*").execute()
request = service.files().get_media(fileId=file_id)
stream = io.BytesIO(request.execute())

# Play the MP3 file using Pydub
sound = AudioSegment.from_file(stream, format="mp3")
play(sound)