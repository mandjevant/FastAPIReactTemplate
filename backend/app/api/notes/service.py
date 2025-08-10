from sqlmodel import Session, select
from app.models import Note
from typing import List, Optional
import uuid


class NoteService:
    """Service class for Note CRUD operations."""

    @staticmethod
    def get_notes(db: Session, user_id: uuid.UUID) -> List[Note]:
        """Get all notes for a user.

        Parameters
        ----------
        db : Session
            Database session.
        user_id : uuid.UUID
            The user's unique identifier.

        Returns
        -------
        List[Note]
            List of notes belonging to the user.
        """
        return list(db.exec(select(Note).where(Note.user_id == user_id)).all())

    @staticmethod
    def get_note(db: Session, note_id: int, user_id: uuid.UUID) -> Optional[Note]:
        """Get a single note by id for a user.

        Parameters
        ----------
        db : Session
            Database session.
        note_id : int
            Note primary key.
        user_id : uuid.UUID
            The user's unique identifier.

        Returns
        -------
        Optional[Note]
            The note if found, else None.
        """
        return db.exec(
            select(Note).where(Note.id == note_id, Note.user_id == user_id)
        ).first()

    @staticmethod
    def create_note(db: Session, title: str, content: str, user_id: uuid.UUID) -> Note:
        """Create a new note for a user.

        Parameters
        ----------
        db : Session
            Database session.
        title : str
            Note title.
        content : str
            Note content.
        user_id : uuid.UUID
            The user's unique identifier.

        Returns
        -------
        Note
            The created note.
        """
        note = Note(title=title, content=content, user_id=user_id)
        db.add(note)
        db.commit()
        db.refresh(note)
        return note

    @staticmethod
    def delete_note(db: Session, note_id: int, user_id: uuid.UUID) -> bool:
        """Delete a note by id for a user.

        Parameters
        ----------
        db : Session
            Database session.
        note_id : int
            Note primary key.
        user_id : uuid.UUID
            The user's unique identifier.

        Returns
        -------
        bool
            True if deleted, False if not found.
        """
        note = db.exec(
            select(Note).where(Note.id == note_id, Note.user_id == user_id)
        ).first()
        if note:
            db.delete(note)
            db.commit()
            return True
        return False
