import pandas as pd
import pickle
import numpy as np
from fastai.vision import *
from fastai.callbacks.hooks import *
import matplotlib.pyplot as plt
from lshash.lshash import LSHash
from PIL import Image
from tqdm import tqdm_notebook


pd.set_option('display.max_columns', 500)

path = Path('./101_ObjectCategories')

tfms = get_transforms(
	do_flip=False, 
	flip_vert=False, 
	max_rotate=0, 
	max_lighting=0, 
	max_zoom=1, 
	max_warp=0
)
data = (ImageList.from_folder(path)
		.random_split_by_pct(0.2)
		.label_from_folder()
		.transform(tfms=tfms, size=224)
		.databunch(bs=64))

print('Number of classes {0}'.format(data.c))
print(data.classes)

print('Train dataset size: {0}'.format(len(data.train_ds.x)))
print('Test dataset size: {0}'.format(len(data.valid_ds.x)))

# data.show_batch(rows=3, figsize=(10,6), hide_axis=False)

## Creating the model
learn = create_cnn(data, models.resnet34, pretrained=True, metrics=accuracy)

## Finding Ideal learning late
learn.lr_find()
# learn.recorder.plot()

learn.fit_one_cycle(5,1e-2)

learn.save('stg1-rn34')

learn.unfreeze()
learn.lr_find()
# learn.recorder.plot()

learn.fit_one_cycle(5, slice(1e-5, 1e-2/5))

learn.save('stg2-rn34')


class SaveFeatures():
	features=None
	def __init__(self, m): 
		self.hook = m.register_forward_hook(self.hook_fn)
		self.features = None
	def hook_fn(self, module, input, output): 
		out = output.detach().cpu().numpy()
		if isinstance(self.features, type(None)):
			self.features = out
		else:
			self.features = np.row_stack((self.features, out))
	def remove(self): 
		self.hook.remove()
		
sf = SaveFeatures(learn.model[1][5]) ## Output before the last FC layer

_= learn.get_preds(data.train_ds)
_= learn.get_preds(DatasetType.Valid)




img_path = [str(x) for x in (list(data.train_ds.items)+list(data.valid_ds.items))]
feature_dict = dict(zip(img_path,sf.features))				# key val of 'image_path':'512_dim_visual_embedding'

pickle.dump(feature_dict, open(path/"feature_dict.p", "wb"))




feature_dict = pickle.load(open(path/'feature_dict.p','rb'))


## Locality Sensitive Hashing
# params
k = 10 # hash size
L = 5  # number of tables
d = 512 # Dimension of Feature vector
lsh = LSHash(hash_size=k, input_dim=d, num_hashtables=L)


# LSH on all the images
# for img_path, vec in tqdm_notebook(feature_dict.items()):
for img_path, vec in (feature_dict.items()):
	print(img_path)
	print(vec)
	lsh.index(vec.flatten(), extra_data=img_path)




## Exporting as pickle
pickle.dump(lsh, open(path/'lsh.p', "wb"))



lsh = pickle.load(open(path/'lsh.p','rb'))

def get_similar_item(idx, feature_dict, lsh_variable, n_items=5):
	response = lsh_variable.query(feature_dict[list(feature_dict.keys())[idx]].flatten(),num_results=n_items+1, distance_func='hamming')
	
	columns = 3
	rows = int(np.ceil(n_items+1/columns))
	fig=plt.figure(figsize=(2*rows, 3*rows))
	for i in range(1, columns*rows +1):
		if i<n_items+2:
			img = Image.open(response[i-1][0][1])						# get path_name from image
			fig.add_subplot(rows, columns, i)
			plt.imshow(img)
	return plt.show()