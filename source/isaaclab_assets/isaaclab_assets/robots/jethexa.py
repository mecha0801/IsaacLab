import isaaclab.sim as sim_utils
from isaaclab.assets.articulation import ArticulationCfg
from isaaclab.actuators import ImplicitActuatorCfg
from isaaclab_assets import ISAACLAB_ASSETS_DATA_DIR


# 다리 관절 액츄에이터 설정
ACTUATOR_CFG = ImplicitActuatorCfg(
    joint_names_expr=[".*_joint_.*"],
    effort_limit=6.0,
    velocity_limit=2.62,
    stiffness=2000.0,
    damping=50.0,
)

JETHEXA_ROBOT_CFG = ArticulationCfg(
    # prim_path="{ENV_REGEX_NS}/Robot",
    spawn=sim_utils.UsdFileCfg(
        usd_path=f"{ISAACLAB_ASSETS_DATA_DIR}/Robots/hiwander/jethexa/robot/robot.usd",
        activate_contact_sensors=True,
        rigid_props=sim_utils.RigidBodyPropertiesCfg(
            rigid_body_enabled=True,
            disable_gravity=False,
            angular_damping=0.05,
            enable_gyroscopic_forces=True,
        ),
        articulation_props=sim_utils.ArticulationRootPropertiesCfg(
            enabled_self_collisions=True
        ),
        copy_from_source=False
    ),
    init_state=ArticulationCfg.InitialStateCfg(
        pos=(0.0, 0.0, 0.2),
        rot=(1.0, 0.0, 0.0, 0.0),
        joint_pos={
            "coxa_joint_.*": 0.0,
            "femur_joint_.*": 0.0,
            "tibia_joint_.*": -0.0,
        },
        joint_vel={".*": 0.0},
    ),
    actuators={"legs": ACTUATOR_CFG},
    soft_joint_pos_limit_factor=0.9,
)