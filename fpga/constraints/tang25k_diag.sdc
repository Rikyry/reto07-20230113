create_clock -name clk_50m -period 20.000 -waveform {0.000 10.000} [get_ports {clk}]
set_false_path -from [get_ports {sw[*]}] -to [get_cells {sw_meta*}]
set_max_delay 10.000 -to [get_ports {led[*]}]
set_min_delay 0.000 -to [get_ports {led[*]}]
