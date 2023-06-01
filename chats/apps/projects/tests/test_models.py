from django.db import IntegrityError
from rest_framework.test import APITestCase

from chats.apps.projects.models import Project, ProjectPermission
from chats.apps.sectors.models import Sector


class ConstraintTests(APITestCase):
    fixtures = ["chats/fixtures/fixture_sector.json"]

    def setUp(self):
        self.project_permission = ProjectPermission.objects.get(
            uuid="e416fd45-2896-43a5-bd7a-5067f03c77fa"
        )

    def test_unique_user_permission_constraint(self):
        with self.assertRaises(IntegrityError) as context:
            ProjectPermission.objects.create(
                user=self.project_permission.user,
                project=self.project_permission.project,
            )
        self.assertTrue(
            'duplicate key value violates unique constraint "unique_user_permission"'
            in str(context.exception)
        )


class PropertyTests(APITestCase):
    fixtures = ["chats/fixtures/fixture_sector.json"]

    def setUp(self):
        self.project_permission = ProjectPermission.objects.get(
            uuid="e416fd45-2896-43a5-bd7a-5067f03c77fa"
        )
        self.project = Project.objects.get(uuid="34a93b52-231e-11ed-861d-0242ac120002")
        self.sector = Sector.objects.get(uuid="21aecf8c-0c73-4059-ba82-4343e0cc627c")

    def test_name_property(self):
        """
        Verify if the property for get project name its returning the correct value.
        """
        self.assertEqual(self.project.__str__(), self.project.name)

    def test_get_permission(self):
        """
        Verify if the property to see if user permission its returning the correct value.
        """
        permission_returned = self.project.get_permission(self.project_permission.user)
        self.assertEqual(permission_returned.user, self.project_permission.user)

    def test_admin_permissions(self):
        """
        Verify if the property to return admin permission of project its returning the correct value.
        """
        permissions_count = self.project.admin_permissions.count()
        self.assertEqual(permissions_count, 3)

    def test_random_admin(self):
        """
        Verify if the property to return admin permission of project its returning the correct value.
        """
        first_admin = self.project.admin_permissions.first()
        self.assertEqual(self.project.random_admin, first_admin)

    def test_name_property_project_permission(self):
        """
        Verify if the property for get project name its returning the correct value.
        """
        self.assertEqual(
            self.project_permission.__str__(), self.project_permission.project.name
        )

    def test_is_admin(self):
        """
        Verify if the property to see if user is admin its returning the correct value.
        """
        self.assertEqual(self.project_permission.is_admin, True)

    def test_get_project_permission(self):
        """
        Verify if the property to see if user is admin its returning the correct value.
        """
        permission_returned = self.project_permission.get_permission(
            self.project_permission.user
        )
        self.assertEqual(permission_returned.user, self.project_permission.user)

    def test_get_sectors(self):
        """
        Verify if the property to see if user is admin its returning the correct value.
        """
        sector_project = self.project.get_sectors(
            user=self.project_permission.user.email
        )

        self.assertTrue(self.sector in sector_project)

    def test_is_manager(self):
        """
        Verify if the property to see if user is admin its returning the correct value.
        """
        user_permission = self.project_permission.is_manager(sector=self.sector)
        self.assertEqual(user_permission, True)
