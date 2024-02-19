# Meridium

Meridium is a computer performance application designed to help speed up your PC. It provides a range of features including cleaning temporary files, tweaking Windows registry, and more.\n

The application is divided into two parts: a desktop application and a web application, which communicate with each other using WebSockets. This was not necessary for the functionality of the application, but was done as a learning exercise to understand networking with WebSockets. The Desktop act isn't interactive whatsoever, and just serves as a websocket client and run's code in the background with a loop. The Web App, is a reactive website using NiceGUI! It sends messages to the desktop app with websockets in order to make changes to the computer. Super duper crazy right? A reminder once again that this was just a learning project!

![2r2332r2332](https://github.com/Justice219/meridium/assets/65798268/ef4ef41c-732e-446f-8772-de3860924d8c)
![jjjjj](https://github.com/Justice219/meridium/assets/65798268/84297b65-cefc-478d-a294-e3ab8761e01c)

## Features

- **File Cleaning**: Meridium can clean up temporary files from various applications such as browsers, Spotify, Discord, and Windows itself. This helps free up disk space and can improve system performance.

- **Windows Registry Tweaking**: Meridium can make changes to the Windows registry to help optimize system performance.

- **Performance Boost**: By cleaning up unnecessary files and tweaking system settings, Meridium can help speed up your PC.

## Project Structure

The project is divided into two main parts: the desktop application and the web application.

- The desktop application is located in the `desktop` directory. It includes the main application logic and system-level operations such as file cleaning and registry tweaking.

- The web application is located in the `web` directory. It provides a user interface for interacting with the desktop application.

## Installation
Before running the application, you need to install the required Python packages. You can do this by running the following command in your terminal:

```sh
pip install -r requirements.txt
```

## Running the Application

To run the application, you simply need to run the `main.py` script:

```sh
python main.py
```
![4t44434t](https://github.com/Justice219/meridium/assets/65798268/67e16823-c405-4556-b28c-7a5a8ea633dc)

This script starts both the desktop and web parts of the application.

## Contributing

Contributions to Meridium are welcome! Please read our contributing guidelines before submitting a pull request.

## License

Meridium is licensed under the MIT license. See the LICENSE file for more details.
