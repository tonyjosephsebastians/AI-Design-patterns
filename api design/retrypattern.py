import time
from fastapi import FastAPI ,HTTPException

app = FastAPI()

# Concept:
# A temporary issue happens (like timeout / network glitch).
# Retry means: try again a few times before failing.

class TemporaryError(Exception):
    pass


def retry(function, max_retries=3, delay=1):
    """
    Try function again if TemporaryError happens.
    """
    for attempt in range(max_retries + 1):  # first try + retries
        try:
            return function()
        except TemporaryError:
            if attempt == max_retries:
                raise
            time.sleep(delay)


# This creates the issue:
# It fails first 2 times, then works.
call_count = {"count": 0}

def fake_service():
    call_count["count"] += 1
    if call_count["count"] <= 2:
        raise TemporaryError("Temporary failure")
    return {"message": "Success", "attempt": call_count["count"]}


@app.get("/without-retry")
def without_retry():
    call_count["count"] = 0
    try:
        return fake_service()  # only 1 try -> usually fails
    except TemporaryError as e:
        raise HTTPException(status_code=503, detail=str(e))


@app.get("/with-retry")
def with_retry():
    call_count["count"] = 0
    try:
        return retry(fake_service, max_retries=3, delay=1)  # retries -> succeeds
    except TemporaryError as e:
        raise HTTPException(status_code=503, detail=str(e))