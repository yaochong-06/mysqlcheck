# linux build scripts
rm -rf dist/
rm -rf build/
pyinstaller linux.spec
cp README.md /root/mysqlcheck/dist
cd dist/ && tar -cvf mysqlcheck.tar main README.md
rm -rf /root/mysqlcheck/build/
mv /root/mysqlcheck/dist/mysqlcheck.tar /root
rm -rf /root/main
mv /root/mysqlcheck/dist/main /root
rm -rf /root/mysqlcheck/dist/