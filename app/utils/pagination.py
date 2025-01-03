from typing import Optional
from sqlalchemy.orm import Query

def paginate(query: Query, limit: int, starting_after: Optional[str] = None) -> list:
    """
    Generic pagination function for SQLAlchemy queries.
    
    Args:
        query: The base SQLAlchemy query
        limit: Maximum number of items to return
        starting_after: ID of the item after which to start
        
    Returns:
        List of paginated items
    """
    if starting_after:
        query = query.filter(query.column_descriptions[0]['type'].id > starting_after)
    return query.limit(limit).all() 