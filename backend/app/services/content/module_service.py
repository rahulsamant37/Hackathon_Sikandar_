from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4

from app.schemas.module import Module, ModuleCreate, ModuleUpdate
from app.services.db import get_supabase_client

def get_modules_by_course(course_id: str) -> List[Module]:
    """
    Get all modules for a specific course.
    """
    supabase = get_supabase_client()
    response = supabase.table("modules").select("*").eq("course_id", course_id).order("sequence_number").execute()
    
    modules = []
    for module_data in response.data:
        modules.append(
            Module(
                module_id=module_data["module_id"],
                course_id=module_data["course_id"],
                title=module_data["title"],
                description=module_data.get("description"),
                sequence_number=module_data["sequence_number"],
                status=module_data["status"],
                created_at=module_data["created_at"],
                updated_at=module_data.get("updated_at")
            )
        )
    
    return modules

def get_module(module_id: str) -> Optional[Module]:
    """
    Get a specific module by ID.
    """
    supabase = get_supabase_client()
    response = supabase.table("modules").select("*").eq("module_id", module_id).execute()
    
    if not response.data:
        return None
    
    module_data = response.data[0]
    return Module(
        module_id=module_data["module_id"],
        course_id=module_data["course_id"],
        title=module_data["title"],
        description=module_data.get("description"),
        sequence_number=module_data["sequence_number"],
        status=module_data["status"],
        created_at=module_data["created_at"],
        updated_at=module_data.get("updated_at")
    )

def create_module(module_in: ModuleCreate) -> Module:
    """
    Create a new module.
    """
    supabase = get_supabase_client()
    
    module_id = str(uuid4())
    now = datetime.utcnow().isoformat()
    
    new_module = {
        "module_id": module_id,
        "course_id": str(module_in.course_id),
        "title": module_in.title,
        "description": module_in.description,
        "sequence_number": module_in.sequence_number,
        "status": module_in.status,
        "created_at": now
    }
    
    supabase.table("modules").insert(new_module).execute()
    
    return Module(
        module_id=module_id,
        course_id=module_in.course_id,
        title=module_in.title,
        description=module_in.description,
        sequence_number=module_in.sequence_number,
        status=module_in.status,
        created_at=now
    )

def update_module(module_id: str, module_in: ModuleUpdate) -> Optional[Module]:
    """
    Update a module.
    """
    supabase = get_supabase_client()
    
    # Get current module data
    current_module = get_module(module_id)
    if not current_module:
        return None
    
    # Prepare update data
    update_data = {}
    if module_in.title is not None:
        update_data["title"] = module_in.title
    if module_in.description is not None:
        update_data["description"] = module_in.description
    if module_in.sequence_number is not None:
        update_data["sequence_number"] = module_in.sequence_number
    if module_in.status is not None:
        update_data["status"] = module_in.status
    
    update_data["updated_at"] = datetime.utcnow().isoformat()
    
    # Update module
    supabase.table("modules").update(update_data).eq("module_id", module_id).execute()
    
    # Get updated module
    return get_module(module_id)
