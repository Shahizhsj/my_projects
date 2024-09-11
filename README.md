# Deep Learning Projects

Welcome to my repository! Here you'll find a collection of my deep learning projects, each showcasing different applications and techniques in the field of artificial intelligence. Explore the descriptions below to get an insight into what each project entails.

## 🚀 **Satellite Image Description**
**Description:** This project involves developing a model to automatically describe satellite images. By leveraging advanced computer vision techniques, the model generates detailed textual descriptions of the content within satellite imagery, which can be useful for various applications such as geographic analysis and disaster management.

**Key Features:**
- Utilizes state-of-the-art image captioning models
- Trains on a diverse dataset of satellite images
- Evaluates model performance with various metrics

**Notebook:** [Satellite_image_description.ipynb](Satellite_image_description.ipynb)

---

## 🚗 **Vehicle Detection**
**Description:** In this project, a vehicle detection system is built to identify and locate vehicles in images or video frames. This is achieved using object detection algorithms which can be applied to enhance traffic monitoring systems, autonomous driving, and other vehicular surveillance applications.

**Key Features:**
- Implements object detection models such as YOLO or SSD
- Uses annotated datasets for training
- Achieves real-time vehicle detection and localization

**Notebook:** [Vechinle_detection.ipynb](Vechinle_detection.ipynb)

---

## 🐱🐶 **Cat vs Dog Classification**
**Description:** This project focuses on building a binary classification model to distinguish between images of cats and dogs. Utilizing Convolutional Neural Networks (CNNs), the model classifies images into one of the two categories with high accuracy.

**Key Features:**
- Implements CNN architectures for image classification
- Trains on the popular Cats vs Dogs dataset
- Achieves high classification accuracy and efficiency

**Notebook:** [cat_vs_dog.ipynb](cat_vs_dog.ipynb)

---

## 🎨 **Digit Generation using GANs**
**Description:** This project explores the generation of handwritten digits using Generative Adversarial Networks (GANs). By training a GAN on the MNIST dataset, the model learns to generate new digits that resemble the handwritten samples in the dataset.

**Key Features:**
- Uses GANs to generate new image samples
- Demonstrates the capabilities of GANs in generating realistic images
- Evaluates the quality of generated digits

**Notebook:** [digit-generation-using-gan-s.ipynb](digit-generation-using-gan-s.ipynb)

---

## 🧑‍🔬 **Face Detection**
**Description:** This project involves creating a model to detect and recognize faces in images. The model uses advanced techniques in facial recognition and object detection to identify and locate faces with high precision.

**Key Features:**
- Implements face detection algorithms such as Haar Cascades or MTCNN
- Trains on a dataset of facial images
- Provides real-time face detection capabilities

**Notebook:** [face_detection.ipynb](face_detection.ipynb)

---

## 🖼️ **Image Segmentation**
**Description:** This project focuses on segmenting different regions of interest within images. Using techniques like U-Net or Mask R-CNN, the model segments images into various classes, which can be applied to medical imaging, autonomous driving, and more.

**Key Features:**
- Uses segmentation algorithms for detailed image analysis
- Trains on annotated datasets for accurate segmentation
- Evaluates segmentation performance with standard metrics

**Notebook:** [image_segmentation.ipynb](image_segmentation.ipynb)

---

## 🚀 **YOLO Inference**
**Description:** This project involves applying the YOLO (You Only Look Once) object detection algorithm to perform real-time inference on images or video streams. YOLO is known for its speed and accuracy in detecting multiple objects within a single frame.

**Key Features:**
- Implements YOLO for object detection and localization
- Demonstrates real-time detection capabilities
- Uses pre-trained YOLO models for inference

**Video:** [inference_yolo.avi](inference_yolo.avi)

---

## 😷 **Mask Detection**
**Description:** This project focuses on detecting whether individuals are wearing masks correctly or not. The model is trained to classify images into categories such as 'With Mask,' 'Without Mask,' and 'Mask Worn Incorrectly,' which can be useful for health and safety applications.

**Key Features:**
- Utilizes object detection techniques to identify mask usage
- Trains on a dataset with mask-related annotations
- Provides actionable insights for mask compliance

**Notebook:** [mask_detection.ipynb](mask_detection.ipynb)

---

## 🤟 **Sign Language Detection**
**Description:** This project aims to recognize and interpret sign language gestures from images or video streams. By training a model on a dataset of sign language gestures, it can identify and translate gestures into text or speech.

**Key Features:**
- Implements gesture recognition algorithms
- Trains on sign language datasets
- Provides real-time gesture interpretation

**Notebook:** [sign_language_detection.ipynb](sign_language_detection.ipynb)

# Web Scraping for Mobile Comparison

This project leverages Selenium for web scraping and Gradio for creating a user-friendly interface to compare mobile phones' specifications and reviews. 

## Project Overview

The script uses Selenium to automate interactions with the **MySmartPrice** website, extracting detailed information about mobile phones. Gradio provides a simple interface for users to enter mobile models and view the collected data.

## Features

- **Search Functionality:** Automated search for mobile models on MySmartPrice.
- **Specification Extraction:** Retrieves and displays specifications of the selected mobile model.
- **Review Extraction:** Collects additional review details about the mobile phone.
- **Comparison Interface:** Allows users to compare multiple mobile models via a web interface.

## How It Works

1. **Web Scraping:** Utilizes Selenium to navigate the MySmartPrice website, perform searches, and extract product details.
2. **User Input:** Gradio interface enables users to input mobile model names for comparison.
3. **Multi-threading:** Concurrently fetches data for multiple models to improve efficiency.

## Technologies Used

- **Python:** Main programming language.
- **Selenium:** For web scraping and automation.
- **Gradio:** For building the web interface.
- **Concurrent Futures:** To handle asynchronous tasks.

## Usage

1. **Run the Script:** Execute the `web_scraping.py` file to start the application.
2. **Input Mobile Models:** Enter the mobile model names in the provided text boxes.
3. **Compare Models:** Click the "Compare!" button to view specifications and reviews.

**Code:** [web_scrapping.py](web_scrapping.py)
