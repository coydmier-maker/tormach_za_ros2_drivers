# `tormach_za_ros2_drivers fix`

Remember to run docker using

        ./src/tormach_za_ros2_drivers/devel_scripts/docker-dev.sh

Currently trying to run this off a Ubnuntu machine running Humble 22.04. If you're having an issue where it
"cannot shutdown a ROS adapter that is not running" due to init_sim not being found by your drivers, use this fix.

All I did was change line 386 of __init__.py (located in /src/tormach_za_ros2_drivers/za6_hardware/hal_plumber) from:

    self.drive_cls.init_sim(sim_device_data=self.sim_device_data)

to

    self.drive_cls.init_class(sim_device_data=self.sim_device_data)

and
drive_state.py (located in /src/tormach_za_ros2_drivers/za6_hardware/hal_plumber) from:

    self.drive_cls.init_sim(sim_device_data=self.sim_device_data)
to

    drv_cls.init_class(sim_device_data=sim_dev_data)

Rebuild using after fixes:

    rm -rf build install log
    colcon build --symlink-install
    source install/setup.bash

Run using:

        source install/setup.bash
        ros2 launch za6_bringup bringup.launch

Feel free to leave any issues in my repository. I'll try my best to help.
