class MangoDataloader(Dataset):
    def __init__(self,imagepaths,labels,transformer,imagepathroot,image_size):
        self.imagepathlist = imagepaths
        self.labellist = labels
        self.transformer=transformer
        self.image_size =image_size
        self.imagepathroot=imagepathroot
    def RGB_CMY(self,img):
        b, g, r = cv2.split(img) 	# split the channels
        M = 1 - b
        Y = 1 - g
        C = 1 - r
        result = cv2.merge((C, M, Y)) 	# merge the channels
        return result
    def loadimage(self,imagepath):
        imagepath = os.path.join(self.imagepathroot,imagepath)
        img = cv2.imread(imagepath)
        img = cv2.resize(img, (self.image_size,self.image_size), interpolation = cv2.INTER_AREA)
        RGBimg=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        R,G,B = cv2.split(RGBimg)
        XYZimg =cv2.cvtColor(img,cv2.COLOR_BGR2XYZ  )
        X,Y,Z = cv2.split(img)
        YUVimg=cv2.cvtColor(img,cv2.COLOR_BGR2YUV)
        Y,U,V = cv2.split(YUVimg)# Y 亮度 U 藍色 V 紅色
        HLSimg=cv2.cvtColor(img,cv2.COLOR_BGR2HLS)
        HH,L,SS = cv2.split(HLSimg)# Y 亮度 U 藍色 V 紅色
        HSVimg=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
        H,S,VV = cv2.split(HSVimg) # H 色彩 S 顏色深淺 V 明暗程度
        Labimg=cv2.cvtColor(img,cv2.COLOR_BGR2Lab)
        C,I,E = cv2.split(Labimg)# Y 亮度 U 藍色 V 紅色
        # C,M,YYY = cv2.split(self.RGB_CMY(RGBimg))
        # ML =((np.array(M).astype(int)+np.array(L//2+Y//2).astype(int))//2).astype(int)
        # YL =((np.array(YYY).astype(int)+np.array(L//2+Y//2).astype(int))//2).astype(int)
        newlight = ((L.astype(int)-Y.astype(int)/2)+(255-np.max(L.astype(int)-Y.astype(int)/2))).astype(int)
        newdot = ((X.astype(int)-VV.astype(int)/2)+(255-np.max(X.astype(int)-VV.astype(int)/2))).astype(int)
        newdot = newdot-newlight//2+(255-np.max(newdot-newlight//2))
        # finalnew =(newdot.astype(int)-newlight.astype(int)/2).astype(int)
        source=np.array([V,E,R,G,B,newlight])#S # Y
        # source=np.array([V,E,G])#S # Y
        source=source / 255
        source = np.moveaxis(source, 0, 2)
        source = self.transformer(source).type(torch.FloatTensor)
        newdot = (newdot/255)[None,:,:]
        newdot = np.moveaxis(newdot, 0, 2)
        newdot = self.transformer(newdot).type(torch.FloatTensor)
        I = (I/255)[None,:,:]
        I = np.moveaxis(I, 0, 2)
        I = self.transformer(I).type(torch.FloatTensor)
        S = (S/255)[None,:,:]
        S = np.moveaxis(S, 0, 2)
        S = self.transformer(S).type(torch.FloatTensor)
        # for i in range(source.shape[2]):
        #     hist.append(cv2.calcHist([source],[i], None, [256], [0.0,255.0])/400000)
        return source,newdot,I,S
    def __getitem__(self,index):
        imp = self.imagepathlist[index]
        img,dotimg,Iimg,Simg = self.loadimage(imp)
        label = self.labellist[index]
        return img  ,dotimg ,Iimg,Simg,label,imp
    def __len__(self):
        return len(self.imagepathlist)