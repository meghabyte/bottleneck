# Policy Learning with a Language Bottleneck


This repository contains the code for the paper [Policy Learning with a Language Bottleneck](https://cs.stanford.edu/~megha). In this work, we show how artificial agents that periodically generate and condition on linguistic rules describing their own most rewarding behavior can learn more generalizable policies that enable stronger human-AI interaction. For any questions, please contact megha@cs.stanford.edu! 

If you find this repository useful, please cite:

```
@inproceedings{srivastava2024bottleneck,
    title = "Policy Learning with a Language Bottleneck",
    author = "Srivastava, Megha and Colas, Cedric and Sadigh, Dorsa and Andreas, Jacob",
    booktitle = "arxiv",
    year = "2024",
}
```
This repository includes code for all tasks, including user study interfaces and data. The four tasks we consider in our paper are: SelectSay, Maze, Builder, and Birds. 

Our code requires the following packages: ``transformers==4.35.2, torch==2.0.1, torchvision==0.15.2``. For large language (+vision) model inference and fine-tuning we use services from https://replicate.com/ and https://www.together.ai/, and have put placeholders in this repository where an Authentication Key is required. 

For the SelectSay environment, we adapt the code provided by https://github.com/hengyuan-hu/instruct-rl. If you use our code, please make sure to also cite:
```
@inproceedings{hu2023instructrl,
    title = "Language Instructed Reinforcement Learning for Human-AI Coordination ",
    author = "Hu, Hengyuan and Sadigh, Dorsa",
    booktitle = "International Conference on Machine Learning",
    year = "2023",
}
```

For the Maze environment, we modify the gym-maze environment from https://github.com/MattChanTK/gym-maze. In particular, we adapt their code to create random mazes of arbitrary size. If you use our code, please make sure to also cite them. 

