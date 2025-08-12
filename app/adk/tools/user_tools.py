from app.services.user_service import user_service
from app.database.session import SessionLocal
from app.core.logger import logger
from typing import Dict, Any, Optional

def get_user_details_tool(phone_number: str) -> Optional[Dict[str, Any]]:
    """
    Get the details of a user by their phone number.

    Args: 
        phone_number: The phone number of the user to get details for.
    
    Returns:
        A dictionary containing user information if found, otherwise None.
    """
    db = SessionLocal()
    try:
        logger.info(f"Getting user details for phone number: {phone_number}...")
        user = user_service.get_user_details_by_phone(db, phone_number)
        if user is None:
            logger.warning(f"User not found for phone number: {phone_number} !")
            return None
        logger.info(f"User details found for phone number: {phone_number} !")
        return user
    except Exception as e:
        logger.error(f"Error getting user details for phone number '{phone_number}': {e}")
        return None
    finally:
        db.close()


# def search_user_by_name(name: str) -> Optional[Dict[str, Any]]:
#     """
#     Search for a user by name.

#     Args:
#         name: The name of the user to search for.

#     Returns:
#         A dictionary containing user information if found, otherwise None.
#     """
#     try:
#         logger.info(f"Searching for user by name: {name}")
#         query = f"full_name ILIKE '%{name}%'"
#         user = crud_user.get_by_query(db, query)
#         if user is None:
#             logger.warning(f"User not found for query: {query}")
#             return None
        
#         logger.info(f"Search result: {user}")
#         return user

#     except Exception as e:
#         logger.error(f"Error getting user info by name '{name}': {e}")
#         return None


# def search_user_by_email(email: str) -> Optional[Dict[str, Any]]:
#     """
#     Search for a user by email.
#     Args:
#         email: The email of the user to search for.
#     Returns:
#         A dictionary containing user information if found, otherwise None.
#     """
#     try:
#         logger.info(f"Searching for user by email: {email}")
#         query = f"email ILIKE '%{email}%'"
#         user = crud_user.get_by_query(db, query=query)
#         if user is None:
#             logger.warning(f"User not found for query: {query}")
#             return None
        
#         logger.info(f"Search result: {user}")
#         return user
#     except Exception as e:
#         logger.error(f"Error getting user info by email '{email}': {e}")
#         return None
    

# def search_user_by_phone_number(phone_number: str) -> Optional[Dict[str, Any]]: 
#     """
#     Search for a user by phone number.
#     Args:
#         phone_number: The phone number of the user to search for.
#     Returns:
#         A dictionary containing user information if found, otherwise None.
#     """
#     try:
#         logger.info(f"Searching for user by phone number: {phone_number}")
#         query = f"phone_number ILIKE '%{phone_number}%'"
#         user = crud_user.get_by_query(db, query=query)            
#         if user is None:
#             logger.warning(f"User not found for query: {query}")
#             return None
        
#         logger.info(f"Search result: {user}")
#         return user
#     except Exception as e:
#         logger.error(f"Error getting user info by phone number '{phone_number}': {e}")
#         return None
    
# def search_user_by_pin_code(pin_code: str) -> Optional[Dict[str, Any]]:
#     """
#     Search for a user by pin code.
#     Args:
#         pin_code: The pin code of the user to search for.
#     Returns:
#         A dictionary containing user information if found, otherwise None.
#     """
#     try:
#         logger.info(f"Searching for user by pin code: {pin_code}")
#         query = f"pin_code ILIKE '%{pin_code}%'"
#         user = crud_user.get_by_query(db, query=query)        
#         if user is None:
#             logger.warning(f"User not found for query: {query}")
#             return None
#         logger.info(f"Search result: {user}")
#         return user
#     except Exception as e:
#         logger.error(f"Error getting user info by pin code '{pin_code}': {e}")
#         return None
    
# def search_user_holding_loans(user_id: str) -> Optional[List[Dict[str, Any]]]:
#     """
#     Search for a user's loans by user id
#     Args:
#         user_id: The ID of the user to search for.
#     Returns:
#         A list of dictionaries containing user loans if found, otherwise None.
#     """
#     try:
#         logger.info(f"Searching for user loans by user ID: {user_id}") 
#         loans = crud_loan.get_by_user_id(db, user_id)
#         if not loans:
#             logger.warning(f"User loans not found for ID: {user_id}")
#             return None
    
#         logger.info(f"{len(loans)} loans are found for user {user_id}")
#         # logger.info(f"Search result: {loans}")
#         return [loan.to_dict() for loan in loans]
#     except Exception as e:
#         logger.error(f"Error getting user loans by ID '{user_id}': {e}")
#         return None