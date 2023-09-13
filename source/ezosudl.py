import main

osu_dir = input("Input your osu directory:")
list_file = input("Input your beatmap file:")
main.main([f"-o={osu_dir}",f"-s={osu_dir}/Songs", f"-l={list_file}"])