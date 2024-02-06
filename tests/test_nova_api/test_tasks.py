"""Test the part of the API to do with tasks."""
import unittest
import os
import uuid
from datetime import datetime, date

from itk_dev_shared_components.kmd_nova.authentication import NovaAccess
from itk_dev_shared_components.kmd_nova.nova_objects import NovaCase, CaseParty, Task
from itk_dev_shared_components.kmd_nova import nova_cases, nova_tasks


class NovaCasesTest(unittest.TestCase):
    """Test the part of the API to do with tasks."""
    def setUp(self):
        credentials = os.getenv('nova_api_credentials')
        credentials = credentials.split(',')
        self.nova_access = NovaAccess(client_id=credentials[0], client_secret=credentials[1])

    def test_get_tasks(self):
        """Test getting tasks from a case."""
        case = nova_cases.get_cases(self.nova_access, case_number="S2023-61078")[0]
        tasks = nova_tasks.get_tasks(case.uuid, self.nova_access)
        task = self._find_task_by_name(tasks, "Test opgave")

        self.assertIsInstance(task, Task)
        self.assertEqual(task.deadline.date(), date(2024, 2, 6))
        self.assertEqual(task.started_date.date(), date(2024, 2, 7))
        self.assertEqual(task.closed_date.date(), date(2024, 2, 8))
        self.assertEqual(task.description, "Dette er en beskrivelse")
        self.assertEqual(task.case_worker_ident, "AZ68933")
        self.assertEqual(task.case_worker_uuid, "6874a25c-201b-4328-9cf5-4b2a7d5e707a")
        self.assertEqual(task.status_code, "F")

    def test_add_task_minimal(self):
        """Test adding a Task to Nova with minimal information set."""
        case = nova_cases.get_cases(self.nova_access, case_number="S2023-61078")[0]

        # Test with minimal attributes set
        new_task = Task(
            uuid=str(uuid.uuid4()),
            title=f"Test Task {datetime.now()}",
            status_code="F",
            deadline=datetime.now(),
            case_worker_uuid="6874a25c-201b-4328-9cf5-4b2a7d5e707a"
        )

        nova_tasks.attach_task_to_case(case.uuid, new_task, self.nova_access)

        # Check if it got created by finding it in Nova
        tasks = nova_tasks.get_tasks(case.uuid, self.nova_access)
        nova_task = self._find_task_by_name(tasks, new_task.title)

        self.assertEqual(nova_task.title, new_task.title)
        self.assertEqual(nova_task.uuid, new_task.uuid)
        self.assertEqual(nova_task.deadline.date(), new_task.deadline.date())
        self.assertEqual(nova_task.case_worker_uuid, new_task.case_worker_uuid)
        self.assertEqual(nova_task.status_code, new_task.status_code)

    def test_add_task_full(self):
        """Test adding a Task to Nova with all information set."""
        case = nova_cases.get_cases(self.nova_access, case_number="S2023-61078")[0]

        # Test with minimal attributes set
        new_task = Task(
            uuid=str(uuid.uuid4()),
            title=f"Test Task {datetime.now()}",
            status_code="F",
            deadline=datetime.now(),
            case_worker_uuid="6874a25c-201b-4328-9cf5-4b2a7d5e707a",
            case_worker_ident="AZ68933",
            started_date=datetime.now(),
            closed_date=datetime.now(),
            description="This is a description."
        )

        nova_tasks.attach_task_to_case(case.uuid, new_task, self.nova_access)

        # Check if it got created by finding it in Nova
        tasks = nova_tasks.get_tasks(case.uuid, self.nova_access)
        nova_task = self._find_task_by_name(tasks, new_task.title)

        self.assertEqual(nova_task.title, new_task.title)
        self.assertEqual(nova_task.uuid, new_task.uuid)
        self.assertEqual(nova_task.deadline.date(), new_task.deadline.date())
        self.assertEqual(nova_task.started_date.date(), new_task.started_date.date())
        self.assertEqual(nova_task.closed_date.date(), new_task.closed_date.date())
        self.assertEqual(nova_task.case_worker_uuid, new_task.case_worker_uuid)
        self.assertEqual(nova_task.case_worker_ident, new_task.case_worker_ident)
        self.assertEqual(nova_task.status_code, new_task.status_code)
        self.assertEqual(nova_task.description, new_task.description)

    def _find_task_by_name(self, tasks: list[Task], title: str) -> Task:
        """Find a task by its title in a list of tasks."""
        for task in tasks:
            if task.title == title:
                return task

        raise ValueError("No task with the given title exists.")


if __name__ == '__main__':
    unittest.main()
