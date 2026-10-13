"""Generate a student assignment pipeline diagram with the Diagrams library.

Install on Nobara:
    sudo dnf install graphviz
    uv add diagrams

Run from this file's directory:
    uv run python diagrams_demo.py

Outputs: assignment_pipeline.png and assignment_pipeline.svg
"""

from diagrams_demo import Cluster, Diagram, Edge
from diagrams.aws.compute import Lambda
from diagrams.aws.database import Dynamodb
from diagrams.aws.engagement import SES
from diagrams.aws.general import Users
from diagrams.aws.integration import SQS
from diagrams.aws.network import APIGateway
from diagrams.aws.storage import S3


graph_style = {
    "bgcolor": "#FAFBFF",
    "fontname": "DejaVu Sans",
    "fontsize": "22",
    "pad": "0.4",
    "ranksep": "0.9",
    "nodesep": "0.5",
    "splines": "spline",
}

with Diagram(
    "From submission to feedback",
    filename="assignment_pipeline",
    show=False,
    direction="LR",
    outformat=["png", "svg"],
    graph_attr=graph_style,
):
    students = Users("Students")

    with Cluster("1  Accept submissions"):
        api = APIGateway("Course API")
        receive = Lambda("Validate upload")
        files = S3("Submitted files")

    with Cluster("2  Grade asynchronously"):
        queue = SQS("Grading queue")
        grader = Lambda("Run checks")
        grades = Dynamodb("Results")

    with Cluster("3  Return feedback"):
        report = Lambda("Provide feedback")
        email = SES("Notify student")

    students >> Edge(label="upload", color="#2563EB") >> api >> receive
    receive >> Edge(label="save", color="#2563EB") >> files
    receive >> Edge(label="enqueue", color="#7C3AED") >> queue
    queue >> Edge(label="process", color="#7C3AED") >> grader
    files >> Edge(label="read", color="#64748B", style="dashed") >> grader
    grader >> Edge(label="score", color="#16A34A") >> grades
    grades >> Edge(label="summarize", color="#16A34A") >> report >> email
    email >> Edge(label="feedback", color="#EA580C") >> students

print("Created assignment_pipeline.png and assignment_pipeline.svg")
