
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
<!--[![LinkedIn][linkedin-shield]][linkedin-url]-->



<!-- PROJECT LOGO -->
<br />
<p align="center">
  <h3 align="center">MiCloud</h3>

  <p align="center">
    Library for connecting to xiaomi cloud.
    <br />
    <br />
    <a href="https://github.com/Squachen/micloud/issues">Report Bug</a>
    ·
    <a href="https://github.com/Squachen/micloud/issues">Request Feature</a>
  </p>
</p>


## About The Project

Simple implementation for logging in to your Xiaomi cloud account and fetch device information.


<!-- USAGE EXAMPLES -->
## Usage

How to get and use micloud.

###  Getting it

To download micloud, either fork this github repo or use Pypi via pip.
```sh
$ pip install micloud
```

### Using it
You can use micloud in your project or directly from the terminal.
#### In terminal:
```
Usage: micloud [OPTIONS]

Options:
  -u, --username TEXT  Your Xiaomi username.
  -c, --country TEXT   Language code of the server to query. Default: "de"
  --pretty             Pretty print json output.
  --help               Show this message and exit.
```
<img src="https://raw.githubusercontent.com/Squachen/micloud/master/docs/cli_example1.png" width="500">

#### In code:
As of right now there's not much you can do. You can login and get device info from Xiaomi cloud:
```Python
from micloud import MiCloud

mc = MiCloud("USERNAME", "PASSWORD")
mc.login()
token = mc.get_token() # to get your cloud service token.
device_list = mc.get_devices() # get list of devices
```
To query a different server, use the country argument:
```Python
device_list = mc.get_devices(country="cn")
```
And to save the device list as json:
```Python
mc.get_devices(country="cn", save=True, file="devices.json")
```

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

Sammy Svensson - [@S_Svensson](https://twitter.com/@S_Svensson) - sammy@ssvensson.se

Project Link: [https://github.com/squachen/micloud](https://github.com/squachen/micloud)




<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/squachen/micloud.svg?style=flat-square
[contributors-url]: https://github.com/squachen/micloud/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Squachen/micloud.svg?style=flat-square
[forks-url]: https://github.com/squachen/micloud/network/members
[stars-shield]: https://img.shields.io/github/stars/squachen/micloud.svg?style=flat-square
[stars-url]: https://github.com/squachen/micloud/stargazers
[issues-shield]: https://img.shields.io/github/issues/squachen/micloud.svg?style=flat-square
[issues-url]: https://github.com/squachen/micloud/issues
[license-shield]: https://img.shields.io/github/license/squachen/micloud.svg?style=flat-square
[license-url]: https://github.com/squachen/micloud/blob/master/LICENSE.txt

