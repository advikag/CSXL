from fastapi import Depends
import pytest
from sqlalchemy import false, true

from backend.database import db_session
from backend.models.member_type import MembershipType
from backend.services.organization import OrganizationService
from backend.services.permission import PermissionService
from backend.models.member_details import MemberDetails


# Tested Dependencies
from ...models.member import Member
from ...models.pagination import PaginationParams
from ...services import MemberService
from ...services.exceptions import ResourceNotFoundException
from ...models import Organization
from ...services import OrganizationService


# Data Setup and Injected Service Fixtures
from .core_data import setup_insert_data_fixture
from .fixtures import (
    member_svc_integration,
    organization_svc_integration,
    user_svc,
    user_svc_integration,
    permission_svc_mock,
)

# Data Models for Fake Data Inserted in Setup
from .user_data import root, ambassador, user
from .member_data import amy, sally, rhonda, manny
from .permission_data import (
    ambassador_permission,
    ambassador_permission_coworking_reservation,
)
from .organization.organization_test_data import cads, cssg

__authors__ = ["Pallavi Sastry", "Lalitha Vadrevu", "Erin Ma", "Advika Ganesh"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


def test_get_member_details(
    member_svc_integration: MemberService,
    organization_svc_integration: OrganizationService,
):
    """Test to get member details"""
    organization_details = organization_svc_integration.get_by_slug(cads.slug)
    member_details = member_svc_integration.new_member(
        organization_details, user.id, organization_details.term, user
    )
    assert member_details.user.id == user.id
    assert member_details.user.first_name == user.first_name
    assert member_details.user.last_name == user.last_name
    assert member_details.user.last_name == user.last_name
    assert member_details.user.pronouns == user.pronouns


def test_new_member(
    member_svc_integration: MemberService,
    organization_svc_integration: OrganizationService,
):
    """Test that a new member can be added."""
    organization_details = organization_svc_integration.get_by_slug(cads.slug)
    new_member = member_svc_integration.new_member(
        organization_details, user.id, organization_details.term, user
    )
    assert new_member is not None
    assert new_member.user.first_name == sally.user.first_name
    assert new_member.user.id == sally.user_id


def test_delete_member(
    member_svc_integration: MemberService,
    organization_svc_integration: OrganizationService,
):
    """Test that a member can be deleted using their user id."""
    organization_details = organization_svc_integration.get_by_slug(cssg.slug)
    new_member = member_svc_integration.new_member(
        organization_details, root.id, organization_details.term, root
    )
    assert new_member is not None
    member_svc_integration.delete_member(
        organization_details, new_member.user_id, root, organization_details.term
    )
    assert (
        member_svc_integration.get_member_details(
            organization_details, organization_details.term, root
        )
        == []
    )


def test_get_approved_member_details(
    member_svc_integration: MemberService,
    organization_svc_integration: OrganizationService,
):
    """Test that only the approved members are being fetched by get_approved_member_details."""
    organization_details = organization_svc_integration.get_by_slug(cads.slug)
    member_svc_integration.new_member(
        organization_details, user.id, organization_details.term, root
    )
    non_approved_member_details = member_svc_integration.get_approved_member_details(
        organization_details, organization_details.term, root
    )
    assert len(non_approved_member_details) == 0
    member_svc_integration.approve_member(
        organization_details, user.id, organization_details.term, root
    )
    approved_member_details = member_svc_integration.get_approved_member_details(
        organization_details, organization_details.term, root
    )
    assert len(approved_member_details) == 1


def test_get_pending_member_details(
    member_svc_integration: MemberService,
    organization_svc_integration: OrganizationService,
):
    """Test that only the approved members are being fetched by get_approved_member_details."""
    organization_details = organization_svc_integration.get_by_slug(cads.slug)
    member_svc_integration.new_member(
        organization_details, user.id, organization_details.term, root
    )
    non_approved_member_details = member_svc_integration.get_pending_member_details(
        organization_details, organization_details.term, root
    )
    print(non_approved_member_details)
    assert len(non_approved_member_details) == 1
    member_svc_integration.approve_member(
        organization_details, user.id, organization_details.term, root
    )
    approved_member_details = member_svc_integration.get_pending_member_details(
        organization_details, organization_details.term, root
    )
    print(approved_member_details)
    assert len(approved_member_details) == 0


def test_approve_member(
    member_svc_integration: MemberService,
    organization_svc_integration: OrganizationService,
):
    """Test that a member can be approved and added to the members list."""
    organization_details = organization_svc_integration.get_by_slug(cads.slug)
    member_svc_integration.new_member(
        organization_details, root.id, organization_details.term, root
    )
    non_approved_member_details = member_svc_integration.get_approved_member_details(
        organization_details, organization_details.term, root
    )
    assert len(non_approved_member_details) == 0
    member_svc_integration.approve_member(
        organization_details, root.id, organization_details.term, root
    )
    approved_member_details = member_svc_integration.get_approved_member_details(
        organization_details, organization_details.term, root
    )

    assert approved_member_details[0].user_id == root.id
    assert approved_member_details[0].user.first_name == root.first_name


def test_get_member_by_id(
    member_svc_integration: MemberService,
    organization_svc_integration: OrganizationService,
):
    """Test to retrieve member by id."""
    organization_details = organization_svc_integration.get_by_slug(cads.slug)
    member_details = member_svc_integration.new_member(
        organization_details, user.id, organization_details.term, user
    )
    assert member_details.user.id == user.id
    assert member_details.user.first_name == user.first_name


def test_make_leader(
    member_svc_integration: MemberService,
    organization_svc_integration: OrganizationService,
):
    """Test to change the member status from MEMBER to LEADER."""
    organization_details = organization_svc_integration.get_by_slug(cads.slug)
    new_member_details = member_svc_integration.new_member(
        organization_details, user.id, organization_details.term, root
    )
    assert new_member_details.member_type == MembershipType.MEMBER
    new_leader_details = member_svc_integration.make_leader(
        organization_details, user.id, organization_details.term, root
    )
    assert new_leader_details.member_type == MembershipType.LEADER


def test_get_leader_details(
    member_svc_integration: MemberService,
    organization_svc_integration: OrganizationService,
):
    """Tests that retrieve the MemberDetails of all the LEADERs of an org."""
    organization_details = organization_svc_integration.get_by_slug(cads.slug)
    member_svc_integration.new_member(
        organization_details, user.id, organization_details.term, user
    )
    new_leader_details = member_svc_integration.make_leader(
        organization_details, user.id, organization_details.term, root
    )
    assert new_leader_details.member_type == MembershipType.LEADER
    assert user.first_name == new_leader_details.user.first_name
    assert user.last_name == new_leader_details.user.last_name
    assert user.id == new_leader_details.user.id


def test_get_member_details_by_term(
    member_svc_integration: MemberService,
    organization_svc_integration: OrganizationService,
):
    """Tests service function get_member_details_by_term."""
    organization_details = organization_svc_integration.get_by_slug(cads.slug)
    member_svc_integration.new_member(
        organization_details, root.id, organization_details.term, root
    )
    # approving member so the memeber is assigned the organization term
    member_svc_integration.approve_member(
        organization_details, root.id, organization_details.term, root
    )
    member_details_by_term = member_svc_integration.get_member_details_by_term(
        organization_details, organization_details.term, root
    )
    assert rhonda.user_id == member_details_by_term[0].user_id
    assert rhonda.user.first_name == member_details_by_term[0].user.first_name


def test_remove_leader(
    member_svc_integration: MemberService,
    organization_svc_integration: OrganizationService,
):
    """Tests the remove_leader function that changes the membership type from LEADER to MEMBER."""
    organization_details = organization_svc_integration.get_by_slug(cads.slug)
    new_member_details = member_svc_integration.new_member(
        organization_details, user.id, organization_details.term, root
    )
    assert new_member_details.member_type == MembershipType.MEMBER
    new_leader_details = member_svc_integration.make_leader(
        organization_details, user.id, organization_details.term, root
    )
    assert new_leader_details.member_type == MembershipType.LEADER
    removed_leader_details = member_svc_integration.remove_leader(
        organization_details, user.id, organization_details.term, root
    )
    assert removed_leader_details.member_type == MembershipType.MEMBER


def test_make_admin(
    member_svc_integration: MemberService,
    organization_svc_integration: OrganizationService,
):
    """Tests that the make_admiin function gives the appropriate admin status."""
    organization_details = organization_svc_integration.get_by_slug(cads.slug)
    new_member_details = member_svc_integration.new_member(
        organization_details, user.id, organization_details.term, root
    )
    admin_details = member_svc_integration.make_admin(
        organization_details,
        new_member_details.user_id,
        organization_details.term,
        root,
    )
    assert admin_details.admin_status == True


def test_remove_admin(
    member_svc_integration: MemberService,
    organization_svc_integration: OrganizationService,
):
    """Tests that the make_admiin function gives the appropriate admin status."""
    organization_details = organization_svc_integration.get_by_slug(cads.slug)
    new_member_details = member_svc_integration.new_member(
        organization_details, user.id, organization_details.term, root
    )
    admin_details = member_svc_integration.make_admin(
        organization_details,
        new_member_details.user_id,
        organization_details.term,
        root,
    )
    assert admin_details.admin_status == True
    removed_admin_details = member_svc_integration.remove_admin(
        organization_details, admin_details.user_id, organization_details.term, root
    )
    assert removed_admin_details.admin_status == False


def test_update(
    member_svc_integration: MemberService,
    organization_svc_integration: OrganizationService,
):
    """Tests that the make_admiin function gives the appropriate admin status."""
    organization_details = organization_svc_integration.get_by_slug(cads.slug)
    new_member_details = member_svc_integration.new_member(
        organization_details, user.id, organization_details.term, root
    )
    assert new_member_details.title == ""
    new_member_details.title = "Vice President"
    update_member_details = member_svc_integration.update(
        organization_details, root, new_member_details
    )
    assert update_member_details.title == "Vice President"
