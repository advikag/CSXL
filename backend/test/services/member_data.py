import pytest
from sqlalchemy.orm import Session

from backend.entities.member_entity import MemberEntity
from backend.models.member import Member
from backend.models.member_details import MemberDetails
from backend.models.organization import Organization
from backend.models.member_type import MembershipType
from ...models.user import User
from ...entities.user_entity import UserEntity
from .reset_table_id_seq import reset_table_id_seq
from .user_data import root, ambassador, user

__authors__ = ["Pallavi Sastry", "Lalitha Vadrevu", "Erin Ma", "Advika Ganesh"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


rhonda = MemberDetails(
    organization_id=1,
    user_id=1,
    approval_status=False,
    admin_status=True,
    member_type=0,
    term="",
    title="",
    user=root,
)

amy = MemberDetails(
    organization_id=2,
    user_id=2,
    approval_status=False,
    admin_status=False,
    member_type=0,
    term="",
    title="",
    user=ambassador,
)

sally = MemberDetails(
    organization_id=3,
    user_id=3,
    approval_status=False,
    admin_status=False,
    member_type=0,
    term="",
    title="",
    user=user,
)

manny = MemberDetails(
    organization_id=4,
    user_id=4,
    approval_status=True,
    admin_status=False,
    member_type=0,
    term="",
    title="",
    user=user,
)


users = [rhonda, amy, sally]


# Define a function to insert fake data into the database
def insert_fake_data(session: Session):
    global users
    entities = []
    for user in users:
        entity = MemberEntity.from_model(user)
        session.add(entity)
        entities.append(entity)
    reset_table_id_seq(session, UserEntity, UserEntity.id, len(users) + 1)
    session.commit()


# Define a fixture to automatically insert fake data when tests are run
@pytest.fixture(autouse=True)
def fake_data_fixture(session: Session):
    insert_fake_data(session)
    session.commit()
    yield
