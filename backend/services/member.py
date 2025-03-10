from sqlite3 import IntegrityError
from typing import Sequence
from sqlalchemy.orm import joinedload

from fastapi import Depends
from sqlalchemy.orm import Session
from backend.entities.member_entity import MemberEntity
from backend.entities.role_entity import RoleEntity
from backend.entities.user_entity import UserEntity
from backend.models import permission
from backend.models.member_details import MemberDetails
from backend.models.organization_details import OrganizationDetails
from backend.models.member_type import MembershipType
from backend.models.member import Member
from backend.models.role import Role


from ..models import User
from ..database import db_session
from .permission import PermissionService
from . import UserService
from .exceptions import ResourceNotFoundException

from .exceptions import ResourceNotFoundException


__authors__ = ["Pallavi Sastry", "Lalitha Vadrevu", "Erin Ma", "Advika Ganesh"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class MemberService:
    """Service that performs all of the actions on the `Member` table"""

    _session: Session
    id: int = 0

    roles_dict = {
        "app-team": 3,
        "acm": 4,
        "bit": 5,
        "cads": 6,
        "carvr": 7,
        "cssg": 8,
        "ctf": 9,
        "enabling-tech": 10,
        "esports": 11,
        "game-dev": 12,
        "gwc": 13,
        "hacknc": 14,
        "ktp": 15,
        "pearl-hacks": 16,
        "pm-club": 17,
        "queer-hack": 18,
        "wics": 19,
    }

    def __init__(
        self,
        session: Session = Depends(db_session),
        permission: PermissionService = Depends(),
        user_svc: UserService = Depends(),
    ):
        """Initializes the `MemberService` session"""
        self._session = session
        self._permission = permission
        self._user_svc = user_svc

    def approve_member(
        self,
        organization: OrganizationDetails,
        member_id: int,
        term: str,
        subject: User,
    ) -> MemberDetails:
        """Approves a member to add them officially to the organization.
        Args:
            organization_id: The ID of the organization to which the member belongs.
            member_id: The ID of the member to add.
            subject: The user attempting to perform the add operation.
        """
        member = (
            self._session.query(MemberEntity)
            .filter(
                MemberEntity.user_id == member_id,
                MemberEntity.organization_id == organization.id,
                MemberEntity.term == term,
            )
            .one()
        )

        self._permission.enforce(
            subject,
            "member.approve_member",
            f"organization/{organization.slug}",
        )

        member.approval_status = True
        self._session.commit()
        return member.to_details_model(subject)

    def get_member_details(
        self, organization: OrganizationDetails, term: str, subject: User | None = None
    ) -> list[MemberDetails]:

        self._permission.enforce(
            subject,
            "member.get_member_details",
            f"organization/{organization.slug}",
        )
        if organization.users != [None]:

            members = (
                self._session.query(MemberEntity)
                .filter(
                    MemberEntity.organization_id == organization.id,
                    MemberEntity.approval_status == True,
                    MemberEntity.member_type == MembershipType.MEMBER,
                    MemberEntity.term == term,
                )
                .all()
            )

            member_info = []
            for member in members:
                input_user = UserEntity.to_model(member.user)
                member_info.append(member.to_details_model(input_user))

            return member_info

    def get_approved_member_details(
        self, organization: OrganizationDetails, term: str, subject: User | None = None
    ) -> list[MemberDetails]:

        members = (
            self._session.query(MemberEntity)
            .filter(
                MemberEntity.organization_id == organization.id,
                MemberEntity.approval_status == True,
                MemberEntity.member_type == MembershipType.MEMBER,
                MemberEntity.term == term,
            )
            .all()
        )

        member_info = []
        for member in members:
            input_user = UserEntity.to_model(member.user)
            member_info.append(member.to_details_model(input_user))

        return member_info

    def get_pending_member_details(
        self, organization: OrganizationDetails, term: str, subject: User | None = None
    ) -> list[MemberDetails]:

        members = (
            self._session.query(MemberEntity)
            .filter(
                MemberEntity.organization_id == organization.id,
                MemberEntity.approval_status == False,
                MemberEntity.term == term,
            )
            .all()
        )

        self._permission.enforce(
            subject,
            "member.get_pending_member_details",
            f"organization/{organization.slug}",
        )

        member_info = []
        for member in members:
            input_user = UserEntity.to_model(member.user)
            member_info.append(member.to_details_model(input_user))

        return member_info

    def new_member(
        self,
        organization: OrganizationDetails,
        memberId: int,
        termId: str,
        subject: User,
    ) -> MemberDetails:
        """Stores a member in the database.

        Args:
            subject: currently logged in user
        Returns:
            MemberDetails: Added member.
        """

        existing_member = (
            self._session.query(MemberEntity)
            .filter(MemberEntity.organization_id == organization.id)
            .filter(MemberEntity.user_id == memberId)
            .first()
        )

        if existing_member:
            return MemberDetails()

        model = Member(
            organization_id=organization.id,
            user_id=memberId,
            approval_status=False,
            admin_status=False,
            member_type=MembershipType.MEMBER,
            term=termId,
            title="",
        )

        member_entity = MemberEntity.from_model(model)

        member_entity.id = memberId
        self._session.add(member_entity)
        self._session.commit()
        organization.users.append(subject)

        return member_entity.to_details_model(subject)

    def delete_member(
        self,
        organization: OrganizationDetails,
        member_id: int,
        subject: User,
        term: str,
    ) -> None:
        """Deletes a member from an organization.

        Args:
            organization_id: The ID of the organization to which the member belongs.
            member_id: The ID of the member to delete.
            subject: The user attempting to perform the delete operation.

        """

        self._permission.enforce(
            subject,
            "member.delete_member",
            f"organization/{organization.slug}",
        )
        member = (
            self._session.query(MemberEntity)
            .filter(
                MemberEntity.user_id == member_id,
                MemberEntity.organization_id == organization.id,
                MemberEntity.term == term,
            )
            .one()
        )

        user_to_remove = member.user  # Grab the user before deleting the member
        self._session.delete(member)
        self._session.commit()
        member_model = member.user.to_model()
        organization.users.remove(member_model)

    def make_admin(
        self,
        organization: OrganizationDetails,
        member_id: int,
        term: str,
        subject: User,
    ) -> MemberDetails:
        """Makes an approved member an admin of the organization.
        Args:
            organization_id: The ID of the organization to which the member belongs.
            member_id: The ID of the member to add.
            subject: The user attempting to perform the add operation.
        """

        self._permission.enforce(
            subject,
            "member.make_admin",
            f"organization/{organization.slug}",
        )

        member = (
            self._session.query(MemberEntity)
            .filter(
                MemberEntity.user_id == member_id,
                MemberEntity.organization_id == organization.id,
                MemberEntity.term == term,
            )
            .one()
        )

        role_id = self.roles_dict[organization.slug]

        member.admin_status = True
        self._session.commit()
        role = self._session.get(RoleEntity, role_id)
        user = self._session.get(UserEntity, member.user_id)
        if user:
            role.users.append(user)
            self._session.commit()

        input_user = UserEntity.to_model(member.user)
        return member.to_details_model(input_user)

    def remove_admin(
        self,
        organization: OrganizationDetails,
        member_id: int,
        term: str,
        subject: User,
    ) -> MemberDetails:
        """Makes an approved member an admin of the organization.
        Args:
            organization_id: The ID of the organization to which the member belongs.
            member_id: The ID of the member to add.
            subject: The user attempting to perform the add operation.
        """

        self._permission.enforce(
            subject,
            "member.remove_admin",
            f"organization/{organization.slug}",
        )

        member = (
            self._session.query(MemberEntity)
            .filter(
                MemberEntity.user_id == member_id,
                MemberEntity.organization_id == organization.id,
                MemberEntity.term == term,
            )
            .one()
        )

        role_id = self.roles_dict[organization.slug]
        member.admin_status = False
        self._session.commit()
        role = self._session.get(RoleEntity, role_id)
        user = self._session.get(UserEntity, member.id)
        role.users.remove(user)
        self._session.commit()
        input_user = UserEntity.to_model(member.user)
        return member.to_details_model(input_user)

    def get_member_by_id(
        self,
        organization: OrganizationDetails,
        term: str,
        member_id: int,
        subject: User,
    ) -> list[MemberDetails]:
        """Approves a member to make them an admin of the organization.
        Args:
            organization_id: The ID of the organization to which the member belongs.
            member_id: The ID of the member to add.
            subject: The user attempting to perform the add operation.
        """

        self._permission.enforce(
            subject,
            "member.get_member_by_id",
            f"organization/{organization.slug}",
        )

        member = (
            self._session.query(MemberEntity)
            .filter(
                MemberEntity.user_id == member_id,
                MemberEntity.organization_id == organization.id,
                MemberEntity.term == term,
            )
            .one()
        )
        input_user = UserEntity.to_model(member.user)
        return [member.to_details_model(input_user)]

    def make_leader(
        self,
        organization: OrganizationDetails,
        member_id: int,
        term: str,
        subject: User,
    ) -> MemberDetails:
        """Makes an approved member into a leader.
        Args:
            organization_id: The ID of the organization to which the member belongs.
            member_id: The ID of the member to add.
            subject: The user attempting to perform the add operation.
        """

        self._permission.enforce(
            subject,
            "member.make_leader",
            f"organization/{organization.slug}",
        )

        member = (
            self._session.query(MemberEntity)
            .filter(
                MemberEntity.user_id == member_id,
                MemberEntity.organization_id == organization.id,
                MemberEntity.term == term,
            )
            .one()
        )
        member.member_type = MembershipType.LEADER
        self._session.commit()
        input_user = UserEntity.to_model(member.user)
        return member.to_details_model(input_user)

    def get_leader_details(
        self, organization: OrganizationDetails, term: str
    ) -> list[MemberDetails]:

        members = (
            self._session.query(MemberEntity)
            .filter(
                MemberEntity.organization_id == organization.id,
                MemberEntity.member_type == MembershipType.LEADER,
                MemberEntity.term == term,
            )
            .all()
        )

        member_info = []
        for member in members:
            input_user = UserEntity.to_model(member.user)
            member_info.append(member.to_details_model(input_user))

        return member_info

    def get_member_details_by_term(
        self, organization: OrganizationDetails, term: str, subject: User | None = None
    ) -> list[MemberDetails]:
        """
        Get all members from an organization filtered by term.

        Args:
            organization: The OrganizationDetails object representing the organization
            term: a string representing the term to filter members by term
            subject: The user attempting to perform the operation

        Returns:
            list[MemberDetails]: All member details filtered by term
        """
        # Implement logic to fetch members filtered by term from the database
        members = (
            self._session.query(MemberEntity)
            .filter(
                MemberEntity.organization_id == organization.id,
                MemberEntity.term == term,
            )
            .all()
        )

        member_info = []
        for member in members:
            input_user = UserEntity.to_model(member.user)
            member_info.append(member.to_details_model(input_user))

        return member_info

    def remove_leader(
        self,
        organization: OrganizationDetails,
        member_id: int,
        term: str,
        subject: User,
    ) -> MemberDetails:
        """Changes the membership type from LEADER to MEMBER
        Args:
            organization_id: The ID of the organization to which the member belongs.
            member_id: The ID of the member to add.
            subject: The user attempting to perform the add operation.
        """

        self._permission.enforce(
            subject,
            "member.remove_leader",
            f"organization/{organization.slug}",
        )

        member = (
            self._session.query(MemberEntity)
            .filter(
                MemberEntity.user_id == member_id,
                MemberEntity.organization_id == organization.id,
                MemberEntity.term == term,
            )
            .one()
        )

        member.member_type = MembershipType.MEMBER
        self._session.commit()
        input_user = UserEntity.to_model(member.user)

        return member.to_details_model(input_user)

    def update(
        self,
        organization: OrganizationDetails,
        subject: User,
        member: MemberDetails,
    ) -> MemberDetails:
        """
        Update the member details

        Parameters:
            subject: a valid User model representing the currently logged in User
            member (Member): Member to be updated

        Returns:
            Member: Updated member object
        """

        self._permission.enforce(
            subject,
            "member.update_leader",
            f"organization/{organization.slug}",
        )

        obj = (
            self._session.query(MemberEntity)
            .filter(
                MemberEntity.user_id == member.user_id,
                MemberEntity.organization_id == member.organization_id,
                MemberEntity.term == member.term,
            )
            .one()
            if member.user_id
            else None
        )

        if obj is None:
            raise ResourceNotFoundException(
                f"No member found with matching id: {member.user_id}"
            )

        # obj.admin_status = member.admin_status
        # obj.approval_status = member.approval_status
        # obj.member_type = member.member_type
        obj.title = member.title

        self._session.commit()

        return obj.to_details_model(subject)
