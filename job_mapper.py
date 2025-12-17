from typing import Dict, Any
from models import JobData


def normalize_priority(is_urgent) -> str:
    """
    DOTSTAFF urgent flag → priority
    """
    if not is_urgent:
        return "normal"

    val = str(is_urgent).strip().lower()
    return "high" if val in ("yes", "true", "urgent", "1") else "normal"


def normalize_status(dotstaff_status: str) -> str:
    """
    DOTSTAFF status → system status
    """
    if not dotstaff_status:
        return "unknown"

    s = dotstaff_status.lower()

    if "active" in s:
        return "open"
    if "interview" in s:
        return "on_hold"
    if "closed" in s or "no longer" in s:
        return "closed"

    return "unknown"


def map_job_to_payload(job: JobData) -> Dict[str, Any]:
    """
    Convert JobData scraped from DOTSTAFF into final job payload
    """

    return {
        # -----------------------------
        # PRIORITY
        # -----------------------------
        "priority": normalize_priority(job.is_urgent),

        # -----------------------------
        # IDENTIFIERS (NULL AS REQUESTED)
        # -----------------------------
        "requisitionId": job.requisition_id,
        "companyId": None,
        "clientId": None,
        "pocId": None,

        # -----------------------------
        # JOB INFO
        # -----------------------------
        "jobTitle": job.job_title,
        "jobType": "full-time",
        "jobMode": "onsite",
        "expYears": "0-2",
        "engagementType": "Contract",
        "vendorPlatform": "DOTSTAFF",

        # -----------------------------
        # OPENINGS / PAY
        # -----------------------------
        "noOfOpenings": job.total_positions or 1,
        "maxSubmission": 0,

        "maxPayRateCurrency": "USD",
        "maxPayRateRate": job.max_salary or 0.0,
        "maxPayRateUnit": "Hourly",

        "minPayRateCurrency": "USD",
        "minPayRateRate": job.min_salary or 0.0,
        "minPayRateUnit": "Hourly",

        "requiredHours": 0,
        "requiredDocuments": [],
        "securityClearance": False,
        "backgroundVerification": False,

        # -----------------------------
        # DATES
        # -----------------------------
        "jobOpenDate": job.job_posted_date,
        "jobCloseDate": job.job_closed_date,
        "contractOpenDate": job.contract_start_date,
        "contractCloseDate": job.job_expiry_date,
        "contractExtendable": False,

        # -----------------------------
        # LOCATION
        # -----------------------------
        "country": job.country,
        "state": job.state,
        "city": job.city,

        # -----------------------------
        # CONTENT
        # -----------------------------
        "jobDescription": job.job_description,
        "skills": [],

        # -----------------------------
        # STATUS (NON-ACTIVE SUPPORTED)
        # -----------------------------
        "status": normalize_status(job.job_status),

        # -----------------------------
        # STATIC REQUIRED FIELDS
        # -----------------------------
        "jobDetailsFilePath": "",
        "consented": True,
        "jobBoards": [],
        "rejectionReasons": [],
        "published": True
    }