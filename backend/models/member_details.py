from backend.models.member import Member
from backend.models.user import User

__authors__ = ["Pallavi Sastry", "Lalitha Vadrevu", "Erin Ma", "Advika Ganesh"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class MemberDetails(Member):
    """
    Pydantic model to represent a `Member`, including the organizations the user is in

    This model is based on the `MemberEntity` model, which defines the shape
    of the `Member` database in the PostgreSQL database.
    """

    user: User
