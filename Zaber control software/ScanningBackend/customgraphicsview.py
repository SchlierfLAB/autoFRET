from PyQt5.QtWidgets import QGraphicsView, QRubberBand
from PyQt5.QtCore import QPoint, Qt, QRect, QEvent, QSize
from PyQt5.QtGui import QPen, QPainter, QColor, QBrush, QMouseEvent


class CustomGraphicsView(QGraphicsView):

    def __init__(self, *args, **kwargs):
        QGraphicsView.__init__(self)
        self.coords = QPoint(0,0)
        self.guidePen = QPen(Qt.black, 0.1, Qt.SolidLine)
        

    def mouseMoveEvent(self,ev):
        self.coords = self.mapToScene(ev.pos())

        QGraphicsView.mouseMoveEvent(self,ev)
        self.viewport().update()



    def drawForeground(self, painter, rect):
        # if self.guidesEnabled:
        painter.setClipRect(rect)
        painter.setPen(self.guidePen)
        painter.setBrush(QBrush(QColor(0,200,0,120)))
        painter.drawRect(self.coords.x(), rect.top(), 20, rect.bottom()+22)
        painter.drawRect(rect.left(), self.coords.y(), rect.right()+22, 20)