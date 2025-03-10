"""Determines the if the member is a member or a leader"""

from enum import Enum

__authors__ = ["Pallavi Sastry", "Lalitha Vadrevu", "Erin Ma", "Advika Ganesh"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class MembershipType(Enum):
    """
    Determines the type of membership
    """

    MEMBER = 0
    LEADER = 1
