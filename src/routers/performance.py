from fastapi import APIRouter
from typing import List, Optional, Dict
from datetime import date
from fastapi import Depends, Query
from sqlmodel import Session
from typing import Annotated

from src.db.database import get_session
from src.services.performance import get_performance_metrics
from src.schemas.performance import FilterParams, PerformanceTimeSeries, ComparePerformance
from src.services.performance import get_performance_comparison

router = APIRouter()


@router.get("/performance-time-series", response_model=List[PerformanceTimeSeries])
def performance_time_series(
    filter_params: Annotated[FilterParams, Query()],
    session: Session = Depends(get_session)
):
    """
    Get performance metrics for a given period
    """
    try:
        if filter_params.aggregate_by not in ["day", "week", "month"]:
            return {"error": "aggregate_by must be one of: day, week, month", "status": "error"}, 400
        
        if (filter_params.start_date and filter_params.end_date) and filter_params.start_date > filter_params.end_date:
            return {"error": "start_date must be before or equal to end_date", "status": "error"}, 400
            
        return get_performance_metrics(
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





@router.get("/compare-performance", response_model=ComparePerformance)
def compare_performance(
    start_date: date,
    end_date: date,
    compare_mode: str,
    session: Session = Depends(get_session)
):
    """
    Compare performance metrics between two periods
    """
    try:
        if compare_mode not in ["preceding", "previous_month"]:
            return {"error": "compare_mode must be either 'preceding' or 'previous_month'", "status": "error"}, 400
            
        if start_date > end_date:
            return {"error": "start_date must be before or equal to end_date", "status": "error"}, 400
        
        return get_performance_comparison(
            session=session,
            start_date=start_date,
            end_date=end_date,
            compare_mode=compare_mode
        )

    except Exception as e:
        error_message = "An error occurred while comparing performance metrics"
        if isinstance(e, ValueError):
            error_message = str(e)
        else:
            print(f"Performance comparison error: {str(e)}")
        return {"error": error_message, "status": "error"}, 500
