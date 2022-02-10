# Missing Parts Reconstruction Algorithm
There are two sets of depth images of the same size (116x120). They both represent different human faces. Images in test 
set have arbitrary distributed missing part. \
The repository contains a script that receives an image with missing data and outputs its
reconstructed representation.

# Train samples
![](dataset/train/person-2/frame11_dep.png) 
![](dataset/train/person-4/frame11_dep.png)
![](dataset/train/person-5/frame11_dep.png)
![](dataset/train/person-6/frame11_dep.png)
![](dataset/train/person-7/frame11_dep.png)

# Reconstruction results

|               Original image                |              Reconstructed using symmetry               |         Reconstructed using average image  <br/>and symmetry          |
|:-------------------------------------------:|:-------------------------------------------------------:|:---------------------------------------------------:|
| ![](dataset/test/person-17/frame11_dep.png) | ![](images_reconstructed/person-17/frame11_dep_sym.png) | ![](images_reconstructed/person-17/frame11_dep.png) |
| ![](dataset/test/person-18/frame11_dep.png) | ![](images_reconstructed/person-18/frame11_dep_sym.png) | ![](images_reconstructed/person-18/frame11_dep.png) |
| ![](dataset/test/person-19/frame11_dep.png) | ![](images_reconstructed/person-19/frame11_dep_sym.png) | ![](images_reconstructed/person-19/frame11_dep.png) |
| ![](dataset/test/person-20/frame11_dep.png) | ![](images_reconstructed/person-20/frame11_dep_sym.png) | ![](images_reconstructed/person-20/frame11_dep.png) |

# Requirements
- Ubuntu 18.04
- Python 3.7.4
- numpy 1.17.2
- pillow 6.2.0

# Installation
To install dependencies run the following command:

    pip install -r requirements.txt

# How to run
To create average image run

    python main.py train /path/to/trainfolder

To reconstruct images in test folder run and store results in /path/out folder run:

    python main.py test /path/to/testfolder --out=/path/out

# Algorithm description
When train is launched, an average image is created in the following way. At the first iteration, the average image 
equals to the first image(or the first batch). By default, batch size equals to 1
Next, the intersection area between the current and the average image is taken and average pixel values between 
current(or batch) and average image are calculated for each image in dataset.

When inferencing, the algorithm tries to replace white areas. For each such pixel symmetrical to vertical image line pixel
value is used if it is not white otherwise value from an average image.

#Limitations
- In case an image to reconstruct is wider than an average image and the missing area is in that place, hollows may 
appear (shown in reconstruction example)