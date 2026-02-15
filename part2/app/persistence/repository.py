"""
In-memory repository implementation
"""

class InMemoryRepository:
    """In-memory storage for objects"""
    
    def __init__(self):
        """Initialize empty storage"""
        self.storage = {}
    
    def add(self, obj):
        """Add object to storage"""
        self.storage[obj.id] = obj
        return obj
    
    def get(self, obj_id):
        """Get object by ID"""
        return self.storage.get(obj_id)
    
    def get_all(self):
        """Get all objects"""
        return list(self.storage.values())
    
    def update(self, obj_id, data):
        """Update object with new data"""
        obj = self.get(obj_id)
        if not obj:
            return None
        
        for key, value in data.items():
            if hasattr(obj, key):
                setattr(obj, key, value)
        
        if hasattr(obj, 'save'):
            obj.save()
        
        return obj
    
    def delete(self, obj_id):
        """Delete object from storage"""
        return self.storage.pop(obj_id, None)
    
    def exists(self, obj_id):
        """Check if object exists"""
        return obj_id in self.storage
    
    def clear(self):
        """Clear all storage (for testing)"""
        self.storage = {}
