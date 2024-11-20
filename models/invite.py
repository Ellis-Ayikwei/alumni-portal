import code
from datetime import datetime
from click import DateTime, group
from sqlalchemy import Column, Date, ForeignKey, Integer, String
from models import user
from models.basemodel import BaseModel, Base



class Invite(BaseModel, Base):
    """
    A model representing an invite code
    """
    __tablename__ = 'invites'


    code = Column(String(100), nullable=False)
    last_used_at = Column(Date, nullable=True)
    group_id = Column(String(60), ForeignKey('alumni_groups.id'), nullable=False)
    creator_id = Column(String(60), ForeignKey('users.id'), nullable=True)
    times_used = Column(Integer, default=0)
    

    def generate_code(self) -> 'Invite':
        """Generate an invite code for a user.

        Generates a new unique invite code for the specified group, user, and group member.

        Returns:
            Invite: The newly created Invite object
        """
        from models import storage
        
       
        existing_invite: Invite = (
            storage._DBStorage__session.query(Invite)
            .filter_by(group_id=self.group_id, creator_id=self.creator_id)
            .first()
        )
        if existing_invite:
            return existing_invite
        
        new_code = generate_base62_uuid(12)
        print("new_code", new_code)
        self.code = new_code
        storage.new(self)
        storage.save()
        return self
        
        


def generate_base62_uuid(length=8):
    """
    Generate a Base62-encoded UUID4 with a specified length.

    Parameters:
        length (int): Desired length of the generated ID.

    Returns:
        str: A Base62-encoded UUID4 string.
        
    """
    
    import uuid
    import base64
    full_uuid = uuid.uuid4()

    uuid_bytes = full_uuid.bytes

    base64_uuid = base64.urlsafe_b64encode(uuid_bytes).decode('utf-8')

    base62_uuid = base64_uuid.rstrip("=").replace("-", "").replace("_", "")[:length]

    return base62_uuid


