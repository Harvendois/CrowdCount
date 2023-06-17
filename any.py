import os

file_path = 'D:/CJH/CrowdCount/Shanghai/ShanghaiTech/part_A_final/test_data/ground-truth/IMG_1.h5'
if os.path.isfile(file_path):
    print("File exists")
else:
    print("File not found")
