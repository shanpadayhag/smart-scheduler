from typing import List
from data_transfer_objects.projects.project_dto import ProjectDTO
from data_transfer_objects.tasks.task_dto import TaskDTO

class NotionProjectDTO(ProjectDTO):
    def __init__(self, id: str, name: str, tasks: List[TaskDTO]) -> None:
        super().__init__(id, name, tasks)