% from alembic import op
import sqlalchemy as sa

% if upgrade_ops:
${upgrade_ops}

% endif
% if downgrade_ops:
${downgrade_ops}

% endif
