import chainer
import chainer.functinons as F
import chainer.links as L
from chainer import iterators, optimizers, training


class Model(chainer.Chain):

    def __init__(self, n_out):
        super(Model, self).__init__(
                conv1_1 = L.Convolution2D(3, 64, 3, stride=1, pad=1),
                conv1_2 = L.Convolution2D(64, 64, 3, stride=1, pad=1),

                conv2_1 = L.Convolution2D(64, 128, 3, stride=1, pad=1),
                conv2_2 = L.Convolution2D(128, 128, 3, stride=1, pad=1),

                conv3_1 = L.Convolution2D(128, 256, 3, stride=1, pad=1),
                conv3_2 = L.Convolution2D(256, 256, 3, stride=1, pad=1),
                conv3_3 = L.Convolution2D(256, 256, 3, stride=1, pad=1),

                conv4_1 = L.Convolution2D(256, 512, 3, stride=1, pad=1),
                conv4_2 = L.Convolution2D(512, 512, 3, stride=1, pad=1),
                conv4_3 = L.Convolution2D(512, 512, 3, stride=1, pad=1),
                
                conv5_1 = L.Convolution2D(512, 512, 3, stride=1, pad=1),
                conv5_2 = L.Convolution2D(512, 512, 3, stride=1, pad=1),
                conv5_3 = L.Convolution2D(512, 512, 3, stride=1, pad=1),

                fc6 = L.Linear(None, 4096),
                fc7 = L.Linear(4096, 4096),
                fc8= L.Linear(4096, n_out)
                )

        self.train = False

    def __call__(self, x, t):
        h = F.relu(self.conv1_1(x))
        h = F.relu(self.conv1_2(h))
        h = F.max_pooling_2d(h, 2, stride=2)

        h = F.relu(self.conv2_1(x))
        h = F.relu(self.conv2_2(x))
        h = F.max_pooling_2d(h, 2, stride=2)

        h = F.relu(self.conv3_1(x))
        h = F.relu(self.conv3_1(x))
        h = F.relu(self.conv3_1(x))
        h = F.max_pooling_2d(h, 2, stride=2)

        h = F.relu(self.conv4_1(x))
        h = F.relu(self.conv4_1(x))
        h = F.relu(self.conv4_1(x))
        h = F.max_pooling_2d(h, 2, stride=2)

        h = F.relu(self.conv5_1(x))
        h = F.relu(self.conv5_1(x))
        h = F.relu(self.conv5_1(x))
        h = F.max_pooling_2d(h, 2, stride=2)

        h = F.dropoup(F.relu(self.fc6(h)), train = self.train, ratio=0.5)
        h = F.dropoup(F.relu(self.fc7(h)), train = self.train, ratio=0.5)
        h = self.fc8(h)

        if self.train:
            self.loss = F.softmax_cross_entropy(h, t)
            self.acc = F.accuracy(h, t)
            return self.loss
        else:
            self.pred = F.softmax(h)
            return self.pred

