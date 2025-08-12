"""CRUD operations for user model"""
from app.database.models.user import User 
from sqlalchemy.orm import Session 
from sqlalchemy import text
from typing import Optional, Union, Dict, Any, List
from app.schemas.user_details import UserInfo
import uuid

class CRUDUser:
    def get(self, db: Session, user_id: uuid.UUID) -> Optional[User]:
        """Get user by ID.

        Args:
            db (Session) : The database session.
            user_id (uuid.UUID) : The ID of the user to get.

        Returns:
            User : The user object.
        
        """
        db_obj = db.query(User).filter(User.id == user_id, User.is_active == True, User.is_superuser == False).first()
        if not db_obj:
            return None
        return db_obj
    
    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        """Get user by email.

        Args:
            db (Session) : The database session.
            email (str) : The email of the user to get.

        Returns:
            User : The user object.
        
        """
        db_obj = db.query(User).filter(User.email == email, User.is_active == True, User.is_superuser == False).first()
        return db_obj
    
    def get_by_phone(self, db: Session, phone_number: str) -> Optional[User]:
        """Get user by phone number.
        
        Args:
        --- 
            db (Session) : The database session.
            phone_number (str) : The phone number of the user to get.

        Returns:    
            User : The user object.
        
        """
        db_obj = db.query(User).filter(User.phone_number == phone_number, User.is_active == True, User.is_superuser == False).first()
        return db_obj
    
    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100, filters: Optional[Dict[str, Any]] = None) -> List[User]:
        """Get multiple users with optional filtering.
        
        Args:
        --- 
            db (Session) : The database session.
            skip (int) : The number of users to skip.
            limit (int) : The number of users to return.
            filters (Optional[Dict[str, Any]]) : The filters to apply to the query.

        Returns:
        --- 
            List[User] : The list of users.
        """
        query = db.query(User)
        if filters:
            for field, value in filters.items():
                if hasattr(User, field) and value is not None:
                    if isinstance(value, str):
                        query = query.filter(getattr(User, field).ilike(f"%{value}%"))
                    else:
                        query = query.filter(getattr(User, field) == value)
        return query.offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in : Union[UserInfo, Dict[str, Any]]) -> User:
        """Create a new user.

        Args:
        --- 
            db (Session) : The database session.
            obj_in (Union[UserCreate, UserInfo, Dict[str, Any]]) : The user data to create.

        Returns:
        --- 
            User : The created user object.
        """
        if isinstance(obj_in, dict):
            create_data = obj_in
        elif hasattr(obj_in, 'full_name'):  # User object from schema
            create_data = {
                "full_name" : obj_in.full_name,
                "email" : obj_in.email,
                "phone_number" : obj_in.phone_number,
                "cibil_score" : obj_in.cibil_score,
                "total_assets" : obj_in.total_assets,
                "total_liabilities" : obj_in.total_liabilities,
                "net_worth" : obj_in.net_worth
            }
        else:
            create_data = obj_in.dict()
        db_obj = User(**create_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update(self, db: Session, *, db_obj: User, obj_in : Union[Dict[str, Any]]) -> User:
        """Update existing user.
        
        Args:
        --- 
            db (Session) : The database session.
            db_obj (User) : The user object to update.
            obj_in (Union[UserUpdate, Dict[str, Any]]) : The user data to update.

        Returns:
        --- 
            User : The updated user object.
        """
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        
        for field, value in update_data.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def delete(self, db: Session, *, user_id: uuid.UUID) -> bool:
        """Delete user.
        
        Args:
        --- 
            db (Session) : The database session.
            user_id (uuid.UUID) : The ID of the user to delete.

        Returns:
        --- 
            bool : True if the user is deleted, False otherwise.
        """
        obj = db.query(User).get(user_id)
        if obj:
            db.delete(obj)
            db.commit()
            return True
        return False
    
    def is_exists(self, db: Session, user_id: uuid.UUID) -> bool:
        """Checks if user exists.
        
        Args:
        --- 
            db (Session) : The database session.
            user_id (uuid.UUID) : The ID of the user to check.

        Returns:
        --- 
            bool : True if the user exists, False otherwise.
        """
        return db.query(User).filter(User.id == user_id).first() is not None
    
    def get_by_query(self, db: Session, query: str) -> Optional[Dict[str, Any]]:
        """Get user by query.
        
        Args:
        --- 
            db (Session) : The database session.
            query (str) : The query to get the user.

        Returns:
        --- 
            User : The user object.
        """
        query = query + " AND is_active = True AND is_superuser = False"

        user = db.query(User).filter(text(query)).first()
        if user:
            return user.to_dict()
        return None
    
    def get_user_with_relationships(self, db: Session, user_id: int) -> Optional[User]:
        """Get user with all related data (bank accounts, loans, investments).
        
        Args:
            db (Session): The database session.
            user_id (int): The ID of the user to get.

        Returns:
            User: The user object with relationships loaded.
        """
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            # Load relationships
            _ = user.bank_accounts
            _ = user.loans
            _ = user.investments
        return user

user = CRUDUser()