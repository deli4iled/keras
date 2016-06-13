from keras.models import model_from_json
from keras.optimizers import SGD

from scipy import misc
import numpy as np
import copy

if __name__ == "__main__":

    print "Preparing test image."
    # Read image
    im = misc.imread('models/cat.jpg')

    # Resize
    im = misc.imresize(im, (224, 224)).astype(np.float32)
    
    # Change RGB to BGR
    aux = copy.copy(im)
    im[:,:,0] = aux[:,:,2]
    im[:,:,2] = aux[:,:,0]

    # Remove train image mean
    im[:,:,0] -= 104.006
    im[:,:,1] -= 116.669
    im[:,:,2] -= 122.679

    # Transpose image dimensions (Keras' uses the channels as the 1st dimension)
    im = np.transpose(im, (2, 0, 1))

    # Insert a new dimension for the batch_size
    im = np.expand_dims(im, axis=0)


    # Load the converted model
    print "Loading model."
    # Load model structure
    model = model_from_json(open('models/Keras_model_structure.json').read())
    # Load model weights
    model.load_weights('models/Keras_model_weights.h5') 

    # Compile converted model
    print "Compiling model."
    sgd = SGD(lr=0.1, decay=1e-6, momentum=0.9, nesterov=True)
    loss = dict()
    
    print(model.outputs[0])
    print(type(model.outputs[0]))
    
    attrs = vars(model.outputs[0])
    print ', '.join("%s: %s" % item for item in attrs.items())
    
    # {u'': 'categorical_crossentropy', u'loss3/loss3': 'categorical_crossentropy', u'loss2/loss': 'categorical_crossentropy'}
    for out in ["loss1/loss", "loss2/loss", "loss3/loss3"]:
        loss[out] = 'categorical_crossentropy'
        last_out = out
    print("loss", loss)
    model.compile(optimizer=sgd, loss=loss)
    #model.compile(optimizer=sgd, loss='categorical_crossentropy')
    
    # Predict image output
    print "Applying prediction."
    in_data = dict()
    for input in ['data']:
        in_data[input] = im
    print("im.shape", im.shape)
    out = model.predict(im)

    # Load ImageNet classes file
    classes = []
    with open('models/classes.txt', 'r') as list_:
        for line in list_:
            classes.append(line.rstrip('\n'))

    print(out)
    print("len(out)", len(out))
    print classes[np.argmax(out[0])]
    print classes[np.argmax(out[1])]
    print classes[np.argmax(out[2])]
