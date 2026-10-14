"""Application configuration settings."""

from pathlib import Path

from pydantic import BaseModel, Field


class Settings(BaseModel):
    app_name: str = "Web-OOP Mini-LMS"
    app_version: str = "0.1.0"
    base_dir: Path = Path(__file__).resolve().parent.parent
    data_dir: Path = base_dir / "data"
    db_file: Path = data_dir / "web_oop.db"
    database_url: str = Field(default="")
    static_dir: Path = Path(__file__).resolve().parent / "static"
    templates_dir: Path = Path(__file__).resolve().parent / "templates"
    runner_timeout_seconds: float = 5.0

    def model_post_init(self, __context: object) -> None:
        if not self.database_url:
            self.database_url = f"sqlite:///{self.db_file.as_posix()}"


settings = Settings()
