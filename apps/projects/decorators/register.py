from functools import wraps

def db_transaction(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        session = kwargs.get('session')
        try:
            result = func(*args, **kwargs)
            if session:
                session.commit()
            return result
        except Exception as e:
            print(f"Error: {e}")
            if session:
                session.rollback()
            raise  # Propaga la excepción después de hacer el rollback
        finally:
            if session and session.is_active:
                session.close()
    return wrapper