from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.api.deps import get_db, get_current_user
from app.models import Note, User
from app.api.notes.service import NoteService
from typing import List

router = APIRouter(prefix="/notes", tags=["notes"])


@router.get("/", response_model=List[Note])
def read_notes(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
) -> List[Note]:
    """Get all notes for the current user.

    Parameters
    ----------
    db : Session
        Database session.
    current_user : User
        The authenticated user.

    Returns
    -------
    List[Note]
        List of notes for the user.
    """
    return NoteService.get_notes(db, current_user.id)


@router.post("/", response_model=Note)
def create_note(
    note: Note,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Note:
    """Create a new note for the current user.

    Parameters
    ----------
    note : Note
        The note data from the request body.
    db : Session
        Database session.
    current_user : User
        The authenticated user.

    Returns
    -------
    Note
        The created note.
    """
    return NoteService.create_note(db, note.title, note.content, current_user.id)


@router.get("/{note_id}", response_model=Note)
def read_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Note:
    """Get a single note by id for the current user.

    Parameters
    ----------
    note_id : int
        The note's primary key.
    db : Session
        Database session.
    current_user : User
        The authenticated user.

    Returns
    -------
    Note
        The note if found.

    Raises
    ------
    HTTPException
        If the note is not found.
    """
    note = NoteService.get_note(db, note_id, current_user.id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    """Delete a note by id for the current user.

    Parameters
    ----------
    note_id : int
        The note's primary key.
    db : Session
        Database session.
    current_user : User
        The authenticated user.

    Raises
    ------
    HTTPException
        If the note is not found.
    """
    success = NoteService.delete_note(db, note_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Note not found")
