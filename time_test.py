
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division

import argparse
import os
import shutil
import time
import importlib
import math
import warnings

parser=argparse.ArgumentParser(description='PyTorch Condense Convolutional Networks Training')
parser.add_argument('--batch', default=32,type=int,
                    help='batch size')
parser.add_argument('--gpu',
                    help='gpu available')
parser.add_argument('--print_freq',default=10,type=int,
                    help='print freq')
args = parser.parse_args()
os.environ["CUDA_VISIBLE_DEVICES"] = args.gpu

import torch
import torch.nn as nn
import torch.nn.parallel

import torch.backends.cudnn as cudnn
import torch.optim
import torch.utils.data
from networks.resblock import GoNetWork

class AverageMeter(object):
    """Computes and stores the average and current value"""
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0
    
    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count


def main():
    input=torch.zeros(args.batch,17,19,19)
    input2=torch.zeros(args.batch,17,19,19)
    model=GoNetWork(17,39)
    model=torch.nn.DataParallel(model).cuda()
    end = time.time()
    batch_time = AverageMeter()
    for i in range(10000):
        input_var=torch.autograd.Variable(input)
        policy,value=model(input_var)
        batch_time.update(time.time() - end)
        end = time.time()
        if i % args.print_freq == 0:
            print('Test: [{0}/{1}]\t'
                  'Time {batch_time.val:.3f} ({batch_time.avg:.3f})\t'
                  .format(i, 10000, batch_time=batch_time))
    return 0

if __name__ == '__main__':
    main()


