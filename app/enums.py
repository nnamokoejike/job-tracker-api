from enum import Enum


class ApplicationStatus(str, Enum):
    APPLIED = "applied"
    INTERVIEW = "interview"
    ASSESSMENT = "assessment"
    OFFER = "offer"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"
