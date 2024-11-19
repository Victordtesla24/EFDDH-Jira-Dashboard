"""Data processing utilities for the dashboard."""
from typing import Dict, Any, Optional
import pandas as pd
from pandera.typing import DataFrame
import pandera as pa

from .logger import logger
from .constants import StatusType, PriorityType

class JiraSchema(pa.DataFrameModel):
    """Schema for Jira data validation."""
    Issue_Key: pa.Field[str] = pa.Field(nullable=False)
    Story_Points: pa.Field[float] = pa.Field(ge=0, nullable=True)
    Status: pa.Field[str] = pa.Field(isin=[s.value for s in StatusType])
    Sprint: pa.Field[str] = pa.Field(nullable=True)
    Created: pa.Field[pd.Timestamp] = pa.Field()
    Due_Date: pa.Field[pd.Timestamp] = pa.Field(nullable=True)
    Priority: pa.Field[str] = pa.Field(isin=[p.value for p in PriorityType])
    Epic: pa.Field[str] = pa.Field(nullable=True)

class DataProcessor:
    """Main class for processing data."""
    
    def __init__(self) -> None:
        """Initialize the data processor."""
        self.data: Optional[pd.DataFrame] = None
        self.schema = JiraSchema
        logger.info("DataProcessor initialized")
