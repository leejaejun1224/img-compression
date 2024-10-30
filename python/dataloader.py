import os


def dataloader(video_sets):
    video_dicts = {}
    with open(video_sets, 'r') as file:
        file_names = file.read().split()
        video_dicts["input_video"] = file_names[0]
        video_dicts["output_video"] = file_names[1]
    
    return video_dicts