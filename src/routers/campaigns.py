from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, List
from src.db.database import get_session
from sqlmodel import Session
from src.services.campaigns import get_campaign_metrics, update_campaign_name
from src.schemas.campaigns import CampaignMetrics
from src.utils.logger import logger

router = APIRouter()

@router.get("/campaigns", response_model=List[CampaignMetrics])
def get_campaigns(session: Session = Depends(get_session)):
    """
    Get all campaigns and their metrics
    """
    try:
        logger.info("Getting campaign metrics")
        return get_campaign_metrics(session)
    except ValueError as e:
        # Handle expected validation errors
        logger.warning(f"Validation error in get_campaigns: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Log unexpected errors with traceback
        logger.exception("Unexpected error in get_campaigns")
        raise HTTPException(
            status_code=500,
            detail="An internal server error occurred. Please try again later."
        )
    
    

@router.patch("/campaigns")
def update_campaign(campaign_id: int, campaign_name: str, session: Session = Depends(get_session)):
    """
    Update the name of a campaign
    """
    try:
        logger.info(f"Updating campaign name to {campaign_name} for campaign ID {campaign_id}")
        return update_campaign_name(campaign_id, campaign_name, session)
    except ValueError as e:
        # Handle expected validation errors like campaign not found
        logger.warning(f"Validation error in update_campaign: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        # Log unexpected errors with full traceback
        logger.exception("Unexpected error in update_campaign")
        raise HTTPException(
            status_code=500, 
            detail="An internal server error occurred. Please try again later."
        )
