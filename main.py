from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from sqlalchemy import func
from pydantic import BaseModel

from database import create_db_and_tables, get_session
from models import Challenge, Submission
from sandbox import execute_in_sandbox

app = FastAPI(title="CTF Secure Coding Engine")

@app.on_event("startup") #it talk to databse before FastAPI starts accepting 
def on_startup():
    create_db_and_tables()
#create a New Challenge (Admin Use)
@app.post("/challenges/", response_model=Challenge)
def create_challenge(challenge: Challenge, session: Session=Depends(get_session)): #
    session.add(challenge)
    session.commit()
    session.refresh(challenge)
    return challenge

class Payload(BaseModel):
    challenge_id: int
    user_id: int
    code: str

@app.post("/submit/", response_model=Submission)
def submit_code(payload: Payload, session: Session=Depends(get_session)):
    #Fetch the challenge to get the expected flag
    challenge = session.get(Challenge, payload.challenge_id)
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge is not found")
    
    output= execute_in_sandbox(payload.code)
    is_correct= challenge.expected_flag in output

    submission= Submission(
        challenge_id=payload.challenge_id,
        user_id= payload.user_id,
        submitted_code= payload.code,
        is_correct= is_correct,
        execution_output=output
    
    )
    session.add(submission)
    session.commit()
    session.refresh(submission)

    return submission

@app.get("/leaderboard/")
def get_leaderboard(session: Session = Depends(get_session)):
    statement=(
        select(Submission.user_id, func.sum(Challenge.points).label("totoal_points"))
        . join(Challenge, Submission.challenge_id == Challenge.id)
        .where(Submission.is_correct == True)
        .group_by(Submission.user_id)
        .order_by(func.sum(Challenge.points).desc())
    )
    result = session.exec(statement).all()

    leaderboard=[]
    for rank, row in enumerate(result, start=1):
        leaderboard.append({
            "rank":rank,
            "user_id": row[0],
            "total_points": row[1]
        })
    
    return leaderboard