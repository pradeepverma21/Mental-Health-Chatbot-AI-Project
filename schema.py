from pydantic import BaseModel, Field

class MentalHealthOutput(BaseModel):
    mood: str = Field(..., description="The user's current emotional state.")
    reason: str = Field(..., description="The reason behind the mood.")
    suggestion: str = Field(..., description="Recommended activity or support tip.")
