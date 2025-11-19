import logging
from django.contrib.auth.models import User, Group

# Configure logging
logger = logging.getLogger(__name__)

def create_users_and_groups():
    logger.info("Starting user/group creation...")

    # Create superuser
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser("admin", "admin@example.com", "ChangeMe123!")
        logger.info("✅ Superuser 'admin' created")
    else:
        logger.info("ℹ️ Superuser 'admin' already exists")

    # Create groups
    for group_name in ["AIQ", "HEA"]:
        group, created = Group.objects.get_or_create(name=group_name)
        if created:
            logger.info(f"✅ Group '{group_name}' created")
        else:
            logger.info(f"ℹ️ Group '{group_name}' already exists")

    # AIQ admin user
    if not User.objects.filter(username="aiqadmin-xper@hma.com").exists():
        user = User.objects.create_user(
            "aiqadmin-xper@hma.com",
            "aiqadmin-xper@hma.com",
            "hma12345",
        )
        Group.objects.get(name="AIQ").user_set.add(user)
        logger.info("✅ User 'aiqadmin-xper@hma.com' created and added to group 'AIQ'")
    else:
        logger.info("ℹ️ User 'aiqadmin-xper@hma.com' already exists")

    # HEA admin user
    if not User.objects.filter(username="heaadmin-xper@hma.com").exists():
        user = User.objects.create_user(
            "heaadmin-xper@hma.com",
            "heaadmin-xper@hma.com",
            "hma12345",
        )
        Group.objects.get(name="HEA").user_set.add(user)
        logger.info("✅ User 'heaadmin-xper@hma.com' created and added to group 'HEA'")
    else:
        logger.info("ℹ️ User 'heaadmin-xper@hma.com' already exists")

    logger.info("Finished user/group creation.")

# Call the function
create_users_and_groups()