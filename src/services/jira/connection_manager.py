import logging
import time
from datetime import datetime
from typing import Any, Dict, Optional

import streamlit as st

logger = logging.getLogger(__name__)


class ConnectionManager:
    def __init__(self):
        self.max_retries = 5
        self.retry_delay = 2
        self.connection_status = {
            "last_connected": None,
            "retry_count": 0,
            "errors": [],
            "status": "disconnected",
        }
        self.health_check_interval = 30  # seconds

    def initialize(self):
        """Initialize connection management in session state"""
        if "connection_manager" not in st.session_state:
            st.session_state.connection_manager = {
                "last_health_check": datetime.now(),
                "connection_history": [],
                "reconnection_attempts": 0,
                "max_reconnection_attempts": 5,
                "connection_stable": True,
            }

    def update_connection_status(self, status: str, error: Optional[str] = None):
        """Update connection status with error tracking"""
        try:
            self.connection_status["status"] = status
            if status == "connected":
                self.connection_status["last_connected"] = datetime.now()
                self.connection_status["retry_count"] = 0
            elif status == "error" and error:
                self.connection_status["errors"].append(
                    {"timestamp": datetime.now(), "error": error}
                )
                self._handle_connection_error(error)
        except Exception as e:
            logger.error(f"Error updating connection status: {str(e)}")

    def _handle_connection_error(self, error: str):
        """Handle connection errors with retry logic"""
        try:
            if self.connection_status["retry_count"] < self.max_retries:
                self.connection_status["retry_count"] += 1
                logger.warning(
                    f"Connection error, attempt {self.connection_status['retry_count']}: {error}"
                )
                time.sleep(self.retry_delay)
                self._attempt_reconnection()
            else:
                logger.error("Max retry attempts reached")
                self._initiate_fallback_procedure()
        except Exception as e:
            logger.error(f"Error handling connection error: {str(e)}")

    def _attempt_reconnection(self):
        """Attempt to reconnect with exponential backoff"""
        try:
            logger.info("Attempting reconnection...")
            # Update session state
            if "connection_manager" in st.session_state:
                st.session_state.connection_manager["reconnection_attempts"] += 1
                st.session_state.connection_manager["last_health_check"] = (
                    datetime.now()
                )

            # Reset connection if needed
            if hasattr(st, "_connection") and st._connection:
                st._connection.disconnect()
                time.sleep(self.retry_delay * self.connection_status["retry_count"])

        except Exception as e:
            logger.error(f"Error during reconnection attempt: {str(e)}")

    def _initiate_fallback_procedure(self):
        """Initiate fallback procedures when connection cannot be restored"""
        try:
            logger.warning("Initiating fallback procedure")
            if "connection_manager" in st.session_state:
                st.session_state.connection_manager["connection_stable"] = False

            # Store current state
            if "df" in st.session_state:
                st.session_state["backup_data"] = st.session_state.df.copy()

            # Update UI
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
        """Check if connection exists and is valid."""
        return bool(self._conn and self._conn.is_connected())


# Create global instance
connection_manager = ConnectionManager()
