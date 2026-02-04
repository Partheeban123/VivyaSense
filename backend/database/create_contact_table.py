"""
Create contact_submissions table in the database
Run this script to add the contact form table to your existing database
"""
from sqlalchemy import create_engine
from database.models import Base, ContactSubmission
from core.config import settings
from loguru import logger as log


def create_contact_table():
    """Create the contact_submissions table"""
    try:
        # Create engine
        engine = create_engine(settings.DATABASE_URL)
        
        # Create only the ContactSubmission table
        ContactSubmission.__table__.create(engine, checkfirst=True)
        
        log.info("✅ Successfully created contact_submissions table")
        return True
        
    except Exception as e:
        log.error(f"❌ Failed to create contact_submissions table: {str(e)}")
        return False


if __name__ == "__main__":
    log.info("Creating contact_submissions table...")
    success = create_contact_table()
    
    if success:
        log.info("✅ Database migration completed successfully!")
    else:
        log.error("❌ Database migration failed!")

