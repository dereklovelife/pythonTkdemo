# _*_ coding: utf-8 _*_
from Tkinter import *
import demo

class Board(object):
    def __init__(self):
        self.root = Tk()
        self.PTP = demo.PointToPointDemo(1)
        self.mytime = 1000


        self.distacnce = DoubleVar(self.root)
        self.distacnce.set(self.PTP.channelMode.distance)
        self.numofAttena = IntVar(self.root)
        self.numofAttena.set(self.PTP.channelMode.numofAttena)
        self.noisePower = DoubleVar(self.root)
        self.noisePower.set(self.PTP.channelMode.np)
        self.conversion = DoubleVar(self.root)
        self.conversion.set(self.PTP.conversion)
        self.alpha = DoubleVar(self.root)
        self.alpha.set(self.PTP.channelMode.alpha)
        self.time = IntVar(self.root)
        self.time.set(self.mytime)

        self.dlabel = Label(self.root, text = u"距离(m)")
        self.slabel = Label(self.root, text = u"发送端天线数量")
        self.hlabel = Label(self.root, text = u"信道类型")
        self.nlabel = Label(self.root, text = u"噪声功率(dbm)")
        self.clabel = Label(self.root, text = u"能量转换效率（0-1）")
        self.alabel = Label(self.root, text = u"路径损耗因子")
        self.tlabel = Label(self.root, text = u"计算次数")

        self.distacnceEntry = Entry(self.root, textvariable=self.distacnce)
        self.noiseEntry = Entry(self.root, textvariable=self.noisePower)
        self.conversionEntry = Entry(self.root, textvariable=self.conversion)
        self.alphaEntry = Entry(self.root, textvariable = self.alpha)
        self.antennaEntry = Entry(self.root, textvariable = self.numofAttena)
        self.timeEntry = Entry(self.root, textvariable = self.time)

        self.dlabel.pack()
        self.distacnceEntry.pack()
        self.alabel.pack()
        self.alphaEntry.pack()
        self.slabel.pack()
        self.antennaEntry.pack()
        self.nlabel.pack()
        self.noiseEntry.pack()
        self.clabel.pack()
        self.conversionEntry.pack()
        self.tlabel.pack()
        self.timeEntry.pack()

        self.label = Label(self.root, text = u'吞吐率(bps/Hz): ')
        self.label.pack()
        self.assure = Button(self.root, text = u'确定', command = self.showThrouput)
        self.assure.pack()
        self.quit = Button(self.root, text = u'退出', command = self.root.quit)
        self.quit.pack()

    def run(self):
        mainloop()
        try:
            self.root.destroy()
        except:
            pass

    def showThrouput(self):
        try:
            self.PTP.channelMode.setDistance(float(self.distacnce.get()))
            self.PTP.channelMode.setNoise(float(self.noisePower.get()))
            self.PTP.setConversion(float(self.conversion.get()))
            self.PTP.channelMode.setAlpha(float(self.alpha.get()))
            self.PTP.channelMode.setNumOfAntenna(int(self.numofAttena.get()))
            self.mytime = int(self.time.get())
            self.label['text'] = u'计算中...'
            self.label['text'] = u"平均吞吐率(bps/Hz): \n" + str(self.PTP.getAvgThroughput(self.mytime))

        except Exception, e:
            print e
            self.label['text'] = "Error!"

if __name__ == "__main__":
    b = Board()
    b.run()
