import matplotlib.pyplot as plt
from json_utils import (
    json2list
)


json_list = json2list("221011")
val_list = []
for name, json_obj in json_list.items():
    try:
        tempo_list = json_obj["annotation_data_info"]["tempo"]
        if len(tempo_list)==1:
            tempo = tempo_list[0]["annotation_code"]
            if not tempo:
                print(f"{name} has None in tempo field.")
            else:
                val_list.append(tempo)
        elif len(tempo_list)==0:
            print(f"{name} has no tempo annotations")
        else:
            print(f"{name} has multiple tempo annotations")
    except KeyError:
        print(f"{name}.json don't have bpm key or has different format of fields.")

if None in val_list:
    print("none exist")

plt.hist(val_list, bins = 60, range=(0,600))
plt.show()