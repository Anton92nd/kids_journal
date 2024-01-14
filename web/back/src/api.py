from http.client import HTTPException

import uvicorn
from fastapi import APIRouter, FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.exception_handlers.unauthorized import handle_auth_error
from src.routers.user import try_merge_user_by_phone
from src.settings import load_api_settings
from src.routers.auth import login
from src.routers.child import create_child
from src.routers.employee import create_employee, get_employee_by_tg_id
from src.routers.groups import (
    add_children_to_group,
    add_group_to_organization,
    get_children_by_group_id,
    get_group,
    get_groups_by_organization,
)
from src.routers.organization import (
    create_organization,
    get_organization,
    get_organizations,
)
from src.routers.parent import (
    create_parent,
    get_parent_by_tg_id,
    get_parents_by_child_id,
)


def init_app() -> FastAPI:
    app = FastAPI(debug=True)
    router = APIRouter()

    # Groups
    router.add_api_route("/groups", add_group_to_organization, methods=["POST"])
    router.add_api_route(
        "/organizations/{organizationId}/groups",
        get_groups_by_organization,
        methods=["GET"],
    )
    router.add_api_route("/groups/{groupId}", get_group, methods=["GET"])
    router.add_api_route(
        "/groups/link_children", add_children_to_group, methods=["POST"]
    )

    # Organizations
    router.add_api_route("/organizations", create_organization, methods=["POST"])
    router.add_api_route("/organizations", get_organizations, methods=["GET"])
    router.add_api_route(
        "/organizations/{organization_id}", get_organization, methods=["GET"]
    )

    # Auth
    router.add_api_route("/login", login, methods=["GET"])

    # Parent
    router.add_api_route("/parents", create_parent, methods=["POST"])
    router.add_api_route("/parents/{tgId}", get_parent_by_tg_id, methods=["GET"])
    router.add_api_route(
        "/parents/child/{childId}", get_parents_by_child_id, methods=["GET"]
    )

    # Employee
    router.add_api_route("/employee", create_employee, methods=["POST"])
    router.add_api_route("/employee/{tgId}", get_employee_by_tg_id, methods=["GET"])

    # Child
    router.add_api_route("/child", create_child, methods=["POST"])
    router.add_api_route("/child/{groupId}", get_children_by_group_id, methods=["GET"])

    # User
    router.add_api_route("/user/{phone}", try_merge_user_by_phone, methods=["POST"])

    api_settings = load_api_settings()

    # Midddlewares
    app.add_middleware(
        CORSMiddleware,
        allow_origins=api_settings.allow_origins,
        allow_credentials=api_settings.allow_credentials,
        allow_methods=api_settings.allow_methods,
        allow_headers=api_settings.allow_headers,
    )

    # Exception handlers
    app.add_exception_handler(HTTPException, handle_auth_error)

    app.include_router(router)
    return app


if __name__ == "__main__":
    uvicorn.run(init_app, port=8000)
