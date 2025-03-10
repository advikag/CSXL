"""Mock data for specific roles.

Two roles are setup for testing and development purposes:

1. root (will have sudo permissions to do everything)
2. ambassador (will have a subset of specific permissions)
"""

import pytest
from sqlalchemy.orm import Session
from .reset_table_id_seq import reset_table_id_seq
from ...entities.role_entity import RoleEntity
from ...models.role import Role

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

root_role = Role(id=1, name="root")
ambassador_role = Role(id=2, name="ambassadors")
appteam_role = Role(id=3, name="app-team")
acm_role = Role(id=4, name="acm")
bit_role = Role(id=5, name="bit")
cads_role = Role(id=6, name="cads")
carvr_role = Role(id=7, name="carvr")
cssg_role = Role(id=8, name="cssg")
ctf_role = Role(id=9, name="ctf")
enablingtech_role = Role(id=10, name="enabling-tech")
esports_role = Role(id=11, name="esports")
gamedev_role = Role(id=12, name="game-dev")
gwc_role = Role(id=13, name="gwc")
hacknc_role = Role(id=14, name="hacknc")
ktp_role = Role(id=15, name="ktp")
pearlhacks_role = Role(id=16, name="pearl-hacks")
pm_role = Role(id=17, name="pm-club")
queerhack_role = Role(id=18, name="queer-hack")
wics_role = Role(id=19, name="wics")


roles = [
    root_role,
    ambassador_role,
    appteam_role,
    acm_role,
    bit_role,
    cads_role,
    carvr_role,
    cssg_role,
    ctf_role,
    enablingtech_role,
    esports_role,
    gamedev_role,
    gwc_role,
    hacknc_role,
    ktp_role,
    pearlhacks_role,
    pm_role,
    queerhack_role,
    wics_role,
]

org_roles = [
    appteam_role,
    acm_role,
    bit_role,
    cads_role,
    carvr_role,
    cssg_role,
    ctf_role,
    enablingtech_role,
    esports_role,
    gamedev_role,
    gwc_role,
    hacknc_role,
    ktp_role,
    pearlhacks_role,
    pm_role,
    queerhack_role,
    wics_role,
]

def insert_fake_data(session: Session):
    for role in roles:
        entity = RoleEntity.from_model(role)
        session.add(entity)

    reset_table_id_seq(session, RoleEntity, RoleEntity.id, len(roles) + 1)


@pytest.fixture(autouse=True)
def fake_data_fixture(session: Session):
    insert_fake_data(session)
    session.commit()
    yield
