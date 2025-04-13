from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.module import Module, ModuleCreate, ModuleUpdate
from app.schemas.user import User
from app.services.auth.auth_service import get_current_user
from app.services.content.module_service import create_module, get_module, get_modules_by_course, update_module

router = APIRouter()

@router.get("/course/{course_id}", response_model=List[Module])
def read_modules_by_course(
    course_id: str,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Retrieve all modules for a specific course.
    """
    return get_modules_by_course(course_id=course_id)

@router.post("/", response_model=Module)
def create_new_module(
    module_in: ModuleCreate,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Create new module.
    """
    if current_user.role not in ["instructor", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return create_module(module_in=module_in)

@router.get("/{module_id}", response_model=Module)
def read_module(
    module_id: str,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get module by ID.
    """
    module = get_module(module_id=module_id)
    if not module:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Module not found"
        )
    return module

@router.put("/{module_id}", response_model=Module)
def update_module_endpoint(
    module_id: str,
    module_in: ModuleUpdate,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Update a module.
    """
    if current_user.role not in ["instructor", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    module = get_module(module_id=module_id)
    if not module:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Module not found"
        )
    
    return update_module(module_id=module_id, module_in=module_in)
