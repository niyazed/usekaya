from fastapi import APIRouter, HTTPException
from typing import List, Optional, Dict
from datetime import date
from fastapi import Depends, Query
from sqlmodel import Session
from typing import Annotated

from src.db.database import get_session
from src.services.performance import get_performance_metrics
from src.schemas.performance import FilterParams, PerformanceTimeSeries, ComparePerformance
from src.services.performance import get_performance_comparison
from src.utils.logger import logger


router = APIRouter()


@router.get("/performance-time-series", response_model=List[PerformanceTimeSeries])
def performance_time_series(
    filter_params: Annotated[FilterParams, Query()],
    session: Session = Depends(get_session)
):
    """
    Get performance metrics for a given period
    """
    # Validate aggregate_by parameter
    if filter_params.aggregate_by not in ["day", "week", "month"]:
        logger.warning(f"Invalid aggregate_by value: {filter_params.aggregate_by}")
        raise HTTPException(
            status_code=400,
            detail="aggregate_by must be one of: day, week, month"
        )
    
    # Validate date range
    if (filter_params.start_date and filter_params.end_date) and filter_params.start_date > filter_params.end_date:
        logger.warning(f"Invalid date range: start_date {filter_params.start_date} after end_date {filter_params.end_date}")
        raise HTTPException(
            status_code=400,
            detail="start_date must be before or equal to end_date"
        )
        
    try:
        logger.info("Getting performance metrics", 
                   extra={
                       "aggregate_by": filter_params.aggregate_by,
                       "start_date": filter_params.start_date,
                       "end_date": filter_params.end_date
                   })
        return get_performance_metrics(
            session=session,
            aggregate_by=filter_params.aggregate_by,
            campaigns=filter_params.campaigns,
            start_date=filter_params.start_date,
            end_date=filter_params.end_date
        )
        
    except ValueError as e:
        # Handle expected validation errors
        logger.warning(f"Validation error in performance_time_series: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
        
    except Exception as e:
        # Log unexpected errors with full traceback
        logger.exception("Unexpected error in performance_time_series")
        raise HTTPException(
            status_code=500,
            detail="An internal server error occurred. Please try again later."
        )





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
    # Validate compare_mode parameter
    if compare_mode not in ["preceding", "previous_month"]:
        logger.warning(f"Invalid compare_mode value: {compare_mode}")
        raise HTTPException(
            status_code=400,
            detail="compare_mode must be either 'preceding' or 'previous_month'"
        )
        
    # Validate date range
    if start_date > end_date:
        logger.warning(f"Invalid date range: start_date {start_date} after end_date {end_date}")
        raise HTTPException(
            status_code=400,
            detail="start_date must be before or equal to end_date"
        )

    try:
        logger.info(f"Comparing performance metrics for period starting {start_date} and ending {end_date}, using {compare_mode} mode", 
                   extra={
                       "start_date": str(start_date),
                       "end_date": str(end_date),
                       "compare_mode": compare_mode
                   })
        return get_performance_comparison(
            session=session,
            start_date=start_date,
            end_date=end_date,
            compare_mode=compare_mode
        )
        
    except ValueError as e:
        # Handle expected validation errors
        logger.warning(f"Validation error in compare_performance: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
        
    except Exception as e:
        # Log unexpected errors with full traceback
        logger.exception("Unexpected error in compare_performance")
        raise HTTPException(
            status_code=500,
            detail="An internal server error occurred. Please try again later."
        )
