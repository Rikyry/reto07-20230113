create_clock -name clk_50m -period 20.000 -waveform {0.000 10.000} [get_ports {clk}]
// Entrada asincrona
set_false_path -from [get_ports {sw[*]}] -to [get_cells {sw_meta*}]
// Reset externo
set_false_path -from [get_ports {rst_n}] -to [get_cells {rst_pipe*}]
// Margen para los LED
set_max_delay 10.000 -to [get_ports {led[*]}]
set_min_delay 0.000 -to [get_ports {led[*]}]
