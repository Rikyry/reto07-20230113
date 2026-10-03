set board [file dirname [file normalize [info script]]]
set root [file dirname $board]
create_project -name reto07_20230113 -dir [file join $board gowin] -pn GW5A-LV25MG121NC1/I0 -device_version A -force
foreach name {control_logic datapath result_register top_20230113 tang_top_20230113} {
    add_file [file join $root src ${name}.v]
}
add_file [file join $board constraints tang25k.cst]
add_file [file join $board constraints tang25k.sdc]
foreach name {tb_top_20230113 tb_tang_top_20230113} {
    set tb [file join $root sim ${name}.v]
    add_file $tb
    set_file_enable $tb false
}
set_option -top_module tang_top_20230113
set_option -verilog_std v2001
set_option -output_base_name reto07_20230113
set_option -gen_text_timing_rpt 1
set_option -use_sspi_as_gpio 1
set_option -use_cpu_as_gpio 1
run all

# Guardar resultados
file mkdir [file join $board bitstream]
file mkdir [file join $board reports]
set out [file join $board gowin reto07_20230113 impl]
file copy -force [file join $out pnr reto07_20230113.fs] [file join $board bitstream reto07_20230113.fs]
foreach f [glob [file join $out pnr *.tr] [file join $out pnr *.rpt.txt] [file join $out pnr *.pin.html] [file join $out gwsynthesis *_syn.rpt.html]] {file copy -force $f [file join $board reports]}

# Rutas relativas
set project [file join $board gowin reto07_20230113 reto07_20230113.gprj]
set f [open $project r]
set xml [read $f]
close $f
set xml [string map [list "${root}/" "../../../"] $xml]
set f [open $project w]
puts -nonewline $f $xml
close $f
