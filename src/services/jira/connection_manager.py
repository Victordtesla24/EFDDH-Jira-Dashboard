import logging
import time
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

import streamlit as st

logger = logging.getLogger(__name__)


class ConnectionManager:
    def __init__(self) -> None:
        self.max_retries: int = 5
        self.retry_delay: int = 2
        self.connection_status: Dict[
            str, Union[datetime, int, List[Dict[str, Any]], str, None]
        ] = {
            "last_connected": None,
            "retry_count": 0,
            "errors": [],
            "status": "disconnected",
        }
        self.health_check_interval: int = 30  # seconds
        self._conn: Optional[Any] = None

    def initialize(self) -> None:
        """Initialize connection management in session state"""
        if "connection_manager" not in st.session_state:
            st.session_state.connection_manager = {
                "last_health_check": datetime.now(),
                "connection_history": [],
                "reconnection_attempts": 0,
                "max_reconnection_attempts": 5,
                "connection_stable": True,
            }

    def update_connection_status(
        self, status: str, error: Optional[str] = None
    ) -> None:
        """Update connection status with error tracking"""
        try:
            self.connection_status["status"] = status
            if status == "connected":
                self.connection_status["last_connected"] = datetime.now()
                self.connection_status["retry_count"] = 0
            elif status == "error" and error:
                if isinstance(self.connection_status["errors"], list):
                    self.connection_status["errors"].append(
                        {"timestamp": datetime.now(), "error": error}
                    )
                self._handle_connection_error(error)
        except Exception as e:
            logger.error(f"Error updating connection status: {str(e)}")

    def _handle_connection_error(self, error: str) -> None:
        """Handle connection errors with retry logic"""
        try:
            retry_count = self.connection_status.get("retry_count", 0)
            if isinstance(retry_count, int) and retry_count < self.max_retries:
                self.connection_status["retry_count"] = retry_count + 1
                logger.warning(f"Connection error, attempt {retry_count + 1}: {error}")
                time.sleep(self.retry_delay)
                self._attempt_reconnection()
            else:
                logger.error("Max retry attempts reached")
                self._initiate_fallback_procedure()
        except Exception as e:
            logger.error(f"Error handling connection error: {str(e)}")

    def _attempt_reconnection(self) -> None:
        """Attempt to reconnect with exponential backoff"""
        try:
            logger.info("Attempting reconnection...")
            if "connection_manager" in st.session_state:
                st.session_state.connection_manager["reconnection_attempts"] += 1
                st.session_state.connection_manager["last_health_check"] = (
                    datetime.now()
                )

            retry_count = self.connection_status.get("retry_count", 0)
            if isinstance(retry_count, int):
                time.sleep(self.retry_delay * retry_count)

        except Exception as e:
            logger.error(f"Error during reconnection attempt: {str(e)}")

    def _initiate_fallback_procedure(self) -> None:
        """Initiate fallback procedures when connection cannot be restored."""
        try:
            logger.warning("Initiating fallback procedure")
            if "connection_manager" in st.session_state:
                st.session_state.connection_manager["connection_stable"] = False

            if "df" in st.session_state:
                st.session_state["backup_data"] = st.session_state.df.copy()

            st.warning("Connection issues detected. Operating in offline mode.")
        except Exception as e:
            logger.error(f"Error initiating fallback procedure: {str(e)}")

    def perform_health_check(self) -> Dict[str, Any]:
        """Perform connection health check"""
        try:
            current_time = datetime.now()
            if "connection_manager" in st.session_state:
                last_check = st.session_state.connection_manager["last_health_check"]
                if (
                    current_time - last_check
                ).total_seconds() > self.health_check_interval:
                    st.session_state.connection_manager["last_health_check"] = (
                        current_time
                    )

                    return {
                        "status": (
                            "healthy"
                            if st.session_state.connection_manager["connection_stable"]
                            else "degraded"
                        ),
                        "last_check": current_time,
                        "reconnection_attempts": st.session_state.connection_manager[
                            "reconnection_attempts"
                        ],
                        "uptime": (current_time - last_check).total_seconds(),
                    }
            return {"status": "unknown", "last_check": current_time}
        except Exception as e:
            logger.error(f"Error performing health check: {str(e)}")
            return {"status": "error", "error": str(e)}

    def _connection(self) -> bool:
        """Check connection status."""
        return hasattr(self, "_conn") and bool(self._conn)


# Create global instance
connection_manager = ConnectionManager()
