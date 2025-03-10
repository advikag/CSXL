from pydantic import BaseModel

from backend.models.member_type import MembershipType


__authors__ = ["Pallavi Sastry"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class Member(BaseModel):
    organization_id: int
    user_id: int
    approval_status: bool
    admin_status: bool
    member_type: MembershipType
    term: str
    title: str
