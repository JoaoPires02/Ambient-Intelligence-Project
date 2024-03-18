# Smart Classroom

Although typical classrooms already provide enough for better education, it is very possible to improve them even further by minimalizing any possible distractions, saving time in any non education related things and improving quality of study. With this, our solution is able to fulfill these aspects through the beauty of automation.

Within this file, you will find the general idea behind this project, as well as the full design and components that give the functionalities we want. After it, you can find the needed software requirements coupled with the instructions for installation and deployment.

## General Information

This project aims to reduce the time wasting actions through ways of automation, holding functionalities such as: automation in changing the environment aspects of the classroom, automatic filling of the attendance sheet for the teacher, the student's ability to give feedback and vote for environment changes and finally giving "admin" access to the teacher so they are able to change any of environment factors to their liking (being these last two supported by a web application).

## Built With

### Hardware

* [Raspberry Pi 4 Model B](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/) - 1 unit - Development board for the actuators used
* [Arduino Starter Kit](https://store.arduino.cc/products/arduino-starter-kit-multi-language) - 1 unit - which contains various needed sensors and the development board for them
    * [Arduino Uno]() - 1 unit - development board for the sensors
    * [Alphanumeric LCD]() - 1 unit - displays real, simulated and ideal temperature
    * [Yellow LED]() - 6 units - shows the behavior of the classroom lights
    * [Red LED]() - 1 unit - shows the behavior of the projector
    * [Temperature Sensor]() - 2 units - captures the real temperature
    * [Phototransistor]() - 3 units - captures the ambience lighting
    * [Pushbuttons]() - 4 units - to show the location of a seated student

### Software

* [Raspberry Pi OS](https://www.raspberrypi.com/software/) - Operating system
    * [GPIO]() - Library
* [Python](https://www.python.org/) - Programming Language
    * [Flask]() - Library
* [Arduino/C++](https://www.arduino.cc/en/software) - Programming Language and Platform
* [HTML/CSS/Javascript]() - Programming Language behind the application

## Getting Started

### Assembly Instructions

(TO DO)

Describe step-by-step assembly instructions (montar circuito).

When necessary, and especially when wiring is involved, include diagrams/photos.

### Software Prerequisites

(TO DO)

In this section include detailed instructions for installing additional software the application is dependent upon (such as PostgreSQL database, for example).

```
installation command
```

### Installation

(TO DO)

Give step-by-step instructions on building and running the application on the testing environment. 

Describe the step.

```
Give the command example
```

And repeat.

```
until finished
```

You can also add screenshots to show expected results, when relevant.

## Demo

(TO DO)

Give a tour of the best features of the application.
Add screenshots when relevant.

## Deployment

(TO DO)

Add additional notes about how to deploy this on a host or a cloud provider.

Mention virtualization/container tools and commands.

```
Give an example command
```

Provide instructions for connecting to servers and tell clients how to obtain necessary permissions.

## Additional Information

### Authors

* **João Pires** - *Controller/Parser* - [JoaoPires02](https://github.com/JoaoPires02)

* **Marco Castro** - *Controller/Parser* - [MarcoCastro0406](https://github.com/MarcoCastro0406)

* **Miguel Gago** - *FrontEnd* - [miguelgago13](https://github.com/miguelgago13)

### Versioning

We use [SemVer](http://semver.org/) for versioning. 
For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

### License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

### Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.