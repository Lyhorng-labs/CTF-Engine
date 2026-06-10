from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone

class Challenge(SQLModel, table=True):
    id: Optional[int]= Field(default=None, primary_key=True)#id mark optional cuz user first no id yet
    title: str= Field(index=True)# adding an index to title and user id for searching fast 
    description: str
    difficulty: str
    points: int
    expected_flag: str
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class Submission(SQLModel, table=True):
    id: Optional[int]= Field(default=None, primary_key=True)
    challenge_id: int =Field(foreign_key="challenge.id")# link a submission directly to specific Challenge
    user_id: int = Field(index=True)
    submitted_code: str
    is_correct: bool = Field(default=False)
    execution_output: Optional[str] =None
    submitted_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())