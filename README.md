# EUI-64 and Privacy Extension DEMO

## About

This is a little GitHub-Repository explaining how the eui-64 method and privacy-extentions work in IPv6. If you're german you can use the german-readme-files in `/README_DE` if you don't want to read the english readme-files. The explanation for each method is described in the respective folder.

## Test EUI64 And Privacy-Extentions

If you want to know how the theory works in practice I provided two python files. One for eui-64 method and one for privacy extensions. Feel free to use them as you like. Please read on if you want to execute the python files.

### Requirements For Provided Python-Files

If you want to execute the provided python files you need to have python 3 installed on your machine. If you're not familiar with installing python you can find plenty of tutorials in the web.

In addition you need the python module [get-mac](https://pypi.org/project/get-mac/). This module is used to get the mac-address of your machine. Don't worry nothing nasty is going to happen. Your mac-address is needed in order to create the (theoratical) eui-64 address or privacy-extensions.

**Please keep in mind** that you might need to replace the `interface` in each python file in order to get them to work. The line where you might need to replace the interface is described as `get_mac_address(interface='xxx')` where `xxx` resembles your interface. If you don't know which interface to pick, issue the `ipconfig` command in a windows cmd or `ifconfig` if you're on linux and copy the name of your adapter and place it in the brackets of `interface='your-interface-goes-here'`.