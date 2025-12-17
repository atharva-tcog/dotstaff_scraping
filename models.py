# from dataclasses import dataclass

# @dataclass
# class JobData:
#     requisition_id: str
#     company_id: str
#     job_title: str
#     job_status: str
#     city: str
#     state: str
#     country: str
#     location: str
#     min_salary: float
#     max_salary: float
#     job_description: str
#     job_posted_date: str
#     job_closed_date: str
#     contract_start_date: str
#     job_expiry_date: str
#     duration: str
#     total_positions: int
#     qualification: str
#     salary_type: str
#     source: str = "DotStaff"

from dataclasses import dataclass
from typing import Optional


@dataclass
class JobData:
    # -----------------------------
    # CORE IDENTIFIERS
    # -----------------------------
    requisition_id: str

    company_id: Optional[int] = None
    client_id: Optional[int] = None
    poc_id: Optional[int] = None

    # -----------------------------
    # JOB META
    # -----------------------------
    job_title: Optional[str] = None
    job_status: Optional[str] = None
    is_urgent: Optional[str] = None  # Yes / No from DOTSTAFF

    # -----------------------------
    # LOCATION
    # -----------------------------
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    location: Optional[str] = None

    # -----------------------------
    # COMPENSATION
    # -----------------------------
    min_salary: Optional[float] = 0.0
    max_salary: Optional[float] = 0.0
    salary_type: Optional[str] = None

    # -----------------------------
    # DESCRIPTION
    # -----------------------------
    job_description: Optional[str] = None
    qualification: Optional[str] = None

    # -----------------------------
    # DATES
    # -----------------------------
    job_posted_date: Optional[str] = None
    job_closed_date: Optional[str] = None
    contract_start_date: Optional[str] = None
    job_expiry_date: Optional[str] = None

    # -----------------------------
    # CONTRACT / OPENINGS
    # -----------------------------
    duration: Optional[str] = None
    total_positions: Optional[int] = 1

    # -----------------------------
    # SOURCE
    # -----------------------------
    source: str = "DOTSTAFF"