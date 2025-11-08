import os
import uuid
from typing import Optional, BinaryIO
from pathlib import Path
from fastapi import UploadFile, HTTPException, status
from sqlalchemy.orm import Session

from app.models.template import Asset
from app.core.config import settings


class FileStorageService:
    def __init__(self, db: Session):
        self.db = db
        self.upload_dir = Path(settings.UPLOAD_DIR)
        self.upload_dir.mkdir(exist_ok=True)

    def validate_file(self, file: UploadFile) -> None:
        """Validate file size and type"""
        # Check file size
        if file.size and file.size > settings.MAX_UPLOAD_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File size exceeds maximum allowed size of {settings.MAX_UPLOAD_SIZE} bytes"
            )

        # Check file extension
        if file.filename:
            file_ext = Path(file.filename).suffix.lower()
            if file_ext not in settings.ALLOWED_EXTENSIONS:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"File type {file_ext} is not allowed"
                )

    def generate_unique_filename(self, original_filename: str) -> str:
        """Generate unique filename to prevent conflicts"""
        file_ext = Path(original_filename).suffix
        unique_id = str(uuid.uuid4())
        return f"{unique_id}{file_ext}"

    def get_file_type(self, filename: str, mime_type: str) -> str:
        """Categorize file type"""
        if mime_type.startswith('image/'):
            return 'image'
        elif mime_type.startswith('video/'):
            return 'video'
        elif mime_type.startswith('audio/'):
            return 'audio'
        elif 'pdf' in mime_type:
            return 'document'
        elif 'word' in mime_type or 'document' in mime_type:
            return 'document'
        elif 'sheet' in mime_type or 'excel' in mime_type:
            return 'spreadsheet'
        else:
            return 'other'

    async def save_uploaded_file(self, file: UploadFile, uploaded_by: int, tags: list = None) -> Asset:
        """Save uploaded file and create asset record"""
        self.validate_file(file)

        # Generate unique filename
        unique_filename = self.generate_unique_filename(file.filename)
        file_path = self.upload_dir / unique_filename

        # Save file
        try:
            with open(file_path, "wb") as buffer:
                content = await file.read()
                buffer.write(content)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error saving file: {str(e)}"
            )

        # Create asset record
        asset_type = self.get_file_type(file.filename, file.content_type)
        asset = Asset(
            filename=unique_filename,
            original_filename=file.filename,
            file_path=str(file_path),
            file_size=file.size or len(content),
            mime_type=file.content_type,
            uploaded_by=uploaded_by,
            asset_type=asset_type,
            tags=tags or []
        )

        self.db.add(asset)
        self.db.commit()
        self.db.refresh(asset)

        return asset

    def delete_file(self, asset_id: int, user_id: int) -> bool:
        """Delete file and asset record"""
        asset = self.db.query(Asset).filter(
            Asset.id == asset_id,
            Asset.uploaded_by == user_id
        ).first()

        if not asset:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Asset not found"
            )

        # Delete physical file
        try:
            file_path = Path(asset.file_path)
            if file_path.exists():
                file_path.unlink()
        except Exception as e:
            # Log error but continue with database deletion
            print(f"Error deleting file: {str(e)}")

        # Delete asset record
        self.db.delete(asset)
        self.db.commit()

        return True

    def get_file_url(self, asset: Asset) -> str:
        """Generate URL for accessing the file"""
        # In production, this would return a CDN URL or serve via FastAPI StaticFiles
        return f"/assets/{asset.filename}"

    def get_user_assets(self, user_id: int, asset_type: str = None) -> list:
        """Get all assets uploaded by a user"""
        query = self.db.query(Asset).filter(Asset.uploaded_by == user_id)
        if asset_type:
            query = query.filter(Asset.asset_type == asset_type)
        return query.all()