from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as P
import numpy as np

OUT=Path(__file__).resolve().parents[1]/'assets'/'refuerzos-conceptuales.svg'
OUT.parent.mkdir(exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':15})
navy='#172c41'; muted='#536579'; blue='#2379b7'; pale='#d7eafa'; gold='#d6a342'; orange='#e28636'; plastic='#c2c9d0'; green='#dcece2'; red='#c75c59'
fig=plt.figure(figsize=(15,12.8),facecolor='#f5f7fa',dpi=140)
fig.text(.045,.962,'Cómo trabajarían los refuerzos',fontsize=29,weight='bold',color=navy)
fig.text(.045,.931,'Esquemas conceptuales · No reproducen el X20 Pro ni indican dónde perforar.',fontsize=15,color=muted)

def panel(rect):
    ax=fig.add_axes(rect); ax.set_xlim(0,10);ax.set_ylim(0,6);ax.axis('off')
    ax.add_patch(P.FancyBboxPatch((.02,.02),9.96,5.96,boxstyle='round,pad=0,rounding_size=.18',facecolor='white',edgecolor='#e0e5eb',lw=1))
    return ax
def label(ax,txt,xy,target,align='left',c=muted,fs=14):
    ax.annotate(txt,xy=target,xytext=xy,ha=align,va='center',fontsize=fs,color=c,
      arrowprops={'arrowstyle':'-','color':c,'lw':1.2,'connectionstyle':'angle,angleA=0,angleB=90,rad=3'})
def screw(ax,x,y,r=.16):
    ax.add_patch(P.Circle((x,y),r,fc='#eef4fa',ec=navy,lw=1.3))
    ax.plot([x-r*.5,x+r*.5],[y,y],color=navy,lw=1.1)
    ax.plot([x,x],[y-r*.5,y+r*.5],color=navy,lw=1.1)

a=panel([.04,.51,.445,.37])
a.text(.42,5.45,'A. Collar o abrazadera',color=navy,weight='bold',fontsize=20)
a.add_patch(P.Rectangle((1.55,1.45),6.9,.48,fc=plastic,ec='#929da9'))
a.add_patch(P.Rectangle((4.15,1.90),1.7,1.10,fc=plastic,ec='none'))
a.add_patch(P.Circle((5,3.24),1.03,fc=plastic,ec='#929da9',lw=1.5))
a.add_patch(P.Circle((5,3.24),.52,fc='white',ec='#929da9',lw=1.5))
a.add_patch(P.Circle((5,3.24),.38,fc=orange,ec='#b36322',lw=1.5))
a.plot([4.93,5.05,4.93,5.09],[4.25,4.06,3.89,3.73],color=red,lw=3)
a.add_patch(P.Arc((5,3.24),2.34,2.34,theta1=-44,theta2=224,color=blue,lw=9))
label(a,'Collar exterior',(.55,4.35),(4.05,3.9),c=blue)
label(a,'Barrita\n(pasador)',(7.0,3.45),(5.28,3.25),c='#a95d23')
label(a,'Raíz de\nplástico',(.55,2.3),(4.22,2.1))
a.text(.42,.65,'Puede contener la grieta. La raíz de plástico\nsigue soportando la carga.',fontsize=13.5,color=muted,va='center',linespacing=1.45)

b=panel([.515,.51,.445,.37])
b.text(.42,5.45,'B. Soporte metálico nuevo',color=navy,weight='bold',fontsize=20)
b.add_patch(P.Rectangle((1.05,1.45),7.9,1.35,fc=green,ec='#96b8a4'))
# Frontal conceptual: a supporting plate with two broad mounting feet.
shape=[(1.85,2.0),(8.15,2.0),(8.15,2.65),(6.45,2.65),(6.05,3.7),(5.65,4.1),(4.35,4.1),(3.95,3.7),(3.55,2.65),(1.85,2.65)]
b.add_patch(P.Polygon(shape,closed=True,fc=pale,ec=blue,lw=2.7,joinstyle='round'))
b.add_patch(P.Circle((5,3.28),.67,fc=gold,ec='#a27b28',lw=1.4))
b.add_patch(P.Circle((5,3.28),.44,fc='white',ec='#a27b28',lw=1.2))
b.add_patch(P.Circle((5,3.28),.34,fc=orange,ec='#b36322',lw=1.2))
screw(b,2.6,2.32);screw(b,7.4,2.32)
label(b,'Casquillo',(.52,4.47),(4.5,3.7),c='#926b1c')
label(b,'Metal que\nrecoge la carga',(7.04,4.25),(6.16,3.38),c=blue)
label(b,'Zona sana',(.48,1.0),(1.45,1.72),fs=13)
b.text(5.45,1.04,'Fijaciones por definir',ha='center',fontsize=12,color=muted)
b.text(.42,.37,'El apoyo nuevo debe conservar el eje y el movimiento.',fontsize=12.5,color=muted)

c=panel([.04,.11,.92,.36])
c.set_xlim(0,20)
c.patches[0].set_width(19.96)
c.text(.45,5.45,'C. Anclaje metálico del muelle',color=navy,weight='bold',fontsize=20)
# Cutaway of a through eye bolt: stem, washers, sound substrate, backing plate and nut.
c.add_patch(P.Rectangle((2.5,2.32),9.0,.72,fc=green,ec='#96b8a4',lw=1.2))
c.add_patch(P.Rectangle((5.72,1.18),.42,3.04,fc='#a5b2bf',ec=navy,lw=1.0,zorder=2))
for y in np.arange(1.25,3.6,.16):
    c.plot([5.72,6.14],[y,y+.1],color='#6b7a89',lw=.8,zorder=3)
c.add_patch(P.Circle((5.93,4.18),.52,fc='white',ec=blue,lw=10,zorder=5))
# Upper nut and washer, lower backing plate and retaining nut.
c.add_patch(P.Rectangle((5.49,3.2),.88,.35,fc=pale,ec=blue,lw=1.5,zorder=5))
c.add_patch(P.Rectangle((4.7,3.04),2.46,.16,fc=blue,ec=blue,zorder=5))
c.add_patch(P.Rectangle((3.6,2.10),4.8,.22,fc=blue,ec=blue,zorder=5))
c.add_patch(P.Rectangle((5.49,1.72),.88,.38,fc=pale,ec=blue,lw=1.5,zorder=5))
# A hook and extension spring are drawn for identification, not a prescribed orientation.
c.plot([6.35,7.0],[4.18,4.18],color='#606f7e',lw=2.5)
c.add_patch(P.Arc((6.39,4.18),.5,.5,theta1=70,theta2=300,color='#606f7e',lw=2.5))
xs=np.linspace(7,10.45,420)
c.plot(xs,4.18+.24*np.sin(np.linspace(0,14*np.pi,420)),color='#606f7e',lw=2.6)
c.plot([10.45,10.85],[4.18,4.18],color='#606f7e',lw=2.5)
c.add_patch(P.Arc((11.02,4.18),.45,.45,theta1=-110,theta2=140,color='#606f7e',lw=2.5))
label(c,'Argolla / cáncamo',(.65,4.6),(5.41,4.2),c=blue,fs=14)
label(c,'Muelle', (11.5,4.48),(9.4,4.37),fs=14)
label(c,'Arandela ancha',(12.5,3.45),(6.9,3.12),c=blue,fs=14)
label(c,'Plástico sano',(12.5,2.68),(10.9,2.68),fs=14)
label(c,'Contraplaca',(12.5,1.92),(8.1,2.19),c=blue,fs=14)
label(c,'Tuerca', (3.5,1.25),(5.55,1.88),align='right',c=blue,fs=14)
c.text(.65,.55,'La contraplaca es una chapita de respaldo. Su función es repartir el esfuerzo en más superficie.',fontsize=14,color=muted)
fig.text(.045,.067,'La forma, el tamaño y las fijaciones se deciden al ver la rotura real.',fontsize=16,color=navy,weight='bold')
fig.text(.045,.041,'El refuerzo del pasador debe fijarse a la misma pieza que tenía el apoyo original y dejar libre la suspensión.',fontsize=13.7,color=muted)
fig.savefig(OUT,facecolor=fig.get_facecolor())
print(str(OUT))
