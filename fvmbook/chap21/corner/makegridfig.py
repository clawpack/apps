
# make the figure for the book showing the interface.

from pylab import *

figure(5)
clf()
plot([0,0,1],[-1,0,0.55],'g',linewidth=2)
text(.4,-.6,'right',fontsize=20)
text(-.6,0,'left',fontsize=20)
axis('scaled')
xlim([-1,1])
ylim([-1,1])
savefig('interface.png', bbox_inches='tight')
print("Created interface.png")

