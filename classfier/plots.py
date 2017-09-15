import matplotlib.pyplot as plt
plt.rc('font', weight='bold')
def draw_precision_recall(precision, recall, title):
    x = range(1, 11)
    line1, = plt.plot(x, precision, marker='o', label='precision')
    line2, = plt.plot(x, recall, marker='x', label='recall', linestyle='--')
    plt.ylim([0, 1] )
    plt.xlabel(r'$\eta$', fontsize=16)
    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)
    plt.legend(loc='upper right')
    plt.legend(frameon=False)
    plt.savefig('../plot/'+title+'.eps', format='eps', dpi=1200)
    plt.close()

# tainan
"""
Title : decision tree(classifier)
set defferent alert threshold
label: both are contagious region
"""
title = "plot1"

precision = [0.76, 0.76, 0.76, 0.73, 0.7, 0.7, 0.66, 0.64, 0.57, 0.55]
recall = [0.66, 0.74, 0.73, 0.72, 0.68, 0.72, 0.71, 0.73, 0.72, 0.74]
draw_precision_recall(precision, recall, title)


"""
Title : decision tree(classifier)
set defferent alert threshold
label: not a contagious region
"""
title = "plot2"
precision = [0.93, 0.97, 0.98, 0.98, 0.98, 0.99, 0.99, 0.99, 0.99, 0.99]
recall = [0.97, 0.98, 0.98, 0.98, 0.98, 0.99, 0.99, 0.99, 0.99, 0.99]
draw_precision_recall(precision, recall, title)

"""
Title : decision tree(classifier)
set defferent alert threshold
label: only self is contagious region
"""
title = "plot3"
precision = [0.06, 0.12, 0.08, 0.06, 0.1, 0.05, 0.09, 0.08, 0.03, 0.04]
recall = [0, 0.03, 0.08, 0.1, 0.16, 0.06, 0.08, 0.09, 0.03, 0.03]
draw_precision_recall(precision, recall, title)


# Kaohsiung
"""
Title : decision tree(classifier)
set defferent alert threshold
label: both are contagious region
"""
title = "plot4"
precision = [0.76, 0.67, 0.55, 0.41, 0.37, 0.27, 0.26, 0.29, 0.26, 0.18]
recall = [0.5, 0.46, 0.44, 0.36, 0.34, 0.27, 0.28, 0.22, 0.12, 0.14]
draw_precision_recall(precision, recall, title)

"""
Title : decision tree(classifier)
set defferent alert threshold
label: not a contagious region
"""
title = "plot5"
precision = [0.92, 0.96, 0.97, 0.98, 0.99, 0.99, 0.99, 0.99, 1, 1]
recall = [0.98, 0.98, 0.98, 0.98, 0.99, 0.99, 0.99, 1, 1, 1]
draw_precision_recall(precision, recall, title)

"""
Title : decision tree(classifier)
set defferent alert threshold
label: only self is contagious region
"""
title = "plot6"
precision = [0, 0.09, 0.09, 0.01, 0.05, 0.06, 0.08, 0.09, 0.08, 0.08]
recall = [0, 0.03, 0.05, 0.01, 0.05, 0.06, 0.08, 0.12, 0.09, 0.08]
draw_precision_recall(precision, recall, title)


"""
tainan
title: ic model
threshold = 0.5
label: both are contagious region
"""
title = "plot7"
precision = [0.56, 0.47, 0.43, 0.43, 0.43, 0.42, 0.39, 0.37, 0.36, 0.33]
recall = [0.87, 0.86, 0.81, 0.79, 0.77, 0.69, 0.58, 0.56, 0.5, 0.44]
draw_precision_recall(precision, recall, title)


"""
tainan
title: ic model
threshold = 0.5
label: not a contagoius region
"""
title = "plot8"
precision = [0.97, 0.98, 0.98, 0.99, 0.99, 0.99, 0.98, 0.99, 0.99, 0.99]
recall = [0.89, 0.91, 0.92, 0.94, 0.95, 0.96, 0.97, 0.97, 0.98, 0.98]
draw_precision_recall(precision, recall, title)

"""
tainan
title: ic model
threshold = 0.5
label: only self is contagious region
"""
title = "plot9"
precision = [0.04, 0.05, 0.03, 0.06, 0.05, 0.06, 0, 0, 0.02, 0]
recall = [0.01, 0.02, 0.02, 0.05, 0.05, 0.06, 0, 0, 0.03, 0]
draw_precision_recall(precision, recall, title)



"""
kaohsiung
title: ic model
threshold = 0.5
label: both are contagious region
"""
title = "plot10"
precision = [0.62, 0.53, 0.45, 0.37, 0.29, 0.21, 0.13, 0.15, 0.15, float('NaN')]
recall = [0.81, 0.73, 0.58, 0.46, 0.3, 0.16, 0.07, 0.04, 0.04, 0]
draw_precision_recall(precision, recall, title)


"""
kaohsiung
title: ic model
threshold = 0.5
label: not a contagoius region
"""
title = "plot11"
precision = [0.96, 0.97, 0.98, 0.98, 0.98, 0.99, 0.99, 0.99, 0.99, 1]
recall = [0.93, 0.95, 0.97, 0.98, 0.98, 0.99, 1, 1, 1, 1]
draw_precision_recall(precision, recall, title)

"""
kaohsiung
title: ic model
threshold = 0.5
label: only self is contagious region
"""
title = "plot12"
precision = [0.04, 0.05, 0.05, 0.06, 0.06, 0.03, 0.03, 0, 0.03, 0.05]
recall = [0.01, 0.03, 0.03, 0.04, 0.05, 0.02, 0.02, 0, 0.01, 0.01]
draw_precision_recall(precision, recall, title)