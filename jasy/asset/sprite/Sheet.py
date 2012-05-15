#
# Jasy - Web Tooling Framework
# Copyright 2010-2012 Zynga Inc.
#

import sys, math, logging, Image, ImageDraw

class SpriteSheet():

    def __init__(self, packer, blocks):

        self.packer = packer
        self.width = packer.root.w
        self.height = packer.root.h
        self.blocks = blocks

        self.area = self.width * self.height
        self.usedArea = sum([s.w * s.h for s in blocks])
        self.used = (100 / self.area) * self.usedArea


    def __len__(self):
        return len(self.blocks)


    def export(self, projectId=''):
        
        data = {}

        for block in self.blocks:

            info = block.toJSON()
            
            data[block.image.relPath] = info

            for d in block.duplicates:
                data[d.relPath] = info

        return data


    def toImage(self, filename, showDebug=False):

        img = Image.new('RGBA', (self.width, self.height))
        draw = ImageDraw.Draw(img)

        #draw.rectangle((0, 0, self.width, self.height), fill=(255, 255, 0, 255))

        # Load images and pack them in
        for block in self.blocks:
            res = Image.open(block.image.src)

            x, y = block.fit.x, block.fit.y
            if block.rotated:
                logging.debug('%s is rotated' % block.image.src)
                res = res.rotate(90)

            img.paste(res, (x, y))
            del res

            if showDebug:
                x, y, w, h = block.fit.x, block.fit.y, block.w, block.h
                draw.rectangle((x, y , x + w , y + h), outline=(0, 0, 255, 255) if block.rotated else (255, 0, 0, 255))

        if showDebug:
            for i, block in enumerate(self.packer.getUnused()):
                x, y, w, h = block.x, block.y, block.w, block.h
                draw.rectangle((x, y , x + w , y + h), fill=(255, 255, 0, 255))

        img.save(filename)

