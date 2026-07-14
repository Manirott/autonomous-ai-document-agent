import logging
from typing import Dict, List

from document import DocumentGenerator
from llm import LLM
from models import AgentResponse, ExecutionStep, Task
from prompts import (
    EXECUTOR_PROMPT,
    PLANNER_PROMPT,
    REFLECTION_PROMPT,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class AutonomousAgent:

    def __init__(self):

        self.llm = LLM()

        self.document_generator = DocumentGenerator()

        self.execution_trace: List[ExecutionStep] = []

    # ----------------------------------------------------
    # Trace Helper
    # ----------------------------------------------------

    def add_trace(self, step, status, details=None):

        self.execution_trace.append(
            ExecutionStep(
                step=step,
                status=status,
                details=details
            )
        )

    # ----------------------------------------------------
    # Validation
    # ----------------------------------------------------

    def validate_request(self, request: str):

        self.add_trace(
            "Request Validation",
            "Running"
        )

        if not request:

            raise ValueError("Request cannot be empty.")

        if len(request.strip()) < 5:

            raise ValueError("Request is too short.")

        self.add_trace(
            "Request Validation",
            "Completed"
        )

    # ----------------------------------------------------
    # Planning
    # ----------------------------------------------------

    def create_plan(self, request: str):

        self.add_trace(
            "Planning",
            "Running"
        )

        prompt = f"""
{PLANNER_PROMPT}

User Request:

{request}
"""

        result = self.llm.generate_json(prompt)

        self.add_trace(
            "Planning",
            "Completed"
        )

        return result

    # ----------------------------------------------------
    # Reflection
    # ----------------------------------------------------

    def reflect_plan(self, plan: Dict):

        self.add_trace(
            "Reflection",
            "Running"
        )

        prompt = f"""
{REFLECTION_PROMPT}

Execution Plan

{plan}
"""

        reflection = self.llm.generate_json(prompt)

        self.add_trace(
            "Reflection",
            "Completed"
        )

        if reflection["approved"]:

            return plan

        plan["tasks"] = reflection["updated_tasks"]

        return plan
    # ----------------------------------------------------
    # Task Execution
    # ----------------------------------------------------

    def execute_tasks(
        self,
        plan: Dict
    ):

        self.add_trace(
            "Task Execution",
            "Running"
        )

        sections = {}

        completed_tasks = []

        previous_content = ""

        document_type = plan["document_type"]
        topic = plan["topic"]
        audience = plan["audience"]

        for task in plan["tasks"]:

            logging.info(f"Executing: {task['name']}")

            prompt = f"""
{EXECUTOR_PROMPT}

Document Type:
{document_type}

Topic:
{topic}

Audience:
{audience}

Current Task:
{task['name']}

Previously Generated Sections:

{previous_content}
"""

            content = self.llm.generate(prompt)

            sections[task["name"]] = content

            previous_content += f"\n\n## {task['name']}\n{content}"

            completed_tasks.append(
                Task(
                    id=task["id"],
                    name=task["name"],
                    status="Completed",
                    output=content
                )
            )

        self.add_trace(
            "Task Execution",
            "Completed"
        )

        return sections, completed_tasks

    # ----------------------------------------------------
    # Document Generation
    # ----------------------------------------------------

    def generate_document(
        self,
        plan: Dict,
        sections: Dict[str, str]
    ):

        self.add_trace(
            "Document Generation",
            "Running"
        )

        title = f"{plan['topic']}"

        path = self.document_generator.generate(
            title=title,
            document_type=plan["document_type"],
            assumptions=plan["assumptions"],
            sections=sections
        )

        self.add_trace(
            "Document Generation",
            "Completed",
            path
        )

        return path

    # ----------------------------------------------------
    # Main Agent Workflow
    # ----------------------------------------------------

    def run(self, request: str):

        try:

            self.execution_trace = []

            self.validate_request(request)

            plan = self.create_plan(request)

            plan = self.reflect_plan(plan)

            sections, completed_tasks = self.execute_tasks(plan)

            document_path = self.generate_document(
                plan,
                sections
            )

            return AgentResponse(

                status="Success",

                message="Document generated successfully.",

                document_type=plan["document_type"],

                document_path=document_path,

                assumptions=plan["assumptions"],

                tasks=completed_tasks,

                execution_trace=self.execution_trace

            )

        except Exception as e:

            logging.exception(e)

            self.add_trace(
                "Error",
                "Failed",
                str(e)
            )

            return AgentResponse(

                status="Failed",

                message=str(e),

                execution_trace=self.execution_trace
            )