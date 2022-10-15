@REM set your dataset path & excel file path.
@REM if your excel file path is None, default path is same with dataset path.
chcp 65001
python update_count_table.py ^
--dataset D:\NIA_77_1\221011 ^
--cls_json classJson 
python update_time_table.py ^
--dataset D:\NIA_77_1\221011 ^
--cls_json classJson 
python update_error_table.py ^
--dataset D:\NIA_77_1\221011