"""seed default roles

Revision ID: 95e463cde68d
Revises: 3f91d99d978a
Create Date: 2026-07-23 15:13:30.385030

"""

from typing import Sequence, Union
from datetime import datetime
import uuid

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "95e463cde68d"
down_revision: Union[str, Sequence[str], None] = "3f91d99d978a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    roles = sa.table(
        "roles",
        sa.column("id", sa.UUID()),
        sa.column("name", sa.String()),
        sa.column("description", sa.String()),
        sa.column("created_at", sa.DateTime(timezone=True)),
        sa.column("updated_at", sa.DateTime(timezone=True)),
        sa.column("created_by", sa.UUID()),
        sa.column("updated_by", sa.UUID()),
        sa.column("is_active", sa.Boolean()),
    )

    now = datetime.utcnow()

    op.bulk_insert(
        roles,
        [
            {
                "id": uuid.uuid4(),
                "name": "Super Admin",
                "description": "Full system access",
                "created_at": now,
                "updated_at": now,
                "created_by": None,
                "updated_by": None,
                "is_active": True,
            },
            {
                "id": uuid.uuid4(),
                "name": "HR Manager",
                "description": "Manage employees and leave",
                "created_at": now,
                "updated_at": now,
                "created_by": None,
                "updated_by": None,
                "is_active": True,
            },
            {
                "id": uuid.uuid4(),
                "name": "Manager",
                "description": "Approve leave requests",
                "created_at": now,
                "updated_at": now,
                "created_by": None,
                "updated_by": None,
                "is_active": True,
            },
            {
                "id": uuid.uuid4(),
                "name": "Employee",
                "description": "Standard employee access",
                "created_at": now,
                "updated_at": now,
                "created_by": None,
                "updated_by": None,
                "is_active": True,
            },
        ],
    )


def downgrade() -> None:

    op.execute(
        """
        DELETE FROM roles
        WHERE name IN (
            'Super Admin',
            'HR Manager',
            'Manager',
            'Employee'
        )
        """
    )