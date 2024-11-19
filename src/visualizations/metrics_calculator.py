import logging
from datetime import datetime
from typing import Dict, Any, Optional

import pandas as pd
from ..utils.constants import StatusType, PriorityType
from ..utils.logger import get_logger

logger = get_logger(__name__)


class MetricsCalculator:
    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df
        self.accuracy_metrics = {}
        self._validate_data()
        
    def _validate_data(self):
        """Validate data quality and calculate accuracy metrics"""
        try:
            total_records = len(self.df)
            
            # Data completeness
            self.accuracy_metrics['completeness'] = {
                'story_points': 1 - (self.df['Story Points'].isnull().sum() / total_records),
                'due_dates': 1 - (self.df['Due Date'].isnull().sum() / total_records),
                'sprint_data': 1 - (self.df['Sprint'].isnull().sum() / total_records)
            }
            
            # Data consistency
            self.accuracy_metrics['consistency'] = {
                'valid_status': (self.df['Status'].isin([StatusType.TODO.value, StatusType.IN_PROGRESS.value, StatusType.DONE.value, StatusType.BLOCKED.value]).sum() / total_records),
                'valid_points': ((self.df['Story Points'] >= 0) & (self.df['Story Points'].notnull())).sum() / total_records,
                'valid_dates': (self.df['Due Date'] >= self.df['Created']).sum() / len(self.df['Due Date'].dropna())
            }
            
            # Data freshness
            if 'Updated' in self.df.columns:
                max_update = self.df['Updated'].max()
                self.accuracy_metrics['freshness'] = (pd.Timestamp.now() - max_update).days
                
            logger.info(f"Data quality metrics: {self.accuracy_metrics}")
            
        except Exception as e:
            logger.error(f"Error in data validation: {str(e)}")
            raise

    def get_sprint_velocity(self):
        """Calculate sprint velocity with confidence score"""
        try:
            velocity = self.df.groupby('Sprint')['Story Points'].sum()
            confidence_score = self.accuracy_metrics['completeness']['story_points'] * \
                             self.accuracy_metrics['consistency']['valid_points']
                             
            return {
                'velocity': velocity,
                'confidence': confidence_score,
                'missing_data_pct': 1 - confidence_score
            }
        except Exception as e:
            logger.error(f"Error calculating sprint velocity: {str(e)}")
            raise

    def get_completion_rate(self) -> Dict[str, float]:
        """Calculate completion rate with data quality indicators"""
        try:
            completed = self.df[self.df['Status'].isin([StatusType.DONE.value, StatusType.CLOSED.value])].shape[0]
            total = len(self.df)
            
            confidence_score = self.accuracy_metrics['consistency']['valid_status']
            
            return {
                'rate': completed / total if total > 0 else 0,
                'confidence': confidence_score,
                'sample_size': total
            }
        except Exception as e:
            logger.error(f"Error calculating completion rate: {str(e)}")
            raise

    def get_metrics_confidence(self) -> Dict[str, float]:
        """Calculate confidence scores for metrics calculations."""
        try:
            confidence = {
                'velocity': self._calculate_velocity_confidence(),
                'completion_rate': self._calculate_completion_confidence(),
                'quality': self._calculate_quality_confidence()
            }
            
            # Log low confidence metrics
            for metric, score in confidence.items():
                if score < 0.8:  # 80% threshold
                    logger.warning(f"Low confidence in {metric} calculation: {score:.2%}")
                
            return confidence
            
        except Exception as e:
            logger.error(f"Error calculating metrics confidence: {str(e)}")
            return {}
