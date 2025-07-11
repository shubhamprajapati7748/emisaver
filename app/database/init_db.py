"""Initialize the database with the first superuser."""
from app.core.logger import logger
from app.database.session import SessionLocal, create_tables 
from app.database.models.user import User

def init_db() -> None:
    """
    Initialize the database by creating tables and adding initial data.
    """
    try:
        # creates all tables
        logger.info("creating database tables.")
        create_tables()
        logger.info("Database tables created successfully !")

        # create superuse if it doesn't exist 
        db = SessionLocal()

        try:
            # check if superuser already exits 
            superuser = db.query(User).filter(User.is_superuser== True).first()
            if not superuser:
                logger.info("Creating superuser...")
                superuser = User(
                    full_name = "Admin user",
                    email = "admin@emisaver.com",
                    phone_number = "+919999999999",
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
    

# if __name__ == "__main__":
#     init_db()