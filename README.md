# Auditing and Training Fair ML Models @EDS-2023

> Companion presentation slides [here](https://docs.google.com/presentation/d/1RI9sfqirrZt9NyAtbzTCuokp-IsA7mVv6rS42X6rNnw/edit?usp=sharing).

A brief tutorial on how you can assess the whole fairness-accuracy trade-off curve attainable by a single model (by post-processing),
as well as improving your model's fairness with open-source tools.

## Getting started

Install all requirements
```
pip install -r requirements.txt
```

And run the tutorial notebook at [`notebooks/training-fairer-models.ipynb`](notebooks/training-fairer-models.ipynb) with
```
cd notebooks
python -m jupyter notebook
```

The notebook was already ran and its outputs saved, but feel free to re-run and tinker with it!


## Used tools

- [`error-parity`](https://github.com/socialfoundations/error-parity)
  - Enables post-processing any predictor (and mapping its fairness-accuracy frontier);
- [`fairlearn`](https://github.com/fairlearn/fairlearn)
  - Contains popular in-processing fair ML algorithms (among many other features);


---

For an in-depth tutorial on algorithmic fairness check out [this repository](https://dssg.github.io/fairness_tutorial/).
 