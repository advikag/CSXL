"""Definition of SQLAlchemy table-backed object mapping entity for Events."""

from sqlalchemy import Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.entities.user_entity import UserEntity
from backend.models.member import Member
from backend.models.member_type import MembershipType
from ..models.member_details import MemberDetails
from .entity_base import EntityBase
from typing import Self
from ..models.organization import Organization
from ..models.user import User

from sqlalchemy import Enum as SQLAlchemyEnum

__authors__ = ["Pallavi Sastry", "Erin Ma", "Advika Ganesh", "Lalitha Vadrevu"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class MemberEntity(EntityBase):
    """Serves as the database model schema defining the shape of the `Members` table"""

    # Name for the events table in the PostgreSQL database
    __tablename__ = "members"

    # Unique ID for the member
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # status of membership. Default to false
    approval_status: Mapped[bool] = mapped_column(Boolean, default=False)

    # admin status. Default to false
    admin_status: Mapped[bool] = mapped_column(Boolean, default=False)

    member_type: Mapped[MembershipType] = mapped_column(
        SQLAlchemyEnum(MembershipType), default=MembershipType.MEMBER
    )

    term: Mapped[str] = mapped_column(String)
    # two foreign key fields
    # Organization that is having members
    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organization.id"), primary_key=True
    )
    # User that provides member info
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)

    # relationship fields
    organization: Mapped["OrganizationEntity"] = relationship(back_populates="members")
    user: Mapped["UserEntity"] = relationship(back_populates="members")

    # Optional title
    title: Mapped[str] = mapped_column(String)

    @classmethod
    def from_model(cls, model: Member) -> Self:
        """
        Class method that converts an `Member` model into a `MemberEntity`

        Parameters:
            - model (Member): Model to convert into an entity
        Returns:
            MemberEntity: Entity created from model
        """
        return cls(
            organization_id=model.organization_id,
            user_id=model.user_id,
            approval_status=model.approval_status,
            admin_status=model.admin_status,
            member_type=model.member_type,
            term=model.term,
            title=model.title,
        )

    def to_model(self, subject: User | None = None) -> Member:
        """
        Converts a `MemberEntity` object into a `Member` model object

        Returns:
            Event: `Member` object from the entity
        """

        return Member(
            organization_id=self.organization_id,
            user_id=self.user_id,
            approval_status=self.approval_status,
            admin_status=self.admin_status,
            user=subject,
            member_type=self.member_type,
            term=self.term,
            title=self.title,
        )

    def to_details_model(self, subject: User | None = None) -> MemberDetails:
        """Create a MemberDetails model from an MemberEntity

        Returns:
            MemberDetails: A MemberDetails model for API usage.
        """

        return MemberDetails(
            organization_id=self.organization_id,
            user_id=self.user_id,
            approval_status=self.approval_status,
            admin_status=self.admin_status,
            member_type=self.member_type,
            term=self.term,
            user=subject,
            title=self.title,
        )
