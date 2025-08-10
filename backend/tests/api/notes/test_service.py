import pytest
from app.api.notes.service import NoteService
import uuid


@pytest.fixture
def user_id():
    return uuid.uuid4()


def test_create_note(db_session, user_id):
    note = NoteService.create_note(db_session, "Title", "Content", user_id)
    assert note.title == "Title"
    assert note.content == "Content"
    assert note.user_id == user_id


def test_get_notes(db_session, user_id):
    notes = NoteService.get_notes(db_session, user_id)
    assert isinstance(notes, list)


def test_get_note_not_found(db_session, user_id):
    note = NoteService.get_note(db_session, 9999, user_id)
    assert note is None


def test_delete_note_not_found(db_session, user_id):
    result = NoteService.delete_note(db_session, 9999, user_id)
    assert result is False
