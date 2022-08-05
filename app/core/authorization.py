from functools import wraps

from app import crud
from app.core.exceptions import NotAllowedException


def authorize_to_create_project(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user = kwargs['user']
        if not user.is_manager():
            raise NotAllowedException()
        return func(*args, **kwargs)
    return wrapper


def authorize_to_update_or_delete_task(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user = kwargs['user']
        task = crud.task.get(db=kwargs['db'], id=kwargs['task_id'])
        is_authorized = user.is_manager() or task.user_id == user.id
        if not is_authorized:
            raise NotAllowedException()
        return func(*args, **kwargs)
    return wrapper
