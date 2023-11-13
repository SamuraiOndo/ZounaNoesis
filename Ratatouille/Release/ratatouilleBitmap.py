
from inc_noesis import *
import noesis
import rapi
import os
def registerNoesisTypes():
    handle = noesis.register("Ratatouille Bitmap_Z",".Bitmap_Z")
    noesis.setHandlerTypeCheck(handle,noepyCheckType)
    noesis.setHandlerLoadRGBA(handle,getTex)
    return 1

def noepyCheckType(data):
    bs = NoeBitStream(data,NOE_LITTLEENDIAN)
    bs.seek(4)
    if bs.readInt() == 4:
        bs.seek(0x10)
        if bs.readUInt() == 1471281566:
            return 1
        else: 
            return 0
    else:
        return 0

def getTex(data,texList):
    bs = NoeBitStream(data,NOE_LITTLEENDIAN)
    bs.seek(4)
    linksize = bs.readUInt()
    texSize = bs.readUInt()
    bs.seek(0x20)
    texWidth = bs.readUInt()
    texHeight = bs.readUInt()
    ddscheckrat = bs.readUInt()
    if ddscheckrat != 0:
        ddssize = (ddscheckrat - 0x80)
        bs.seek(0x88)
        ddstyperat = bs.readString()
        print(ddstyperat)
        bs.seek(0xb4)
        texName = os.path.splitext(rapi.getInputName())[0]+"_"+str(texName)
        texData = bs.readBytes(ddssize)
        if ddstyperat == "DXT1":
            texList.append(NoeTexture(texName,texWidth,texHeight,texData,noesis.NOESISTEX_DXT1))
        if ddstyperat == "DXT5":
            texList.append(NoeTexture(texName,texWidth,texHeight,texData,noesis.NOESISTEX_DXT5))
    if ddscheckrat == 0:
        bs.seek(0x2c)
        versionnum = bs.readBytes(0x01)
        print(versionnum)
        if versionnum == b'\x0c':
            texName = os.path.splitext(rapi.getInputName())[0]+"_"+str(texName)
            bs.seek(0x34)
            texData = bs.readBytes(texWidth * texHeight * 4)
            data = rapi.imageDecodeRaw(texData, texWidth, texHeight, "B8G8R8A8")
            texList.append(NoeTexture(texName,texWidth,texHeight,data,noesis.NOESISTEX_RGBA32))
        if versionnum == b'\x0d':
            texName = os.path.splitext(rapi.getInputName())[0]+"_"+str(texName)
            bs.seek(0x34)
            texData = bs.readBytes(texWidth * texHeight * 3)
            data = rapi.imageDecodeRaw(texData, texWidth, texHeight, "B8G8R8")
            texList.append(NoeTexture(texName,texWidth,texHeight,data,noesis.NOESISTEX_RGBA32))
        if versionnum == b'\x07':
            texName = os.path.splitext(rapi.getInputName())[0]+"_"+str(texName)
            bs.seek(0x34)
            texData = bs.readBytes(texWidth * texHeight)
            data = rapi.imageDecodeRaw(texData, texWidth, texHeight, "R2G2B2A2")
            texList.append(NoeTexture(texName,texWidth,texHeight,data,noesis.NOESISTEX_RGBA32))
