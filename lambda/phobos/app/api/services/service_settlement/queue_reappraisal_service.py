from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dao.reappraisal_service_dao import ReappraisalServiceDAO
from app.api.exceptions.reappraisal_service_exception import (
    ReappraisalServiceNotFoundAPIException,
    InvalidStatusException,
    FilePendingException,
)
from app.api.model.reappraisal_service.reappraisal_service_create import (
    ReappraisalServiceQueueRequest,
)
from app.api.model.reappraisal_service.reappraisal_service_table import (
    ReappraisalServiceTable,
)
from app.api.model.enum.reappraisal_service_status_enum import ReappraisalServiceStatusEnum
from app.api.services.search_filter.matchtype_enum import MatchTypeEnum
from app.api.services.search_filter.searchfilter import DAOFilterSearchParam


class QueuedReappraisalService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.dao = ReappraisalServiceDAO(session)

    async def queue_reappraisal_service(self, reappraisal_service_id: str):
        # Fetch the existing record
        reappraisal_serviceDao = ReappraisalServiceDAO(self.session)
        reappraisal = await reappraisal_serviceDao.get_reappraisal_service(
            reappraisal_service_id
        )
        if not reappraisal:
            raise ReappraisalServiceNotFoundAPIException(reappraisal_service_id)

        if reappraisal.rs_status != ReappraisalServiceStatusEnum.ACTIVE:
            if reappraisal.rs_status == ReappraisalServiceStatusEnum.READY_FOR_PAYMENT:
                raise InvalidStatusException(
                    message="Reappraisal Status Already Ready for Payment",
                    reappraisal_service_id=reappraisal_service_id,
                )
            raise InvalidStatusException(reappraisal_service_id=reappraisal_service_id)
        # Check that file is not empty
        if not reappraisal.rs_completion_file_path:
            raise FilePendingException(reappraisal_service_id=reappraisal_service_id)

        # Build update model with only the fields needed
        update_model = ReappraisalServiceQueueRequest(
            rs_status=ReappraisalServiceStatusEnum.READY_FOR_PAYMENT
        )

        # Call DAO's generic update method
        updated_reappraisal = await self.dao.update_reappraisal_service(
            reappraisal_service_id, update_model
        )

        return updated_reappraisal
