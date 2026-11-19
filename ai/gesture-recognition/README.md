# AI Gesture Recognition

A lightweight CNN for recognizing hand-drawn gestures in a mind-mapping application.

## Goal

Allow users to access tools by drawing shapes on the canvas instead of navigating through multiple buttons.

## Why a Neural Network?

Direct template matching can require comparing a drawing against many reference shapes.

A trained CNN instead predicts the shape class in a single forward pass, without checking each stored example individually.

## Supported Shapes

- Triangle
- Circle
- Rectangle / Square
- Equal (=)
- Not Equal (≠)

## Architecture

- Input: 32×32 grayscale
- Conv2D: 16 filters, 3×3
- ReLU + MaxPool
- Conv2D: 32 filters, 3×3
- ReLU + MaxPool
- Fully connected layer: 32 neurons
- Output: 5 classes

## Results

Test accuracy: 99.64% on held-out synthetic drawings.

Performance on real handwritten gestures has not yet been measured.

## Trade-off

The current classifier supports a fixed set of shapes. Adding a new class requires updating and retraining or fine-tuning the network.

A future version may support user-defined gestures without full retraining.

## Training

Run:

    python train.py

Then evaluate:

    python evaluate.py

The training images are expected in `data/training/`, grouped by shape.
