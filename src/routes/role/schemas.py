from pydantic import BaseModel, ConfigDict


class RoleSchema(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class RoleAccessSchema(BaseModel):
    add_user_permission: bool
    read_users_permission: bool
    update_users_permission: bool
    delete_users_permission: bool
    read_roles_permission: bool
    update_roles_permission: bool

    model_config = ConfigDict(from_attributes=True)
