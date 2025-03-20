import json

from .. import controllers

from ..models.response import CODE
from ..models.utils import Promise
from ..models import response as res
from fastapi import Request
from fastapi import Path, Query, Body


async def get_user_profile(
    request: Request,
    user_id: str = Path(..., description="The ID of the user to get profiles for"),
    topk: int = Query(
        None, description="Number of profiles to retrieve, default is all"
    ),
    max_token_size: int = Query(
        None,
        description="Max token size of returned profile content, default is all",
    ),
    prefer_topics: list[str] = Query(
        None,
        description="Rank prefer topics at first to try to keep them in filtering, default order is by updated time",
    ),
    only_topics: list[str] = Query(
        None,
        description="Only return profiles with these topics, default is all",
    ),
    max_subtopic_size: int = Query(
        None,
        description="Max subtopic size of the same topic in returned profile, default is all",
    ),
    topic_limits_json: str = Query(
        None,
        description='Set specific subtopic limits for topics in JSON, for example {"topic1": 3, "topic2": 5}. The limits in this param will override `max_subtopic_size`.',
    ),
) -> res.UserProfileResponse:
    """Get the real-time user profiles for long term memory"""
    project_id = request.state.memobase_project_id
    topic_limits_json = topic_limits_json or "{}"
    try:
        topic_limits = res.StrIntData(data=json.loads(topic_limits_json)).data
    except Exception as e:
        return Promise.reject(
            CODE.BAD_REQUEST, f"Invalid topic_limits JSON: {e}"
        ).to_response(res.UserProfileResponse)
    p = await controllers.profile.get_user_profiles(user_id, project_id)
    p = await controllers.profile.truncate_profiles(
        p.data(),
        prefer_topics=prefer_topics,
        topk=topk,
        max_token_size=max_token_size,
        only_topics=only_topics,
        max_subtopic_size=max_subtopic_size,
        topic_limits=topic_limits,
    )
    return p.to_response(res.UserProfileResponse)


async def delete_user_profile(
    request: Request,
    user_id: str = Path(..., description="The ID of the user"),
    profile_id: str = Path(..., description="The ID of the profile to delete"),
) -> res.BaseResponse:
    """Get the real-time user profiles for long term memory"""
    project_id = request.state.memobase_project_id
    p = await controllers.profile.delete_user_profile(user_id, project_id, profile_id)
    return p.to_response(res.IdResponse)


async def update_user_profile(
    request: Request,
    user_id: str = Path(..., description="The ID of the user"),
    profile_id: str = Path(..., description="The ID of the profile to update"),
    content: res.ProfileDelta = Body(
        ..., description="The content of the profile to update"
    ),
) -> res.BaseResponse:
    """Update the real-time user profiles for long term memory"""
    project_id = request.state.memobase_project_id
    p = await controllers.profile.update_user_profiles(
        user_id, project_id, [profile_id], [content.content], [content.attributes]
    )
    if p.ok():
        return Promise.resolve(None).to_response(res.BaseResponse)
    return Promise.reject(p.code(), p.msg()).to_response(res.BaseResponse)


async def add_user_profile(
    request: Request,
    user_id: str = Path(..., description="The ID of the user"),
    content: res.ProfileDelta = Body(
        ..., description="The content of the profile to add"
    ),
) -> res.IdResponse:
    """Add the real-time user profiles for long term memory"""
    project_id = request.state.memobase_project_id
    p = await controllers.profile.add_user_profiles(
        user_id, project_id, [content.content], [content.attributes]
    )
    if p.ok():
        return Promise.resolve(res.IdData(id=p.data().ids[0])).to_response(
            res.IdResponse
        )
    return Promise.reject(p.code(), p.msg()).to_response(res.IdResponse)
