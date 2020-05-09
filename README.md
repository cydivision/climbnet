# CLIMBNET - 🧗🏻‍♂️CNN for detecting + segmenting indoor climbing holds

<img src="https://user-images.githubusercontent.com/3492780/81486875-9df4e280-921d-11ea-8a5b-56d67c93f49f.png" alt="result" width="75%" height="75%"/>

## Overview

Climbnet is a CCN that detects holds on climbing gym walls and returns the appropriate boundary mask for use in instance segmentation.

## Categories

`HOLD` - Includes holds as well as the large shaped volumes.

<img src="https://user-images.githubusercontent.com/3492780/81486871-9d5c4c00-921d-11ea-9dce-a7c1eae0d317.jpg" alt="holds" width="25%"/> <img src="https://user-images.githubusercontent.com/3492780/81486872-9df4e280-921d-11ea-83c0-d824e8ac1d1d.png" alt="shaped volumes" width="25%"/>

`VOLUME` - This refers to any and all box volumes.

> They are usually made of wood, triangular in shape, and often have bolt holes so that holds can be mounted on them. Sometimes they are themselves a hold or specific to a particular route as opposed to being just another part of the wall.

<!-- <img src="./images/volumes_1.png" alt="result" width="25%"/>  -->
<img src="https://user-images.githubusercontent.com/3492780/81486880-9f260f80-921d-11ea-97f8-68c8cb90541f.png" alt="volumes" width="25%%"/>

| Category | Total |
| -------- | :---: |
| Hold     | 7307  |
| Volume   |  520  |

## Model

This project uses Facebook's [detectron2](https://github.com/facebookresearch/detectron2) implmentation of [Mask R-CNN](https://github.com/facebookresearch/detectron2/blob/master/configs/COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml) and was trained using `210` images.

The weights are available for download using the following link.

📁 [google drive](https://drive.google.com/drive/folders/1MMd7vu9b6XbNrVTxLZ_uehNue5ZBPgnL?usp=sharing)

## Installation

There are two ways to run the model.  

### Method 1  
   
Use the `demo.py` file provided with this project.    

Install the required dependencies
```
# python 3.6+ 
pip install -r requirements.txt
```

Run the demo
```
cd test
python demo.py demo_image1.jpg <path_to_model_weights>
```

#### Method 2

Follow the steps outlined in the detectron2 [getting started guide](https://github.com/facebookresearch/detectron2/blob/master/GETTING_STARTED.md). Replace the model weights with those from this project.  
> Classes returned during inference will be incorrect. Instead of `Holds` and `Volumes` you will instead see classes from the `COCO` dataset.

```
python demo.py --config-file ../configs/COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml \
  --input input1.jpg input2.jpg \
  [--other-options]
  --opts MODEL.WEIGHTS <climbnet weights>
```

## Issues

#### 📷 Imagery

Most of the imagery used was sourced from the internet. As a result of that, many of the images have already had compression or filters applied to them and are rather small in size, usually `1280x1280` or smaller.

A lot of the imagery was taken from the same vantage point (directly facing the wall), which may lead to issues when running inference on imagery with different vantage points(sport climbs) or extremely sloped walls.

#### 🦥 Model Size, Inference Time

One of the downsides of using `detectron2` is that the size of the available networks+weights are very large. The inference time is also not very fast, especially when using a `cpu`. 

#### 🤿 Segmented Polygons

There are some segmented polygons in the data which affect the inference accuracy. They exist because the program that I used for tagging [Hyperlabel](https://hyperlabel.com) does not support grouping as per the `COCO` specification. Both `Holds` and `Volumes` are affected.

> Ex. Both pieces of the polygon below should be sent through the network as a part of a single hold but are currently passed as two distinctly separate holds

<img src="https://user-images.githubusercontent.com/3492780/81486876-9e8d7900-921d-11ea-83b9-bfb751ba775b.png" alt="result" width="50%" height="50%"/>


## Contributing

Contributions and suggestions are welcome and encouraged, especially additional high quality image for training. 

## Questions

Open an issue or send me send me an [e-mail](mailto:sebastian@cydivision.com)

## TODO

- [ ] Add open source imagery
- [ ] Collect and tag more images
- [ ] Upload pre-processing script
- [ ] Upload mask export script
- [ ] Create video explaining tagging process for contributors
- [ ] Explore reducing model size using Centermask, Mobilenet, etc.
- [ ] Correct segmented polygons in the data
- [ ] Include training stats. BOX AP, MASK AP etc.
