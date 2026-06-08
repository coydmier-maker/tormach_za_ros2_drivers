# `tormach_za_ros2_drivers fix`

This repository fixes a problem with the original drivers that would cause /joint_states values associated with joints 2 and 3 to become inverted from the true encoder values. The only changes are in za6_hardware/config/hal_device_config.yaml, and they all involve adding negative signs to values associated with joints 2 and 3.
