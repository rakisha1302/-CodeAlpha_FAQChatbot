"""Loads, validates, adds, deletes and saves FAQs stored in a CSV file."""
from pathlib import Path

import pandas as pd

COLUMNS = ["category", "question", "answer"]


class FAQStore:
    def __init__(self, path):
        self.path = Path(path)
        self.df = pd.DataFrame(columns=COLUMNS)

    def load(self) -> list:
        """Load the CSV. Returns a list of warning messages (never raises)."""
        warnings = []
        try:
            raw = pd.read_csv(self.path, dtype=str).fillna("")
        except FileNotFoundError:
            return [f"FAQ file not found: {self.path.name}. Add FAQs in the Admin page to create it."]
        except Exception as exc:
            return [f"Could not read the FAQ file: {exc}"]
        if not set(COLUMNS).issubset(raw.columns):
            return [f"FAQ file must contain the columns: {', '.join(COLUMNS)}."]
        raw = raw[COLUMNS].apply(lambda col: col.str.strip())
        valid = raw[(raw != "").all(axis=1)]
        if len(valid) < len(raw):
            warnings.append(f"{len(raw) - len(valid)} invalid FAQ row(s) with empty fields were skipped.")
        dupes = valid.duplicated(subset="question", keep="first").sum()
        if dupes:
            warnings.append(f"{dupes} duplicate question(s) were skipped.")
            valid = valid.drop_duplicates(subset="question", keep="first")
        self.df = valid.reset_index(drop=True)
        return warnings

    def save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.df.to_csv(self.path, index=False)

    def add(self, category, question, answer):
        category, question, answer = (str(v or "").strip() for v in (category, question, answer))
        if not (category and question and answer):
            raise ValueError("Category, question and answer are all required.")
        if question.lower() in self.df["question"].str.lower().values:
            raise ValueError("This question already exists.")
        self.df = pd.concat([self.df, pd.DataFrame([[category, question, answer]], columns=COLUMNS)],
                            ignore_index=True)
        self.save()

    def delete(self, question):
        before = len(self.df)
        self.df = self.df[self.df["question"] != question].reset_index(drop=True)
        if len(self.df) == before:
            raise ValueError("FAQ not found.")
        self.save()

    def categories(self) -> list:
        return sorted(self.df["category"].unique().tolist())
