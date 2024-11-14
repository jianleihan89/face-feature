"""
Envoke OpenFace Tools for Extracting Face Feature in video

OpenFace are installed as docker container.
"""
import os
from multiprocessing import Process
import traceback

DOCKER_ID = '4355dbcb9f33'
folder = 'video'
output_dir = 'output'
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
            # mkdir in container path
            mk_cmd = f'mkdir -p {video_folder_in_ctn}'
            os.system(f"{docker_cmd} '{mk_cmd}' ")

            # copy video on host into container
            os.system(f'docker cp {folder}/{video} {DOCKER_ID}:{video_folder_in_ctn}')

            # execute binary in container to extract feature
            extact_cmd = f'{exec_in_ctn} -f {video_folder_in_ctn}/{video} -out_dir {output_folder_in_ctn}'
            os.system(f"{docker_cmd} '{extact_cmd}' ")

            # format output filename
            video_name = video.split('.')[0]
            output_video_dir = f'{output_dir}/{video_name}'
            os.system(f'mkdir {output_video_dir}')

            os.system(f'docker cp {DOCKER_ID}:{output_folder_in_ctn}/{video_name}.csv {output_video_dir}')
            os.system(f'docker cp {DOCKER_ID}:{output_folder_in_ctn}/{video_name}.hog {output_video_dir}')
            os.system(f"{docker_cmd} 'rm -rf {output_folder_in_ctn}/*' ")
        
        except Exception as e:
            traceback.print_exc()
            continue

task()