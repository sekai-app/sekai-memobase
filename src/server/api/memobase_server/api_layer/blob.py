from fastapi import BackgroundTasks, Request
from fastapi import Path, Body
import traceback

from .. import controllers

from ..env import LOG, TelemetryKeyName
from ..models.response import CODE
from ..models.utils import Promise
from ..models import response as res
from ..telemetry.capture_key import capture_int_key


async def insert_blob(
    request: Request,
    user_id: str = Path(..., description="The ID of the user to insert the blob for"),
    blob_data: res.BlobData = Body(..., description="The blob data to insert"),
    background_tasks: BackgroundTasks = BackgroundTasks(),
) -> res.IdResponse:
    project_id = request.state.memobase_project_id
    background_tasks.add_task(
        capture_int_key, TelemetryKeyName.insert_blob_request, project_id=project_id
    )

    p = await controllers.billing.get_project_billing(project_id)
    if not p.ok():
        return p.to_response(res.IdResponse)
    billing = p.data()

    if billing.token_left is not None and billing.token_left < 0:
        return Promise.reject(
            CODE.SERVICE_UNAVAILABLE,
            f"Your project reaches Memobase token limit, "
            f"Left: {billing.token_left}, this project used: {billing.project_token_cost_month}. "
            f"Your quota will be refilled on {billing.next_refill_at}. "
            "\nhttps://www.memobase.io/pricing for more information.",
        ).to_response(res.IdResponse)

    try:
        p = await controllers.blob.insert_blob(user_id, project_id, blob_data)
        if not p.ok():
            return p.to_response(res.IdResponse)

        # TODO if single user insert too fast will cause random order insert to buffer
        # So no background task for insert buffer yet
        pb = await controllers.buffer.insert_blob_to_buffer(
            user_id, project_id, p.data().id, blob_data.to_blob()
        )
        if not pb.ok():
            return pb.to_response(res.IdResponse)
    except Exception as e:
        LOG.error(f"Error inserting blob: {e}, {traceback.format_exc()}")
        return Promise.reject(
            CODE.INTERNAL_SERVER_ERROR, f"Error inserting blob: {e}"
        ).to_response(res.IdResponse)

    background_tasks.add_task(
        capture_int_key,
        TelemetryKeyName.insert_blob_success_request,
        project_id=project_id,
    )
    return p.to_response(res.IdResponse)


async def get_blob(
    request: Request,
    user_id: str = Path(..., description="The ID of the user"),
    blob_id: str = Path(..., description="The ID of the blob to retrieve"),
) -> res.BlobDataResponse:
    project_id = request.state.memobase_project_id
    p = await controllers.blob.get_blob(user_id, project_id, blob_id)
    return p.to_response(res.BlobDataResponse)


async def delete_blob(
    request: Request,
    user_id: str = Path(..., description="The ID of the user"),
    blob_id: str = Path(..., description="The ID of the blob to delete"),
) -> res.BaseResponse:
    project_id = request.state.memobase_project_id
    p = await controllers.blob.remove_blob(user_id, project_id, blob_id)
    return p.to_response(res.BaseResponse)
