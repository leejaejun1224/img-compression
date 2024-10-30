#include <opencv2/opencv.hpp>
#include <iostream>
#include <zstd.h>  
#include <thread>
#include <vector>
#include <mutex>
#include <chrono>

std::vector<unsigned char> zstd_compress(const std::vector<unsigned char>& data) {
    size_t src_len = data.size();
    size_t dest_len = ZSTD_compressBound(src_len);  
    std::vector<unsigned char> compressed(dest_len);
    
    size_t compressed_size = ZSTD_compress(compressed.data(), dest_len, data.data(), src_len, 5); 
    if (ZSTD_isError(compressed_size)) {
        std::cerr << "Compression failed: " << ZSTD_getErrorName(compressed_size) << std::endl;
    } else {
        compressed.resize(compressed_size); 
    }
    return compressed;
}

std::vector<unsigned char> zstd_decompress(const std::vector<unsigned char>& data, size_t uncompressed_size) {
    std::vector<unsigned char> decompressed(uncompressed_size);
    
    size_t decompressed_size = ZSTD_decompress(decompressed.data(), uncompressed_size, data.data(), data.size());
    if (ZSTD_isError(decompressed_size)) {
        std::cerr << "Decompression failed: " << ZSTD_getErrorName(decompressed_size) << std::endl;
    }
    return decompressed;
}

void compress_channel(const cv::Mat& channel, std::vector<unsigned char>& compressed_output, std::mutex& mtx) {
    std::vector<unsigned char> channel_data(channel.data, channel.data + channel.total());  
    std::vector<unsigned char> compressed = zstd_compress(channel_data);
    
    std::lock_guard<std::mutex> lock(mtx);
    compressed_output = compressed;
}

int main() {
    std::string img_path = "../imgs/test1.bmp";
    
    cv::Mat image = cv::imread(img_path, cv::IMREAD_UNCHANGED);
    if (image.empty()) {
        std::cerr << "이미지를 불러올 수 없습니다." << std::endl;
        return -1;
    }
    
    size_t original_size = image.total() * image.elemSize();
    std::cout << "Original image size: " << original_size << " bytes" << std::endl;
    
    std::vector<cv::Mat> channels(3);
    cv::split(image, channels); 
    
    std::vector<std::vector<unsigned char>> compressed_channels(3);
    std::mutex mtx;  

    std::vector<std::thread> threads;
    auto start = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < 3; ++i) {
        threads.emplace_back(compress_channel, std::ref(channels[i]), std::ref(compressed_channels[i]), std::ref(mtx));
    }
    
    for (auto& th : threads) {
        th.join();
    }
    auto compressEnd = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed = compressEnd - start;
    std::cout << "Compressed speed: " << elapsed.count() << " seconds" << std::endl;

    size_t total_compressed_size = 0;
    for (int i = 0; i < 3; ++i) {
        size_t compressed_size = compressed_channels[i].size();
        total_compressed_size += compressed_size;
        std::cout << "Channel " << i << " compressed size: " << compressed_size << " bytes" << std::endl;
    }

    double compression_ratio = (static_cast<double>(total_compressed_size) / original_size) * 100;
    std::cout << "Total compressed size: " << total_compressed_size << " bytes" << std::endl;
    std::cout << "Compression ratio: " << compression_ratio << "% of original size" << std::endl;

    return 0;
}
