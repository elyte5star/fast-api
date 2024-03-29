from fastapi import APIRouter, Depends
from modules.schemas.requests.auth import JWTcredentials
from modules.schemas.requests.job import GetJobRequest, RequestBase
from modules.schemas.responses.job import (
    GetJobsResponse,
    BaseResponse,
    GetJobResponse,
)
from modules.auth.dependency import security

router = APIRouter(prefix="/job", tags=["Jobs"])


@router.get("", response_model=GetJobsResponse, summary="Get all jobs")
async def get_jobs(
    cred: JWTcredentials = Depends(security),
) -> GetJobsResponse:
    return await handler.get_jobs(RequestBase(cred=cred))


@router.get("/{job_id}", response_model=GetJobResponse, summary="Check job status")
async def get_job(
    job_id: str, cred: JWTcredentials = Depends(security)
) -> BaseResponse:
    return await handler.get_job(GetJobRequest(cred=cred, job_id=job_id))
