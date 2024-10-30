#include <iostream>
#include <string>
#include "snappy.h"
#include <opencv2/opencv.hpp>
#include <fstream>
#include <chrono>
#include <thread>
#include <vector>
#include <mutex>

// 파일 크기를 얻는 함수
int getFileSize(const std::string& filename) {
    std::ifstream file(filename, std::ifstream::ate | std::ifstream::binary);
    return static_cast<int>(file.tellg());
}

// 바이너리 파일 저장 함수
void saveBinaryFile(const std::string& filename, const std::string& data) {
    std::ofstream file(filename, std::ios::out | std::ios::binary);
    file.write(data.data(), data.size());
    file.close();
}

// 각 채널별로 압축하는 함수 (멀티스레드용)
void compress_channel(const std::string& raw_data, std::string& compressed_output, std::mutex& mtx, int channel_index) {
    std::string output;
    auto start = std::chrono::high_resolution_clock::now();

    // Snappy 압축 수행
    snappy::Compress(raw_data.c_str(), raw_data.size(), &output);

    auto compressEnd = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed = compressEnd - start;

    // 결과 저장 (mutex로 보호)
    std::lock_guard<std::mutex> lock(mtx);
    compressed_output = output;

    // 결과 출력
    double compressionRate = static_cast<double>(output.size()) / raw_data.size() * 100;
    std::cout << "Channel " << channel_index << " compressed size : " << output.size() << " bytes" << std::endl;
    std::cout << "Channel " << channel_index << " compressed speed : " << elapsed.count() << " seconds" << std::endl;
    std::cout << "Channel " << channel_index << " compressed rate : " << compressionRate << "%" << std::endl;
}

int main(int argc, const char* argv[]) {
    std::string imgPath = "../imgs/test1.bmp";  // 업로드된 파일 경로
    std::string compressedImgPath = "../results/test.snappy";  // 압축된 데이터 저장 경로

    // BMP 이미지 로드 (OpenCV 사용)
    cv::Mat image = cv::imread(imgPath, cv::IMREAD_UNCHANGED);
    if (image.empty()) {
        std::cerr << "이미지를 불러올 수 없습니다: " << imgPath << std::endl;
        return -1;
    }

    // 채널 분리
    std::vector<cv::Mat> channels(3);
    cv::split(image, channels);  // B, G, R 채널 분리

    // 압축 결과 저장 공간
    std::vector<std::string> compressed_channels(3);
    std::mutex mtx;  // 멀티스레딩 동기화

    // 스레드를 이용하여 병렬 압축 수행
    std::vector<std::thread> threads;
    auto total_start = std::chrono::high_resolution_clock::now();  // 전체 압축 시간 측정 시작
    for (int i = 0; i < 3; ++i) {
        // 각 채널을 압축하고 결과를 저장하는 스레드 시작
        std::vector<uchar> buf;
        cv::imencode(".bmp", channels[i], buf);
        std::string rawImageData(buf.begin(), buf.end());

        threads.emplace_back(compress_channel, rawImageData, std::ref(compressed_channels[i]), std::ref(mtx), i);
    }

    // 스레드 종료 대기
    for (auto& th : threads) {
        th.join();
    }
    auto total_end = std::chrono::high_resolution_clock::now();  // 전체 압축 시간 측정 종료

    // 총 압축된 데이터 크기 계산 및 출력
    size_t total_compressed_size = 0;
    for (int i = 0; i < 3; ++i) {
        total_compressed_size += compressed_channels[i].size();
    }

    std::cout << "Total compressed size: " << total_compressed_size << " bytes" << std::endl;

    // 전체 압축 시간 출력
    std::chrono::duration<double> total_elapsed = total_end - total_start;
    std::cout << "Total compression speed: " << total_elapsed.count() << " seconds" << std::endl;

    // 결과 파일 저장 (선택적으로 하나의 채널만 저장 또는 전체 데이터 저장)
    saveBinaryFile(compressedImgPath, compressed_channels[0]);  // 예시로 첫 번째 채널 저장

    return 0;
}
