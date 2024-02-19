# Meridium 1.1

Meridium is an innovative computer performance application designed to optimize and speed up your PC. Leveraging a suite of tools for cleaning temporary files, tweaking Windows registry settings, and more, Meridium stands out with its unique architecture. It comprises a desktop application and a web application that communicate via WebSockets—a design choice made to explore networking concepts. Although this dual-part setup isn't necessary for the core functionality, it adds a fascinating layer of complexity and learning to the project.

**Note** - Requires A Windows Computer! This should be assumed though

![2r2332r2332](https://github.com/Justice219/meridium/assets/65798268/ef4ef41c-732e-446f-8772-de3860924d8c)
![jjjjj](https://github.com/Justice219/meridium/assets/65798268/84297b65-cefc-478d-a294-e3ab8761e01c)

## Key Features

- **File Cleaning**: Effortlessly removes temporary files from browsers, Spotify, Discord, and Windows, freeing up valuable disk space and enhancing system performance.
- **Windows Registry Tweaking**: Optimizes system performance through strategic modifications to the Windows registry.
- **Performance Boost**: Achieves a faster PC by eliminating unnecessary files and adjusting system settings for optimal operation.

## Project Overview

Meridium is divided into two interconnected parts:

- **Desktop Application**: Acts as a WebSocket client, running non-interactive background processes.
- **Web Application**: A dynamic NiceGUI-powered interface that communicates with the desktop application to execute system modifications.

### Desktop Directory

Contains the core application logic, including file cleaning and registry tweaking functionalities.

### Web Directory

Houses the user interface for managing and interacting with the desktop application's features.

## Getting Started

### Installation

Prepare your environment by installing the required Python packages:

```sh
pip install -r requirements.txt
```

### Running Meridium

Launch the application with the following command:

```sh
python main.py
```
![4t44434t](https://github.com/Justice219/meridium/assets/65798268/eb857efe-d2e5-4389-b6e8-700f9fd427ec)

This command initiates both the desktop and web components, enabling full application functionality.

## Contributing to Meridium

We welcome contributions! If you're interested in improving Meridium, please consult our contributing guidelines before submitting a pull request.

## License

Meridium is open-sourced under the MIT license, fostering innovation and collaboration. For more details, refer to the LICENSE file.
