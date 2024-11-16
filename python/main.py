import argparse
from compression import *
from visualize import *
from verifying import *
from dataloader import *




def main(args):

    ### Dataloader
    video_dicts = dataloader(args.video_sets)
    input_video = video_dicts["input_video"]
    output_video = video_dicts["output_video"]
    
    
    ### Compressing
    print("Compressing start. codec : ", args.codec)
    if args.codec == "h264":
        compress_video_lossless_h264_dummy(input_video, output_video)
    elif args.codec == "huffyuv":
        compress_video_lossless_huffyuv(input_video, output_video)
    
    ### Lossless check
    print("Making sure it's lossless")
    check_lossless_by_frames(input_video, output_video)
    
    
    ### Visualizing --option
    # press q for stop streaming
    if args.visualize:
        print("Visualizing")
        play_video(output_video)
    
    


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--video_sets", dest="video_sets", type=str)
    parser.add_argument("--visualize", dest="visualize", type=bool, default=False)
    parser.add_argument("--codec", dest="codec", type=str, default="h264")
    args = parser.parse_args()
    main(args)

