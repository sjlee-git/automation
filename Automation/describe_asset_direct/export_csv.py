import csv

def export_by_csv(file_name,data_list):

    # temp file
    f = open(file_name, "w+", encoding='utf-8-sig', newline='')
    temp_csv_file = csv.writer(f)


    # write
    temp_csv_file.writerow(list(data_list[0].keys()))

    # 데이터 입력
    for data in data_list: temp_csv_file.writerow(list(data.values()))

    # 닫기
    f.close()