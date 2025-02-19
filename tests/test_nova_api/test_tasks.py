"""Test the part of the API to do with tasks."""
import unittest
import os
import uuid
from datetime import datetime, date
import random
import json

from dotenv import load_dotenv

from itk_dev_shared_components.kmd_nova.authentication import NovaAccess
from itk_dev_shared_components.kmd_nova.nova_objects import Task, Caseworker
from itk_dev_shared_components.kmd_nova import nova_cases, nova_tasks

load_dotenv()


class NovaCasesTest(unittest.TestCase):
    """Test the part of the API to do with tasks."""
    @classmethod
    def setUpClass(cls):
        credentials = os.getenv('NOVA_CREDENTIALS')
        credentials = credentials.split(',')
        cls.nova_access = NovaAccess(client_id=credentials[0], client_secret=credentials[1])

    def test_get_tasks(self):
        """Test getting tasks from a case."""
        case = self._get_test_case()
        tasks = nova_tasks.get_tasks(case.uuid, self.nova_access)
        task = self._find_task_by_title(tasks, "Test opgave")

        self.assertIsInstance(task, Task)
        self.assertEqual(task.deadline.date(), date(2024, 2, 6))
        self.assertEqual(task.started_date.date(), date(2024, 2, 7))
        self.assertEqual(task.closed_date.date(), date(2024, 2, 8))
        self.assertEqual(task.description, "Dette er en beskrivelse")
        self.assertEqual(task.caseworker.ident, "AZX0080")
        self.assertEqual(task.caseworker.uuid, "0bacdddd-5c61-4676-9a61-b01a18cec1d5")
        self.assertEqual(task.status_code, "F")

    def test_add_task_minimal(self):
        """Test adding a Task to Nova with minimal information set."""
        case = self._get_test_case()

        caseworker_dict = json.loads(os.environ['NOVA_USER'])
        caseworker = Caseworker(
            **caseworker_dict
        )

        # Test with minimal attributes set
        new_task = Task(
            uuid=str(uuid.uuid4()),
            title=f"Test Task {datetime.now()}",
            status_code="F",
            deadline=datetime.now(),
            caseworker=caseworker
        )

        nova_tasks.attach_task_to_case(case.uuid, new_task, self.nova_access)

        # Check if it got created by finding it in Nova
        tasks = nova_tasks.get_tasks(case.uuid, self.nova_access)
        nova_task = self._find_task_by_title(tasks, new_task.title)

        self.assertEqual(nova_task.title, new_task.title)
        self.assertEqual(nova_task.uuid, new_task.uuid)
        self.assertEqual(nova_task.deadline.date(), new_task.deadline.date())
        self.assertEqual(nova_task.caseworker.uuid, new_task.caseworker.uuid)
        self.assertEqual(nova_task.status_code, new_task.status_code)

    def test_add_task_with_group(self):
        """Test adding a Task to Nova with a user group as caseworker."""
        case = self._get_test_case()

        caseworker_dict = json.loads(os.environ['NOVA_USER_GROUP'])
        caseworker = Caseworker(
            type='group',
            ident=None,
            uuid=caseworker_dict['uuid'],
            name=caseworker_dict['name']
        )

        # Test with minimal attributes set
        new_task = Task(
            uuid=str(uuid.uuid4()),
            title=f"Test Task {datetime.now()}",
            status_code="F",
            deadline=datetime.now(),
            caseworker=caseworker
        )

        nova_tasks.attach_task_to_case(case.uuid, new_task, self.nova_access)

        # Check if it got created by finding it in Nova
        tasks = nova_tasks.get_tasks(case.uuid, self.nova_access)
        nova_task = self._find_task_by_title(tasks, new_task.title)

        self.assertEqual(nova_task.title, new_task.title)
        self.assertEqual(nova_task.uuid, new_task.uuid)
        self.assertEqual(nova_task.deadline.date(), new_task.deadline.date())
        self.assertEqual(nova_task.caseworker, new_task.caseworker)
        self.assertEqual(nova_task.status_code, new_task.status_code)

    def test_add_task_full(self):
        """Test adding a Task to Nova with all information set."""
        case = self._get_test_case()

        caseworker_dict = json.loads(os.environ['NOVA_USER'])
        caseworker = Caseworker(
            name = caseworker_dict['name'],
            ident = caseworker_dict['ident'],
            uuid = caseworker_dict['uuid']
        )

        # Test with minimal attributes set
        new_task = Task(
            uuid=str(uuid.uuid4()),
            title=f"Test Task {datetime.now()}",
            status_code="F",
            deadline=datetime.now(),
            caseworker=caseworker,
            started_date=datetime.now(),
            closed_date=datetime.now(),
            description="This is a description."
        )

        nova_tasks.attach_task_to_case(case.uuid, new_task, self.nova_access)

        # Check if it got created by finding it in Nova
        tasks = nova_tasks.get_tasks(case.uuid, self.nova_access)
        nova_task = self._find_task_by_title(tasks, new_task.title)

        self.assertEqual(nova_task.title, new_task.title)
        self.assertEqual(nova_task.uuid, new_task.uuid)
        self.assertEqual(nova_task.deadline.date(), new_task.deadline.date())
        self.assertEqual(nova_task.started_date.date(), new_task.started_date.date())
        self.assertEqual(nova_task.closed_date.date(), new_task.closed_date.date())
        self.assertEqual(nova_task.caseworker.uuid, new_task.caseworker.uuid)
        self.assertEqual(nova_task.caseworker.ident, new_task.caseworker.ident)
        self.assertEqual(nova_task.status_code, new_task.status_code)
        self.assertEqual(nova_task.description, new_task.description)

    def test_update_task(self):
        """Test updating values on an existing task in Nova."""
        # Create a new task to test on
        case = self._get_test_case()
        title = f"Test Update Task {datetime.now()}"

        caseworker_dict = json.loads(os.environ['NOVA_USER'])
        caseworker = Caseworker(
            **caseworker_dict
        )

        task = Task(
            uuid=str(uuid.uuid4()),
            title=title,
            status_code="N",
            deadline=datetime.now(),
            caseworker=caseworker
        )

        nova_tasks.attach_task_to_case(case.uuid, task, self.nova_access)

        # Change some values and update them
        new_deadline = datetime(year=random.randint(2020, 2025), month=random.randint(1, 12), day=random.randint(1, 25))
        task.deadline = new_deadline
        task.status_code = "F"
        task.description = "Updated Description"

        nova_tasks.update_task(task, case.uuid, self.nova_access)

        # Check if it got updated by finding it in Nova
        tasks = nova_tasks.get_tasks(case.uuid, self.nova_access)
        nova_task = self._find_task_by_title(tasks, title)

        self.assertEqual(nova_task.deadline.date(), task.deadline.date())
        self.assertEqual(nova_task.status_code,  task.status_code)
        self.assertEqual(nova_task.description, task.description)

    def _find_task_by_title(self, tasks: list[Task], title: str) -> Task:
        """Find a task by its title in a list of tasks."""
        for task in tasks:
            if task.title == title:
                return task

        raise ValueError("No task with the given title exists.")

    def _get_test_case(self):
        return nova_cases.get_cases(self.nova_access, case_number="S2023-61078")[0]


if __name__ == '__main__':
    unittest.main()
