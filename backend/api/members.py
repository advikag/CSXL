"""Event API

Event routes are used to create, retrieve, and update Events."""

from http.client import HTTPException
from fastapi import APIRouter, Depends
from backend.models.member import Member
from backend.models.member_details import MemberDetails

from backend.services.member import MemberService
from backend.services.organization import OrganizationService

from .authentication import registered_user
from ..models.user import User

__authors__ = ["Pallavi Sastry", "Lalitha Vadrevu", "Erin Ma", "Advika Ganesh"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"

api = APIRouter(prefix="/api")
openapi_tags = {
    "name": "Members",
    "description": "Create, update, delete, and retrieve CS members part of an organization.",
}


@api.get(
    "/organizations/{slug}/members/{term}",
    response_model=list[MemberDetails],
    tags=["Members"],
)
def get_member_details(
    slug: str,
    term: str,
    subject: User = Depends(registered_user),
    member_service: MemberService = Depends(),
    organization_service: OrganizationService = Depends(),
) -> list[MemberDetails]:
    """
    Get all member from an organization

    Args:
        slug: a valid str representing a unique Organization
        subject: a valid User model representing the currently logged in User
        event_service: a valid MemberService
        orgnaization_service: a valid OrganizationService

    Returns:
        list[MemberDetails]: All `MemberDetails`s in the `Member` database table from a specific organization
    """
    organization = organization_service.get_by_slug(slug)
    return member_service.get_member_details_by_term(organization, term, subject)
    # return member_service.get_member_details(organization, subject)


@api.get(
    "/organizations/{slug}/members/{term}/{memberId}/edit",
    response_model=list[MemberDetails],
    tags=["Members"],
)
def get_members_by_id(
    slug: str,
    term: str,
    memberId: int,
    subject: User = Depends(registered_user),
    member_service: MemberService = Depends(),
    organization_service: OrganizationService = Depends(),
) -> list[MemberDetails]:
    """
    Get all member from an organization

    Args:
        slug: a valid str representing a unique Organization
        subject: a valid User model representing the currently logged in User
        event_service: a valid MemberService
        orgnaization_service: a valid OrganizationService

    Returns:
        list[MemberDetails]: All `MemberDetails`s in the `Member` database table from a specific organization
    """
    organization = organization_service.get_by_slug(slug)
    return member_service.get_member_by_id(organization, term, memberId, subject)


@api.get(
    "/organizations/{slug}/members/{term}/approved",
    response_model=list[MemberDetails],
    tags=["Members"],
)
def get_approved_member_details(
    slug: str,
    term: str,
    subject: User = Depends(registered_user),
    member_service: MemberService = Depends(),
    organization_service: OrganizationService = Depends(),
) -> list[MemberDetails]:
    """
    Get all approved member from an organization

    Args:
        slug: a valid str representing a unique Organization
        subject: a valid User model representing the currently logged in User
        member_service: a valid MemberService
        orgnaization_service: a valid OrganizationService
        term: academic semester term

    Returns:
        list[MemberDetails]: All `MemberDetails`s in the `Member` database table from a specific organization
    """
    organization = organization_service.get_by_slug(slug)
    return member_service.get_approved_member_details(organization, term, subject)


@api.get(
    "/organizations/{slug}/members/{term}/pending",
    response_model=list[MemberDetails],
    tags=["Members"],
)
def get_pending_member_details(
    slug: str,
    term: str,
    subject: User = Depends(registered_user),
    member_service: MemberService = Depends(),
    organization_service: OrganizationService = Depends(),
) -> list[MemberDetails]:
    """
    Get all pending member from an organization

    Args:
        slug: a valid str representing a unique Organization
        subject: a valid User model representing the currently logged in User
        member_service: a valid MemberService
        orgnaization_service: a valid OrganizationService
        term: academic semester term

    Returns:
        list[MemberDetails]: All `MemberDetails`s in the `Member` database table from a specific organization
    """
    organization = organization_service.get_by_slug(slug)
    return member_service.get_pending_member_details(organization, term, subject)


@api.put(
    "/organizations/{slug}/members/{term}/{memberId}/approved",
    response_model=MemberDetails,
    tags=["Member"],
)
def approve_member(
    slug: str,
    memberId: int,
    term: str,
    subject: User = Depends(registered_user),
    member_service: MemberService = Depends(),
    organization_service: OrganizationService = Depends(),
) -> MemberDetails:
    """
    approve member.
    Parameters:
        slug: a valid str representing a unique Organization
        subject: a valid User model representing the currently logged in User
        member_service: a valid MemberService
        orgnaization_service: a valid OrganizationService
        term: academic semester term
    Returns:
        Member: modifies member approval status
    """
    organization = organization_service.get_by_slug(slug)
    return member_service.approve_member(organization, memberId, term, subject)


@api.put(
    "/organizations/{slug}/members/{term}/{memberId}/admin",
    response_model=MemberDetails,
    tags=["Member"],
)
def admin_status(
    slug: str,
    memberId: int,
    term: str,
    subject: User = Depends(registered_user),
    member_service: MemberService = Depends(),
    organization_service: OrganizationService = Depends(),
) -> MemberDetails:
    """
    Make an approved member into an admin.
    Parameters:
        slug: a valid str representing a unique Organization
        subject: a valid User model representing the currently logged in User
        member_service: a valid MemberService
        orgnaization_service: a valid OrganizationService
        term: academic semester term
    Returns:
        Member: modifies admin status
    """
    organization = organization_service.get_by_slug(slug)
    return member_service.make_admin(organization, memberId, term, subject)


@api.put(
    "/organizations/{slug}/members/{term}/{memberId}/removeAdmin",
    response_model=MemberDetails,
    tags=["Member"],
)
def remove_admin(
    slug: str,
    memberId: int,
    term: str,
    subject: User = Depends(registered_user),
    member_service: MemberService = Depends(),
    organization_service: OrganizationService = Depends(),
) -> MemberDetails:
    """
    Remove admin from admin status
    Parameters:
        slug: a valid str representing a unique Organization
        subject: a valid User model representing the currently logged in User
        member_service: a valid MemberService
        orgnaization_service: a valid OrganizationService
        term: academic semester term
    Returns:
        Member: modifies member
    """
    organization = organization_service.get_by_slug(slug)
    return member_service.remove_admin(organization, memberId, term, subject)


@api.post(
    "/organizations/{slug}/members/{term}/{memberId}",
    response_model=MemberDetails,
    tags=["Member"],
)
def add_member(
    slug: str,
    memberId: int,
    term: str,
    subject: User = Depends(registered_user),
    member_service: MemberService = Depends(),
    organization_service: OrganizationService = Depends(),
) -> MemberDetails:
    """
    Create member.

    Parameters:
        member_service: a valid MemberService

    Returns:
        Member: Adds member
    """
    organization = organization_service.get_by_slug(slug)
    try:
        return member_service.new_member(organization, memberId, term, subject)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to add member")


@api.delete(
    "/organizations/{slug}/members/{term}/{memberId}",
    response_model=None,
    tags=["Member"],
)
def delete_member(
    slug: str,
    memberId: int,
    term: str,
    subject: User = Depends(registered_user),
    member_service: MemberService = Depends(),
    organization_service: OrganizationService = Depends(),
) -> None:
    """
    Delete member.

    Parameters:
        slug: a valid str representing a unique Organization
        subject: a valid User model representing the currently logged in User
        member_service: a valid MemberService
        orgnaization_service: a valid OrganizationService
        term: academic semester term

    Returns:
        Member: Adds member
    """
    organization = organization_service.get_by_slug(slug)
    member_service.delete_member(organization, memberId, subject, term)
    return {"message": "Member deleted successfully"}


@api.put(
    "/organizations/{slug}/members/{term}/{memberId}/leader",
    response_model=MemberDetails,
    tags=["Member"],
)
def make_leader(
    slug: str,
    memberId: int,
    term: str,
    subject: User = Depends(registered_user),
    member_service: MemberService = Depends(),
    organization_service: OrganizationService = Depends(),
) -> MemberDetails:
    """
    Make an approved member into a leader
    Parameters:
        slug: a valid str representing a unique Organization
        subject: a valid User model representing the currently logged in User
        member_service: a valid MemberService
        orgnaization_service: a valid OrganizationService
        term: academic semester term
    Returns:
        Member: modifies member
    """
    organization = organization_service.get_by_slug(slug)
    return member_service.make_leader(organization, memberId, term, subject)


@api.get(
    "/organizations/{slug}/members/{term}/getLeaders",
    response_model=list[MemberDetails],
    tags=["Members"],
)
def get_leader_details(
    slug: str,
    term: str,
    member_service: MemberService = Depends(),
    organization_service: OrganizationService = Depends(),
) -> list[MemberDetails]:
    """
    Get all leaders from an organization

    Args:
        slug: a valid str representing a unique Organization
        subject: a valid User model representing the currently logged in User
        member_service: a valid MemberService
        orgnaization_service: a valid OrganizationService
        term: academic semester term

    Returns:
        list[MemberDetails]: All `MemberDetails`s in the `Member` database table from a specific organization
    """
    organization = organization_service.get_by_slug(slug)
    return member_service.get_leader_details(organization, term)


@api.put(
    "/organizations/{slug}/members/{term}/{memberId}/removeLeader",
    response_model=MemberDetails,
    tags=["Members"],
)
def remove_leader(
    slug: str,
    memberId: int,
    term: str,
    subject: User = Depends(registered_user),
    member_service: MemberService = Depends(),
    organization_service: OrganizationService = Depends(),
) -> MemberDetails:
    """
    Changes the membership type from LEADER to MEMBER
    Parameters:
        slug: a valid str representing a unique Organization
        subject: a valid User model representing the currently logged in User
        member_service: a valid MemberService
        orgnaization_service: a valid OrganizationService
        term: academic semester term
    Returns:
        Member: modifies member
    """
    organization = organization_service.get_by_slug(slug)
    return member_service.remove_leader(organization, memberId, term, subject)


@api.put(
    "/organizations/{slug}/members/{term}/{memberId}/edit",
    response_model=MemberDetails,
    tags=["Members"],
)
def update_member(
    slug: str,
    member: MemberDetails,
    subject: User = Depends(registered_user),
    member_service: MemberService = Depends(),
    organization_service: OrganizationService = Depends(),
) -> MemberDetails:
    """
    Update member

    Parameters:
        member: a valid MemberDetails model
        subject: a valid User model representing the currently logged in User
        member_service: a valid MemberService

    Returns:
        Member: Updated member
    """
    organization = organization_service.get_by_slug(slug)
    return member_service.update(organization, subject, member)
