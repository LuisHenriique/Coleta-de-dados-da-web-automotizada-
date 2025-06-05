from dataclasses import dataclass, field
from typing import List
from course import Course

@dataclass
class Unit:
    listOfCourses:  List[Course] = field(default_factory=list)