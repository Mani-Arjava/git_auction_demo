# from app.api.db_connection.db_connection import DBSessionDependency
# from app.api.model.payout_statement.payout_statement_get import (
#     UpdateSettlementStatusResponse,
# )
# from app.api.dao.payout_statement_dao import PayoutStatementDAO
# from sqlmodel.ext.asyncio.session import AsyncSession
# from app.api.model.enum.settlement_status_enum import (
#     UpdatedSettlementStatusEnum,
# )
# from app.api.model.enum.reappraisal_service_status_enum import ReappraisalServiceStatusEnum
# from app.api.exceptions.payout_statement_exception import (
#     PayoutStatementSettlementStatusAPIException,
#     PayoutStatementNotFoundAPIException,
# )
# from app.api.exceptions.reappraisal_service_exception import (
#     ReappraiserServiceSettlementStatusAlreadyExistsAPIException,
#     ReappraiserServiceServiceStatusAPIException,
# )
# from app.api.exceptions.reimbursement_settlement_exception import (
#     ReimbursementSettlementStatusAlreadyExistsAPIException,
# )
# from app.api.exceptions.advance_exception import (
#     RsAdvanceSettlementStatusAPIException,
# )
# from app.api.exceptions.charge_settlement_exception import (
#     ChargeSettlementStatusAPIException,
# )
# from app.api.exceptions.advance_settlement_exception import (
#     AdvanceSettlementStatusAPIException,
# )


# class SettlementService:

#     def __init__(self, session: DBSessionDependency):
#         self.session = session

#     async def update_settle_status(
#         self,
#         payout_statement_id: str,
#         payout_settlement_status: UpdatedSettlementStatusEnum,
#     ):

#         terminal_status = {
#             UpdatedSettlementStatusEnum.SETTLED,
#             UpdatedSettlementStatusEnum.WRITTEN_OFF,
#         }
#         payout_statement_dao = PayoutStatementDAO(self.session)
#         payout_statement = await payout_statement_dao.get_payout_statement(
#             payout_statement_id=payout_statement_id
#         )
#         if not payout_statement:
#             raise PayoutStatementNotFoundAPIException(pst_id=payout_statement_id)

#         ######REIMBURSEMENT######
#         # get reimbursement settlement data based on payout_statement_id:
#         for reimbursement_settlement in payout_statement.reimbursement_settlements:
#             if (
#                 reimbursement_settlement.reimbursement_settlement_status
#                 in terminal_status
#             ):
#                 raise ReimbursementSettlementStatusAlreadyExistsAPIException(
#                     rs_reimbursement_id=reimbursement_settlement.rs_reimbursement_id,
#                     payout_statement_id=payout_statement_id,
#                     existing_status=reimbursement_settlement.reimbursement_settlement_status,
#                     new_status=payout_settlement_status,
#                 )

#             else:
#                 reimbursement_settlement.reimbursement_settlement_status = (
#                     payout_settlement_status
#                 )
#             # get reimbursement data based on reimbursement settlement table:
#             reimbursement = reimbursement_settlement.reimbursement

#             if reimbursement.rs_reimbursement_settlement_status in terminal_status:
#                 raise ReimbursementSettlementStatusAlreadyExistsAPIException(
#                     rs_reimbursement_id=reimbursement.rs_reimbursement_id,
#                     payout_statement_id=payout_statement_id,
#                     existing_status=reimbursement.rs_reimbursement_settlement_status,
#                     new_status=payout_settlement_status,
#                 )
#             else:
#                 reimbursement.rs_reimbursement_settlement_status = (
#                     payout_settlement_status
#                 )
#         ######REAPPRAISER SERVICE#######
#         # get charge settlement data based on payout_statement_id:
#         for settle_status in payout_statement.service_charge_settlements:
#             if settle_status.rs_charge_settlement_status in terminal_status:
#                 raise ChargeSettlementStatusAPIException(
#                     reappraisal_service_id=settle_status.reappraisal_service_id,
#                     payout_statement_id=settle_status.payout_statement_id,
#                     existing_status=settle_status.rs_charge_settlement_status,
#                     new_status=payout_settlement_status,
#                 )
#             else:
#                 settle_status.rs_charge_settlement_status = payout_settlement_status

#             # get reappraiser_service data based on charge settlement table rs_id
#             service = settle_status.service
#             if service.rs_status != ReappraisalServiceStatusEnum.CONSOLIDATED:
#                 raise ReappraiserServiceServiceStatusAPIException(
#                     reappraisal_service_id=service.reappraisal_service_id
#                 )
#             elif service.rs_settlement_status not in terminal_status:
#                 service.rs_status = ReappraisalServiceStatusEnum.CLOSED
#                 service.rs_settlement_status = payout_settlement_status
#             else:
#                 raise ReappraiserServiceSettlementStatusAlreadyExistsAPIException(
#                     reappraisal_service_id=service.reappraisal_service_id,
#                     payout_statement_id=payout_statement_id,
#                     existing_status=service.rs_settlement_status,
#                     new_status=payout_settlement_status,
#                 )

#         ######ADVANCE######
#         # get charge settlement data based on payout_statement_id:
#         for settle_status in payout_statement.advance_settlements:

#             if settle_status.rs_advance_settlement_status in terminal_status:
#                 raise AdvanceSettlementStatusAPIException(
#                     rs_advance_id=settle_status.rs_advance_id,
#                     payout_statement_id=payout_statement_id,
#                     existing_status=settle_status.rs_advance_settlement_status,
#                     new_status=payout_settlement_status,
#                 )
#             else:
#                 settle_status.rs_advance_settlement_status = payout_settlement_status

#             # get advance_ data based on charge settlement table rs_advance_id:
#             advance = settle_status.advance
#             if advance.rs_advance_settlement_status in terminal_status:
#                 raise RsAdvanceSettlementStatusAPIException(
#                     rs_advance_id=advance.rs_advance_id,
#                     existing_status=advance.rs_advance_settlement_status,
#                     new_status=payout_settlement_status,
#                 )
#             else:
#                 advance.rs_advance_settlement_status = payout_settlement_status

#         # get payout_statement data based on payout_stateement_id :

#         if payout_statement.pst_status in terminal_status:
#             raise PayoutStatementSettlementStatusAPIException(
#                 payout_statement_id=payout_statement_id,
#                 existing_status=payout_statement.pst_status,
#                 new_status=payout_settlement_status,
#             )
#         else:
#             payout_statement.pst_status = payout_settlement_status

#             await self.session.commit()
#             await self.session.refresh(payout_statement)
#             return UpdateSettlementStatusResponse.model_validate(payout_statement)
