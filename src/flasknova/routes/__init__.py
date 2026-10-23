from dataclasses import dataclass
from logging import Logger
from os import name, system
from pathlib import Path
from re import MULTILINE, finditer
from typing import TypeVar

from flask_nova import get_flasknova_logger


@dataclass
class HTTP:
  BASE_URL_TYPE = TypeVar("BASE_URL_TYPE", sentinel, str)
  PATTERN: str = r"^(GET|POST|PUT|PATCH|DELETE|HEAD|OPTIONS)\s+(\S+)"
  CONTENT: str = Path("src/flasknova/artifacts/app_request.http").read_text(encoding="utf-8")

  def __post_init__(self) -> None:
    self.LOGGER: Logger = get_flasknova_logger()
    self.BASE_URL: self.BASE_URL_TYPE = sentinel("EMPTY_BASE_URL")

    for line in self.CONTENT.split("\n"):
      if "@base_url" in line:
        self.BASE_URL = line.split(" ")[-1]

  def parse_log(self, method: str, log: str):
    match method:
      case "GET":
        self.LOGGER.debug(log)
      case "POST":
        self.LOGGER.info(log)
      case "PUT" | "PATCH":
        self.LOGGER.warning(log)
      case "DELETE":
        self.LOGGER.error(log)
      case "HEAD" | "OPTIONS":
        self.LOGGER.critical(log)

  def get_logs(self) -> None:
    for match in finditer(self.PATTERN, self.CONTENT, MULTILINE):
      method, url = match.groups()
      self.parse_log(method, f"{method} {url.replace('{{base_url}}', self.BASE_URL)}")


def main() -> None:
  # Clearing the terminal screen
  system("cls" if name == "nt" else "clear")

  HTTP().get_logs()


if __name__ == "__main__":
  main()
