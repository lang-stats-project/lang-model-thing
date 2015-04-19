### Random Baseline Experiment

I generated random 5 and 10 features:

    make random-features.5
    make random-features.10

I specify which features to use in experiment 0. take a look at `run/run.0`.
I run & evaluate the experiment:

    make eval.0

Training dev and model file is under `run/RUN0`. The score is in `eval.0`.
