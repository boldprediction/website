For the memcache to work, Here is the list of packages to be installed -
1. memcached ( MAC OS : Homebrew : brew install memcached / Linux : apt-get install memcached)
2. pymemcache ( pip install pymemcache)

run the memcache by running the following command 
$ memcached& ( To run it in the background : Linux)
$ brew services start memcached ( To run it in the background : MACOS)


Note : memcache runs on port 11211 (default). To change the port, refer to the documentation of memcache.