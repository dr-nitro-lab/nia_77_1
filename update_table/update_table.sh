# set your dataset path & excel file path.
# if your excel file path is None, default path is same with dataset path.
python update_count_table.py \
--dataset D:/NIA_77_1/221011 \
--cls_json classJson
python update_time_table.py \
--dataset D:/NIA_77_1/221011 \
--cls_json classJson 
python update_error_table.py \
--dataset D:/NIA_77_1/221011