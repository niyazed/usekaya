from fastapi import APIRouter
from typing import List, Optional, Dict
from datetime import date
from fastapi import Depends, Query
from sqlmodel import Session
from src.db.database import get_session
from src.services.performance import get_performance_time_series
from typing import Annotated
from src.schemas.performance import FilterParams, PerformanceTimeSeries

router = APIRouter()


# @router.get("/performance-time-series", response_model=List[PerformanceTimeSeries])
@router.get("/performance-time-series")
def get_time_series(
    filter_params: Annotated[FilterParams, Query()],
    session: Session = Depends(get_session)
):
    try:
        if filter_params.aggregate_by not in ["day", "week", "month"]:
            return {"error": "aggregate_by must be one of: day, week, month", "status": "error"}, 400
            
        return get_performance_time_series(
            session=session,
            aggregate_by=filter_params.aggregate_by,
            campaigns=filter_params.campaigns,
            start_date=filter_params.start_date,
            end_date=filter_params.end_date
        )
        
    except Exception as e:
        error_message = "An error occurred while getting performance metrics"
        if isinstance(e, ValueError):
            error_message = str(e)
        else:
            print(f"Performance metrics error: {str(e)}")
        return {"error": error_message, "status": "error"}, 500
