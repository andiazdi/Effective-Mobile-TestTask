from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.dependencies.database import base


class Role(base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)

    users = relationship("User", back_populates="role")

class RoleAccess(base):
    __tablename__ = "role_access"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    add_user_permission = Column(Boolean, default=False)
    read_users_permission = Column(Boolean, default=False)
    update_users_permission = Column(Boolean, default=False)
    delete_users_permission = Column(Boolean, default=False)
    read_roles_permission = Column(Boolean, default=False)
    update_roles_permission = Column(Boolean, default=False)
