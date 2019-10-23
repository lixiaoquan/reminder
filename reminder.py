import re
from datetime import datetime, timedelta
import evernote.edam.type.ttypes as Types
from evernote.api.client import EvernoteClient, NoteStore

class Study(object):
    def __init__(self, name, time):
        self.name = name
        self.time = datetime.strptime(time, "%Y-%m-%d")


def create_note(note_store, notebook_guid, title, content = None):
    note = Types.Note()
    note.title = title
    note.content = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
    note.content += '<en-note>'
    note.content += content or ''
    note.notebookGuid = notebook_guid
    note.content += '</en-note>'
    note_store.createNote(note)

fobj = open('/home/xiaoquan.li/.yx_token', 'r')
token = fobj.readlines()[0][:-1]

client = EvernoteClient(token=token, service_host='app.yinxiang.com')

note_store = client.get_note_store()

notebook_review = None

# Make API calls
notebooks = note_store.listNotebooks()
for notebook in notebooks:
    if notebook.name == 'Review':
        notebook_review = notebook

assert notebook_review

# Get note
f = NoteStore.NoteFilter()
f.notebookGuid = notebook_review.guid
note_first_day_guid = None
for note in note_store.findNotes(token, f, 0, 999).notes:
    if note.title == 'first_day':
        note_first_day_guid = note.guid

# Get study
note_first_day = note_store.getNoteContent(token, note_first_day_guid)

print(note_first_day)

content = re.compile(r">(.*?)<").findall(note_first_day)

record = []

for c in content:
    if c is not '':
        tmp = c.split()
        record.append(Study(tmp[0], tmp[1]))


tomorrow = datetime.today() + timedelta(days=1)

# Create tomorrow's review list
create_note(note_store, notebook_review.guid, tomorrow.strftime("%Y-%m-%d Highend English"), 'test')
