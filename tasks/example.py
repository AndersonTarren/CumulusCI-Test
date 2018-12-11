from cumulusci.core.tasks import BaseTask
from cumulusci.tasks.util import Sleep
from cumulusci.core.exceptions import SalesforceException


class ExampleTask(BaseTask):
    def _run_task(self):
        self.logger.info("Called _run_task")


class StaticPreflightTask(BaseTask):

    task_options = {
        "task_name": {
            "description": "Task that this preflight is for",
            "required": True,
        },
        "status_code": {
            "description": 'Status code to return, default to "ok".',
            "required": False,
        },
        "msg": {"description": "Message to be included", "required": False},
    }

    def _run_task(self):
        self.return_values["status_code"] = self.options.get("status_code", "ok")
        self.return_values["task_name"] = self.options.get("task_name")
        self.return_values["msg"] = self.options.get("msg", "")


class StaticSleep(Sleep):
    task_options = dict(**Sleep.task_options, **{
        "task_name": {
            "description": "Task that this preflight is for",
            "required": True,
        },
        "status_code": {
            "description": 'Status code to return, default to "ok".',
            "required": False,
        },
        "msg": {"description": "Message to be included", "required": False},
    })

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = self.options.get("task_name")

    def _run_task(self):
        status_code = self.options.get("status_code", "ok")
        msg = self.options.get("msg", "")
        self.return_values["status_code"] = status_code
        self.return_values["msg"] = msg
        self.return_values["task_name"] = self.options.get("task_name")
        if status_code == "error":
            raise SalesforceException(msg)
