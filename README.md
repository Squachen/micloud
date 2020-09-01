
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



<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
* [Usage](#usage)
* [Roadmap](#roadmap)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)
* [Acknowledgements](#acknowledgements)


## About The Project

Simple implementation for logging in to your Xiaomi cloud account.
This is a very early release where you can fetch device information.

I’m new to python so the code quality might be poor until I get up to speed with standards and common practices.

<!-- USAGE EXAMPLES -->
## Usage

How to get and use micloud.

###  Getting it

To download micloud, either fork this github repo or use Pypi via pip.
```sh
$ pip install micloud
```

### Using it

As of right now there's not much you can do. You can login and get device info from Xiaomi cloud:

```Python
from micloud import MiCloud

mc = MiCloud(o"USERNAME", "PASSWORD")
mc.login()
token = mc.get_token() # to get your cloud service token.
device_list = mc.get_devices() # get list of devices
```

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

Sammy Svensson - [@@S_Svensson](https://twitter.com/@S_Svensson) - sammy@ssvensson.se

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
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/Squachen
[product-screenshot]: images/screenshot.png
