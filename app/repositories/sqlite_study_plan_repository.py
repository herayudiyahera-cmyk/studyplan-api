
import sqlite3
from datetime import date
from pathlib import Path

from app.models.study_plan import StudyPlan
from app.repositories.study_plan_repository import StudyPlanRepository


class SQLiteStudyPlanRepository(StudyPlanRepository):
    """Repository untuk menyimpan target belajar di SQLite."""

    def __init__(self, db_path: str = "studyplan.db"):
        self.db_path = str(Path(db_path).resolve())
        self._create_table()

    def _connect(self):
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _create_table(self):
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS study_plans (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL DEFAULT '',
                    deadline TEXT NOT NULL,
                    priority TEXT NOT NULL
                        CHECK (priority IN ('low', 'medium', 'high')),
                    status TEXT NOT NULL DEFAULT 'pending'
                        CHECK (
                            status IN (
                                'pending',
                                'in_progress',
                                'completed'
                            )
                        )
                )
                """
            )

    @staticmethod
    def _to_model(row) -> StudyPlan | None:
        if row is None:
            return None

        return StudyPlan(
            id=row["id"],
            title=row["title"],
            description=row["description"],
            deadline=date.fromisoformat(row["deadline"]),
            priority=row["priority"],
            status=row["status"],
        )

    def get_all(self) -> list[StudyPlan]:
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT * FROM study_plans ORDER BY id"
            ).fetchall()

        return [self._to_model(row) for row in rows]

    def get_by_id(self, plan_id: int) -> StudyPlan | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM study_plans WHERE id = ?",
                (plan_id,),
            ).fetchone()

        return self._to_model(row)

    def add(self, plan: StudyPlan) -> StudyPlan:
        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO study_plans
                    (title, description, deadline, priority, status)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    plan.title,
                    plan.description,
                    plan.deadline.isoformat(),
                    plan.priority,
                    plan.status,
                ),
            )
            plan.id = cursor.lastrowid

        return plan

    def update(self, plan: StudyPlan) -> StudyPlan:
        with self._connect() as connection:
            cursor = connection.execute(
                """
                UPDATE study_plans
                SET title = ?, description = ?, deadline = ?,
                    priority = ?, status = ?
                WHERE id = ?
                """,
                (
                    plan.title,
                    plan.description,
                    plan.deadline.isoformat(),
                    plan.priority,
                    plan.status,
                    plan.id,
                ),
            )

            if cursor.rowcount == 0:
                raise ValueError("Target belajar tidak ditemukan")

        return plan

    def delete(self, plan_id: int) -> bool:
        with self._connect() as connection:
            cursor = connection.execute(
                "DELETE FROM study_plans WHERE id = ?",
                (plan_id,),
            )

        return cursor.rowcount > 0
