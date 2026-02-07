"""Task monitoring utilities."""

from celery.result import AsyncResult
from app.tasks.celery_app import celery_app
from typing import Dict, Any


def get_task_status(task_id: str) -> Dict[str, Any]:
    """
    Get the status of a Celery task.
    
    Args:
        task_id: Celery task ID
        
    Returns:
        Dictionary with task status information
    """
    result = AsyncResult(task_id, app=celery_app)
    
    response = {
        "task_id": task_id,
        "status": result.state,
        "ready": result.ready(),
        "successful": result.successful() if result.ready() else None,
    }
    
    if result.state == "PENDING":
        response["info"] = "Task is waiting to be executed"
    elif result.state == "PROGRESS":
        response["info"] = result.info
    elif result.state == "SUCCESS":
        response["result"] = result.result
    elif result.state == "FAILURE":
        response["error"] = str(result.info)
    else:
        response["info"] = str(result.info)
    
    return response


def revoke_task(task_id: str, terminate: bool = False) -> Dict[str, Any]:
    """
    Revoke a running task.
    
    Args:
        task_id: Celery task ID
        terminate: Whether to terminate the task immediately
        
    Returns:
        Dictionary with revocation status
    """
    celery_app.control.revoke(task_id, terminate=terminate)
    
    return {
        "task_id": task_id,
        "revoked": True,
        "terminated": terminate
    }


def get_active_tasks() -> Dict[str, Any]:
    """
    Get all active tasks.
    
    Returns:
        Dictionary with active tasks information
    """
    inspect = celery_app.control.inspect()
    
    active = inspect.active()
    scheduled = inspect.scheduled()
    reserved = inspect.reserved()
    
    return {
        "active": active or {},
        "scheduled": scheduled or {},
        "reserved": reserved or {}
    }
