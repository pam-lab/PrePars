# Download verbs dataset which is downloaded from 
# https://www.peykaregan.ir/dataset/%D9%85%D8%AC%D9%85%D9%88%D8%B9%D9%87-%D8%A7%D9%81%D8%B9%D8%A7%D9%84-%D8%AA%D8%B5%D8%B1%DB%8C%D9%81%E2%80%8C%D8%B4%D8%AF%D9%87-%D9%81%D8%A7%D8%B1%D8%B3%DB%8C
gdown --id 1aIDGD3hHjDyWZ5i8vmgtMxRAzSxGFCWY 
unzip -o PVC.zip
cd PVC/Data && unzip -o '*.zip'
cd PVC/Data/TXT && awk -F '@' '{print $1}' verb.txt > all_verbs.txt