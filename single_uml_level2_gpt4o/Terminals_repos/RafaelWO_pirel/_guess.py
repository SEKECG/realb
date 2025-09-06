import random
import csv
import os
import logging
from pathlib import Path
from rich.prompt import Prompt
from rich.console import Console
from pirel.releases import PythonReleases, PythonRelease

STATS_DIR = Path.home() / ".pirel_stats"
STATS_FILENAME = STATS_DIR / "quiz_scores.csv"
STATS_FIELDNAMES = ["question", "score"]
logger = logging.getLogger(__name__)

class Question:
    def __init__(self, releases):
        self.releases = releases
        self.target_release = random.choice(releases.to_list())
        self.correct_answer = self.get_target_field(self.target_release)
        self.choices = self.build_choices()

    def __repr__(self):
        return f"{self.__class__.__name__}(target_release={self.target_release.version})"

    def ask(self):
        prompt = PirelPrompt(self.format_question(), choices=self.choices)
        answer = prompt()
        return answer == self.correct_answer

    def build_choices(self):
        incorrect_choices = self.generate_incorrect_choices()
        choices = [self.correct_answer] + [self.get_target_field(choice) for choice in incorrect_choices]
        random.shuffle(choices)
        return choices

    def get_target_field(self, release):
        raise NotImplementedError

    def format_question(self):
        raise NotImplementedError

    def generate_incorrect_choices(self, *predicates, k=3):
        releases = [release for release in self.releases.to_list() if all(pred(release) for pred in predicates)]
        releases.remove(self.target_release)
        random.shuffle(releases)
        return releases[:k]

class DateVersionQuestion(Question):
    def __init__(self, releases):
        super().__init__(releases)
        self.get_target_field = lambda release: release.version

    def format_question(self):
        return f"What Python version was released on {self.target_release.released}?"

class LatestVersionQuestion(Question):
    def __init__(self, releases):
        super().__init__(releases)
        self.target_release = max(releases.to_list(), key=lambda r: r.version_tuple)
        self.get_target_field = lambda release: release.version

    def incorrect_choices(self):
        return [release for release in self.releases.to_list() if release.version.startswith("3")]

class ReleaseManagerVersionQuestion(Question):
    def __init__(self, releases):
        super().__init__(releases)
        self.get_target_field = lambda release: release._release_manager

    def format_question(self):
        return f"Who was the release manager for Python {self.target_release.version}?"

    def incorrect_choices(self):
        return [release for release in self.releases.to_list() if release._release_manager != self.target_release._release_manager]

class VersionDateQuestion(Question):
    def __init__(self, releases):
        super().__init__(releases)
        self.get_target_field = lambda release: release.released

    def format_question(self):
        return f"When was Python {self.target_release.version} released?"

def get_random_question():
    releases = PythonReleases()
    question_classes = [DateVersionQuestion, LatestVersionQuestion, ReleaseManagerVersionQuestion, VersionDateQuestion]
    return random.choice(question_classes)(releases)

def store_question_score(question, score):
    STATS_DIR.mkdir(parents=True, exist_ok=True)
    with open(STATS_FILENAME, mode="a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=STATS_FIELDNAMES)
        if file.tell() == 0:
            writer.writeheader()
        writer.writerow({"question": repr(question), "score": score})

class PirelPrompt(Prompt):
    def __init__(self, prompt, choices, console=None, password=False, case_sensitive=True, show_default=True):
        super().__init__(prompt, choices=choices, console=console, password=password, case_sensitive=case_sensitive, show_default=show_default)
        self.choice_enum = {chr(97 + i): choice for i, choice in enumerate(choices)}
        self.illegal_choice_message = "Please choose a valid option."
        self.prompt_suffix = "> "

    def check_choice(self, value):
        return value in self.choice_enum

    def make_prompt(self, default):
        choices_text = "\n".join([f"{chr(97 + i)}) {choice}" for i, choice in enumerate(self.choices)])
        return f"{self.prompt}\n{choices_text}\n{self.prompt_suffix}"

    def process_response(self, value):
        if not self.check_choice(value):
            raise ValueError(self.illegal_choice_message)
        return self.choice_enum[value]