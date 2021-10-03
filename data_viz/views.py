"""Py file for data_viz views."""
import json

import pandas as pd
from django.views.generic import TemplateView


class DataVizView(TemplateView):
    """View dashboard.html."""

    template_name = "data_viz/dashboard.html"

    def get_context_data(self, **kwargs):
        """Get context data.

        Args:
          **kwargs: Keyword arguments.

        Returns:
          The statistics to be generated and displayed to dashboar.html
        """
        context = self.generate_stats()

        return context

    def generate_stats(self):
        """Generate statistics based from RBI JSON file."""
        # ### Initial Setup
        with open("data1.json", encoding="UTF-8") as json_file:
            data = json.load(json_file)

        df = pd.DataFrame(data["rows"])

        # ### Convert Dates to Datetime
        df["created_at"] = pd.to_datetime(df["created_at"], utc=True)
        df["birth_date"] = pd.to_datetime(df["birth_date"], errors="coerce", format="%B %d, %Y")
        df["date_accomplished"] = pd.to_datetime(
            df["date_accomplished"], errors="coerce", format="%Y-%m-%d"
        )

        # ### Convert Monthly Income to Int
        df["monthly_income"] = (
            df["monthly_income"]
            .str.replace(",", "", regex=False)
            .str.replace(" ", "", regex=False)
            .str.replace(".", "", regex=False)
        )
        df["monthly_income"].fillna(0, inplace=True)
        df["monthly_income"] = df["monthly_income"].astype("int")

        # ### Create Age Groups Given Age
        # #### Calculate Age From Birth Date
        now = pd.Timestamp.now()
        df["age"] = (now - df["birth_date"]).astype("<m8[Y]")
        df["age"] = df["age"].astype("Int64")

        # #### Calculate Age Groups
        bins = [0, 2, 4, 13, 20, 110]
        labels = ["Infant", "Toddler", "Kid", "Teen", "Adult"]
        df["age_group"] = pd.cut(df["age"], bins=bins, labels=labels, right=False)

        age_group_labels = df["age_group"].value_counts().index.values.tolist()
        age_group_values = df["age_group"].value_counts().values.tolist()

        # ### Number of Citizenship per Category
        citizenship_labels = df.groupby("citizenship").size().index.values.tolist()
        citizenship_values = df.groupby("citizenship").size().values.tolist()

        # ### Number of Civil Status per Category
        civil_status_labels = df.groupby("civil_status").size().index.values.tolist()
        civil_status_values = df.groupby("civil_status").size().values.tolist()

        # ### Number of Members in Family
        # house_num_labels = df["house_num"].value_counts().index.values
        # house_num_values = df["house_num"].value_counts().values

        # ### Average Family Members in A house
        house_members_avg = df["house_num"].value_counts().mean().astype(int)

        # ### Social Class Given Monthly Income
        bins = [0, 7890, 15780, 31560, 78900, 118350, 157800, 200000, 500000]
        labels = [
            "Not Applicable",
            "Poor",
            "Low Income",
            "Lower Middle Income",
            "Middle Middle Income",
            "Upper Middle Income",
            "Upper Income",
            "Rich",
        ]
        df["social_class"] = pd.cut(df["monthly_income"], bins=bins, labels=labels, right=False)

        social_class_labels = df["social_class"].value_counts().index.values.tolist()
        social_class_values = df["social_class"].value_counts().values.tolist()

        # ### Number of RBI in Database
        num_recorded_rbi = len(df.groupby("house_num").sum().index.values.tolist())

        # ### Average Salary per Person
        person_avg_salary = df[df["monthly_income"] != 0]["monthly_income"].mean().astype("int")

        # ### Average Salary per Household
        household = df.groupby(["house_num"])["monthly_income"].sum()
        household_avg_salary = household.values.mean().astype("int")

        data = {
            "age_group": {"labels": age_group_labels, "values": age_group_values},
            "citizenship": {"labels": citizenship_labels, "values": citizenship_values},
            "civil_status": {"labels": civil_status_labels, "values": civil_status_values},
            "house_members": {"avg": house_members_avg},
            "rbi": {"count": num_recorded_rbi},
            "avg_salary": {"person": person_avg_salary, "household": f"{household_avg_salary:,}"},
            "social_class": {"labels": social_class_labels, "values": social_class_values},
            "total_population": {"values": f"{len(df.index):,}"},
        }
        return data
