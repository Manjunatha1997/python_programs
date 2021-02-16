import requests
from bs4 import BeautifulSoup as bs
import os

r = requests.get('https://www.cottonworks.com/resources/defects-glossary/')
web_page = bs(r.content)


divs = web_page.find_all('div', attrs={'class':'defect-thumb'})

output_path_directory = '/home/manju/Desktop/fabrics/'


defect_names = []

count = 0
img_count = 0

all_urls = []
for i in divs:
    defect_name = web_page.select('div.defect-thumb ul li span')[count].string
    image_url = web_page.select('div.defect-thumb a img')[img_count]
    # print(image_url['src'])
    image_url = image_url['src']
    image_data = requests.get(image_url).content

    if os.path.isdir(output_path_directory+defect_name):
        os.mkdir(output_path_directory+defect_name+str(img_count))
        fw = open(output_path_directory+defect_name+'/'+'image.jpg','wb')
        fw.write(image_data)
        fw.close()
    else:
        os.mkdir(output_path_directory+defect_name)
        fw = open(output_path_directory + defect_name + '/'+'image.jpg','wb')
        fw.write(image_data)
        fw.close()
    # image_data = requests.get(image_url['src']).content
    #
    # fw = open('image.jpg','wb')
    # fw.write(image_data)
    # fw.close()

    # all_urls.append(image_url['src'])
    # print('defect name:',defect_name)
    count += 3
    img_count += 1
    defect_names.append(defect_name)




#
# print(len(set(defect_names)))
# print(len(all_urls))
# print(all_urls)
# Creating Folders
# c = 1
# for folder in defect_names:
#     # if not os.path.isdir(output_path_directory+folder):
#     #     os.mkdir(output_path_directory+folder)
#     if os.path.isdir(output_path_directory+folder):
#         os.mkdir(output_path_directory+folder+str(c))
#         c += 1
#     else:
#         os.mkdir(output_path_directory+folder)