import argparse
from h264 import *
from visualize import *
from verifying import *
from dataloader import *




def main(args):
    input_video = '/home/jaejun/Videos/raw/test2_raw.avi'
    output_video = '/home/jaejun/Videos/results/test2_raw_compressed.avi'
    
    # dataloader 추가하기.
    input_video, output_video = dataloader(args.video_sets)
    
    # compressing start
    print("Compressing start. codec : ", args.codec)
    if args.codec == "h264":
        compress_video_lossless_h264(input_video, output_video)
    
    
    # comparing
    print("Making sure it's lossless")
    check_lossless(input_video, output_video)
    
    
    # visualizing --option
    ## press q for stop streaming
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

