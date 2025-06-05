from dataclasses import dataclass
from typing import List

from course import Course

@dataclass
class Unit:
    listOfCourses: list[Course]