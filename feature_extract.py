"""
This file is not relevant to DDS.
Just a attemption of OpenFace Tools

OpenFace are installed as docker container.
"""
import os
from multiprocessing import Process

DOCKER_ID = '52f250c487f3'
folder = '/home/yzk/data/finance_mv'
output_dir = '/home/yzk/data/mv_llds'
docker_cmd = f"docker exec -it {DOCKER_ID} /bin/bash -c "
video_folder_in_ctn = '/home/openface-build/videos'
output_folder_in_ctn = '/home/openface-build/output'
exec_in_ctn = './build/bin/FaceLandmarkVidMulti'


def task(video_id=None):
    if video_id is None:
        video_list = os.listdir(folder)
    else:
        video_list = video_id
    for video in video_list:
        try:
            os.system(f'docker cp {folder}/{video} {DOCKER_ID}:{video_folder_in_ctn}')
            extact_cmd = f'{exec_in_ctn} -f {video_folder_in_ctn}/{video} -out_dir {output_folder_in_ctn}'
            os.system(f"{docker_cmd} '{extact_cmd}' ")

            video_name = video.split('.')[0]
            output_video_dir = f'{output_dir}/{video_name}'
            os.system(f'mkdir {output_video_dir}')

            os.system(f'docker cp {DOCKER_ID}:{output_folder_in_ctn}/{video_name}.csv {output_video_dir}')
            os.system(f'docker cp {DOCKER_ID}:{output_folder_in_ctn}/{video_name}.hog {output_video_dir}')
            os.system(f"{docker_cmd} 'rm -rf {output_folder_in_ctn}/*' ")
        
        except Exception:
            continue