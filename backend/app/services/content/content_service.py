from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4

from app.schemas.content import Content, ContentCreate, ContentUpdate
from app.services.db import get_supabase_client

def get_content_by_module(module_id: str) -> List[Content]:
    """
    Get all content items for a specific module.
    """
    supabase = get_supabase_client()
    response = supabase.table("content_items").select("*").eq("module_id", module_id).execute()
    
    content_items = []
    for content_data in response.data:
        content_items.append(
            Content(
                content_id=content_data["content_id"],
                module_id=content_data["module_id"],
                title=content_data["title"],
                type=content_data["type"],
                content=content_data["content"],
                metadata=content_data["metadata"],
                version=content_data["version"],
                created_at=content_data["created_at"],
                updated_at=content_data.get("updated_at")
            )
        )
    
    return content_items

def get_content(content_id: str) -> Optional[Content]:
    """
    Get a specific content item by ID.
    """
    supabase = get_supabase_client()
    response = supabase.table("content_items").select("*").eq("content_id", content_id).execute()
    
    if not response.data:
        return None
    
    content_data = response.data[0]
    return Content(
        content_id=content_data["content_id"],
        module_id=content_data["module_id"],
        title=content_data["title"],
        type=content_data["type"],
        content=content_data["content"],
        metadata=content_data["metadata"],
        version=content_data["version"],
        created_at=content_data["created_at"],
        updated_at=content_data.get("updated_at")
    )

def create_content(content_in: ContentCreate) -> Content:
    """
    Create a new content item.
    """
    supabase = get_supabase_client()
    
    content_id = str(uuid4())
    now = datetime.utcnow().isoformat()
    
    new_content = {
        "content_id": content_id,
        "module_id": str(content_in.module_id),
        "title": content_in.title,
        "type": content_in.type,
        "content": content_in.content,
        "metadata": content_in.metadata,
        "version": content_in.version,
        "created_at": now
    }
    
    supabase.table("content_items").insert(new_content).execute()
    
    return Content(
        content_id=content_id,
        module_id=content_in.module_id,
        title=content_in.title,
        type=content_in.type,
        content=content_in.content,
        metadata=content_in.metadata,
        version=content_in.version,
        created_at=now
    )

def update_content(content_id: str, content_in: ContentUpdate) -> Optional[Content]:
    """
    Update a content item.
    """
    supabase = get_supabase_client()
    
    # Get current content data
    current_content = get_content(content_id)
    if not current_content:
        return None
    
    # Prepare update data
    update_data = {}
    if content_in.title is not None:
        update_data["title"] = content_in.title
    if content_in.content is not None:
        update_data["content"] = content_in.content
    if content_in.metadata is not None:
        update_data["metadata"] = content_in.metadata
    if content_in.version is not None:
        update_data["version"] = content_in.version
    
    update_data["updated_at"] = datetime.utcnow().isoformat()
    
    # Update content
    supabase.table("content_items").update(update_data).eq("content_id", content_id).execute()
    
    # Get updated content
    return get_content(content_id)
