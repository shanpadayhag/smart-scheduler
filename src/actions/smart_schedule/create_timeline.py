from datetime import datetime
from src.configs.env.env import Env
from src.data_transfer_objects.events.google_event_dto import GoogleEventDTO, EventDTO
from src.data_transfer_objects.projects.project_dto import ProjectDTO
from src.data_transfer_objects.tasks.task_dto import TaskDTO

def createTimeline(
    projects: list[ProjectDTO],
    tasks: list[TaskDTO],
    googleEvents: list[GoogleEventDTO],
    startDate: datetime,
    endDate: datetime,
    reschedule: bool = False,
) -> list[EventDTO]:
    workingHours = Env.workingHours[(startDate.weekday() + 1) % 7]
    timelineWeekDate = workingHours
    timelineEvents = sorted(googleEvents, key=lambda value: (
        value.startDate,
        value.endDate,
        value.title))
    sortedTasks = sorted(tasks, key=lambda value: (value.due, value.priority, value.estimatedTime))

    if len(workingHours) <= 0:
        return []

    if (timelineWeekDate[0] <= startDate.hour):
        timelineStartHour = (startDate.hour + 1) % 24 if startDate.minute != 0 else startDate.hour
    else:
        timelineStartHour = timelineWeekDate[0]

    timelineEndHour = timelineWeekDate[1]

    for task in sortedTasks:
        currentTaskEventStart = timelineStartHour
        currentTaskEventEnd = timelineStartHour + task.estimatedTime
        currentTaskYear = startDate.year
        currentTaskMonth = startDate.month
        currentTaskDay = startDate.day

        for event in timelineEvents:
            if (currentTaskEventStart >= event.startDate.hour and currentTaskEventEnd > event.startDate.hour) \
            or (currentTaskEventStart < event.endDate.hour and currentTaskEventEnd <= event.endDate.hour):
                currentTaskEventStart = event.endDate.hour
                currentTaskEventEnd = event.endDate.hour + task.estimatedTime

        if currentTaskEventEnd > timelineEndHour:
            continue

        timelineEvents.append(EventDTO(
            title=task.title,
            startDate=datetime(year=currentTaskYear, month=currentTaskMonth, day=currentTaskDay, hour=currentTaskEventStart),
            endDate=datetime(year=currentTaskYear, month=currentTaskMonth, day=currentTaskDay, hour=currentTaskEventEnd)))

    return filter(lambda event: not isinstance(event, GoogleEventDTO), timelineEvents)