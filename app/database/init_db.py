"""Initialize the database with the first superuser."""
from app.core.logger import logger
from app.database.session import SessionLocal, create_tables, drop_tables
from app.database.models.user import User
from sqlalchemy.orm import Session

def init_db():
    """
    Initialize the database by creating tables and adding initial data.
    """
    try:
        # Drop existing tables to ensure schema is up to date
        # logger.info("Dropping existing database tables.")
        # drop_tables()
        # logger.info("Existing tables dropped successfully!")
        
        # creates all tables
        logger.info("Creating database tables.")
        create_tables()
        logger.info("Database tables created successfully !")

        # create superuser if it doesn't exist 
        db = SessionLocal()

        try:
            # check if superuser already exists 
            superuser = db.query(User).filter(User.is_superuser== True).first()
            if not superuser:
                logger.info("Creating superuser...")
                superuser = User(
                    full_name = "Admin user",
                    email = "admin@SahiLoan.com",
                    country_code = "+91",
                    dob = "1990-01-01",
                    pin_code = "123456",
                    phone_number = "9999999999",
                    is_superuser = True,
                    is_active = True
                )
                db.add(superuser)
                db.commit()
                logger.info("Superuser created successfully !")
        finally:
            db.close()

        
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise e
    
def close_db(db: Session):
    """
    Close the database connection.
    """
    db.close()

# if __name__ == "__main__":
#     init_db()