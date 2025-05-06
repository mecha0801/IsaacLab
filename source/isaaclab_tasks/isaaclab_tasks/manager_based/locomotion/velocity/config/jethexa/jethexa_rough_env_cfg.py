# Copyright (c) 2022-2024, The Isaac Lab Project Developers.
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause


from isaaclab.utils import configclass

from isaaclab_tasks.manager_based.locomotion.velocity.velocity_env_cfg import LocomotionVelocityRoughEnvCfg

##
# Pre-defined configs
##
from isaaclab_assets.robots.jethexa import JETHEXA_ROBOT_CFG


@configclass
class JethexaRoughEnvCfg(LocomotionVelocityRoughEnvCfg):
    def __post_init__(self):
        super().__post_init__()

        ROOT = "{ENV_REGEX_NS}/robot"          # 로봇 루트 위치
        BASE = ROOT + "/base"

        # 1) 로봇 스폰
        self.scene.robot = JETHEXA_ROBOT_CFG.replace(prim_path=ROOT)
        self.scene.robot.init_state.pos = (0.0, 0.0, 0.12)

        # 2) 센서 경로
        self.scene.height_scanner.prim_path = BASE
        self.scene.contact_forces.prim_path = ROOT + "/.*"

        # # 3) 발·허벅지 링크 정규식
        FOOT_REGEX = "tibia_.*"
        THIGH_REGEX = "femur_.*"

        # ─────────────────────────────────────────
        #   보상·종료조건 쪽 센서-필터 업데이트
        # ─────────────────────────────────────────
        self.rewards.feet_air_time.params["sensor_cfg"].body_names = FOOT_REGEX
        self.rewards.undesired_contacts.params["sensor_cfg"].body_names = THIGH_REGEX
        self.terminations.base_contact.params["sensor_cfg"].body_names = "base"
        self.terminations.base_contact.params["threshold"] = 50.0

        # # 4) 이벤트(질량·힘)에서 base 이름 통일
        # for term in ("add_base_mass", "base_external_force_torque"):
        #     getattr(self.events, term).params["asset_cfg"].body_names = "base"
        # for term in ("add_base_mass", "base_external_force_torque"):
        #     getattr(self.events, term).params["asset_cfg"].body_names = "base"
        # self.terminations.base_contact.params["sensor_cfg"].body_names = "base"



@configclass
class JethexaRoughEnvCfg_PLAY(JethexaRoughEnvCfg):
    def __post_init__(self):
        # post init of parent
        super().__post_init__()

        # make a smaller scene for play
        self.scene.num_envs = 50
        self.scene.env_spacing = 2.5
        # spawn the robot randomly in the grid (instead of their terrain levels)
        self.scene.terrain.max_init_terrain_level = None
        # reduce the number of terrains to save memory
        if self.scene.terrain.terrain_generator is not None:
            self.scene.terrain.terrain_generator.num_rows = 5
            self.scene.terrain.terrain_generator.num_cols = 5
            self.scene.terrain.terrain_generator.curriculum = False

        # disable randomization for play
        self.observations.policy.enable_corruption = False
        # remove random pushing event
        self.events.base_external_force_torque = None
        self.events.push_robot = None