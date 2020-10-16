# Hex Lang by Alexander Abraham
# licensed under the MIT license

cd ../sample
hex --help
hex --version
hex --verbose example.hex
hex --lint example.hex
hex --cpp example.hex
ls
file example.cpp
rm -rf *.cpp
hex --bin example.hex
ls
file example.bin
rm -rf *.bin
rm -rf *.cpp
hex --bin example.hex --static
ls
file example.bin
rm -rf *.bin
rm -rf *.cpp
