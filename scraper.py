from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import time

from models import JobData
from config import DOTSTAFF_URL, CHROME_DRIVER_PATH
from logger import get_logger

logger = get_logger(__name__)


class DotstaffScraper:

    def __init__(self, username: str, password: str, headless: bool = False):
        self.username = username
        self.password = password

        options = Options()
        options.add_argument("--start-maximized")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        if headless:
            options.add_argument("--headless=new")
            options.add_argument("--disable-gpu")

        service = Service(CHROME_DRIVER_PATH)
        self.driver = webdriver.Chrome(service=service, options=options)
        self.wait = WebDriverWait(self.driver, 30)

        logger.info("Chrome driver initialized")

    # -------------------------------------------------
    # AJAX WAIT
    # -------------------------------------------------
    def _wait_for_ajax(self, timeout=20):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located((By.CLASS_NAME, "raDiv"))
            )
        except TimeoutException:
            logger.warning("AJAX overlay still visible")

    # -------------------------------------------------
    # LOGIN
    # -------------------------------------------------
    def login(self):
        logger.info("Opening DOTSTAFF portal")
        self.driver.get(DOTSTAFF_URL)

        self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[@autocomplete='username']"))
        ).send_keys(self.username)

        self.driver.find_element(By.XPATH, "//input[@value='Next']").click()

        self.wait.until(
            EC.presence_of_element_located((By.NAME, "credentials.passcode"))
        ).send_keys(self.password)

        self.driver.find_element(By.XPATH, "//input[contains(@value,'Verify')]").click()

        # ✅ grid load is the real success signal
        self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//table[contains(@id,'PostingsGrid')]")
            )
        )

        logger.info("DOTSTAFF login successful")

    # -------------------------------------------------
    # URGENT FLAG
    # -------------------------------------------------
    def _is_urgent(self) -> bool:
        try:
            text = self.wait.until(
                EC.presence_of_element_located((By.ID, "lblMcpUrgent"))
            ).text.strip().lower()
            return text in ("yes", "urgent", "high", "true")
        except TimeoutException:
            return False

    # -------------------------------------------------
    # FETCH JOB (ACTIVE + INACTIVE)
    # -------------------------------------------------
    def fetch_job(self, posting_id: str) -> JobData | None:
        logger.info(f"Processing posting ID: {posting_id}")

        driver = self.driver
        wait = self.wait
        actions = ActionChains(driver)

        # 🔁 HARD RESET GRID STATE
        driver.get(DOTSTAFF_URL)
        driver.switch_to.default_content()

        wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//table[contains(@id,'PostingsGrid')]")
            )
        )
        self._wait_for_ajax()

        try:
            row = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, f"//tr[td[text()='{posting_id}']]")
                )
            )

            driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});", row
            )
            time.sleep(0.5)

            actions.double_click(row).perform()

            wait.until(
                EC.frame_to_be_available_and_switch_to_it("Posting")
            )

        except TimeoutException:
            logger.info(f"Posting not found: {posting_id}")
            return None

        # ---------------- SAFE HELPERS ----------------
        def safe_text(by, value):
            try:
                return driver.find_element(by, value).text.strip()
            except NoSuchElementException:
                return None

        def safe_int(by, value, default=1):
            try:
                return int(driver.find_element(by, value).text.strip())
            except Exception:
                return default

        status = safe_text(By.ID, "lblstatus") or "unknown"
        is_urgent = self._is_urgent()

        job = JobData(
            requisition_id=posting_id,

            company_id=None,
            client_id=None,
            poc_id=None,

            job_title=safe_text(By.ID, "lblPosition_title"),
            job_status=status,
            is_urgent=is_urgent,

            city=safe_text(By.ID, "lbljob_city"),
            state=safe_text(By.ID, "lbljob_state"),
            country=safe_text(By.ID, "lbljob_Country"),
            location=safe_text(By.ID, "lbljob_street1"),

            min_salary=0.0,
            max_salary=0.0,

            job_description=safe_text(By.ID, "txtMcpJobdescriptionView"),
            job_posted_date=safe_text(By.ID, "lbllive_post_date"),
            job_closed_date=safe_text(By.ID, "lblClosingDateTime"),

            contract_start_date=safe_text(By.ID, "lblContractStartDate"),
            job_expiry_date=safe_text(By.ID, "lblContractEndDate"),
            duration=safe_text(By.ID, "lblDuration"),
            total_positions=safe_int(By.ID, "lblPositions"),

            qualification=safe_text(By.ID, "lblMin_Education"),
            salary_type=safe_text(By.ID, "lblBillType"),
        )

        logger.info(f"Parsed posting {posting_id} (status={status})")
        self._close_posting()
        return job

    # -------------------------------------------------
    # CLOSE POSTING
    # -------------------------------------------------
    def _close_posting(self):
        try:
            self.driver.find_element(
                By.XPATH, "//a[contains(@class,'icon-times')]"
            ).click()
        except Exception:
            pass
        self.driver.switch_to.default_content()

    # -------------------------------------------------
    # CLEAN SHUTDOWN
    # -------------------------------------------------
    def close(self):
        logger.info("Closing Chrome driver")
        self.driver.quit()