<a id="readme-top"></a>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <h1>🏸 Badminton Swing Analyzer</h1>

  <p align="center">
    A Python-based computer vision tool that uses OpenCV and Google's MediaPipe to analyze and improve your badminton swing form.
    <br />
    <a href="#usage"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="[https://github.com/your_github_username/Badminton-Swing-Analyzer/issues/new?labels=bug&template=bug-report---.md](https://github.com/your_github_username/Badminton-Swing-Analyzer/issues/new?labels=bug&template=bug-report---.md)">Report Bug</a>
    &middot;
    <a href="[https://github.com/your_github_username/Badminton-Swing-Analyzer/issues/new?labels=enhancement&template=feature-request---.md](https://github.com/your_github_username/Badminton-Swing-Analyzer/issues/new?labels=enhancement&template=feature-request---.md)">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
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
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

This script tracks a player's body mechanics during a badminton swing to provide instant feedback on their technique. It analyzes key biomechanical markers to determine if you are maximizing your power and reach.

**Key Features:**
*   **Handedness Support:** Works for both left-handed and right-handed players.
*   **Contact Point Analysis:** Measures the angles of your wrist, elbow, and shoulder to ensure you are hitting the shuttlecock at the optimal height.
*   **Elbow Positioning:** Checks if your elbow is properly elevated and facing the ceiling during the swing phase.
*   **Body Rotation Check:** Tracks shoulder and hip widths to verify you are rotating your body fully through the shot.
*   **Visual Feedback:** Maps a digital skeleton directly onto your video, highlighting key joints with red dots and blue lines.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

* [Python](https://www.python.org/)
* [OpenCV](https://opencv.org/)
* [MediaPipe](https://developers.google.com/mediapipe)
* [NumPy](https://numpy.org/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running, follow these simple steps.

### Prerequisites

You will need Python installed on your computer. Install the required libraries using pip:

```sh
pip install opencv-python mediapipe numpy
