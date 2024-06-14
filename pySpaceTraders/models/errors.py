from dataclasses import dataclass
from enum import Enum


@dataclass
class Error:
    error: str
    message: str


class Codes(Enum):
    # HTTP Error Codes
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    PAYMENT_REQUIRED = 402
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    NOT_ACCEPTABLE = 406
    PROXY_AUTHENTICATION_REQUIRED = 407
    REQUEST_TIMEOUT = 408
    CONFLICT = 409
    GONE = 410
    LENGTH_REQUIRED = 411
    PRECONDITION_FAILED = 412
    PAYLOAD_TOO_LARGE = 413
    URI_TOO_LONG = 414
    UNSUPPORTED_MEDIA_TYPE = 415
    RANGE_NOT_SATISFIABLE = 416
    EXPECTATION_FAILED = 417
    IM_A_TEAPOT = 418
    MISDIRECTED_REQUEST = 421
    UNPROCESSABLE_ENTITY = 422
    LOCKED = 423
    FAILED_DEPENDENCY = 424
    TOO_EARLY = 425
    UPGRADE_REQUIRED = 426
    PRECONDITION_REQUIRED = 428
    TOO_MANY_REQUESTS = 429
    REQUEST_HEADER_FIELDS_TOO_LARGE = 431
    UNAVAILABLE_FOR_LEGAL_REASONS = 451

    # class GeneralCodes(Enum):
    # General Error Codes
    COOLDOWN_CONFLICT_ERROR = 4000
    WAYPOINT_NO_ACCESS_ERROR = 4001

    # class AccountCodes(Enum):
    # Account Error Codes
    TOKEN_EMPTY_ERROR = 4100
    TOKEN_MISSING_SUBJECT_ERROR = 4101
    TOKEN_INVALID_SUBJECT_ERROR = 4102
    MISSING_TOKEN_REQUEST_ERROR = 4103
    INVALID_TOKEN_REQUEST_ERROR = 4104
    INVALID_TOKEN_SUBJECT_ERROR = 4105
    ACCOUNT_NOT_EXISTS_ERROR = 4106
    AGENT_NOT_EXISTS_ERROR = 4107
    ACCOUNT_HAS_NO_AGENT_ERROR = 4108
    REGISTER_AGENT_EXISTS_ERROR = 4109
    REGISTER_AGENT_SYMBOL_RESERVED_ERROR = 4110
    REGISTER_AGENT_CONFLICT_SYMBOL_ERROR = 4111

    # class ShipCodes(Enum):
    # Ship Error Codes
    NAVIGATE_IN_TRANSIT_ERROR = 4200
    NAVIGATE_INVALID_DESTINATION_ERROR = 4201
    NAVIGATE_OUTSIDE_SYSTEM_ERROR = 4202
    NAVIGATE_INSUFFICIENT_FUEL_ERROR = 4203
    NAVIGATE_SAME_DESTINATION_ERROR = 4204
    SHIP_EXTRACT_INVALID_WAYPOINT_ERROR = 4205
    SHIP_EXTRACT_PERMISSION_ERROR = 4206
    SHIP_JUMP_NO_SYSTEM_ERROR = 4207
    SHIP_JUMP_SAME_SYSTEM_ERROR = 4208
    SHIP_JUMP_MISSING_MODULE_ERROR = 4210
    SHIP_JUMP_NO_VALID_WAYPOINT_ERROR = 4211
    SHIP_JUMP_MISSING_ANTIMATTER_ERROR = 4212
    SHIP_IN_TRANSIT_ERROR = 4214
    SHIP_MISSING_SENSOR_ARRAYS_ERROR = 4215
    PURCHASE_SHIP_CREDITS_ERROR = 4216
    SHIP_CARGO_EXCEEDS_LIMIT_ERROR = 4217
    SHIP_CARGO_MISSING_ERROR = 4218
    SHIP_CARGO_UNIT_COUNT_ERROR = 4219
    SHIP_SURVEY_VERIFICATION_ERROR = 4220
    SHIP_SURVEY_EXPIRATION_ERROR = 4221
    SHIP_SURVEY_WAYPOINT_TYPE_ERROR = 4222
    SHIP_SURVEY_ORBIT_ERROR = 4223
    SHIP_SURVEY_EXHAUSTED_ERROR = 4224
    SHIP_REFUEL_DOCKED_ERROR = 4225
    SHIP_REFUEL_INVALID_WAYPOINT_ERROR = 4226
    SHIP_MISSING_MOUNTS_ERROR_4227 = 4227
    SHIP_CARGO_FULL_ERROR = 4228
    SHIP_JUMP_FROM_GATE_TO_GATE_ERROR = 4229
    WAYPOINT_CHARTED_ERROR = 4230
    SHIP_TRANSFER_SHIP_NOT_FOUND = 4231
    SHIP_TRANSFER_AGENT_CONFLICT = 4232
    SHIP_TRANSFER_SAME_SHIP_CONFLICT = 4233
    SHIP_TRANSFER_LOCATION_CONFLICT = 4234
    WARP_INSIDE_SYSTEM_ERROR = 4235
    SHIP_NOT_IN_ORBIT_ERROR = 4236
    SHIP_INVALID_REFINERY_GOOD_ERROR = 4237
    SHIP_INVALID_REFINERY_TYPE_ERROR = 4238
    SHIP_MISSING_REFINERY_ERROR = 4239
    SHIP_MISSING_SURVEYOR_ERROR = 4240
    SHIP_MISSING_WARP_DRIVE_ERROR = 4241
    SHIP_MISSING_MINERAL_PROCESSOR_ERROR = 4242
    SHIP_MISSING_MINING_LASERS_ERROR = 4243
    SHIP_NOT_DOCKED_ERROR = 4244
    PURCHASE_SHIP_NOT_PRESENT_ERROR = 4245
    SHIP_MOUNT_NO_SHIPYARD_ERROR = 4246
    SHIP_MISSING_MOUNT_ERROR = 4247
    SHIP_MOUNT_INSUFFICIENT_CREDITS_ERROR = 4248
    SHIP_MISSING_POWER_ERROR = 4249
    SHIP_MISSING_SLOTS_ERROR = 4250
    SHIP_MISSING_MOUNTS_ERROR_4251 = 4251
    SHIP_MISSING_CREW_ERROR = 4252
    SHIP_EXTRACT_DESTABILIZED_ERROR = 4253
    SHIP_JUMP_INVALID_ORIGIN_ERROR = 4254
    SHIP_JUMP_INVALID_WAYPOINT_ERROR = 4255
    SHIP_JUMP_ORIGIN_UNDER_CONSTRUCTION_ERROR = 4256
    SHIP_MISSING_GAS_PROCESSOR_ERROR = 4257
    SHIP_MISSING_GAS_SIPHONS_ERROR = 4258
    SHIP_SIPHON_INVALID_WAYPOINT_ERROR = 4259
    SHIP_SIPHON_PERMISSION_ERROR = 4260
    WAYPOINT_NO_YIELD_ERROR = 4261
    SHIP_JUMP_DESTINATION_UNDER_CONSTRUCTION_ERROR = 4262

    # class ContractCodes(Enum):
    # Contract Error Codes
    ACCEPT_CONTRACT_NOT_AUTHORIZED_ERROR = 4500
    ACCEPT_CONTRACT_CONFLICT_ERROR = 4501
    FULFILL_CONTRACT_DELIVERY_ERROR = 4502
    CONTRACT_DEADLINE_ERROR = 4503
    CONTRACT_FULFILLED_ERROR = 4504
    CONTRACT_NOT_ACCEPTED_ERROR = 4505
    CONTRACT_NOT_AUTHORIZED_ERROR = 4506
    SHIP_DELIVER_TERMS_ERROR = 4508
    SHIP_DELIVER_FULFILLED_ERROR = 4509
    SHIP_DELIVER_INVALID_LOCATION_ERROR = 4510
    EXISTING_CONTRACT_ERROR = 4511

    # class MarketCodes(Enum):
    # Market Error Codes
    MARKET_TRADE_INSUFFICIENT_CREDITS_ERROR = 4600
    MARKET_TRADE_NO_PURCHASE_ERROR = 4601
    MARKET_TRADE_NOT_SOLD_ERROR = 4602
    MARKET_NOT_FOUND_ERROR = 4603
    MARKET_TRADE_UNIT_LIMIT_ERROR = 4604

    # class FactionCodes(Enum):
    # Faction Error Codes
    WAYPOINT_NO_FACTION_ERROR = 4700

    # class ConstructionCodes(Enum):
    # Construction Error Codes
    CONSTRUCTION_MATERIAL_NOT_REQUIRED = 4800
    CONSTRUCTION_MATERIAL_FULFILLED = 4801
    SHIP_CONSTRUCTION_INVALID_LOCATION_ERROR = 4802
