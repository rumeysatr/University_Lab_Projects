"""
Derslik model sınıfı
"""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Classroom:
    """Derslik entity sınıfı"""
    
    id: Optional[int] = None
    name: str = ""
    faculty_id: Optional[int] = None
    capacity: int = 0
    has_computer: bool = False
    is_suitable: bool = True 
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    faculty_name: Optional[str] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'faculty_id': self.faculty_id,
            'capacity': self.capacity,
            'has_computer': self.has_computer,
            'is_suitable': self.is_suitable,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'faculty_name': self.faculty_name
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Classroom':
        return cls(
            id=data.get('id'),
            name=data.get('name', ''),
            faculty_id=data.get('faculty_id'),
            capacity=data.get('capacity', 0),
            has_computer=data.get('has_computer', False),
            is_suitable=data.get('is_suitable', True),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at'),
            faculty_name=data.get('faculty_name')
        )
    
    def __str__(self) -> str:
        faculty_display = self.faculty_name if self.faculty_name else "Belirsiz"
        suitable_status = "✓" if self.is_suitable else "✗"
        return f"{faculty_display} - {self.name} (Kapasite: {self.capacity}, Sınav Uygun: {suitable_status})"
