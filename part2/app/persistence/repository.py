class InMemoryRepository:
    def __init__(self):
        self.storage = {}

    def add(self, obj):
        """Add object to storage"""
        if not hasattr(obj, 'id'):
            return None
        self.storage[obj.id] = obj
        return obj

    def get(self, obj_id):
        """Get object by ID"""
        return self.storage.get(obj_id)

    def get_all(self):
        """Get all objects"""
        return list(self.storage.values())

    def update(self, obj_id, data):
        """Update object"""
        obj = self.get(obj_id)
        if not obj:
            return None
        for key, value in data.items():
            if hasattr(obj, key):
                setattr(obj, key, value)
        return obj

    def delete(self, obj_id):
        """Delete object"""
        if obj_id in self.storage:
            del self.storage[obj_id]
            return True
        return False

    def exists(self, obj_id):
        """Check if object exists"""
        return obj_id in self.storage

    def count(self):
        """Get count of objects"""
        return len(self.storage)
