# %%
import torch 
from midi_model import MIDIModel
from midi_tokenizer import MIDITokenizer
from collections import OrderedDict

ckpt = torch.load('checkpoints/model.ckpt')
for k in ckpt.keys():
    print(k)

# %%

# Load pre-trained weights into the models
def load_pretrained_weights(model, pretrained_weights_dict, model_name):
    new_state_dict = OrderedDict()
    for key, value in pretrained_weights_dict.items():
        # Modify the keys from 'net.embed_tokens.weight' to 'model_name.embed_tokens.weight'
        if key in model_name:
            new_state_dict[key] = value
    model.load_state_dict(new_state_dict, strict=False)
    return model

net_token_model = MIDITokenizer()
net_token_model = load_pretrained_weights(net_token_model, ckpt, ['net_token'])

net_model = MIDIModel(net_token_model)
# Load pre-trained weights into the models
load_pretrained_weights(net_model, ckpt, ['net', 'lm_head'])