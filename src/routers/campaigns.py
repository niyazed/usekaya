from fastapi import APIRouter, Depends
from typing import Dict, List
from src.db.database import get_session
from sqlmodel import Session
from src.services.campaigns import get_campaign_metrics, update_campaign_name
from src.schemas.campaigns import CampaignMetrics
router = APIRouter()

@router.get("/campaigns", response_model=List[CampaignMetrics])
def get_campaigns(session: Session = Depends(get_session)):
    """
    Get all campaigns and their metrics
    """
    try:
        return get_campaign_metrics(session)
    except Exception as e:
        error_message = "An error occurred while getting campaign metrics"
        if isinstance(e, ValueError):
            error_message = str(e)  # Use specific message for known errors
        else:
            # Log the full error for debugging but return a sanitized message
            print(f"Campaign metrics error: {str(e)}")
        return {"error": error_message, "status": "error"}, 500
    
    

@router.patch("/campaigns")
def update_campaign(campaign_id: str, campaign_name: str, session: Session = Depends(get_session)):
    """
    Update the name of a campaign
    """
    try:
        return update_campaign_name(campaign_id, campaign_name, session)
    except Exception as e:
        error_message = "An error occurred while updating the campaign"
        if isinstance(e, ValueError):
            error_message = str(e)  # Use specific message for known errors
        else:
            # Log the full error for debugging but return a sanitized message
            print(f"Campaign update error: {str(e)}")
        return {"error": error_message, "status": "error"}, 500
