from enum import StrEnum


class ReportStatus(StrEnum):

    PENDING = "PENDING"

    APPROVED = "APPROVED"

    REJECTED = "REJECTED"