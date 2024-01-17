# Fine-tuning Midi-Model to sea shanties

## Midi event transformer for music generation

- [online: huggingface](https://huggingface.co/spaces/skytnt/midi-composer)

- [online: colab](https://colab.research.google.com/github/SkyTNT/midi-model/blob/main/demo.ipynb)

- [online: github](https://github.com/SkyTNT/midi-model)

## Pretrained model

Download the pretrained model from [huggingface](https://huggingface.co/skytnt/midi-model/blob/main/model.ckpt) and save it in a new folder called `checkpoints`

## Requirements

- `pip install -r requirements.txt`
  
## Dataset

Download [The Project Gutenberg EBook of The Shanty Book, Part I, Sailor Shanties](https://www.gutenberg.org/files/20774/20774-h/20774-h.htm) and augment it by:

- `python download_shanties.py`
- `python midi_augmentation.py --input_dir shanties/ --output_dir shanties/augmented/`

## Fine-tune from checkpoint and save intermediate generations

`train.py --resume checkpoints/model.ckpt --data shanties/augmented/ --data-val-split 50 --val-step 32 --max-step 10000 --warmup-step 1000`
