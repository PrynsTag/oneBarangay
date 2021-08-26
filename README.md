[![Issues][issues-shield]][issues-url]
[![Apache License][license-shield]][license-url]
[![Circle CI][ci-shield]][ci-url]
[![Coveralls][coverage-shield]][coverage-url]
[![Codacy][codacy-shield]][codacy-url]
[![Requires][requires-shield]][requires-url]
[![Deep Source][deepsource-shield]][deepsource-url]
[![Deep Source][deepsource-resolved-shield]][deepsource-resolved-url]
[![Black][black-shield]][black-url]
[![Isort][isort-shield]][isort-url]

<!-- PROJECT LOGO -->
<br />
<p align="center">
   <a href="#">
    <img src="https://storage.googleapis.com/onebarangay-media/alpha-logo-red.png" alt="Logo">
  </a>

  <h3 align="center">oneBarangay</h3>

  <p align="center">
    An e-Government System for Online Transaction Processing
    <br />
    through Web and Mobile Application with Implementation of OCR Technologies
    <br />
    <a href="#"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="#">View Demo</a>
    ·
    <a href="https://github.com/PrynsTag/oneBarangay/issues">Report Bug</a>
    ·
    <a href="https://github.com/PrynsTag/oneBarangay/issues">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#application-installation">Application Installation</a></li>
        <li>
            <a href="#tools-installation">Tools Installation</a>
            <ol>
               <li><a href="#pre-commit">Pre-commit</a></li>
               <li><a href="#circleci">CircleCI</a></li>
               <li><a href="#gitkraken">GitKraken</a></li>
               <li><a href="#codacy-sentry.io-Deepsource">Codacy, Sentry.io, Deepsource</a></li>
            </ol>
        </li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://example.com)

The manual way of processing transactions in the barangay is still prevalent today. Filling
out necessary records by using pen and paper that are stored in log books and folders in the
barangay. There are records which have been distorted, some records are incomplete and there
has been a loss of data.

Web application systems and mobile applications have helped in the tasks that we
perform on a daily basis. These applications assisted us to make our lives easier in making
transactions. With the emergence of technology in the Philippines, the proposed system, which is
the oneBarangay system, will handle the main office of the barangay to provide a systematic,
efficient, and technological way of handling online document issuing and more secure data.

### Built With

* [Bootstrap](https://getbootstrap.com)
* [Django](https://www.djangoproject.com/)
* [Firebase](https://firebase.google.com/)
* [Google Cloud Platform](https://console.cloud.google.com/)



<!-- GETTING STARTED -->
## Getting Started

The steps are organized to `Run`, `Develop` and `Test` the application.
Make sure you followed the installation steps properly before asking for help.

### Prerequisites

There are two things you need to have in order to run this project:
1. Python 3.9.*
2. Pip 21.1.*

### Application Installation

1. Clone the repo
   ```sh
   git clone https://github.com/your_username_/Project-Name.git
   ```
2. Go to the project directory
3. Create and activate a virtual environment (venv)
4. Install PIP packages
   ```sh
   pip install -r requirements.txt
   ```
5. Copy the environment variables [here](https://console.cloud.google.com/security/secret-manager/secret/oneBarangay-ENV-Variables/versions?project=onebarangay-malanday)
6. Create an `.env` File and paste the values in step 3
7. In local-settings.py, change this line:
    ```sh
    decodedBytes = base64.b64decode("<your-env-value>")
    ```
   To the value of `GOOGLE_STORAGE_CREDENTIALS` in the .env file.

8. Lastly, run `./manage.py runserver` to run the application.

<!-- USAGE EXAMPLES -->
## Tools Installation

Before pushing to the develop branch, always test the code locally. 
In order for this to happen, a set of tools are available for you.

### a. Pre-commit
After you have coded the business logic, run pre-commit in the project root using the code below:
```sh
pre-commit run --all-files
```
And then fix any issues that might occur.

### b. CircleCI
Another tool is also available to automatically test and deploy the application in just one push
using the CI/CD tool known as `CircleCI`.

To run it locally, install the CLI using the steps quoted in the 
[CircleCI Docs](https://circleci.com/docs/2.0/local-cli/).

#### Install with Snap (Linux)
```sh
sudo snap install docker circleci
sudo snap connect circleci:docker docker
```

#### Install with Homebrew (macOS)

```sh
brew install circleci
```

#### Install with Chocolatey (Windows)
For Windows users, we provide a Chocolatey package:

```sh
choco install circleci-cli -y
```

#### Updating the CLI
```sh
circleci update
```

#### Configuring the CLI
Before using the CLI you need to generate a CircleCI API Token from the Personal API Token tab. After you get your token, configure the CLI by running:
```sh
circleci setup
```
The set-up process will prompt you for configuration settings. Use the default CircleCI Host.

#### Validate a CircleCI config
You can avoid pushing additional commits to test your config.yml by using the CLI to validate your config locally.

```sh
circleci config validate
# Config file at .circleci/config.yml is valid
```

_For more detailed explanation, please refer to the [CircleCI Documentation](https://circleci.com/docs/2.0/local-cli/)_

#### Running the Local CLI

After the set-up, there are two things you need to test using CircleCI, the `test` and `build` job.
1. To do this use the code below to run the `test` job:
```sh
circleci local execute -c local-process.yml -e GOOGLE_PROJECT_ID=<the-env-value> -e GOOGLE_COMPUTE_ZONE=<the-env-value> -e GS_BUCKET_NAME=<the-env-value> -e DJANGO_SECRET_KEY=<the-env-value> -e DJANGO_SETTINGS_MODULE=<the-env-value> -e DOCKERHUB_USERNAME=<your-docker-username> -e DOCKERHUB_PASSWORD=<your-docker-username> -e CLOUD_STORAGE_KEY=<the-env-value> -e GCLOUD_AUTH_KEY=<the-env-value> -e  --job test
```
> **_Note_**: Replace the `<the-env-value>` and `<your-docker-credentials>` with the actual value without quotations.

> **_Note_**: You can get your `DOCKER_USERNAME` and `DOCKER_PASSWORD` in [Docker Hub](https://hub.docker.com/).
> All the other values are available in `.env` file mentioned above.

2. Fix any issues that might occur before proceeding. 

3. After that, repeat the steps on Running the Local CLI but this time, change the code at the end from `--job test` to `--job build`
4. Repeat the process until you don't see the error.

#### c. GitKraken
To lessen the git problems when working on the project, use `GitKraken` as a Git UI.

#### d. Codacy Sentry.io Deepsource
For Error Tracking and Static Code Analyzers, 
use [Codacy](https://codacy.com), [Sentry.io](http://sentry.io/) and [Deepsource](https://deepsource.io/)
> **_Note_**: You can use Sentry.io to keep track of unexpected errors in **Production**.
> >> **_Note_**: Create an account first using your **_Student GitHub_** account and notify the Project Repo Admin to be invited in these tools.

<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/PrynsTag/oneBarangay/issues) for a list of proposed features (and known issues).

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. 
Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<!-- LICENSE -->
## License

Distributed under the Apache 2.0 License. See `LICENSE` for more information.

<!-- CONTACT -->
## Contact

Prince Velasco - [LinkedIn](www.linkedin.com/in/princevelasco) - princevelasco16@gmail.com

Project Link: [https://github.com/PrynsTag/oneBarangay](https://github.com/PrynsTag/oneBarangay)

<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements
* [Img Shields](https://shields.io)
* [Choose an Open Source License](https://choosealicense.com)
* [Font Awesome](https://fontawesome.com)
* [CircleCI](https://circleci.com/)
* [Codacy](https://www.codacy.com/)
* [DeepSource](https://deepsource.io/)
* [Sentry.io](https://sentry.io/)
* [Browserstack](https://www.browserstack.com/)
* [Black Code Style](https://github.com/psf/black)
* [Pre-commit](https://pre-commit.com/)
* [Coveralls](http://coveralls.io/)
* [isort](https://pycqa.github.io/isort/)

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues

[license-shield]: https://img.shields.io/github/license/prynstag/oneBarangay?style=for-the-badge
[license-url]: https://github.com/PrynsTag/oneBarangay/blob/develop/LICENSE

[ci-shield]: https://img.shields.io/circleci/build/github/PrynsTag/oneBarangay/develop?label=CircleCI&style=for-the-badge
[ci-url]: https://circleci.com/gh/PrynsTag/oneBarangay/tree/develop

[coverage-shield]: https://img.shields.io/coveralls/github/PrynsTag/oneBarangay?label=Coveralls&style=for-the-badge
[coverage-url]: https://coveralls.io/github/PrynsTag/oneBarangay?branch=develop

[codacy-shield]: https://img.shields.io/codacy/grade/7a9e9a1402a14005ae4a14b5cffdb1ee?label=Codacy&style=for-the-badge
[codacy-url]: https://www.codacy.com/gh/PrynsTag/oneBarangay/dashboard?utm_source=github.com&utm_medium=referral&utm_content=PrynsTag/oneBarangay&utm_campaign=Badge_Grade

[requires-shield]: https://img.shields.io/requires/github/PrynsTag/oneBarangay/develop?style=for-the-badge
[requires-url]: https://requires.io/github/PrynsTag/oneBarangay/requirements/?branch=develop

[deepsource-shield]: https://deepsource.io/gh/PrynsTag/oneBarangay.svg/?label=active+issues&token=QI2m-XNk586t3GYXw6YhzOn6
[deepsource-url]: https://deepsource.io/gh/PrynsTag/oneBarangay/?ref=repository-badge

[deepsource-resolved-shield]: https://deepsource.io/gh/PrynsTag/oneBarangay.svg/?label=resolved+issues&token=QI2m-XNk586t3GYXw6YhzOn6
[deepsource-resolved-url]: https://deepsource.io/gh/PrynsTag/oneBarangay/?ref=repository-badge

[black-shield]: https://img.shields.io/badge/code%20style-black-000000.svg
[black-url]: https://github.com/psf/black

[isort-shield]: https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336
[isort-url]: https://pycqa.github.io/isort/

[product-screenshot]: https://storage.googleapis.com/onebarangay-media/scan-document.png
