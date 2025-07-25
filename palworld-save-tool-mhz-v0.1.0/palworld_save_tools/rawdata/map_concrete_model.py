import json
from typing import Any, Sequence

from palworld_save_tools.archive import *
from palworld_save_tools.json_tools import CustomEncoder
from palworld_save_tools.rawdata.common import (
    pal_item_and_num_read,
    pal_item_and_slot_writer,
    pal_item_booth_trade_info_read,
    pal_item_booth_trade_info_writer,
)


def pal_instance_id_reader(reader: FArchiveReader) -> dict[str, Any]:
    return {
        "player_uid": reader.guid(),
        "instance_id": reader.guid(),
    }


def pal_instance_id_writer(writer: FArchiveWriter, p: dict[str, Any]) -> None:
    writer.guid(p["player_uid"])
    writer.guid(p["instance_id"])


# Generate using extract_map_object_concrete_classes.py
MAP_OBJECT_NAME_TO_CONCRETE_MODEL_CLASS: dict[str, str] = {
    "droppedcharacter": "PalMapObjectDeathDroppedCharacterModel",
    "blastfurnace": "PalMapObjectConvertItemModel",
    "blastfurnace2": "PalMapObjectConvertItemModel",
    "blastfurnace3": "PalMapObjectConvertItemModel",
    "blastfurnace4": "PalMapObjectConvertItemModel",
    "blastfurnace5": "PalMapObjectConvertItemModel",
    "campfire": "PalMapObjectConvertItemModel",
    "characterrankup": "PalMapObjectRankUpCharacterModel",
    "commondropitem3d": "PalMapObjectDropItemModel",
    "cookingstove": "PalMapObjectConvertItemModel",
    "damagablerock_pv": "PalMapObjectItemDropOnDamagModel",
    "damagablerock0001": "PalMapObjectItemDropOnDamagModel",
    "damagablerock0002": "PalMapObjectItemDropOnDamagModel",
    "damagablerock0003": "PalMapObjectItemDropOnDamagModel",
    "damagablerock0004": "PalMapObjectItemDropOnDamagModel",
    "damagablerock0005": "PalMapObjectItemDropOnDamagModel",
    "damagablerock0017": "PalMapObjectItemDropOnDamagModel",
    "damagablerock0018": "PalMapObjectItemDropOnDamagModel",
    "damagablerock0019": "PalMapObjectItemDropOnDamagModel",
    "damagablerock0006": "PalMapObjectItemDropOnDamagModel",
    "damagablerock0007": "PalMapObjectItemDropOnDamagModel",
    "damagablerock0008": "PalMapObjectItemDropOnDamagModel",
    "damagablerock0009": "PalMapObjectItemDropOnDamagModel",
    "damagablerock0010": "PalMapObjectItemDropOnDamagModel",
    "damagablerock0011": "PalMapObjectItemDropOnDamagModel",
    "damagablerock0012": "PalMapObjectItemDropOnDamagModel",
    "damagablerock0013": "PalMapObjectItemDropOnDamagModel",
    "damagablerock0014": "PalMapObjectItemDropOnDamagModel",
    "damagablerock0015": "PalMapObjectItemDropOnDamagModel",
    "damagablerock0016": "PalMapObjectItemDropOnDamagModel",
    "deathpenaltychest": "PalMapObjectDeathPenaltyStorageModel",
    "defensegatlinggun": "PalMapObjectDefenseBulletLauncherModel",
    "defensemachinegun": "PalMapObjectDefenseBulletLauncherModel",
    "defenseminigun": "DEFAULT_UNKNOWN_PalMapObjectConcreteModelBase",
    "defensebowgun": "PalMapObjectDefenseBulletLauncherModel",
    "defensemissile": "PalMapObjectDefenseBulletLauncherModel",
    "defensewait": "PalMapObjectDefenseWaitModel",
    "electricgenerator": "PalMapObjectGenerateEnergyModel",
    "electricgenerator_slave": "PalMapObjectGenerateEnergyModel",
    "electricgenerator2": "PalMapObjectGenerateEnergyModel",
    "electricgenerator3": "PalMapObjectGenerateEnergyModel",
    "electrickitchen": "PalMapObjectConvertItemModel",
    "factory_comfortable_01": "PalMapObjectConvertItemModel",
    "factory_comfortable_02": "PalMapObjectConvertItemModel",
    "factory_hard_01": "PalMapObjectConvertItemModel",
    "factory_hard_02": "PalMapObjectConvertItemModel",
    "factory_hard_03": "PalMapObjectConvertItemModel",
    "farmblockv2_grade01": "PalMapObjectFarmBlockV2Model",
    "farmblockv2_grade02": "PalMapObjectFarmBlockV2Model",
    "farmblockv2_grade03": "PalMapObjectFarmBlockV2Model",
    "farmblockv2_wheet": "PalMapObjectFarmBlockV2Model",
    "farmblockv2_tomato": "PalMapObjectFarmBlockV2Model",
    "farmblockv2_lettuce": "PalMapObjectFarmBlockV2Model",
    "farmblockv2_berries": "PalMapObjectFarmBlockV2Model",
    "farmblockv2_potato": "PalMapObjectFarmBlockV2Model",
    "farmblockv2_onion": "PalMapObjectFarmBlockV2Model",
    "farmblockv2_carrot": "PalMapObjectFarmBlockV2Model",
    "fasttravelpoint": "PalMapObjectFastTravelPointModel",
    "hightechkitchen": "PalMapObjectConvertItemModel",
    "itemchest": "PalMapObjectItemChestModel",
    "itemchest_02": "PalMapObjectItemChestModel",
    "itemchest_03": "PalMapObjectItemChestModel",
    "itemchest_04": "PalMapObjectItemChestModel",
    "dev_itemchest": "PalMapObjectItemChestModel",
    "medicalpalbed": "PalMapObjectMedicalPalBedModel",
    "medicalpalbed_02": "PalMapObjectMedicalPalBedModel",
    "medicalpalbed_03": "PalMapObjectMedicalPalBedModel",
    "medicalpalbed_04": "PalMapObjectMedicalPalBedModel",
    "medicinefacility_01": "PalMapObjectConvertItemModel",
    "medicinefacility_02": "PalMapObjectConvertItemModel",
    "medicinefacility_03": "PalMapObjectConvertItemModel",
    "palfoodbox": "PalMapObjectPalFoodBoxModel",
    "palboxv2": "PalMapObjectBaseCampPoint",
    "displaycharacter": "PalMapObjectDisplayCharacterModel",
    "pickupitem_flint": "PalMapObjectPickupItemOnLevelModel",
    "pickupitem_log": "PalMapObjectPickupItemOnLevelModel",
    "pickupitem_redberry": "PalMapObjectPickupItemOnLevelModel",
    "pickupitem_stone": "PalMapObjectPickupItemOnLevelModel",
    "pickupitem_potato": "PalMapObjectPickupItemOnLevelModel",
    "pickupitem_poppy": "PalMapObjectPickupItemOnLevelModel",
    "playerbed": "PalMapObjectPlayerBedModel",
    "playerbed_02": "PalMapObjectPlayerBedModel",
    "playerbed_03": "PalMapObjectPlayerBedModel",
    "shippingitembox": "PalMapObjectShippingItemModel",
    "spherefactory_black_01": "PalMapObjectConvertItemModel",
    "spherefactory_black_02": "PalMapObjectConvertItemModel",
    "spherefactory_black_03": "PalMapObjectConvertItemModel",
    "spherefactory_white_01": "PalMapObjectConvertItemModel",
    "spherefactory_white_02": "PalMapObjectConvertItemModel",
    "spherefactory_white_03": "PalMapObjectConvertItemModel",
    "stonehouse1": "PalBuildObject",
    "stonepit": "PalMapObjectProductItemModel",
    "strawhouse1": "PalBuildObject",
    "weaponfactory_clean_01": "PalMapObjectConvertItemModel",
    "weaponfactory_clean_02": "PalMapObjectConvertItemModel",
    "weaponfactory_clean_03": "PalMapObjectConvertItemModel",
    "weaponfactory_dirty_01": "PalMapObjectConvertItemModel",
    "weaponfactory_dirty_02": "PalMapObjectConvertItemModel",
    "weaponfactory_dirty_03": "PalMapObjectConvertItemModel",
    "well": "PalMapObjectProductItemModel",
    "woodhouse1": "PalBuildObject",
    "workbench": "PalMapObjectConvertItemModel",
    "recoverotomo": "PalMapObjectRecoverOtomoModel",
    "palegg": "PalMapObjectPalEggModel",
    "palegg_fire": "PalMapObjectPalEggModel",
    "palegg_water": "PalMapObjectPalEggModel",
    "palegg_leaf": "PalMapObjectPalEggModel",
    "palegg_electricity": "PalMapObjectPalEggModel",
    "palegg_ice": "PalMapObjectPalEggModel",
    "palegg_earth": "PalMapObjectPalEggModel",
    "palegg_dark": "PalMapObjectPalEggModel",
    "palegg_dragon": "PalMapObjectPalEggModel",
    "hatchingpalegg": "PalMapObjectHatchingEggModel",
    "treasurebox": "PalMapObjectTreasureBoxModel",
    "treasurebox_visiblecontent": "PalMapObjectPickupItemOnLevelModel",
    "treasurebox_visiblecontent_skillfruits": "PalMapObjectPickupItemOnLevelModel",
    "stationdeforest2": "PalMapObjectProductItemModel",
    "workbench_skillunlock": "PalMapObjectConvertItemModel",
    "workbench_skillcard": "PalMapObjectConvertItemModel",
    "wooden_foundation": "PalBuildObject",
    "wooden_wall": "PalBuildObject",
    "wooden_roof": "PalBuildObject",
    "wooden_stair": "PalBuildObject",
    "wooden_doorwall": "PalMapObjectDoorModel",
    "stone_foundation": "PalBuildObject",
    "stone_wall": "PalBuildObject",
    "stone_roof": "PalBuildObject",
    "stone_stair": "PalBuildObject",
    "stone_doorwall": "PalMapObjectDoorModel",
    "metal_foundation": "PalBuildObject",
    "metal_wall": "PalBuildObject",
    "metal_roof": "PalBuildObject",
    "metal_stair": "PalBuildObject",
    "metal_doorwall": "PalMapObjectDoorModel",
    "buildablegoddessstatue": "PalMapObjectCharacterStatusOperatorModel",
    "spa": "PalMapObjectAmusementModel",
    "spa2": "PalMapObjectAmusementModel",
    "pickupitem_mushroom": "PalMapObjectPickupItemOnLevelModel",
    "defensewall_wood": "PalBuildObject",
    "defensewall": "PalBuildObject",
    "defensewall_metal": "PalBuildObject",
    "heater": "PalMapObjectHeatSourceModel",
    "electricheater": "PalMapObjectHeatSourceModel",
    "cooler": "PalMapObjectHeatSourceModel",
    "electriccooler": "PalMapObjectHeatSourceModel",
    "torch": "PalMapObjectTorchModel",
    "walltorch": "PalMapObjectTorchModel",
    "lamp": "PalMapObjectLampModel",
    "ceilinglamp": "PalMapObjectLampModel",
    "largelamp": "PalMapObjectLampModel",
    "largeceilinglamp": "PalMapObjectLampModel",
    "crusher": "PalMapObjectConvertItemModel",
    "woodcrusher": "PalMapObjectConvertItemModel",
    "flourmill": "PalMapObjectConvertItemModel",
    "trap_leghold": "DEFAULT_UNKNOWN_PalMapObjectConcreteModelBase",
    "trap_leghold_big": "DEFAULT_UNKNOWN_PalMapObjectConcreteModelBase",
    "trap_noose": "DEFAULT_UNKNOWN_PalMapObjectConcreteModelBase",
    "trap_movingpanel": "DEFAULT_UNKNOWN_PalMapObjectConcreteModelBase",
    "trap_mineelecshock": "DEFAULT_UNKNOWN_PalMapObjectConcreteModelBase",
    "trap_minefreeze": "DEFAULT_UNKNOWN_PalMapObjectConcreteModelBase",
    "trap_mineattack": "DEFAULT_UNKNOWN_PalMapObjectConcreteModelBase",
    "breedfarm": "PalMapObjectBreedFarmModel",
    "wood_gate": "PalMapObjectDoorModel",
    "stone_gate": "PalMapObjectDoorModel",
    "metal_gate": "PalMapObjectDoorModel",
    "repairbench": "PalMapObjectRepairItemModel",
    "skillfruit_test": "PalMapObjectPickupItemOnLevelModel",
    "toolboxv1": "PalMapObjectBaseCampPassiveEffectModel",
    "toolboxv2": "PalMapObjectBaseCampPassiveEffectModel",
    "fountain": "PalMapObjectBaseCampPassiveEffectModel",
    "silo": "PalMapObjectBaseCampPassiveEffectModel",
    "transmissiontower": "PalMapObjectBaseCampPassiveEffectModel",
    "flowerbed": "PalMapObjectBaseCampPassiveEffectModel",
    "stump": "PalMapObjectBaseCampPassiveEffectModel",
    "miningtool": "PalMapObjectBaseCampPassiveEffectModel",
    "cauldron": "PalMapObjectBaseCampPassiveEffectModel",
    "snowman": "PalMapObjectBaseCampPassiveEffectModel",
    "olympiccauldron": "PalMapObjectBaseCampPassiveEffectModel",
    "basecampworkhard": "PalMapObjectBaseCampPassiveWorkHardModel",
    "coolerbox": "PalMapObjectItemChest_AffectCorruption",
    "refrigerator": "PalMapObjectItemChest_AffectCorruption",
    "damagedscarecrow": "PalMapObjectDamagedScarecrowModel",
    "signboard": "PalMapObjectSignboardModel",
    "basecampbattledirector": "PalMapObjectBaseCampWorkerDirectorModel",
    "monsterfarm": "PalMapObjectMonsterFarmModel",
    "wood_windowwall": "PalBuildObject",
    "stone_windowwall": "PalBuildObject",
    "metal_windowwall": "PalBuildObject",
    "wood_trianglewall": "PalBuildObject",
    "stone_trianglewall": "PalBuildObject",
    "metal_trianglewall": "PalBuildObject",
    "wood_slantedroof": "PalBuildObject",
    "stone_slantedroof": "PalBuildObject",
    "metal_slantedroof": "PalBuildObject",
    "table1": "PalBuildObject",
    "barrel_wood": "PalMapObjectItemChestModel",
    "box_wood": "PalMapObjectItemChestModel",
    "box01_iron": "PalMapObjectItemChestModel",
    "box02_iron": "PalMapObjectItemChestModel",
    "shelf_wood": "PalMapObjectItemChestModel",
    "shelf_cask_wood": "PalMapObjectItemChestModel",
    "shelf_hang01_wood": "PalMapObjectItemChestModel",
    "shelf01_iron": "PalMapObjectItemChestModel",
    "shelf02_iron": "PalMapObjectItemChestModel",
    "shelf03_iron": "PalMapObjectItemChestModel",
    "shelf04_iron": "PalMapObjectItemChestModel",
    "shelf05_stone": "PalMapObjectItemChestModel",
    "shelf06_stone": "PalMapObjectItemChestModel",
    "shelf07_stone": "PalMapObjectItemChestModel",
    "shelf01_wall_stone": "PalMapObjectItemChestModel",
    "shelf01_wall_iron": "PalMapObjectItemChestModel",
    "shelf01_stone": "PalMapObjectItemChestModel",
    "shelf02_stone": "PalMapObjectItemChestModel",
    "shelf03_stone": "PalMapObjectItemChestModel",
    "shelf04_stone": "PalMapObjectItemChestModel",
    "container01_iron": "PalMapObjectItemChestModel",
    "tablesquare_wood": "PalBuildObject",
    "tablecircular_wood": "PalBuildObject",
    "bench_wood": "PalBuildObject",
    "stool_wood": "PalBuildObject",
    "decal_palsticker_pinkcat": "PalBuildObject",
    "stool_high_wood": "PalBuildObject",
    "counter_wood": "PalBuildObject",
    "rug_wood": "PalBuildObject",
    "shelf_hang02_wood": "PalBuildObject",
    "ivy01": "PalBuildObject",
    "ivy02": "PalBuildObject",
    "ivy03": "PalBuildObject",
    "chair01_wood": "PalBuildObject",
    "box01_stone": "PalBuildObject",
    "barrel01_iron": "PalBuildObject",
    "barrel02_iron": "PalBuildObject",
    "barrel03_iron": "PalBuildObject",
    "cablecoil01_iron": "PalBuildObject",
    "chair01_iron": "PalBuildObject",
    "chair02_iron": "PalBuildObject",
    "clock01_wall_iron": "PalBuildObject",
    "garbagebag_iron": "PalBuildObject",
    "goalsoccer_iron": "PalBuildObject",
    "machinegame01_iron": "PalBuildObject",
    "machinevending01_iron": "PalBuildObject",
    "pipeclay01_iron": "PalBuildObject",
    "signexit_ceiling_iron": "PalBuildObject",
    "signexit_wall_iron": "PalBuildObject",
    "sofa01_iron": "PalBuildObject",
    "sofa02_iron": "PalBuildObject",
    "stool01_iron": "PalBuildObject",
    "tablecircular01_iron": "PalBuildObject",
    "tableside01_iron": "PalBuildObject",
    "tablesquare01_iron": "PalBuildObject",
    "tablesquare02_iron": "PalBuildObject",
    "tire01_iron": "PalBuildObject",
    "trafficbarricade01_iron": "PalBuildObject",
    "trafficbarricade02_iron": "PalBuildObject",
    "trafficbarricade03_iron": "PalBuildObject",
    "trafficbarricade04_iron": "PalBuildObject",
    "trafficbarricade05_iron": "PalBuildObject",
    "trafficcone01_iron": "PalBuildObject",
    "trafficcone02_iron": "PalBuildObject",
    "trafficcone03_iron": "PalBuildObject",
    "trafficlight01_iron": "PalBuildObject",
    "bathtub_stone": "PalBuildObject",
    "chair01_stone": "PalBuildObject",
    "chair02_stone": "PalBuildObject",
    "clock01_stone": "PalBuildObject",
    "curtain01_wall_stone": "PalBuildObject",
    "desk01_stone": "PalBuildObject",
    "globe01_stone": "PalBuildObject",
    "mirror01_stone": "PalBuildObject",
    "mirror02_stone": "PalBuildObject",
    "mirror01_wall_stone": "PalBuildObject",
    "partition_stone": "PalBuildObject",
    "piano01_stone": "PalBuildObject",
    "piano02_stone": "PalBuildObject",
    "rug01_stone": "PalBuildObject",
    "rug02_stone": "PalBuildObject",
    "rug03_stone": "PalBuildObject",
    "rug04_stone": "PalBuildObject",
    "sofa01_stone": "PalBuildObject",
    "sofa02_stone": "PalBuildObject",
    "sofa03_stone": "PalBuildObject",
    "stool01_stone": "PalBuildObject",
    "stove01_stone": "PalBuildObject",
    "tablecircular01_stone": "PalBuildObject",
    "tabledresser01_stone": "PalMapObjectCharacterMakeModel",
    "tablesink01_stone": "PalBuildObject",
    "toilet01_stone": "PalBuildObject",
    "toiletholder01_stone": "PalBuildObject",
    "towlrack01_stone": "PalBuildObject",
    "plant01_plant": "PalBuildObject",
    "plant02_plant": "PalBuildObject",
    "plant03_plant": "PalBuildObject",
    "plant04_plant": "PalBuildObject",
    "light_floorlamp01": "PalMapObjectLampModel",
    "light_floorlamp02": "PalMapObjectLampModel",
    "light_lightpole01": "PalMapObjectLampModel",
    "light_lightpole02": "PalMapObjectLampModel",
    "light_lightpole03": "PalMapObjectLampModel",
    "light_lightpole04": "PalMapObjectLampModel",
    "light_fireplace01": "PalMapObjectTorchModel",
    "light_fireplace02": "PalMapObjectTorchModel",
    "light_candlesticks_top": "PalMapObjectLampModel",
    "light_candlesticks_wall": "PalMapObjectLampModel",
    "television01_iron": "PalBuildObject",
    "desk01_iron": "PalBuildObject",
    "trafficsign01_iron": "PalBuildObject",
    "trafficsign02_iron": "PalBuildObject",
    "trafficsign03_iron": "PalBuildObject",
    "trafficsign04_iron": "PalBuildObject",
    "chair01_pal": "PalBuildObject",
    "altar": "PalBuildObjectRaidBossSummon",
    "copperpit": "PalMapObjectProductItemModel",
    "copperpit_2": "PalMapObjectProductItemModel",
    "electrichatchingpalegg": "PalMapObjectHatchingEggModel",
    "pickupitem_cavemushroom": "PalMapObjectPickupItemOnLevelModel",
    "treasurebox_oilrig": "PalMapObjectTreasureBoxModel",
    "treasurebox_electric": "PalMapObjectTreasureBoxModel",
    "treasurebox_ivy": "PalMapObjectTreasureBoxModel",
    "treasurebox_ice": "PalMapObjectTreasureBoxModel",
    "treasurebox_fire": "PalMapObjectTreasureBoxModel",
    "treasurebox_water": "PalMapObjectTreasureBoxModel",
    "treasurebox_fishingjunk_requiredlonghold": "PalMapObjectTreasureBoxModel",
    "treasurebox_fishingjunk_requiredlonghold2": "PalMapObjectTreasureBoxModel",
    "treasurebox_requiredlonghold": "PalMapObjectTreasureBoxModel",
    "meteordrop_damagable": "PalMapObjectItemDropOnDamagModel",
    "electricgenerator_large": "PalMapObjectGenerateEnergyModel",
    "medicalpalbed_05": "PalMapObjectMedicalPalBedModel",
    "pickupitem_nightstone": "PalMapObjectPickupItemOnLevelModel",
    "workspeedincrease1": "PalMapObjectBaseCampPassiveEffectModel",
    "coalpit": "PalMapObjectProductItemModel",
    "quartzpit": "PalMapObjectProductItemModel",
    "sulfurpit": "PalMapObjectProductItemModel",
    "lab": "PalMapObjectLabModel",
    "palmedicinebox": "PalMapObjectPalMedicineBoxModel",
    "sanitydecrease1": "PalMapObjectBaseCampPassiveEffectModel",
    "energystorage_electric": "PalMapObjectEnergyStorageModel",
    "hugekitchen": "PalMapObjectConvertItemModel",
    "spherefactory_black_04": "PalMapObjectConvertItemModel",
    "icecrusher": "PalMapObjectConvertItemModel",
    "wallsignboard": "PalMapObjectSignboardModel",
    "skinchange": "BlueprintGeneratedClass",
    "dismantlingconveyor": "BlueprintGeneratedClass",
    "japanesestyle_doorwall_01": "PalMapObjectDoorModel",
    "japanesestyle_doorwall_02": "PalMapObjectDoorModel",
    "japanesestyle_doorwall_03": "PalMapObjectDoorModel",
    "factory_money": "PalMapObjectConvertItemModel",
    "multielectrichatchingpalegg": "PalMapObjectMultiHatchingEggModel",
    "coolerpalfoodbox": "BlueprintGeneratedClass",
    "itembooth": "PalMapObjectItemBoothModel",
    "palbooth": "PalMapObjectPalBoothModel",
    "supplydrop": "PalMapObjectSupplyStorageModel",
    "tansu": "PalMapObjectItemChestModel",
    "guildchest": "PalMapObjectGuildChestModel",
    "basecampitemdispenser": "PalMapObjectBaseCampItemDispenserModel",
    "farm_skillfruits": "PalMapObjectFarmSkillFruitsModel",
    "expedition": "PalMapObjectCharacterTeamMissionModel",
    "oilpump": "PalMapObjectProductItemModel",
    "compositedesk": "PalMapObjectConvertItemModel",
    "glass_doorwall": "PalMapObjectDoorModel",
    "zaisu": "PalMapObjectPlayerSitModel",
    "dimensionpalstorage": "PalMapObjectDimensionPalStorageModel",
    "zabuton": "PalBuildObject",
    "headstone": "PalMapObjectSignboardModel",
}


def decode_bytes(
    parent_reader: FArchiveReader, m_bytes: Sequence[int], object_id: str
) -> Optional[dict[str, Any]]:
    if len(m_bytes) == 0:
        return {"values": []}
    reader = parent_reader.internal_copy(bytes(m_bytes), debug=False)
    data: dict[str, Any] = {}

    if object_id.lower() not in MAP_OBJECT_NAME_TO_CONCRETE_MODEL_CLASS:
        print(f"Warning: Map object '{object_id}' not in database, skipping")
        return {"values": m_bytes}

    # Base handling
    data["instance_id"] = reader.guid()
    data["model_instance_id"] = reader.guid()

    map_object_concrete_model = MAP_OBJECT_NAME_TO_CONCRETE_MODEL_CLASS[
        object_id.lower()
    ]
    data["concrete_model_type"] = map_object_concrete_model
    match map_object_concrete_model:
        case "PalMapObjectCharacterTeamMissionModel":
            data["mission_id"] = reader.fstring()
            data["state"] = reader.byte()
            data["start_time"] = reader.i64()
            data["unknown_bytes"] = [int(b) for b in reader.read_to_end()]
        case "PalMapObjectFarmSkillFruitsModel":
            data["leading_bytes"] = reader.byte_list(4)
            data["skill_fruits_id"] = reader.fstring()
            data["current_state"] = reader.byte()
            data["progress_rate"] = reader.float()
            data["trailing_bytes"] = reader.byte_list(20)
        case "PalMapObjectSupplyStorageModel":
            data["created_at_real_time"] = reader.i64()
            data["trailing_bytes"] = reader.byte_list(8)
        case "PalMapObjectItemBoothModel":
            data["leading_bytes"] = reader.byte_list(4)
            data["private_lock_player_uid"] = reader.guid()
            data["trade_infos"] = reader.tarray(pal_item_booth_trade_info_read)
            data["trailing_bytes"] = reader.byte_list(20)
        case "PalMapObjectPalBoothModel":
            data["unknown_bytes"] = [int(b) for b in reader.read_to_end()]
        case "PalMapObjectMultiHatchingEggModel":
            data["unknown_bytes"] = [int(b) for b in reader.read_to_end()]
        case "PalMapObjectEnergyStorageModel":
            data["stored_energy_amount"] = reader.float()
            data["trailing_bytes"] = reader.byte_list(8)
        case "PalMapObjectDeathDroppedCharacterModel":
            data["stored_parameter_id"] = reader.guid()
            data["owner_player_uid"] = reader.guid()
            if not reader.eof():
                data["unknown_bytes"] = [int(b) for b in reader.read_to_end()]
        case "PalMapObjectConvertItemModel":
            data["leading_bytes"] = reader.byte_list(4)
            data["current_recipe_id"] = reader.fstring()
            data["requested_product_num"] = reader.i32()
            data["remain_product_num"] = reader.i32()
            data["work_speed_additional_rate"] = reader.float()
            data["trailing_bytes"] = reader.byte_list(8)
        case "PalMapObjectPickupItemOnLevelModel":
            data["auto_picked_up"] = reader.u32() > 0
        case "PalMapObjectDropItemModel":
            data["auto_picked_up"] = reader.u32() > 0
            data["pickupdable_player_uid"] = reader.guid()
            data["remove_pickup_guard_timer_handle"] = reader.i64()
            data["item_id"] = {
                "static_id": reader.fstring(),
                "dynamic_id": {
                    "created_world_id": reader.guid(),
                    "local_id_in_created_world": reader.guid(),
                },
            }
            data["trailing_bytes"] = reader.byte_list(4)
        case "PalMapObjectItemDropOnDamagModel":
            data["drop_item_infos"] = reader.tarray(pal_item_and_num_read)
            if not reader.eof():
                data["unknown_bytes"] = [int(b) for b in reader.read_to_end()]
        case "PalMapObjectDeathPenaltyStorageModel":
            data["auto_destroy_if_empty"] = reader.u32() > 0
            data["owner_player_uid"] = reader.guid()
            data["created_at"] = reader.u64()
            if not reader.eof():
                data["trailing_bytes"] = reader.byte_list(4)
        case "PalMapObjectDefenseBulletLauncherModel":
            data["leading_bytes"] = reader.byte_list(4)
            data["remaining_bullets"] = reader.i32()
            data["magazine_size"] = reader.i32()
            data["bullet_item_name"] = reader.fstring()
            data["trailing_bytes"] = reader.byte_list(4)
        case "PalMapObjectGenerateEnergyModel":
            data["generate_energy_rate_by_worker"] = reader.float()
            data["stored_energy_amount"] = reader.float()
            data["consume_energy_speed"] = reader.float()
        case "PalMapObjectFarmBlockV2Model":
            data["crop_progress_rate"] = reader.float()
            data["crop_data_id"] = reader.fstring()
            data["current_state"] = reader.byte()
            data["crop_progress_rate_value"] = reader.float()
            data["water_stack_rate_value"] = reader.float()
            data["state_machine"] = {
                "growup_required_time": reader.float(),
                "growup_progress_time": reader.float(),
            }
            data["trailing_bytes"] = reader.byte_list(8)
        case "PalMapObjectFastTravelPointModel":
            data["location_instance_id"] = reader.guid()
        case "PalMapObjectShippingItemModel":
            data["shipping_hours"] = reader.tarray(lambda r: r.i32())
        case "PalMapObjectProductItemModel":
            data["leading_bytes"] = reader.byte_list(4)
            data["work_speed_additional_rate"] = reader.float()
            data["product_item_id"] = reader.fstring()
            data["trailing_bytes"] = reader.byte_list(4)
        case "PalMapObjectRecoverOtomoModel":
            data["recover_amount_by_sec"] = reader.float()
        case "PalMapObjectHatchingEggModel":
            data["leading_bytes"] = reader.byte_list(4)
            data["hatched_character_save_parameter"] = reader.properties_until_end()
            data["current_pal_egg_temp_diff"] = reader.i32()
            data["hatched_character_guid"] = reader.guid()
            data["trailing_bytes"] = reader.byte_list(4)
        case "PalMapObjectTreasureBoxModel":
            data["treasure_grade_type"] = reader.byte()
            data["treasure_special_type"] = reader.byte()
            data["opened"] = reader.byte()
            data["long_hold_interaction_duration"] = reader.float()
            data["interact_player_action_type"] = reader.byte()
            data["is_lock_riding"] = reader.byte()
        case "PalMapObjectBreedFarmModel":
            data["leading_bytes"] = reader.byte_list(4)
            data["spawned_egg_instance_ids"] = reader.tarray(uuid_reader)
            data["trailing_bytes"] = reader.byte_list(4)
        case "PalMapObjectSignboardModel":
            data["leading_bytes"] = reader.byte_list(4)
            data["signboard_text"] = reader.fstring()
            data["last_modified_player_uid"] = reader.guid()
            data["trailing_bytes"] = reader.byte_list(4)
        case "PalMapObjectTorchModel":
            data["ignition_minutes"] = reader.i32()
            data["extinction_date_time"] = reader.i64()
            data["trailing_bytes"] = reader.byte_list(4)
        case "PalMapObjectPalEggModel":
            data["auto_picked_up"] = reader.u32() > 0
            data["pickupdable_player_uid"] = reader.guid()
            data["remove_pickup_guard_timer_handle"] = reader.i64()
        case "PalMapObjectBaseCampPoint":
            data["leading_bytes"] = reader.byte_list(4)
            data["base_camp_id"] = reader.guid()
            data["trailing_bytes"] = reader.byte_list(4)
        case "PalMapObjectItemChestModel" | "PalMapObjectItemChest_AffectCorruption":
            data["leading_bytes"] = reader.byte_list(4)
            data["private_lock_player_uid"] = reader.guid()
            data["trailing_bytes"] = reader.byte_list(4)
        case "PalMapObjectDimensionPalStorageModel":
            data["trailing_bytes"] = reader.byte_list(12)
        case (
            "PalMapObjectPlayerBedModel"
            | "PalBuildObject"
            | "PalMapObjectCharacterStatusOperatorModel"
            | "PalMapObjectRankUpCharacterModel"
            | "BlueprintGeneratedClass"
            | "PalMapObjectMedicalPalBedModel"
            | "PalMapObjectDoorModel"
            | "PalMapObjectMonsterFarmModel"
            | "PalMapObjectAmusementModel"
            | "PalMapObjectLampModel"
            | "PalMapObjectLabModel"
            | "PalMapObjectRepairItemModel"
            | "PalMapObjectBaseCampPassiveWorkHardModel"
            | "PalMapObjectBaseCampPassiveEffectModel"
            | "PalMapObjectBaseCampItemDispenserModel"
            | "PalMapObjectGuildChestModel"
            | "PalMapObjectCharacterMakeModel"
            | "PalMapObjectPalFoodBoxModel"
            | "PalMapObjectPlayerSitModel"
            | "PalMapObjectBaseCampWorkerDirectorModel"
            | "PalMapObjectPalMedicineBoxModel"
            | "PalMapObjectDefenseWaitModel"
            | "PalMapObjectHeatSourceModel"
            | "PalMapObjectDisplayCharacterModel"
            | "Default_PalMapObjectConcreteModelBase"
            | "PalMapObjectDamagedScarecrowModel"
        ):
            data["trailing_bytes"] = reader.byte_list(4)
        case _:
            print(
                f"Warning: Unknown map object concrete model {map_object_concrete_model}, skipping"
            )
            return {"values": m_bytes}

    if not reader.eof():
        raise Exception(
            f"Warning: EOF not reached for {object_id} {map_object_concrete_model}: ori: {''.join(f'{b:02x}' for b in m_bytes)} remaining: {reader.size - reader.data.tell()}"
        )
    return data


def encode_bytes(p: Optional[dict[str, Any]]) -> bytes:
    if p is None:
        return b""

    writer = FArchiveWriter()

    map_object_concrete_model = p["concrete_model_type"]

    # Base handling
    writer.guid(p["instance_id"])
    writer.guid(p["model_instance_id"])

    match map_object_concrete_model:
        case "PalMapObjectCharacterTeamMissionModel":
            writer.fstring(p["mission_id"])
            writer.byte(p["state"])
            writer.i64(p["start_time"])
            writer.write(bytes(p["unknown_bytes"]))
        case "PalMapObjectFarmSkillFruitsModel":
            writer.write(bytes(p["leading_bytes"]))
            writer.fstring(p["skill_fruits_id"])
            writer.byte(p["current_state"])
            writer.float(p["progress_rate"])
            writer.write(bytes(p["trailing_bytes"]))
        case "PalMapObjectSupplyStorageModel":
            writer.i64(p["created_at_real_time"])
            writer.write(bytes(p["trailing_bytes"]))
        case "PalMapObjectItemBoothModel":
            writer.write(bytes(p["leading_bytes"]))
            writer.guid(p["private_lock_player_uid"])
            writer.tarray(pal_item_booth_trade_info_writer, p["trade_infos"])
            writer.write(bytes(p["trailing_bytes"]))
        case "PalMapObjectPalBoothModel":
            writer.write(bytes(p["unknown_bytes"]))
        case "PalMapObjectMultiHatchingEggModel":
            writer.write(bytes(p["unknown_bytes"]))
        case "PalMapObjectEnergyStorageModel":
            writer.float(p["stored_energy_amount"])
            writer.write(bytes(p["trailing_bytes"]))
        case "PalMapObjectDeathDroppedCharacterModel":
            writer.guid(p["stored_parameter_id"])
            writer.guid(p["owner_player_uid"])
            if "unknown_bytes" in p:
                writer.write(bytes(p["unknown_bytes"]))
        case "PalMapObjectConvertItemModel":
            writer.write(bytes(p["leading_bytes"]))
            writer.fstring(p["current_recipe_id"])
            writer.i32(p["requested_product_num"])
            writer.i32(p["remain_product_num"])
            writer.float(p["work_speed_additional_rate"])
            writer.write(bytes(p["trailing_bytes"]))
        case "PalMapObjectPickupItemOnLevelModel":
            writer.u32(1 if p["auto_picked_up"] else 0)
        case "PalMapObjectDropItemModel":
            writer.u32(1 if p["auto_picked_up"] else 0)
            writer.guid(p["pickupdable_player_uid"])
            writer.i64(p["remove_pickup_guard_timer_handle"])
            writer.fstring(p["item_id"]["static_id"])
            writer.guid(p["item_id"]["dynamic_id"]["created_world_id"])
            writer.guid(p["item_id"]["dynamic_id"]["local_id_in_created_world"])
            writer.write(bytes(p["trailing_bytes"]))
        case "PalMapObjectItemDropOnDamagModel":
            writer.tarray(pal_item_and_slot_writer, p["drop_item_infos"])
            if "unknown_bytes" in p:
                writer.write(bytes(p["unknown_bytes"]))
        case "PalMapObjectDeathPenaltyStorageModel":
            writer.u32(1 if p["auto_destroy_if_empty"] else 0)
            writer.guid(p["owner_player_uid"])
            writer.u64(p["created_at"])
            if "trailing_bytes" in p:
                writer.write(bytes(p["trailing_bytes"]))
        case "PalMapObjectDefenseBulletLauncherModel":
            writer.write(bytes(p["leading_bytes"]))
            writer.i32(p["remaining_bullets"])
            writer.i32(p["magazine_size"])
            writer.fstring(p["bullet_item_name"])
            writer.write(bytes(p["trailing_bytes"]))
        case "PalMapObjectGenerateEnergyModel":
            writer.float(p["generate_energy_rate_by_worker"])
            writer.float(p["stored_energy_amount"])
            writer.float(p["consume_energy_speed"])
        case "PalMapObjectFarmBlockV2Model":
            writer.float(p["crop_progress_rate"])
            writer.fstring(p["crop_data_id"])
            writer.byte(p["current_state"])
            writer.float(p["crop_progress_rate_value"])
            writer.float(p["water_stack_rate_value"])
            writer.float(p["state_machine"]["growup_required_time"])
            writer.float(p["state_machine"]["growup_progress_time"])
            writer.write(bytes(p["trailing_bytes"]))
        case "PalMapObjectFastTravelPointModel":
            writer.guid(p["location_instance_id"])
        case "PalMapObjectShippingItemModel":
            writer.tarray(lambda w, x: w.i32(x), p["shipping_hours"])
        case "PalMapObjectProductItemModel":
            writer.write(bytes(p["leading_bytes"]))
            writer.float(p["work_speed_additional_rate"])
            writer.fstring(p["product_item_id"])
            writer.write(bytes(p["trailing_bytes"]))
        case "PalMapObjectRecoverOtomoModel":
            writer.float(p["recover_amount_by_sec"])
        case "PalMapObjectHatchingEggModel":
            writer.write(bytes(p["leading_bytes"]))
            writer.properties(p["hatched_character_save_parameter"])
            writer.i32(p["current_pal_egg_temp_diff"])
            writer.guid(p["hatched_character_guid"])
            writer.write(bytes(p["trailing_bytes"]))
        case "PalMapObjectTreasureBoxModel":
            writer.byte(p["treasure_grade_type"])
            writer.byte(p["treasure_special_type"])
            writer.byte(p["opened"])
            writer.float(p["long_hold_interaction_duration"])
            writer.byte(p["interact_player_action_type"])
            writer.byte(p["is_lock_riding"])
        case "PalMapObjectBreedFarmModel":
            writer.write(bytes(p["leading_bytes"]))
            writer.tarray(uuid_writer, p["spawned_egg_instance_ids"])
            writer.write(bytes(p["trailing_bytes"]))
        case "PalMapObjectSignboardModel":
            writer.write(bytes(p["leading_bytes"]))
            writer.fstring(p["signboard_text"])
            writer.guid(p["last_modified_player_uid"])
            writer.write(bytes(p["trailing_bytes"]))
        case "PalMapObjectTorchModel":
            writer.i32(p["ignition_minutes"])
            writer.i64(p["extinction_date_time"])
            writer.write(bytes(p["trailing_bytes"]))
        case "PalMapObjectPalEggModel":
            writer.u32(1 if p["auto_picked_up"] else 0)
            writer.guid(p["pickupdable_player_uid"])
            writer.i64(p["remove_pickup_guard_timer_handle"])
        case "PalMapObjectBaseCampPoint":
            writer.write(bytes(p["leading_bytes"]))
            writer.guid(p["base_camp_id"])
            writer.write(bytes(p["trailing_bytes"]))
        case "PalMapObjectItemChestModel" | "PalMapObjectItemChest_AffectCorruption":
            writer.write(bytes(p["leading_bytes"]))
            writer.guid(p["private_lock_player_uid"])
            writer.write(bytes(p["trailing_bytes"]))
        case (
            "PalMapObjectPlayerBedModel"
            | "PalBuildObject"
            | "PalMapObjectCharacterStatusOperatorModel"
            | "PalMapObjectRankUpCharacterModel"
            | "BlueprintGeneratedClass"
            | "PalMapObjectMedicalPalBedModel"
            | "PalMapObjectDoorModel"
            | "PalMapObjectMonsterFarmModel"
            | "PalMapObjectAmusementModel"
            | "PalMapObjectLampModel"
            | "PalMapObjectLabModel"
            | "PalMapObjectRepairItemModel"
            | "PalMapObjectBaseCampPassiveWorkHardModel"
            | "PalMapObjectBaseCampPassiveEffectModel"
            | "PalMapObjectBaseCampItemDispenserModel"
            | "PalMapObjectGuildChestModel"
            | "PalMapObjectCharacterMakeModel"
            | "PalMapObjectPalFoodBoxModel"
            | "PalMapObjectPlayerSitModel"
            | "PalMapObjectDimensionPalStorageModel"
            | "PalMapObjectBaseCampWorkerDirectorModel"
            | "PalMapObjectPalMedicineBoxModel"
            | "PalMapObjectDefenseWaitModel"
            | "PalMapObjectHeatSourceModel"
            | "PalMapObjectDisplayCharacterModel"
            | "Default_PalMapObjectConcreteModelBase"
            | "PalMapObjectDamagedScarecrowModel"
        ):
            writer.write(bytes(p["trailing_bytes"]))
        case _:
            raise Exception(
                f"Unknown map object concrete model {map_object_concrete_model}"
            )

    encoded_bytes = writer.bytes()
    return encoded_bytes