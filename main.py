from mail_reader import MailReader
from scraper import DotstaffScraper
from storage.text_writer import TextWriter
from job_mapper import map_job_to_payload
from config import *
from logger import get_logger

logger = get_logger(__name__)


def main():
    logger.info("DOTSTAFF automation started")

    scraper = None

    try:
        # ---------------------------------
        # INIT STORAGE
        # ---------------------------------
        writer = TextWriter(OUTPUT_TXT_PATH)

        # ---------------------------------
        # READ EMAILS (UNSEEN)
        # ---------------------------------
        mail_reader = MailReader(
            EMAIL_USERNAME,
            EMAIL_PASSWORD
        )

        mail_data, _ = mail_reader.fetch_unseen_dotstaff_mails()
        logger.info(f"Mail read completed. Records found: {len(mail_data)}")

        if not mail_data:
            logger.info("No postings to process. Exiting.")
            return

        # ---------------------------------
        # INIT SCRAPER
        # ---------------------------------
        scraper = DotstaffScraper(
            DOTSTAFF_USERNAME,
            DOTSTAFF_PASSWORD
        )
        scraper.login()

        # ---------------------------------
        # PROCESS EACH POSTING
        # ---------------------------------
        for record in mail_data:
            posting_id = record[0]

            if not posting_id:
                logger.warning("Skipping record with empty posting ID")
                continue

            try:
                job = scraper.fetch_job(posting_id)

                if not job:
                    logger.info(f"Posting {posting_id} skipped (inactive or not found)")
                    continue

                # ---------------------------------
                # MAP → PAYLOAD
                # ---------------------------------
                payload = map_job_to_payload(job)

                # ---------------------------------
                # WRITE OUTPUT
                # ---------------------------------
                writer.write_json(payload)

                logger.info(f"Posting {posting_id} saved successfully")

            except Exception:
                logger.error(
                    f"Failed processing posting {posting_id}",
                    exc_info=True
                )
                writer.write_error(f"{posting_id} - processing failed")

    except Exception:
        logger.critical("Fatal error in DOTSTAFF automation", exc_info=True)

    finally:
        # ---------------------------------
        # CLEANUP
        # ---------------------------------
        if scraper:
            scraper.close()
            logger.info("Scraper closed")

        logger.info("DOTSTAFF automation finished")


if __name__ == "__main__":
    main()