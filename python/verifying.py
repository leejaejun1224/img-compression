import subprocess
import re

def check_lossless(input_video, compressed_video):
    # PSNR 계산
    psnr_command = [
        'ffmpeg',
        '-i', input_video,
        '-i', compressed_video,
        '-lavfi', 'psnr',
        '-f', 'null', '-'
    ]

    # SSIM 계산
    ssim_command = [
        'ffmpeg',
        '-i', input_video,
        '-i', compressed_video,
        '-lavfi', 'ssim',
        '-f', 'null', '-'
    ]

    try:
        # PSNR 계산
        psnr_result = subprocess.run(
            psnr_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        psnr_output = psnr_result.stderr
        psnr_match = re.search(r'average:\s*([0-9.]+|\d+\.\d+e[+-]\d+|inf)', psnr_output)
        psnr_value = psnr_match.group(1) if psnr_match else None

        # SSIM 계산
        ssim_result = subprocess.run(
            ssim_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        ssim_output = ssim_result.stderr
        ssim_match = re.search(r'All:([0-9.]+)', ssim_output)
        ssim_value = float(ssim_match.group(1)) if ssim_match else None

        # 무손실 여부 판단
        if psnr_value == 'inf' and ssim_value == 1.0:
            print("압축은 무손실입니다.")
            print(f"PSNR: 무한대, SSIM: {ssim_value}")
        else:
            print("압축은 손실이 있습니다.")
            print(f"PSNR: {psnr_value}, SSIM: {ssim_value}")

    except subprocess.CalledProcessError as e:
        print("FFmpeg 명령어 실행 중 오류가 발생했습니다.")
        print(e)

