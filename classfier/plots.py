
import matplotlib.pyplot as plt


# import ic_model
# plt.rc('font', weight='bold')
def draw(y1, y2, y3, y4, y5, y6, title, ylabel, legend_loc, scale=0):
    x = range(1, 11)
    line1, = plt.plot(x, y1, marker='o', label='AdaBoost', linestyle=':')
    line2, = plt.plot(x, y2, marker='x', label='SVM', linestyle='-')
    line3, = plt.plot(x, y3, marker='^', label='Random Forest', linestyle='-.')
    line4, = plt.plot(x, y4, marker='D', label='Decision Tree', linestyle='--')
    line5, = plt.plot(x, y5, marker='v', label='IC model', linestyle='-')
    line6, = plt.plot(x, y6, marker='>', label='just use last week', linestyle='-')

    if scale:
        # plt.yscale('log')
        plt.ylim([0.85, 1] )
    else:
        plt.ylim([0, 1] )
    plt.xlabel(r'Alert threshold(${\eta}$)', fontweight='bold', fontsize=18)
    plt.ylabel(ylabel, fontweight='bold', fontsize=18)
    plt.xticks(fontsize=18, fontweight='bold')
    plt.yticks(fontsize=18, fontweight='bold')
    legend_properties = {'weight':'bold'}
    plt.legend(loc=legend_loc, frameon=False, fontsize=18, prop=legend_properties)
    plt.savefig('../plot/'+title+'.eps', format='eps', dpi=1200)
    plt.close()


def draw_topk(y1, y2, y3, y4, title):
    x = range(1, 21)
    line1, = plt.plot(x, y1, marker='o', label=r'${\alpha}=0$', linestyle=':')
    line2, = plt.plot(x, y2, marker='x', label=r'${\alpha}=0.0001$', linestyle='-')
    line3, = plt.plot(x, y3, marker='^', label=r'${\alpha}=0.01$', linestyle='-.')
    line4, = plt.plot(x, y4, marker='D', label=r'${\alpha}=1$', linestyle='--')

    plt.ylim([0, 1] )
    plt.xlabel('k', fontweight='bold', fontsize=18)
    plt.ylabel('precision', fontweight='bold', fontsize=18)
    plt.xticks(fontsize=18, fontweight='bold')
    plt.yticks(fontsize=18, fontweight='bold')
    legend_properties = {'weight':'bold'}
    plt.legend(loc='upper right', frameon=False, fontsize=18, prop=legend_properties)
    plt.savefig('../plot/'+title+'.eps', format='eps', dpi=1200)
    plt.close()
