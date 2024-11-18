from datetime import datetime

import numpy as np
import pandas as pd

from utils.logger import logger


class DataProcessor:
    def __init__(self):
        self.df = None

    def load_data_with_retry(self, file):
        try:
            # Read CSV with flexible date parsing
            self.df = pd.read_csv(
                file,
                encoding="utf-8",
                na_values=["", "N/A", "None", "nan"],
                keep_default_na=True,
                dtype={
                    "Story Points": "float64",
                    "Issue key": "str",
                    "Epic": "str",
                    "Status": "str",
                    "Sprint": "str",
                },
            )

            # Convert date columns with multiple format handling
            date_columns = ["Created", "Due Date"]
            for col in date_columns:
                if col in self.df.columns:
                    # Try multiple date formats
                    self.df[col] = pd.to_datetime(
                        self.df[col], format="%d/%m/%Y", errors="coerce"
                    )
                    mask = self.df[col].isna()
                    if mask.any():
                        self.df.loc[mask, col] = pd.to_datetime(
                            self.df.loc[mask, col], format="%Y-%m-%d", errors="coerce"
                        )

            # Clean and preprocess data
            self.df = self.df[
                self.df["Issue key"].notna()
            ]  # Keep rows with valid Issue keys
            self.df["Story Points"] = pd.to_numeric(
                self.df["Story Points"], errors="coerce"
            ).fillna(0)
            self.df["Epic"] = self.df["Epic"].fillna("No Epic")
            self.df["Sprint"] = self.df["Sprint"].fillna("Backlog")

            # Log data processing stats
            logger.info(f"Total records loaded: {len(self.df)}")
            logger.info(f"Records after cleaning: {len(self.df)}")
            logger.info(f"Unique Epics: {self.df['Epic'].nunique()}")
            logger.info(
                f"Date range: {self.df['Created'].min()} to {self.df['Created'].max()}"
            )

            return True
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            return False

    def create_sample_data(self):
        # Create sample data with proper date format
        dates = pd.date_range(start="2024-01-01", end="2024-12-31", freq="D")
        dates = [d.strftime("%d/%m/%Y") for d in dates]  # Format dates as DD/MM/YYYY

        sprints = ["Sprint " + str(i) for i in range(1, 5)]
        epics = ["Epic " + str(i) for i in range(1, 4)]
        assignees = ["Person " + str(i) for i in range(1, 6)]
        statuses = ["To Do", "In Progress", "Done"]
        story_points = np.random.randint(1, 13, 100)  # Add story points

        data = {
            "Created": np.random.choice(dates, 100),
            "Updated": np.random.choice(dates, 100),
            "Sprint": np.random.choice(sprints, 100),
            "Epic": np.random.choice(epics, 100),
            "Assignee": np.random.choice(assignees, 100),
            "Status": np.random.choice(statuses, 100),
            "Story Points": story_points,
        }

        self.df = pd.DataFrame(data)
        self.df.to_csv("data/EFDDH-Jira-Data-All.csv", index=False)
        return True
