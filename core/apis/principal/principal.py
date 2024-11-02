from flask import Blueprint
from core.apis import decorators
from core.apis.assignments.schema import AssignmentGradeSchema, AssignmentSchema
from core.apis.responses import APIResponse
from core.models.assignments import Assignment, GradeEnum
from core.apis.decorators import authenticate_principal, accept_payload
from core import db

principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)

@principal_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@authenticate_principal
def list_all_assignments(p):
    """Returns list of all assignments"""
    all_assignments = Assignment.query.filter(Assignment.state.in_(['SUBMITTED', 'GRADED'])).all()
    all_assignments_dump = AssignmentSchema().dump(all_assignments, many=True)
    return APIResponse.respond(data=all_assignments_dump)

@principal_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@accept_payload
@authenticate_principal
def regrade_assignment(p, incoming_payload):
    """Re-grade an assignment"""
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)
    assignment = Assignment.query.filter_by(id=grade_assignment_payload.id).first()
    if not assignment:
        return APIResponse.respond_error("Assignment not found", 404)
    if assignment.state == 'DRAFT':
        return APIResponse.respond_error("Cannot grade a draft assignment", 400)
    assignment.grade = grade_assignment_payload.grade
    assignment.state = 'GRADED'
    db.session.commit()
    assignment_dump = AssignmentSchema().dump(assignment)
    return APIResponse.respond(data=assignment_dump)