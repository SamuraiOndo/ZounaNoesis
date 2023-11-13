
from inc_noesis import *
import noesis
import rapi
import os
try:
    from lib_zq_nintendo_tex import *
except ImportError:
    print("Get the needed lib from https://github.com/Zheneq/Noesis-Plugins/blob/master/lib_zq_nintendo_tex.py")


def registerNoesisTypes():
    handle = noesis.register("Ratatouille Proto Bitmap_Z",".Bitmap_Z")
    noesis.setHandlerTypeCheck(handle,noepyCheckType)
    noesis.setHandlerLoadRGBA(handle,getTex)
    return 1

def noepyCheckType(data):
    bs = NoeBitStream(data,NOE_BIGENDIAN)
    bs.seek(0x8)
    version = bs.readUInt()
    if version == 1471281566:
        return 1
    else:
        return 0

def getTex(data,texList):
    bs = NoeBitStream(data,NOE_BIGENDIAN)
    bs.seek(0x18)
    texWidth = bs.readUInt()
    texHeight = bs.readUInt()
    bs.seek(0x20)
    ddscheckrat = bs.readUInt()
    if ddscheckrat != 0:    
        bs.seek(0x2c)
        texName = os.path.splitext(rapi.getInputName())[0]
        texData = bs.readBytes(ddscheckrat)
        #texData = rapi.imageDecodeDXT(texData,texWidth,texHeight,noesis.NOESISTEX_DXT1)
        #texList.append(NoeTexture(texName,texWidth,texHeight,texData,noesis.NOESISTEX_DXT1))
        texList.append(textureParser.cmpr(texData,texHeight,texWidth))
    else:
        bs.seek(0x24)
        versionnum = bs.readBytes(0x01)
        if versionnum == b'\x0d':
            bs.seek(0x2c)
            texName = os.path.splitext(rapi.getInputName())[0]
            texData = bs.readBytes(texWidth * texHeight * 3)
            data = rapi.imageDecodeRaw(texData, texWidth, texHeight, "R8G8B8")
            texList.append(NoeTexture(texName,texWidth,texHeight,data,noesis.NOESISTEX_RGBA32))
        if versionnum == b'\x0c':
            bs.seek(0x2c)
            texName = os.path.splitext(rapi.getInputName())[0]
            texData = bs.readBytes(texWidth * texHeight * 4)
            texData = protoDeswizzle(texData,texWidth,texHeight)
            data = rapi.imageDecodeRaw(texData, texWidth, texHeight, "A8B8G8R8")
            texList.append(NoeTexture(texName,texWidth,texHeight,data,noesis.NOESISTEX_RGBA32))           


def protoDeswizzle(src,width,height):
    format = 0xc
    dst = [0]*len(src)
    src_index = 0
    for y in range(height //4):
        for x in range(width //4):
            dst_index = 0x10 * (x + y * width)
            for i in range(4):
                for j in range(4):
                    dst[dst_index + 3] = src[src_index + 1]
                    dst[dst_index + 2] = src[src_index + 0x20]
                    dst[dst_index + 1] = src[src_index + 0x21]
                    if (format == 0xD):
                        dst[dst_index + 0] = 0xFF
                    else:
                        dst[dst_index + 0] = src[src_index]
                    src_index += 2
                    dst_index += 4
                dst_index += 4 * (width - 4)
            src_index += 0x20
    return bytearray(dst)
