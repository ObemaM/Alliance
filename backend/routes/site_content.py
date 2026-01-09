from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_db
from models.site_content import SiteContent
from schemas.site_content import SiteContentResponse, SiteContentCreate, SiteContentUpdate

router = APIRouter(prefix="/site-content", tags=["Site Content"])


@router.get("/", response_model=list[SiteContentResponse])
async def get_all_content(db: AsyncSession = Depends(get_db)):
    query = select(SiteContent)
    result = await db.execute(query)
    content = result.scalars().all()
    return content


@router.get("/{key}", response_model=SiteContentResponse)
async def get_content_by_key(key: str, db: AsyncSession = Depends(get_db)):
    query = select(SiteContent).where(SiteContent.key == key)
    result = await db.execute(query)
    content = result.scalar_one_or_none()
    
    if not content:
        raise HTTPException(status_code=404, detail="Контент не найден")
    
    return content


@router.post("/", response_model=SiteContentResponse)
async def create_content(content: SiteContentCreate, db: AsyncSession = Depends(get_db)):
    new_content = SiteContent(
        key=content.key,
        value=content.value,
        description=content.description
    )
    db.add(new_content)
    await db.commit()
    await db.refresh(new_content)
    return new_content


@router.patch("/{content_id}", response_model=SiteContentResponse)
async def update_content(
    content_id: int,
    content: SiteContentUpdate,
    db: AsyncSession = Depends(get_db)
):
    query = select(SiteContent).where(SiteContent.id == content_id)
    result = await db.execute(query)
    db_content = result.scalar_one_or_none()
    
    if not db_content:
        raise HTTPException(status_code=404, detail="Контент не найден")
    
    if content.key is not None:
        db_content.key = content.key
    if content.value is not None:
        db_content.value = content.value
    if content.description is not None:
        db_content.description = content.description
    
    await db.commit()
    await db.refresh(db_content)
    return db_content


@router.delete("/{content_id}")
async def delete_content(content_id: int, db: AsyncSession = Depends(get_db)):
    query = select(SiteContent).where(SiteContent.id == content_id)
    result = await db.execute(query)
    db_content = result.scalar_one_or_none()
    
    if not db_content:
        raise HTTPException(status_code=404, detail="Контент не найден")
    
    await db.delete(db_content)
    await db.commit()
    
    return {"message": "Контент удален"}
