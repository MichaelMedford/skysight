#! /usr/bin/env python
#

""" Plots of dithers applied to cameras. """

import matplotlib.pyplot as plt

def two_exposures_plot(camera, ditherList):

	cameraA = camera.copy()
	cameraB = camera.copy()

	ditherList[0].apply(cameraA)
	ditherList[1].apply(cameraB)

	cameraAB = cameraA.intersect(cameraB)

	area1 = cameraA.difference(cameraAB).get_area()
	area1 += cameraB.difference(cameraAB).get_area()

	area2 = cameraAB.get_area()

	xlim, ylim = cameraA.union(cameraB).get_limits()

	fig, ax = plt.subplots(2, 2, figsize=(8,8))
	ax = ax.flatten()

	ax[0].set_title('All Exposures')
	ax[0].axis('off')
	cameraA.plot(ax[0],color='r',alpha=0.3,xlim=xlim,ylim=ylim)
	cameraB.plot(ax[0],color='g',alpha=0.3,xlim=xlim,ylim=ylim)
	cameraAB.plot(ax[0],color='b',alpha=0.3,xlim=xlim,ylim=ylim)

	ax[1].set_title('cameraA Only')
	ax[1].axis('off')
	cameraA.difference(cameraAB).plot(ax[1],color='r',alpha=0.3,xlim=xlim,ylim=ylim)
	ax[2].set_title('cameraB Only')
	ax[2].axis('off')
	cameraB.difference(cameraAB).plot(ax[2],color='g',alpha=0.3,xlim=xlim,ylim=ylim)
	ax[3].set_title('cameraAB Only')
	ax[3].axis('off')
	cameraAB.plot(ax[3],color='c',alpha=0.3,xlim=xlim,ylim=ylim)

	fig.text(0.4,.95,'area2 = %.2f'%area2,fontsize=15)
	fig.text(0.1,.95,'area1 = %.2f'%area1,fontsize=15)
