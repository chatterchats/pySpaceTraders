from enum import StrEnum


class FactionSymbol(StrEnum):
    COSMIC = "COSMIC"
    VOID = "VOID"
    GALACTIC = "GALACTIC"
    QUANTUM = "QUANTUM"
    DOMINION = "DOMINION"
    ASTRO = "ASTRO"
    CORSAIRS = "CORSAIRS"
    OBSIDIAN = "OBSIDIAN"
    AEGIS = "AEGIS"
    UNITED = "UNITED"
    SOLITARY = "SOLITARY"
    COBALT = "COBALT"
    OMEGA = "OMEGA"
    ECHO = "ECHO"
    LORDS = "LORDS"
    CULT = "CULT"
    ANCIENTS = "ANCIENTS"
    SHADOW = "SHADOW"
    ETHEREAL = "ETHEREAL"


class ActivityLevel(StrEnum):
    WEAK = "WEAK"
    GROWING = "GROWING"
    STRONG = "STRONG"
    RESTRICTED = "RESTRICTED"


class ContractType(StrEnum):
    PROCUREMENT = "PROCUREMENT"
    TRANSPORT = "TRANSPORT"
    SHUTTLE = "SHUTTLE"


class FactionTraitSymbol(StrEnum):
    BUREAUCRATIC = "BUREAUCRATIC"
    SECRETIVE = "SECRETIVE"
    CAPITALISTIC = "CAPITALISTIC"
    INDUSTRIOUS = "INDUSTRIOUS"
    PEACEFUL = "PEACEFUL"
    DISTRUSTFUL = "DISTRUSTFUL"
    WELCOMING = "WELCOMING"
    SMUGGLERS = "SMUGGLERS"
    SCAVENGERS = "SCAVENGERS"
    REBELLIOUS = "REBELLIOUS"
    EXILES = "EXILES"
    PIRATES = "PIRATES"
    RAIDERS = "RAIDERS"
    CLAN = "CLAN"
    GUILD = "GUILD"
    DOMINION = "DOMINION"
    FRINGE = "FRINGE"
    FORSAKEN = "FORSAKEN"
    ISOLATED = "ISOLATED"
    LOCALIZED = "LOCALIZED"
    ESTABLISHED = "ESTABLISHED"
    NOTABLE = "NOTABLE"
    DOMINANT = "DOMINANT"
    INESCAPABLE = "INESCAPABLE"
    INNOVATIVE = "INNOVATIVE"
    BOLD = "BOLD"
    VISIONARY = "VISIONARY"
    CURIOUS = "CURIOUS"
    DARING = "DARING"
    EXPLORATORY = "EXPLORATORY"
    RESOURCEFUL = "RESOURCEFUL"
    FLEXIBLE = "FLEXIBLE"
    COOPERATIVE = "COOPERATIVE"
    UNITED = "UNITED"
    STRATEGIC = "STRATEGIC"
    INTELLIGENT = "INTELLIGENT"
    RESEARCH_FOCUSED = "RESEARCH_FOCUSED"
    COLLABORATIVE = "COLLABORATIVE"
    PROGRESSIVE = "PROGRESSIVE"
    MILITARISTIC = "MILITARISTIC"
    TECHNOLOGICALLY_ADVANCED = "TECHNOLOGICALLY_ADVANCED"
    AGGRESSIVE = "AGGRESSIVE"
    IMPERIALISTIC = "IMPERIALISTIC"
    TREASURE_HUNTERS = "TREASURE_HUNTERS"
    DEXTEROUS = "DEXTEROUS"
    UNPREDICTABLE = "UNPREDICTABLE"
    BRUTAL = "BRUTAL"
    FLEETING = "FLEETING"
    ADAPTABLE = "ADAPTABLE"
    SELF_SUFFICIENT = "SELF_SUFFICIENT"
    DEFENSIVE = "DEFENSIVE"
    PROUD = "PROUD"
    DIVERSE = "DIVERSE"
    INDEPENDENT = "INDEPENDENT"
    SELF_INTERESTED = "SELF_INTERESTED"
    FRAGMENTED = "FRAGMENTED"
    COMMERCIAL = "COMMERCIAL"
    FREE_MARKETS = "FREE_MARKETS"
    ENTREPRENEURIAL = "ENTREPRENEURIAL"


class ShipConditionEventSymbol(StrEnum):
    REACTOR_OVERLOAD = "REACTOR_OVERLOAD"
    ENERGY_SPIKE_FROM_MINERAL = "ENERGY_SPIKE_FROM_MINERAL"
    SOLAR_FLARE_INTERFERENCE = "SOLAR_FLARE_INTERFERENCE"
    COOLANT_LEAK = "COOLANT_LEAK"
    POWER_DISTRIBUTION_FLUCTUATION = "POWER_DISTRIBUTION_FLUCTUATION"
    MAGNETIC_FIELD_DISRUPTION = "MAGNETIC_FIELD_DISRUPTION"
    HULL_MICROMETEORITE_STRIKES = "HULL_MICROMETEORITE_STRIKES"
    STRUCTURAL_STRESS_FRACTURES = "STRUCTURAL_STRESS_FRACTURES"
    CORROSIVE_MINERAL_CONTAMINATION = "CORROSIVE_MINERAL_CONTAMINATION"
    THERMAL_EXPANSION_MISMATCH = "THERMAL_EXPANSION_MISMATCH"
    VIBRATION_DAMAGE_FROM_DRILLING = "VIBRATION_DAMAGE_FROM_DRILLING"
    ELECTROMAGNETIC_FIELD_INTERFERENCE = "ELECTROMAGNETIC_FIELD_INTERFERENCE"
    IMPACT_WITH_EXTRACTED_DEBRIS = "IMPACT_WITH_EXTRACTED_DEBRIS"
    FUEL_EFFICIENCY_DEGRADATION = "FUEL_EFFICIENCY_DEGRADATION"
    COOLANT_SYSTEM_AGEING = "COOLANT_SYSTEM_AGEING"
    DUST_MICROABRASIONS = "DUST_MICROABRASIONS"
    THRUSTER_NOZZLE_WEAR = "THRUSTER_NOZZLE_WEAR"
    EXHAUST_PORT_CLOGGING = "EXHAUST_PORT_CLOGGING"
    BEARING_LUBRICATION_FADE = "BEARING_LUBRICATION_FADE"
    SENSOR_CALIBRATION_DRIFT = "SENSOR_CALIBRATION_DRIFT"
    HULL_MICROMETEORITE_DAMAGE = "HULL_MICROMETEORITE_DAMAGE"
    SPACE_DEBRIS_COLLISION = "SPACE_DEBRIS_COLLISION"
    THERMAL_STRESS = "THERMAL_STRESS"
    VIBRATION_OVERLOAD = "VIBRATION_OVERLOAD"
    PRESSURE_DIFFERENTIAL_STRESS = "PRESSURE_DIFFERENTIAL_STRESS"
    ELECTROMAGNETIC_SURGE_EFFECTS = "ELECTROMAGNETIC_SURGE_EFFECTS"
    ATMOSPHERIC_ENTRY_HEAT = "ATMOSPHERIC_ENTRY_HEAT"


class ShipEngineSymbol(StrEnum):
    ENGINE_IMPULSE_DRIVE_I = "ENGINE_IMPULSE_DRIVE_I"
    ENGINE_ION_DRIVE_I = "ENGINE_ION_DRIVE_I"
    ENGINE_ION_DRIVE_II = "ENGINE_ION_DRIVE_II"
    ENGINE_HYPER_DRIVE_I = "ENGINE_HYPER_DRIVE_I"


class ShipFrameSymbol(StrEnum):
    FRAME_PROBE = "FRAME_PROBE"
    FRAME_DRONE = "FRAME_DRONE"
    FRAME_INTERCEPTOR = "FRAME_INTERCEPTOR"
    FRAME_RACER = "FRAME_RACER"
    FRAME_FIGHTER = "FRAME_FIGHTER"
    FRAME_FRIGATE = "FRAME_FRIGATE"
    FRAME_SHUTTLE = "FRAME_SHUTTLE"
    FRAME_EXPLORER = "FRAME_EXPLORER"
    FRAME_MINER = "FRAME_MINER"
    FRAME_LIGHT_FREIGHTER = "FRAME_LIGHT_FREIGHTER"
    FRAME_HEAVY_FREIGHTER = "FRAME_HEAVY_FREIGHTER"
    FRAME_TRANSPORT = "FRAME_TRANSPORT"
    FRAME_DESTROYER = "FRAME_DESTROYER"
    FRAME_CRUISER = "FRAME_CRUISER"
    FRAME_CARRIER = "FRAME_CARRIER"


class ShipModuleSymbol(StrEnum):
    MODULE_MINERAL_PROCESSOR_I = "MODULE_MINERAL_PROCESSOR_I"
    MODULE_GAS_PROCESSOR_I = "MODULE_GAS_PROCESSOR_I"
    MODULE_CARGO_HOLD_I = "MODULE_CARGO_HOLD_I"
    MODULE_CARGO_HOLD_II = "MODULE_CARGO_HOLD_II"
    MODULE_CARGO_HOLD_III = "MODULE_CARGO_HOLD_III"
    MODULE_CREW_QUARTERS_I = "MODULE_CREW_QUARTERS_I"
    MODULE_ENVOY_QUARTERS_I = "MODULE_ENVOY_QUARTERS_I"
    MODULE_PASSENGER_CABIN_I = "MODULE_PASSENGER_CABIN_I"
    MODULE_MICRO_REFINERY_I = "MODULE_MICRO_REFINERY_I"
    MODULE_ORE_REFINERY_I = "MODULE_ORE_REFINERY_I"
    MODULE_FUEL_REFINERY_I = "MODULE_FUEL_REFINERY_I"
    MODULE_SCIENCE_LAB_I = "MODULE_SCIENCE_LAB_I"
    MODULE_JUMP_DRIVE_I = "MODULE_JUMP_DRIVE_I"
    MODULE_JUMP_DRIVE_II = "MODULE_JUMP_DRIVE_II"
    MODULE_JUMP_DRIVE_III = "MODULE_JUMP_DRIVE_III"
    MODULE_WARP_DRIVE_I = "MODULE_WARP_DRIVE_I"
    MODULE_WARP_DRIVE_II = "MODULE_WARP_DRIVE_II"
    MODULE_WARP_DRIVE_III = "MODULE_WARP_DRIVE_III"
    MODULE_SHIELD_GENERATOR_I = "MODULE_SHIELD_GENERATOR_I"
    MODULE_SHIELD_GENERATOR_II = "MODULE_SHIELD_GENERATOR_II"


class ShipMountSymbol(StrEnum):
    MOUNT_GAS_SIPHON_I = "MOUNT_GAS_SIPHON_I"
    MOUNT_GAS_SIPHON_II = "MOUNT_GAS_SIPHON_II"
    MOUNT_GAS_SIPHON_III = "MOUNT_GAS_SIPHON_III"
    MOUNT_SURVEYOR_I = "MOUNT_SURVEYOR_I"
    MOUNT_SURVEYOR_II = "MOUNT_SURVEYOR_II"
    MOUNT_SURVEYOR_III = "MOUNT_SURVEYOR_III"
    MOUNT_SENSOR_ARRAY_I = "MOUNT_SENSOR_ARRAY_I"
    MOUNT_SENSOR_ARRAY_II = "MOUNT_SENSOR_ARRAY_II"
    MOUNT_SENSOR_ARRAY_III = "MOUNT_SENSOR_ARRAY_III"
    MOUNT_MINING_LASER_I = "MOUNT_MINING_LASER_I"
    MOUNT_MINING_LASER_II = "MOUNT_MINING_LASER_II"
    MOUNT_MINING_LASER_III = "MOUNT_MINING_LASER_III"
    MOUNT_LASER_CANNON_I = "MOUNT_LASER_CANNON_I"
    MOUNT_MISSILE_LAUNCHER_I = "MOUNT_MISSILE_LAUNCHER_I"
    MOUNT_TURRET_I = "MOUNT_TURRET_I"


class ShipNavStatus(StrEnum):
    IN_TRANSIT = "IN_TRANSIT"
    IN_ORBIT = "IN_ORBIT"
    DOCKED = "DOCKED"


class ShipNavFlightMode(StrEnum):
    DRIFT = "DRIFT"
    STEALTH = "STEALTH"
    CRUISE = "CRUISE"
    BURN = "BURN"


class ShipReactorSymbol(StrEnum):
    REACTOR_SOLAR_I = "REACTOR_SOLAR_I"
    REACTOR_FUSION_I = "REACTOR_FUSION_I"
    REACTOR_FISSION_I = "REACTOR_FISSION_I"
    REACTOR_CHEMICAL_I = "REACTOR_CHEMICAL_I"
    REACTOR_ANTIMATTER_I = "REACTOR_ANTIMATTER_I"


class ShipRole(StrEnum):
    FABRICATOR = "FABRICATOR"
    HARVESTER = "HARVESTER"
    HAULER = "HAULER"
    INTERCEPTOR = "INTERCEPTOR"
    EXCAVATOR = "EXCAVATOR"
    TRANSPORT = "TRANSPORT"
    REPAIR = "REPAIR"
    SURVEYOR = "SURVEYOR"
    COMMAND = "COMMAND"
    CARRIER = "CARRIER"
    PATROL = "PATROL"
    SATELLITE = "SATELLITE"
    EXPLORER = "EXPLORER"
    REFINERY = "REFINERY"


class ShipType(StrEnum):
    SHIP_PROBE = "SHIP_PROBE"
    SHIP_MINING_DRONE = "SHIP_MINING_DRONE"
    SHIP_SIPHON_DRONE = "SHIP_SIPHON_DRONE"
    SHIP_INTERCEPTOR = "SHIP_INTERCEPTOR"
    SHIP_LIGHT_HAULER = "SHIP_LIGHT_HAULER"
    SHIP_COMMAND_FRIGATE = "SHIP_COMMAND_FRIGATE"
    SHIP_EXPLORER = "SHIP_EXPLORER"
    SHIP_HEAVY_FREIGHTER = "SHIP_HEAVY_FREIGHTER"
    SHIP_LIGHT_SHUTTLE = "SHIP_LIGHT_SHUTTLE"
    SHIP_ORE_HOUND = "SHIP_ORE_HOUND"
    SHIP_REFINING_FREIGHTER = "SHIP_REFINING_FREIGHTER"
    SHIP_SURVEYOR = "SHIP_SURVEYOR"


class SupplyLevel(StrEnum):
    SCARCE = "SCARCE"
    LIMITED = "LIMITED"
    MODERATE = "MODERATE"
    HIGH = "HIGH"
    ABUNDANT = "ABUNDANT"


class SystemType(StrEnum):
    NEUTRON_STAR = "NEUTRON_STAR"
    RED_STAR = "RED_STAR"
    ORANGE_STAR = "ORANGE_STAR"
    BLUE_STAR = "BLUE_STAR"
    YOUNG_STAR = "YOUNG_STAR"
    WHITE_DWARF = "WHITE_DWARF"
    BLACK_HOLE = "BLACK_HOLE"
    HYPERGIANT = "HYPERGIANT"
    NEBULA = "NEBULA"
    UNSTABLE = "UNSTABLE"


class TradeSymbol(StrEnum):
    PRECIOUS_STONES = "PRECIOUS_STONES"
    QUARTZ_SAND = "QUARTZ_SAND"
    SILICON_CRYSTALS = "SILICON_CRYSTALS"
    AMMONIA_ICE = "AMMONIA_ICE"
    LIQUID_HYDROGEN = "LIQUID_HYDROGEN"
    LIQUID_NITROGEN = "LIQUID_NITROGEN"
    ICE_WATER = "ICE_WATER"
    EXOTIC_MATTER = "EXOTIC_MATTER"
    ADVANCED_CIRCUITRY = "ADVANCED_CIRCUITRY"
    GRAVITON_EMITTERS = "GRAVITON_EMITTERS"
    IRON = "IRON"
    IRON_ORE = "IRON_ORE"
    COPPER = "COPPER"
    COPPER_ORE = "COPPER_ORE"
    ALUMINUM = "ALUMINUM"
    ALUMINUM_ORE = "ALUMINUM_ORE"
    SILVER = "SILVER"
    SILVER_ORE = "SILVER_ORE"
    GOLD = "GOLD"
    GOLD_ORE = "GOLD_ORE"
    PLATINUM = "PLATINUM"
    PLATINUM_ORE = "PLATINUM_ORE"
    DIAMONDS = "DIAMONDS"
    URANITE = "URANITE"
    URANITE_ORE = "URANITE_ORE"
    MERITIUM = "MERITIUM"
    MERITIUM_ORE = "MERITIUM_ORE"
    HYDROCARBON = "HYDROCARBON"
    ANTIMATTER = "ANTIMATTER"
    FAB_MATS = "FAB_MATS"
    FERTILIZERS = "FERTILIZERS"
    FABRICS = "FABRICS"
    FOOD = "FOOD"
    JEWELRY = "JEWELRY"
    MACHINERY = "MACHINERY"
    FIREARMS = "FIREARMS"
    ASSAULT_RIFLES = "ASSAULT_RIFLES"
    MILITARY_EQUIPMENT = "MILITARY_EQUIPMENT"
    EXPLOSIVES = "EXPLOSIVES"
    LAB_INSTRUMENTS = "LAB_INSTRUMENTS"
    AMMUNITION = "AMMUNITION"
    ELECTRONICS = "ELECTRONICS"
    SHIP_PLATING = "SHIP_PLATING"
    SHIP_PARTS = "SHIP_PARTS"
    EQUIPMENT = "EQUIPMENT"
    FUEL = "FUEL"
    MEDICINE = "MEDICINE"
    DRUGS = "DRUGS"
    CLOTHING = "CLOTHING"
    MICROPROCESSORS = "MICROPROCESSORS"
    PLASTICS = "PLASTICS"
    POLYNUCLEOTIDES = "POLYNUCLEOTIDES"
    BIOCOMPOSITES = "BIOCOMPOSITES"
    QUANTUM_STABILIZERS = "QUANTUM_STABILIZERS"
    NANOBOTS = "NANOBOTS"
    AI_MAINFRAMES = "AI_MAINFRAMES"
    QUANTUM_DRIVES = "QUANTUM_DRIVES"
    ROBOTIC_DRONES = "ROBOTIC_DRONES"
    CYBER_IMPLANTS = "CYBER_IMPLANTS"
    GENE_THERAPEUTICS = "GENE_THERAPEUTICS"
    NEURAL_CHIPS = "NEURAL_CHIPS"
    MOOD_REGULATORS = "MOOD_REGULATORS"
    VIRAL_AGENTS = "VIRAL_AGENTS"
    MICRO_FUSION_GENERATORS = "MICRO_FUSION_GENERATORS"
    SUPERGRAINS = "SUPERGRAINS"
    LASER_RIFLES = "LASER_RIFLES"
    HOLOGRAPHICS = "HOLOGRAPHICS"
    SHIP_SALVAGE = "SHIP_SALVAGE"
    RELIC_TECH = "RELIC_TECH"
    NOVEL_LIFEFORMS = "NOVEL_LIFEFORMS"
    BOTANICAL_SPECIMENS = "BOTANICAL_SPECIMENS"
    CULTURAL_ARTIFACTS = "CULTURAL_ARTIFACTS"
    FRAME_PROBE = "FRAME_PROBE"
    FRAME_DRONE = "FRAME_DRONE"
    FRAME_INTERCEPTOR = "FRAME_INTERCEPTOR"
    FRAME_RACER = "FRAME_RACER"
    FRAME_FIGHTER = "FRAME_FIGHTER"
    FRAME_FRIGATE = "FRAME_FRIGATE"
    FRAME_SHUTTLE = "FRAME_SHUTTLE"
    FRAME_EXPLORER = "FRAME_EXPLORER"
    FRAME_MINER = "FRAME_MINER"
    FRAME_LIGHT_FREIGHTER = "FRAME_LIGHT_FREIGHTER"
    FRAME_HEAVY_FREIGHTER = "FRAME_HEAVY_FREIGHTER"
    FRAME_TRANSPORT = "FRAME_TRANSPORT"
    FRAME_DESTROYER = "FRAME_DESTROYER"
    FRAME_CRUISER = "FRAME_CRUISER"
    FRAME_CARRIER = "FRAME_CARRIER"
    REACTOR_SOLAR_I = "REACTOR_SOLAR_I"
    REACTOR_FUSION_I = "REACTOR_FUSION_I"
    REACTOR_FISSION_I = "REACTOR_FISSION_I"
    REACTOR_CHEMICAL_I = "REACTOR_CHEMICAL_I"
    REACTOR_ANTIMATTER_I = "REACTOR_ANTIMATTER_I"
    ENGINE_IMPULSE_DRIVE_I = "ENGINE_IMPULSE_DRIVE_I"
    ENGINE_ION_DRIVE_I = "ENGINE_ION_DRIVE_I"
    ENGINE_ION_DRIVE_II = "ENGINE_ION_DRIVE_II"
    ENGINE_HYPER_DRIVE_I = "ENGINE_HYPER_DRIVE_I"
    MODULE_MINERAL_PROCESSOR_I = "MODULE_MINERAL_PROCESSOR_I"
    MODULE_GAS_PROCESSOR_I = "MODULE_GAS_PROCESSOR_I"
    MODULE_CARGO_HOLD_I = "MODULE_CARGO_HOLD_I"
    MODULE_CARGO_HOLD_II = "MODULE_CARGO_HOLD_II"
    MODULE_CARGO_HOLD_III = "MODULE_CARGO_HOLD_III"
    MODULE_CREW_QUARTERS_I = "MODULE_CREW_QUARTERS_I"
    MODULE_ENVOY_QUARTERS_I = "MODULE_ENVOY_QUARTERS_I"
    MODULE_PASSENGER_CABIN_I = "MODULE_PASSENGER_CABIN_I"
    MODULE_MICRO_REFINERY_I = "MODULE_MICRO_REFINERY_I"
    MODULE_SCIENCE_LAB_I = "MODULE_SCIENCE_LAB_I"
    MODULE_JUMP_DRIVE_I = "MODULE_JUMP_DRIVE_I"
    MODULE_JUMP_DRIVE_II = "MODULE_JUMP_DRIVE_II"
    MODULE_JUMP_DRIVE_III = "MODULE_JUMP_DRIVE_III"
    MODULE_WARP_DRIVE_I = "MODULE_WARP_DRIVE_I"
    MODULE_WARP_DRIVE_II = "MODULE_WARP_DRIVE_II"
    MODULE_WARP_DRIVE_III = "MODULE_WARP_DRIVE_III"
    MODULE_SHIELD_GENERATOR_I = "MODULE_SHIELD_GENERATOR_I"
    MODULE_SHIELD_GENERATOR_II = "MODULE_SHIELD_GENERATOR_II"
    MODULE_ORE_REFINERY_I = "MODULE_ORE_REFINERY_I"
    MODULE_FUEL_REFINERY_I = "MODULE_FUEL_REFINERY_I"
    MOUNT_GAS_SIPHON_I = "MOUNT_GAS_SIPHON_I"
    MOUNT_GAS_SIPHON_II = "MOUNT_GAS_SIPHON_II"
    MOUNT_GAS_SIPHON_III = "MOUNT_GAS_SIPHON_III"
    MOUNT_SURVEYOR_I = "MOUNT_SURVEYOR_I"
    MOUNT_SURVEYOR_II = "MOUNT_SURVEYOR_II"
    MOUNT_SURVEYOR_III = "MOUNT_SURVEYOR_III"
    MOUNT_SENSOR_ARRAY_I = "MOUNT_SENSOR_ARRAY_I"
    MOUNT_SENSOR_ARRAY_II = "MOUNT_SENSOR_ARRAY_II"
    MOUNT_SENSOR_ARRAY_III = "MOUNT_SENSOR_ARRAY_III"
    MOUNT_MINING_LASER_I = "MOUNT_MINING_LASER_I"
    MOUNT_MINING_LASER_II = "MOUNT_MINING_LASER_II"
    MOUNT_MINING_LASER_III = "MOUNT_MINING_LASER_III"
    MOUNT_LASER_CANNON_I = "MOUNT_LASER_CANNON_I"
    MOUNT_MISSILE_LAUNCHER_I = "MOUNT_MISSILE_LAUNCHER_I"
    MOUNT_TURRET_I = "MOUNT_TURRET_I"
    SHIP_PROBE = "SHIP_PROBE"
    SHIP_MINING_DRONE = "SHIP_MINING_DRONE"
    SHIP_SIPHON_DRONE = "SHIP_SIPHON_DRONE"
    SHIP_INTERCEPTOR = "SHIP_INTERCEPTOR"
    SHIP_LIGHT_HAULER = "SHIP_LIGHT_HAULER"
    SHIP_COMMAND_FRIGATE = "SHIP_COMMAND_FRIGATE"
    SHIP_EXPLORER = "SHIP_EXPLORER"
    SHIP_HEAVY_FREIGHTER = "SHIP_HEAVY_FREIGHTER"
    SHIP_LIGHT_SHUTTLE = "SHIP_LIGHT_SHUTTLE"
    SHIP_ORE_HOUND = "SHIP_ORE_HOUND"
    SHIP_REFINING_FREIGHTER = "SHIP_REFINING_FREIGHTER"
    SHIP_SURVEYOR = "SHIP_SURVEYOR"


class DepositSymbol(StrEnum):
    QUARTZ_SAND = "QUARTZ_SAND"
    SILICON_CRYSTALS = "SILICON_CRYSTALS"
    PRECIOUS_STONES = "PRECIOUS_STONES"
    ICE_WATER = "ICE_WATER"
    AMMONIA_ICE = "AMMONIA_ICE"
    IRON_ORE = "IRON_ORE"
    COPPER_ORE = "COPPER_ORE"
    SILVER_ORE = "SILVER_ORE"
    ALUMINUM_ORE = "ALUMINUM_ORE"
    GOLD_ORE = "GOLD_ORE"
    PLATINUM_ORE = "PLATINUM_ORE"
    DIAMONDS = "DIAMONDS"
    URANITE_ORE = "URANITE_ORE"
    MERITIUM_ORE = "MERITIUM_ORE"


class WaypointModifierSymbol(StrEnum):
    STRIPPED = "STRIPPED"
    UNSTABLE = "UNSTABLE"
    RADIATION_LEAK = "RADIATION_LEAK"
    CRITICAL_LIMIT = "CRITICAL_LIMIT"
    CIVIL_UNREST = "CIVIL_UNREST"


class WaypointTraitSymbol(StrEnum):
    UNCHARTED = "UNCHARTED"
    UNDER_CONSTRUCTION = "UNDER_CONSTRUCTION"
    MARKETPLACE = "MARKETPLACE"
    SHIPYARD = "SHIPYARD"
    OUTPOST = "OUTPOST"
    SCATTERED_SETTLEMENTS = "SCATTERED_SETTLEMENTS"
    SPRAWLING_CITIES = "SPRAWLING_CITIES"
    MEGA_STRUCTURES = "MEGA_STRUCTURES"
    PIRATE_BASE = "PIRATE_BASE"
    OVERCROWDED = "OVERCROWDED"
    HIGH_TECH = "HIGH_TECH"
    CORRUPT = "CORRUPT"
    BUREAUCRATIC = "BUREAUCRATIC"
    TRADING_HUB = "TRADING_HUB"
    INDUSTRIAL = "INDUSTRIAL"
    BLACK_MARKET = "BLACK_MARKET"
    RESEARCH_FACILITY = "RESEARCH_FACILITY"
    MILITARY_BASE = "MILITARY_BASE"
    SURVEILLANCE_OUTPOST = "SURVEILLANCE_OUTPOST"
    EXPLORATION_OUTPOST = "EXPLORATION_OUTPOST"
    MINERAL_DEPOSITS = "MINERAL_DEPOSITS"
    COMMON_METAL_DEPOSITS = "COMMON_METAL_DEPOSITS"
    PRECIOUS_METAL_DEPOSITS = "PRECIOUS_METAL_DEPOSITS"
    RARE_METAL_DEPOSITS = "RARE_METAL_DEPOSITS"
    METHANE_POOLS = "METHANE_POOLS"
    ICE_CRYSTALS = "ICE_CRYSTALS"
    EXPLOSIVE_GASES = "EXPLOSIVE_GASES"
    STRONG_MAGNETOSPHERE = "STRONG_MAGNETOSPHERE"
    VIBRANT_AURORAS = "VIBRANT_AURORAS"
    SALT_FLATS = "SALT_FLATS"
    CANYONS = "CANYONS"
    PERPETUAL_DAYLIGHT = "PERPETUAL_DAYLIGHT"
    PERPETUAL_OVERCAST = "PERPETUAL_OVERCAST"
    DRY_SEABEDS = "DRY_SEABEDS"
    MAGMA_SEAS = "MAGMA_SEAS"
    SUPERVOLCANOES = "SUPERVOLCANOES"
    ASH_CLOUDS = "ASH_CLOUDS"
    VAST_RUINS = "VAST_RUINS"
    MUTATED_FLORA = "MUTATED_FLORA"
    TERRAFORMED = "TERRAFORMED"
    EXTREME_TEMPERATURES = "EXTREME_TEMPERATURES"
    EXTREME_PRESSURE = "EXTREME_PRESSURE"
    DIVERSE_LIFE = "DIVERSE_LIFE"
    SCARCE_LIFE = "SCARCE_LIFE"
    FOSSILS = "FOSSILS"
    WEAK_GRAVITY = "WEAK_GRAVITY"
    STRONG_GRAVITY = "STRONG_GRAVITY"
    CRUSHING_GRAVITY = "CRUSHING_GRAVITY"
    TOXIC_ATMOSPHERE = "TOXIC_ATMOSPHERE"
    CORROSIVE_ATMOSPHERE = "CORROSIVE_ATMOSPHERE"
    BREATHABLE_ATMOSPHERE = "BREATHABLE_ATMOSPHERE"
    THIN_ATMOSPHERE = "THIN_ATMOSPHERE"
    JOVIAN = "JOVIAN"
    ROCKY = "ROCKY"
    VOLCANIC = "VOLCANIC"
    FROZEN = "FROZEN"
    SWAMP = "SWAMP"
    BARREN = "BARREN"
    TEMPERATE = "TEMPERATE"
    JUNGLE = "JUNGLE"
    OCEAN = "OCEAN"
    RADIOACTIVE = "RADIOACTIVE"
    MICRO_GRAVITY_ANOMALIES = "MICRO_GRAVITY_ANOMALIES"
    DEBRIS_CLUSTER = "DEBRIS_CLUSTER"
    DEEP_CRATERS = "DEEP_CRATERS"
    SHALLOW_CRATERS = "SHALLOW_CRATERS"
    UNSTABLE_COMPOSITION = "UNSTABLE_COMPOSITION"
    HOLLOWED_INTERIOR = "HOLLOWED_INTERIOR"
    STRIPPED = "STRIPPED"


class WaypointType(StrEnum):
    PLANET = "PLANET"
    GAS_GIANT = "GAS_GIANT"
    MOON = "MOON"
    ORBITAL_STATION = "ORBITAL_STATION"
    JUMP_GATE = "JUMP_GATE"
    ASTEROID_FIELD = "ASTEROID_FIELD"
    ASTEROID = "ASTEROID"
    ENGINEERED_ASTEROID = "ENGINEERED_ASTEROID"
    ASTEROID_BASE = "ASTEROID_BASE"
    NEBULA = "NEBULA"
    DEBRIS_FIELD = "DEBRIS_FIELD"
    GRAVITY_WELL = "GRAVITY_WELL"
    ARTIFICIAL_GRAVITY_WELL = "ARTIFICIAL_GRAVITY_WELL"
    FUEL_STATION = "FUEL_STATION"
