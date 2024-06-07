from enum import Enum


class Codes(Enum):
    # HTTP Error Codes
    badRequest = 400
    unauthorized = 401
    paymentRequired = 402
    forbidden = 403
    notFound = 404
    methodNotAllowed = 405
    notAcceptable = 406
    proxyAuthenticationRequired = 407
    requestTimeout = 408
    conflict = 409
    gone = 410
    lengthRequired = 411
    preconditionFailed = 412
    payloadTooLarge = 413
    URITooLong = 414
    unsupportedMediaType = 415
    rangeNotSatisfiable = 416
    expectationFailed = 417
    imATeapot = 418
    misdirectedRequest = 421
    unprocessableEntity = 422
    locked = 423
    failedDependency = 424
    tooEarly = 425
    upgradeRequired = 426
    preconditionRequired = 428
    tooManyRequests = 429
    requestHeaderFieldsTooLarge = 431
    unavailableForLegalReasons = 451

    # General Error Codes
    cooldownConflictError = 4000
    waypointNoAccessError = 4001

    # Account Error Codes
    tokenEmptyError = 4100
    tokenMissingSubjectError = 4101
    tokenInvalidSubjectError = 4102
    missingTokenRequestError = 4103
    invalidTokenRequestError = 4104
    invalidTokenSubjectError = 4105
    accountNotExistsError = 4106
    agentNotExistsError = 4107
    accountHasNoAgentError = 4108
    registerAgentExistsError = 4109
    registerAgentSymbolReservedError = 4110
    registerAgentConflictSymbolError = 4111

    # Ship Error Codes
    navigateInTransitError = 4200
    navigateInvalidDestinationError = 4201
    navigateOutsideSystemError = 4202
    navigateInsufficientFuelError = 4203
    navigateSameDestinationError = 4204
    shipExtractInvalidWaypointError = 4205
    shipExtractPermissionError = 4206
    shipJumpNoSystemError = 4207
    shipJumpSameSystemError = 4208
    shipJumpMissingModuleError = 4210
    shipJumpNoValidWaypointError = 4211
    shipJumpMissingAntimatterError = 4212
    shipInTransitError = 4214
    shipMissingSensorArraysError = 4215
    purchaseShipCreditsError = 4216
    shipCargoExceedsLimitError = 4217
    shipCargoMissingError = 4218
    shipCargoUnitCountError = 4219
    shipSurveyVerificationError = 4220
    shipSurveyExpirationError = 4221
    shipSurveyWaypointTypeError = 4222
    shipSurveyOrbitError = 4223
    shipSurveyExhaustedError = 4224
    shipRefuelDockedError = 4225
    shipRefuelInvalidWaypointError = 4226
    shipMissingMountsError4227 = 4227
    shipCargoFullError = 4228
    shipJumpFromGateToGateError = 4229
    waypointChartedError = 4230
    shipTransferShipNotFound = 4231
    shipTransferAgentConflict = 4232
    shipTransferSameShipConflict = 4233
    shipTransferLocationConflict = 4234
    warpInsideSystemError = 4235
    shipNotInOrbitError = 4236
    shipInvalidRefineryGoodError = 4237
    shipInvalidRefineryTypeError = 4238
    shipMissingRefineryError = 4239
    shipMissingSurveyorError = 4240
    shipMissingWarpDriveError = 4241
    shipMissingMineralProcessorError = 4242
    shipMissingMiningLasersError = 4243
    shipNotDockedError = 4244
    purchaseShipNotPresentError = 4245
    shipMountNoShipyardError = 4246
    shipMissingMountError = 4247
    shipMountInsufficientCreditsError = 4248
    shipMissingPowerError = 4249
    shipMissingSlotsError = 4250
    shipMissingMountsError4251 = 4251
    shipMissingCrewError = 4252
    shipExtractDestabilizedError = 4253
    shipJumpInvalidOriginError = 4254
    shipJumpInvalidWaypointError = 4255
    shipJumpOriginUnderConstructionError = 4256
    shipMissingGasProcessorError = 4257
    shipMissingGasSiphonsError = 4258
    shipSiphonInvalidWaypointError = 4259
    shipSiphonPermissionError = 4260
    waypointNoYieldError = 4261
    shipJumpDestinationUnderConstructionError = 4262

    # Contract Error Codes
    acceptContractNotAuthorizedError = 4500
    acceptContractConflictError = 4501
    fulfillContractDeliveryError = 4502
    contractDeadlineError = 4503
    contractFulfilledError = 4504
    contractNotAcceptedError = 4505
    contractNotAuthorizedError = 4506
    shipDeliverTermsError = 4508
    shipDeliverFulfilledError = 4509
    shipDeliverInvalidLocationError = 4510
    existingContractError = 4511

    # Market Error Codes
    marketTradeInsufficientCreditsError = 4600
    marketTradeNoPurchaseError = 4601
    marketTradeNotSoldError = 4602
    marketNotFoundError = 4603
    marketTradeUnitLimitError = 4604

    # Faction Error Codes
    waypointNoFactionError = 4700

    # Construction Error Codes
    constructionMaterialNotRequired = 4800
    constructionMaterialFulfilled = 4801
    shipConstructionInvalidLocationError = 4802
