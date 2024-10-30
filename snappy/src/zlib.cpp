#include <opencv2/opencv.hpp>
#include <iostream>
#include <zlib.h>
#include <thread>
#include <vector>
#include <mutex>

// Zlib 압축 함수
std::vector<unsigned char> zlib_compress(const std::vector<unsigned char>& data) {
    uLong src_len = data.size();
    uLong dest_len = compressBound(src_len);
    std::vector<unsigned char> compressed(dest_len);
    
    if (compress(compressed.data(), &dest_len, data.data(), src_len) == Z_OK) {
        compressed.resize(dest_len);  // 실제 크기에 맞게 조정
    } else {
        std::cerr << "Compression failed!" << std::endl;
    }
    return compressed;
}

// Zlib 압축 해제 함수
std::vector<unsigned char> zlib_decompress(const std::vector<unsigned char>& data, uLong uncompressed_size) {
    std::vector<unsigned char> decompressed(uncompressed_size);
    
    if (uncompress(decompressed.data(), &uncompressed_size, data.data(), data.size()) != Z_OK) {
        std::cerr << "Decompression failed!" << std::endl;
    }
    return decompressed;
}

// 채널 압축 처리 함수 (스레드용)
void compress_channel(const cv::Mat& channel, std::vector<unsigned char>& compressed_output, std::mutex& mtx) {
    std::vector<unsigned char> channel_data(channel.data, channel.data + channel.total());  // 데이터 참조
    std::vector<unsigned char> compressed = zlib_compress(channel_data);
    
    // 결과 저장 (동기화)
    std::lock_guard<std::mutex> lock(mtx);
    compressed_output = compressed;
}

int main() {
    // 이미지 경로 설정
    std::string img_path = "../imgs/test1.bmp";
    
    // 이미지 로드
    cv::Mat image = cv::imread(img_path, cv::IMREAD_UNCHANGED);
    if (image.empty()) {
        std::cerr << "이미지를 불러올 수 없습니다." << std::endl;
        return -1;
    }
    
    // 원본 이미지 크기 계산
    size_t original_size = image.total() * image.elemSize();
    std::cout << "Original image size: " << original_size << " bytes" << std::endl;
    
    // 채널 분리
    std::vector<cv::Mat> channels(3);
    cv::split(image, channels);  // B, G, R 채널 분리
    
    // 압축 결과 저장 공간
    std::vector<std::vector<unsigned char>> compressed_channels(3);
    std::mutex mtx;  // 멀티스레딩 동기화

    // 스레드를 이용하여 병렬 압축
    std::vector<std::thread> threads;
    auto start = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < 3; ++i) {
        threads.emplace_back(compress_channel, std::ref(channels[i]), std::ref(compressed_channels[i]), std::ref(mtx));
    }
    
    // 스레드 종료 대기
    for (auto& th : threads) {
        th.join();
    }
    auto compressEnd = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed = compressEnd - start;
    std::cout << "Compressed speed: " << elapsed.count() << " seconds" << std::endl;

    // 압축된 데이터 크기 출력 및 총 크기 계산
    size_t total_compressed_size = 0;
    for (int i = 0; i < 3; ++i) {
        size_t compressed_size = compressed_channels[i].size();
        total_compressed_size += compressed_size;
        std::cout << "Channel " << i << " compressed size: " << compressed_size << " bytes" << std::endl;
    }

    // 압축률 계산
    double compression_ratio = (static_cast<double>(total_compressed_size) / original_size) * 100;
    std::cout << "Total compressed size: " << total_compressed_size << " bytes" << std::endl;
    std::cout << "Compression ratio: " << compression_ratio << "% of original size" << std::endl;

    return 0;
}
