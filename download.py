import os
import shutil
import time
import urllib.request
import tqdm


def check_exist_remove(dir_path):
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)


def download_task(urls, images_dir, errors, id):
    for url in tqdm.tqdm(urls, desc="Thread %s downloading" % id):
        try:
            id, filename = url.split(" ")[0].split("/")
            real_url = url.split(" ")[1]
        except Exception as e:
            errors.append(url)

        filepath = os.path.join(images_dir, "%s_%s.jpg"%(id, filename))

        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)

        if not os.path.exists(filepath):
            try:
                # Manage redirect urls or broken one
                urllib.request.urlretrieve(real_url, filepath)

                # time.sleep(10)
                # crop_and_adapt_image(filepath, min_side_shape= 300, replace=True)
            except Exception as e:
                # print(e)
                print("%s ----- %s --- %s" % (e,filename, real_url))

                errors.append("%s,%s,%s" % (e, filename, real_url))



if __name__ == '__main__':
    images_dir = "images/"
    check_exist_remove(images_dir)

    with open('darn_url.txt', "r") as f:
        lines = f.readlines()
        total_urls,errors = [],[]

        for each in tqdm.tqdm(lines, desc="Parsing file"):
            total_urls.append(each)

        # divide urls and create threads
        download_task(total_urls,images_dir, errors, 0)

        with open("errors.txt", "w") as fw:
            for er in errors:
                fw.write(er + "\n")